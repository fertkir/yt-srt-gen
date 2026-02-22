# yt-srt-gen

`yt-srt-gen` is a tool for downloading YouTube videos, generating subtitles using OpenAI Whisper, and translating them into another language (e.g., English) automatically.

## Features

* Download YouTube videos using `yt-dlp`.
* Generate subtitles with OpenAI Whisper.
* Translate subtitles to a target language using `googletrans`.
* Supports multiple subtitle formats: `srt`, `vtt`, `txt`, `tsv`, `json`.

## Installation

```bash
pip install yt-srt-gen
```
Install `openai-whisper` if not installed. 
```bash
pip install openai-whisper
```
`yt-srt-gen` requires `openai-whisper`, but it doesn't ship it as a dependency to save up disk space when
both packages are needed separately and installed via `pipx`.

## Usage

```bash
yt-srt-gen <YouTube URL> [OPTIONS]
```

### Arguments

* `<YouTube URL>`: URL of the YouTube video.

### Options

* `--source-language`, `-s`: Language spoken in the audio.
* `--target-language`, `-t`: Language for translated subtitles.
* `--output-format`, `-f`: Subtitle output format (`txt`, `vtt`, `srt`, `tsv`, `json`, `all`, default: `srt`).
* `--whisper-args`, `-w`: Additional arguments to pass to openai-whisper.

### Examples

```bash
yt-srt-gen https://www.youtube.com/watch?v=dQw4w9WgXcQ --source-language es --target-language en --output-format srt
```

```bash
yt-srt-gen https://www.youtube.com/watch?v=dQw4w9WgXcQ -s sr -t en -w "--model small --fp16 False"
```

This will download the video, generate Spanish subtitles, and append English translations.
