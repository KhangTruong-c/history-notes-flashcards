#!/usr/bin/env python3
"""Split a long recording into chronologically named 30-minute M4A segments.

Requires ffmpeg and ffprobe on PATH. Example:
  python split_audio.py lecture.m4a --output-dir segments --minutes 30
"""
import argparse
import json
import math
import re
import shutil
import subprocess
from pathlib import Path


def format_time(seconds):
    seconds = int(seconds)
    h, remainder = divmod(seconds, 3600)
    m, s = divmod(remainder, 60)
    return f"{h:02d}-{m:02d}-{s:02d}"


def main():
    p = argparse.ArgumentParser()
    p.add_argument("input", type=Path)
    p.add_argument("--output-dir", type=Path, default=Path("segments"))
    p.add_argument("--minutes", type=int, default=30)
    a = p.parse_args()
    if not a.input.is_file():
        p.error("Input audio file does not exist")
    if a.minutes <= 0:
        p.error("minutes must be positive")
    for prog in ("ffmpeg", "ffprobe"):
        if not shutil.which(prog):
            p.error(f"{prog} is not installed")
    meta = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "json", str(a.input)], capture_output=True, text=True, check=True)
    duration = float(json.loads(meta.stdout)["format"]["duration"])
    interval = a.minutes * 60
    parts = math.ceil(duration / interval)
    safe = re.sub(r"[^a-zA-Z0-9_-]+", "_", a.input.stem).strip("_")[:48] or "lecture"
    a.output_dir.mkdir(parents=True, exist_ok=True)
    for i in range(parts):
        start = i * interval
        remaining = duration - start
        length = min(interval, remaining)
        outfile = a.output_dir / f"{safe}_Part_{i+1:02d}_{format_time(start)}_to_{format_time(start+length)}.m4a"
        cmd = ["ffmpeg", "-nostdin", "-hide_banner", "-loglevel", "error", "-y", "-ss", str(start), "-i", str(a.input), "-t", str(length), "-vn", "-c:a", "aac", "-b:a", "128k", str(outfile)]
        subprocess.run(cmd, check=True)
        if not outfile.is_file() or outfile.stat().st_size == 0:
            raise RuntimeError(f"Empty/missing audio segment: {outfile}")
        print(f"Part {i+1}/{parts}: {format_time(start)}–{format_time(start+length)} -> {outfile}")
    print(f"Duration: {duration:.2f}s; created {parts} segments")


if __name__ == "__main__":
    main()
