Diarization Error Rate

## Speaker Diarization Benchmark

## What can go wrong?

## When benchmarking speaker diarization systems, one should focus on the following three types of errors.

## A _speaker confusion_happens when a system assigns a speech turn to the wrong speaker, when it merges two speakers into one, or when it splits one speaker into multiple ones.

## A _**missed detection**_ happens when a speech turn (or part of it) is missed, or when two speakers talk on top of each other, and only one of them is detected.

## A _false alarm_ happens when the system detects a speech turn when there is none.

## Diarization error rate

In this benchmark, we report the diarization error rate (or DER), which is defined as the aggregate durations of all three types of errors divided by the total duration of speech in the recording:

![](https://framerusercontent.com/images/HlxXYhO8m3PhRCZbTM7nMkHyZ6w.png?width=2685&height=336)

## Benchmark Results (lower is better)

![](https://framerusercontent.com/images/c5Cv8Whgh2W3kAT9IHhJonXBXk.png?width=1042&height=430)

**Broadcast Interview -** Radio interview speech.

![](https://framerusercontent.com/images/ldqoOkiLN1PaXh1XJx5CPVq7QAA.png?width=1042&height=430)

**Clinical -** Clinical child assessment interviews.

![](https://framerusercontent.com/images/cPs8o9MWMV1H9ToCU2eCaYfhes.png?width=1042&height=430)

**Courtroom -** Formal multi-speaker legal speech.

![](https://framerusercontent.com/images/KSFci3j4EDfW4lGQyFUtbmTXUs.png?width=1042&height=430)

**Conversational telephone speech -** Two-speaker telephone conversations.

![](https://framerusercontent.com/images/exxUtgYqezu4opIRHbhlmQzmphY.png?width=1042&height=430)

**Map task -** Task-oriented dyadic dialogue.

![](https://framerusercontent.com/images/eGwhVeN5SGBcJc6bZDMg89GJwjE.png?width=1042&height=430)

**Meeting -** Spontaneous multi-speaker meetings.

![](https://framerusercontent.com/images/7uPeK9RbAqcjnuvgZZToQH8qfkI.png?width=1042&height=430)

**Restaurant -** Noisy informal group conversations.

![](https://framerusercontent.com/images/EvxL7sPexI8xeGPYCcokL96Rjc.png?width=1042&height=430)

**Sociolinguistic (field) -** Field sociolinguistic interviews.

![](https://framerusercontent.com/images/k5vSn6tntWYZlTPhPGkPA0FHGxQ.png?width=1042&height=430)

**Sociolinguistic (lab) -** Controlled sociolinguistic interviews.

![](https://framerusercontent.com/images/U1KFD5WjhCVc68Sb2NZ7tHe0EoM.png?width=1042&height=430)

**Web video -** Diverse online video speech.

## Evaluation Datasets

DIHARD Broadcast

DIHARD Clinical

DIHARD Court

DIHARD CTS

DIHARD Maptask

DIHARD Meeting

DIHARD Restaurant

DIHARD Socio Field

DIHARD Socio Lab

DIHARD Webvideo

## Models

pyannoteAI - Precision-2

pyannoteAI - OSS Community-1

AssemblyAI - Universal

Deepgram - Nova-3

ElevenLabs - Scribe-v1

Soniox - STT-async-preview-v1

Speechmatics - Enhanced

OpenAI - GPT-4o-transcribe-diarize

AWS - Transcribe, word-level

NVIDIA - OSS NeMo streaming sortformer (very high latency)

## Benchmark Report Methodology

## 10

## distinct areas of use

## 259

## recordings

## 9.3%

## of overlap speech

## ≈67

## hours of challenging, multi‑domain audio

## Methodology

## We compare speaker diarization pipelines on a wide range of benchmarks, covering various acoustic conditions and conversation setups.    We rely on [pyannote.metrics](https://pyannote.github.io/pyannote-metrics/) open source evaluation toolkit, which has become the _de facto_ reference implementation in both academia and industry.    Commercial APIs were accessed via provider endpoints. Open-source models were evaluated using self-hosted instances. We did not provide the number of speakers for any of them.

## Results

## For pyannoteAI OSS and commercial models, we made sure not to leak any test data into our training set. For other providers, there is no guarantee that this is the case, since they do not communicate this piece of information.

Speaker Intelligence Platform for developers

Detect, segment, label and separate speakers in any language.

[Get Started](https://dashboard.pyannote.ai/signin)

[Book a demo](https://www.pyannote.ai/contact-us)

![](https://framerusercontent.com/images/1XnoCfXQd03xfLAfQujsKwYKU.png?width=2880&height=400)

[52m](https://huggingface.co/pyannote)

[9952](https://github.com/pyannote/pyannote-audio)

[24m](https://pepy.tech/projects/pyannote-audio?timeRange=threeMonths&category=version&includeCIDownloads=true&granularity=monthly&viewType=line&versions=4.0.4%2C4.0.3%2C4.0.2)

Product

[Speaker platform](https://www.pyannote.ai/speaker-platform)

[Streaming](https://www.pyannote.ai/streaming)

[Enterprise](https://www.pyannote.ai/enterprise)

[Use cases](https://www.pyannote.ai/usecases)

[Pricing](https://www.pyannote.ai/pricing)

Developers

[Documentation](https://docs.pyannote.ai/introduction)

[Playground](https://dashboard.pyannote.ai/signin)

[Support](mailto: pyannoteAI Support <support@pyannote.ai>)

[Changelog](https://www.pyannote.ai/changelog)

Resources

[About us](https://www.pyannote.ai/about-us)

[Customer Story](https://www.pyannote.ai/customer-story)

[Benchmarks](https://www.pyannote.ai/benchmark)

[Demo](https://www.pyannote.ai/demo)

[Blog](https://www.pyannote.ai/blog)

[Career](https://www.notion.so/pyannoteAI-Job-board-2b062efaec7f80e2a1c0dcb8c728cfff)

©pyannoteAI 2026 ﹒

[Cookie preferences](https://www.pyannote.ai/benchmark#)

[Terms of use](https://www.pyannote.ai/terms-of-use) ﹒

[Privacy policy .](https://www.pyannote.ai/privacy-policy)

[Trust Center](https://trust.pyannote.ai/)

### Cookie preferences

This website utilizes technologies such as cookies to enable essential site functionality, as well as for analytics and personalization. You may change your settings at any time or accept the default settings. [Privacy Policy](https://www.pyannote.ai/privacy-policy)

Manage preferencesReject non-essentialAccept all