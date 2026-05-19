# WhisperDiarize — macOS App

Native macOS app for the whisper-diarize pipeline. Drag, drop, transcribe.

<img width="860" alt="WhisperDiarize screenshot" src="../docs/app-screenshot.png">

## Features

- 🖱️ **Drag & drop** audio files onto the window
- 📊 **Live log** streams output as transcription runs
- 🎨 **Speaker-colored** transcript with per-speaker filter pills
- 🔍 **Search** through the transcript
- 📋 **Copy** to clipboard or **Save** as `.txt`
- ⚙️ **Settings panel** — model, language, speaker count, HF token

## Requirements

- macOS 14+
- Xcode 16+
- `uv` installed ([astral.sh/uv](https://docs.astral.sh/uv/))
- HuggingFace token with diarization model access

## Build & Run

```bash
# Open in Xcode
open app/Package.swift

# Or from the app/ directory
cd app
open Package.swift
```

Then **Product → Run** (`⌘R`).

## First Launch

1. Open **Settings** (`⌘,`) and paste your HuggingFace token
2. Make sure you've accepted the model terms:
   - https://huggingface.co/pyannote/speaker-diarization-3.1
   - https://huggingface.co/pyannote/segmentation-3.0
   - https://huggingface.co/pyannote/speaker-diarization-community-1
3. Drag an audio file onto the window

The Python environment is set up automatically on first use (installs into `~/Library/Application Support/WhisperDiarize/`).

## Architecture

```
App.swift                   @main entry point
ContentView.swift           Root — switches between 4 states
├── DropZoneView.swift      idle: drag & drop + quick settings bar
├── ProcessingView.swift    running: progress + live log stream
├── TranscriptView.swift    done: speaker-colored, searchable transcript
├── ErrorView.swift         failed: error + retry
├── SettingsView.swift      Settings window (⌘,)
└── TranscriptionRunner.swift  ObservableObject — manages subprocess
```

The app bundles `transcribe.py`, `pyproject.toml`, and `uv.lock` as resources, copies them to Application Support on first launch, and runs the Python pipeline as a subprocess via `uv run`.

## Keeping Resources in Sync

When the Python script is updated in the repo root, sync it to the app bundle:

```bash
make sync-app-resources   # from repo root
```
