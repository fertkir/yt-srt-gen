import argparse
import asyncio
import sys
from pathlib import Path

from googletrans import Translator
from whisper.transcribe import cli as whisper_cli
from yt_dlp import YoutubeDL


def download_video(url):
    ydl_opts = {'format': 'bestvideo+bestaudio/best'}
    with YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        video_path = ydl.prepare_filename(info_dict)
    return video_path


def generate_srt(video_path):
    srt_filepath = Path(video_path).with_suffix(".srt")
    if srt_filepath.exists():
        print(str(srt_filepath) + " already exists, skipping the step")
    else:
        old_argv = sys.argv.copy()
        try:
            sys.argv = [
                "whisper", video_path,
                "--device", "cpu",
                "--language", "Serbian",
                "--output_format", "srt",
            ]
            whisper_cli()
        finally:
            sys.argv = old_argv
    return srt_filepath


async def append_english_translation(input_file: str, output_file: str):
    translator = Translator()

    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    new_lines = []
    for line in lines:
        stripped = line.strip()
        new_lines.append(line)  # keep original line
        # Only translate lines that are not empty, numbers, or timestamps
        if stripped and not stripped.isdigit() and "-->" not in stripped:
            translated = (await translator.translate(stripped, src='sr', dest='en')).text
            new_lines.append(translated + '\n')  # append translation

    with open(output_file, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)


def main():
    parser = argparse.ArgumentParser(description="Download YouTube video and generate translated subtitles.")
    parser.add_argument("url", help="YouTube video URL")
    parser.add_argument("--model", default="base", help="Whisper model to use (tiny, base, small, medium, large)")
    args = parser.parse_args()

    print("\n[+] Downloading video...")
    video_path = download_video(args.url)

    print("\n[+] Generating subtitles...")
    srt_path = generate_srt(video_path)

    print("[+] Translating subtitles to English...")
    translated_srt_path = Path(srt_path).with_suffix(".txt")
    asyncio.run(append_english_translation(str(srt_path), str(translated_srt_path)))

    print(f"[+] Done! Translated subtitles saved as: {translated_srt_path}")
