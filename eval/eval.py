#!/usr/bin/env python3
"""
Evaluation harness for the whisper-diarize pipeline.

Metrics:
  DER  — Diarization Error Rate (pyannote.metrics)
         = (missed_speech + false_alarm + speaker_confusion) / total_reference
  WER  — Word Error Rate (jiwer)  [if reference transcript provided]
  Coverage — % of audio with a speaker label (1 - missed_speech_rate)

Usage:
    uv run eval/eval.py                          # all cases
    uv run eval/eval.py --case synth_zh_4spk     # one case
    uv run eval/eval.py --skip-diarization       # use cached results
"""

import argparse
import json
import os
import sys
import time
from pathlib import Path

from dotenv import load_dotenv
load_dotenv(Path(__file__).parent.parent / ".env")

EVAL_DIR   = Path(__file__).parent
CASES_DIR  = EVAL_DIR / "cases"
REPORT_PATH = EVAL_DIR / "report.json"


# ─── CLI ─────────────────────────────────────────────────────────────────────

def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--case", help="Run a single case by name")
    p.add_argument("--skip-diarization", action="store_true",
                   help="Re-use cached diarization RTTM if present")
    p.add_argument("--speakers", type=int, default=None,
                   help="Override number of speakers")
    return p.parse_args()


# ─── Pipeline ────────────────────────────────────────────────────────────────

def run_transcription(audio_path: Path, model="mlx-community/whisper-large-v3-turbo"):
    """Run mlx-whisper and return result dict."""
    cache = audio_path.with_suffix(".whisper.json")
    if cache.exists():
        print(f"  📦 Transcription: loading cache")
        return json.loads(cache.read_text())
    import mlx_whisper
    print(f"  🎙️  Transcribing...")
    result = mlx_whisper.transcribe(str(audio_path), path_or_hf_repo=model,
                                     word_timestamps=True, verbose=None)
    cache.write_text(json.dumps(result))
    return result


def run_diarization(audio_path: Path, hf_token: str, num_speakers=None,
                    cache_path: Path = None, skip=False):
    """Run pyannote diarization and return Annotation object."""
    if skip and cache_path and cache_path.exists():
        print(f"  📦 Diarization: loading cache")
        from pyannote.core import Annotation, Segment
        ann = Annotation()
        for line in cache_path.read_text().splitlines():
            parts = line.split()
            if len(parts) < 8 or parts[0] != "SPEAKER":
                continue
            start, dur, spk = float(parts[3]), float(parts[4]), parts[7]
            ann[Segment(start, start + dur)] = spk
        return ann

    from pyannote.audio import Pipeline
    import torch
    print(f"  👥 Diarizing...")
    device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
    pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization-3.1", token=hf_token)
    pipeline.to(device)
    kwargs = {}
    if num_speakers:
        kwargs["min_speakers"] = kwargs["max_speakers"] = num_speakers
    result = pipeline(str(audio_path), **kwargs)
    ann = result.speaker_diarization

    # Cache as RTTM
    if cache_path:
        lines = []
        for seg, _, spk in ann.itertracks(yield_label=True):
            lines.append(f"SPEAKER audio 1 {seg.start:.3f} {seg.duration:.3f} <NA> <NA> {spk} <NA> <NA>")
        cache_path.write_text("\n".join(lines) + "\n")
    return ann


# ─── Metrics ─────────────────────────────────────────────────────────────────

def compute_der(reference_rttm: Path, hypothesis: "Annotation") -> dict:
    """Compute DER using pyannote.metrics."""
    from pyannote.metrics.diarization import DiarizationErrorRate
    from pyannote.core import Annotation, Segment

    # Load reference
    ref = Annotation()
    for line in reference_rttm.read_text().splitlines():
        parts = line.split()
        if len(parts) < 8 or parts[0] != "SPEAKER":
            continue
        start, dur, spk = float(parts[3]), float(parts[4]), parts[7]
        ref[Segment(start, start + dur)] = spk

    metric = DiarizationErrorRate()
    components = metric.compute_components(ref, hypothesis)
    der = metric(ref, hypothesis) * 100

    total = components["total"]
    missed = components["missed detection"] / total * 100
    false_alarm = components["false alarm"] / total * 100
    confusion = components["confusion"] / total * 100
    coverage = 100 - missed

    return {
        "DER":        round(der, 2),
        "missed":     round(missed, 2),
        "false_alarm":round(false_alarm, 2),
        "confusion":  round(confusion, 2),
        "coverage":   round(coverage, 2),
    }


def _tokenize(text: str) -> str:
    """Insert spaces between CJK characters so jiwer treats each as a word."""
    import unicodedata
    out = []
    for ch in text:
        cat = unicodedata.category(ch)
        if cat.startswith('L') and ord(ch) > 0x2E80:  # CJK / Han
            out.append(f' {ch} ')
        else:
            out.append(ch)
    return ' '.join(''.join(out).split())


def compute_wer(reference_txt: Path, hypothesis_txt: Path) -> dict:
    """Compute CER/WER. For Chinese, character-level metrics are reported."""
    try:
        import jiwer
    except ImportError:
        return {"WER": None, "note": "pip install jiwer to enable WER"}

    ref_lines = [l.split(": ", 1)[-1].strip()
                 for l in reference_txt.read_text().splitlines() if ": " in l]
    hyp_lines = [l.split(": ", 1)[-1].strip()
                 for l in hypothesis_txt.read_text().splitlines() if ": " in l]

    if not ref_lines or not hyp_lines:
        return {"WER": None, "note": "Empty transcript"}

    ref_text = " ".join(ref_lines)
    hyp_text = " ".join(hyp_lines)

    # Tokenise for WER (works correctly for both Chinese and English)
    ref_tok = _tokenize(ref_text)
    hyp_tok = _tokenize(hyp_text)

    measures = jiwer.process_words(ref_tok, hyp_tok)
    cer = jiwer.cer(ref_text, hyp_text)
    return {
        "WER":          round(measures.wer * 100, 2),
        "CER":          round(cer * 100, 2),
        "substitutions": measures.substitutions,
        "deletions":     measures.deletions,
        "insertions":    measures.insertions,
        "note":         "WER = char-level for Chinese",
    }


# ─── Runner ──────────────────────────────────────────────────────────────────

def run_case(case_dir: Path, hf_token: str, skip_diarization=False, speakers=None) -> dict:
    audio     = case_dir / "audio.wav"
    ref_rttm  = case_dir / "reference.rttm"
    ref_txt   = case_dir / "reference.txt"
    hyp_rttm  = case_dir / "hypothesis.rttm"
    hyp_txt   = case_dir / "hypothesis.txt"

    if not audio.exists():
        return {"error": f"audio.wav not found in {case_dir}"}

    print(f"\n{'='*60}")
    print(f"Case: {case_dir.name}")
    print(f"{'='*60}")

    t0 = time.time()

    # 1. Transcribe
    whisper_result = run_transcription(audio)

    # 2. Diarize
    # Auto-detect speaker count from reference if available
    n_speakers = speakers
    if n_speakers is None and ref_rttm.exists():
        spks = set()
        for line in ref_rttm.read_text().splitlines():
            parts = line.split()
            if len(parts) >= 8 and parts[0] == "SPEAKER":
                spks.add(parts[7])
        n_speakers = len(spks) if spks else None
        if n_speakers:
            print(f"  ℹ️  Auto-detected {n_speakers} reference speakers")

    diarization_ann = run_diarization(
        audio, hf_token,
        num_speakers=n_speakers,
        cache_path=hyp_rttm,
        skip=skip_diarization,
    )

    # 3. Merge & produce transcript
    sys.path.insert(0, str(Path(__file__).parent.parent))
    from transcribe import merge_transcript_and_diarization, format_time

    class FakeDiarization:
        """Wrapper so merge fn can call .speaker_diarization.itertracks()"""
        def __init__(self, ann): self.speaker_diarization = ann

    lines = merge_transcript_and_diarization(whisper_result, FakeDiarization(diarization_ann))
    transcript = "\n".join(
        f"[{format_time(l['start'])} → {format_time(l['end'])}]  {l['speaker']}: {l['text']}"
        for l in lines
    )
    hyp_txt.write_text(transcript + "\n")

    elapsed = time.time() - t0
    result = {"case": case_dir.name, "elapsed_s": round(elapsed, 1)}

    # 4. Score
    if ref_rttm.exists():
        der_scores = compute_der(ref_rttm, diarization_ann)
        result["diarization"] = der_scores
        print(f"\n  📊 Diarization:")
        print(f"     DER:        {der_scores['DER']}%  (lower is better)")
        print(f"     Coverage:   {der_scores['coverage']}%")
        print(f"     Missed:     {der_scores['missed']}%")
        print(f"     Confusion:  {der_scores['confusion']}%")
        print(f"     FalseAlarm: {der_scores['false_alarm']}%")

    if ref_txt.exists() and hyp_txt.exists():
        wer_scores = compute_wer(ref_txt, hyp_txt)
        result["transcription"] = wer_scores
        print(f"\n  📝 Transcription:")
        if wer_scores.get("WER") is not None:
            print(f"     WER: {wer_scores['WER']}%  CER: {wer_scores['CER']}%")
        else:
            print(f"     {wer_scores.get('note', 'N/A')}")

    # 5. Segment stats
    segments = list(diarization_ann.itertracks(yield_label=True))
    if segments:
        durations = [(e - s) for (s, e), _, _ in segments]
        result["segments"] = {
            "count":    len(segments),
            "avg_dur_s": round(sum(durations)/len(durations), 2),
            "short_pct": round(100 * sum(1 for d in durations if d < 0.5) / len(durations), 1),
        }
        print(f"\n  🔍 Segments: {len(segments)} total, "
              f"avg {result['segments']['avg_dur_s']}s, "
              f"{result['segments']['short_pct']}% < 0.5s")

    print(f"\n  ⏱️  Elapsed: {elapsed:.1f}s")
    print(f"  💾 Hypothesis saved: {hyp_txt}")
    return result


# ─── Main ────────────────────────────────────────────────────────────────────

def main():
    args = parse_args()
    hf_token = os.environ.get("HF_TOKEN", "")
    if not hf_token:
        print("❌ HF_TOKEN not set in .env", file=sys.stderr)
        sys.exit(1)

    # Discover cases
    if args.case:
        cases = [CASES_DIR / args.case]
    else:
        cases = sorted(p for p in CASES_DIR.iterdir() if p.is_dir())

    if not cases:
        print(f"No cases found in {CASES_DIR}")
        sys.exit(1)

    print(f"🧪 Running {len(cases)} evaluation case(s)...\n")
    results = []
    for case_dir in cases:
        r = run_case(case_dir, hf_token,
                     skip_diarization=args.skip_diarization,
                     speakers=args.speakers)
        results.append(r)

    # Summary
    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    for r in results:
        der = r.get("diarization", {}).get("DER", "N/A")
        wer = r.get("transcription", {}).get("WER", "N/A")
        cov = r.get("diarization", {}).get("coverage", "N/A")
        print(f"  {r['case']:<30}  DER={der}%  WER={wer}%  Coverage={cov}%")

    REPORT_PATH.write_text(json.dumps(results, indent=2, ensure_ascii=False))
    print(f"\n📄 Full report: {REPORT_PATH}")


if __name__ == "__main__":
    main()
