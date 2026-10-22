#!/usr/bin/env python3
"""
auto_edit_video.py - Unified FFmpeg Video Automation Pipeline

Implements:
1. Acoustic silence detection & trimming (150ms in / 250ms out padding, 0.08s audio micro-fades)
2. Contextual zooms (punch-in crop preserving 16:9 and setsar=1)
3. Lower-third graphical composition with smooth opacity fades
4. Output 1080p60 encoding with H.264 & AAC
"""

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import List, Tuple, Dict, Any, Optional


def run_command(cmd: List[str], check: bool = True) -> subprocess.CompletedProcess:
    """Executes a command returning completed process."""
    cmd_str = " ".join(f'"{c}"' if " " in c else c for c in cmd)
    print(f"[EXEC] {cmd_str}")
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding="utf-8", errors="replace")
    if check and result.returncode != 0:
        print(f"[ERROR] Command failed with code {result.returncode}:\n{result.stderr}", file=sys.stderr)
        raise RuntimeError(f"Command execution error: {cmd[0]}")
    return result


def detect_silences(video_path: str, noise_db: float = -30.0, min_duration: float = 0.5) -> List[Tuple[float, float]]:
    """Uses ffmpeg silencedetect to detect silence intervals."""
    cmd = [
        "ffmpeg", "-hide_banner", "-vn",
        "-i", video_path,
        "-af", f"silencedetect=noise={noise_db}dB:d={min_duration}",
        "-f", "null", "-"
    ]
    res = run_command(cmd, check=False)
    
    silences = []
    current_start = None
    
    for line in res.stderr.splitlines():
        start_match = re.search(r"silence_start:\s*([0-9.]+)", line)
        if start_match:
            current_start = float(start_match.group(1))
            continue
        
        end_match = re.search(r"silence_end:\s*([0-9.]+)", line)
        if end_match and current_start is not None:
            end_time = float(end_match.group(1))
            silences.append((current_start, end_time))
            current_start = None

    return silences


def get_video_duration(video_path: str) -> float:
    """Returns duration in seconds using ffprobe."""
    cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        video_path
    ]
    res = run_command(cmd)
    try:
        return float(res.stdout.strip())
    except Exception:
        return 0.0


def calculate_speech_segments(
    total_duration: float,
    silences: List[Tuple[float, float]],
    pad_in: float = 0.15,
    pad_out: float = 0.25
) -> List[Tuple[float, float]]:
    """Calculates active audio segments with natural padding."""
    if not silences:
        return [(0.0, total_duration)]

    segments = []
    last_end = 0.0

    for s_start, s_end in silences:
        seg_start = max(0.0, last_end - pad_out if last_end > 0 else 0.0)
        seg_end = min(total_duration, s_start + pad_in)
        if seg_end - seg_start > 0.3:  # minimum chunk length
            segments.append((seg_start, seg_end))
        last_end = s_end

    if total_duration - (last_end - pad_out) > 0.3:
        segments.append((max(0.0, last_end - pad_out), total_duration))

    return segments


def build_filtergraph(
    segments: List[Tuple[float, float]],
    lower_third_path: Optional[str] = None,
    lt_start: float = 1.0,
    lt_end: float = 10.0,
    punch_ins: Optional[List[Dict[str, Any]]] = None
) -> Tuple[str, str, str]:
    """
    Constructs complex filtergraph preserving aspect ratio, SAR=1, micro-fades,
    and optional lower-third overlay.
    """
    filter_chains = []
    v_outputs = []
    a_outputs = []

    for idx, (st, en) in enumerate(segments):
        duration = en - st
        v_tag = f"v{idx}"
        a_tag = f"a{idx}"

        # Video trim & reset pts
        v_filters = [f"trim=start={st:.3f}:end={en:.3f}", "setpts=PTS-STARTPTS"]

        # Check for punch-in zoom within this segment
        is_zoomed = False
        if punch_ins:
            for p in punch_ins:
                if st >= p.get("start", 0) and en <= p.get("end", 0):
                    crop_w = p.get("w", 1440)
                    crop_h = p.get("h", 810)
                    crop_x = p.get("x", "(in_w-out_w)/2")
                    crop_y = p.get("y", "(in_h-out_h)/2")
                    v_filters.append(f"crop={crop_w}:{crop_h}:{crop_x}:{crop_y}")
                    is_zoomed = True
                    break

        v_filters.append("scale=1920:1080:force_original_aspect_ratio=decrease")
        v_filters.append("pad=1920:1080:(ow-iw)/2:(oh-ih)/2")
        v_filters.append("setsar=1")
        filter_chains.append(f"[0:v]{','.join(v_filters)}[{v_tag}]")
        v_outputs.append(f"[{v_tag}]")

        # Audio trim with micro-fades
        fade_d = min(0.08, duration / 4)
        a_filters = [
            f"atrim=start={st:.3f}:end={en:.3f}",
            "asetpts=PTS-STARTPTS",
            f"afade=t=in:st=0:d={fade_d:.3f}",
            f"afade=t=out:st={(duration - fade_d):.3f}:d={fade_d:.3f}"
        ]
        filter_chains.append(f"[0:a]{','.join(a_filters)}[{a_tag}]")
        a_outputs.append(f"[{a_tag}]")

    # Concat video and audio
    n = len(segments)
    concat_v_in = "".join(v_outputs)
    concat_a_in = "".join(a_outputs)
    filter_chains.append(f"{concat_v_in}concat=n={n}:v=1:a=0[v_concat]")
    filter_chains.append(f"{concat_a_in}concat=n={n}:v=0:a=1[a_final]")

    final_v = "[v_concat]"

    # Overlay lower-third if provided
    if lower_third_path and Path(lower_third_path).exists():
        lt_filter = (
            f"[1:v]format=rgba,"
            f"fade=t=in:st={lt_start}:d=0.4:alpha=1,"
            f"fade=t=out:st={lt_end - 0.4}:d=0.4:alpha=1[lt_faded];"
            f"[v_concat][lt_faded]overlay=0:0:enable='between(t,{lt_start},{lt_end})'[v_final]"
        )
        filter_chains.append(lt_filter)
        final_v = "[v_final]"
    else:
        filter_chains.append(f"[v_concat]null[v_final]")
        final_v = "[v_final]"

    return ";".join(filter_chains), final_v, "[a_final]"


def auto_edit(input_video: str, output_video: str, config_path: Optional[str] = None):
    """Executes full automated pipeline."""
    if not Path(input_video).exists():
        print(f"[ERROR] Input video '{input_video}' does not exist.", file=sys.stderr)
        sys.exit(1)

    config = {}
    if config_path and Path(config_path).exists():
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)

    # Configuration overrides
    noise_db = config.get("noise_db", -30.0)
    min_silence = config.get("min_silence_duration", 0.5)
    pad_in = config.get("pad_in", 0.15)
    pad_out = config.get("pad_out", 0.25)
    lower_third = config.get("lower_third_path")
    lt_start = config.get("lower_third_start", 1.0)
    lt_end = config.get("lower_third_end", 10.0)
    punch_ins = config.get("punch_ins", [])

    print(f"[INFO] Analyzing media: {input_video}")
    total_duration = get_video_duration(input_video)
    print(f"[INFO] Video total duration: {total_duration:.2f}s")

    print("[INFO] Detecting acoustic silences...")
    silences = detect_silences(input_video, noise_db=noise_db, min_duration=min_silence)
    print(f"[INFO] Found {len(silences)} silence zones.")

    segments = calculate_speech_segments(total_duration, silences, pad_in=pad_in, pad_out=pad_out)
    print(f"[INFO] Computed {len(segments)} narrative speech chunks.")

    filtergraph, final_v, final_a = build_filtergraph(
        segments=segments,
        lower_third_path=lower_third,
        lt_start=lt_start,
        lt_end=lt_end,
        punch_ins=punch_ins
    )

    cmd = ["ffmpeg", "-y", "-i", input_video]
    if lower_third and Path(lower_third).exists():
        cmd.extend(["-i", lower_third])

    cmd.extend([
        "-filter_complex", filtergraph,
        "-map", final_v,
        "-map", final_a,
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "18",
        "-r", "60",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "192k",
        "-movflags", "+faststart",
        output_video
    ])

    print(f"[INFO] Rendering finalized cut to {output_video}...")
    run_command(cmd)
    print(f"[SUCCESS] Video rendered successfully: {output_video}")


def main():
    parser = argparse.ArgumentParser(description="FFmpeg Video Auto-Editor with Silence Trimming & Punch-in Zooms")
    parser.add_argument("--input", "-i", required=True, help="Input video file path")
    parser.add_argument("--output", "-o", required=True, help="Output finalized video path")
    parser.add_argument("--config", "-c", help="Path to JSON configuration file")
    parser.add_argument("--lower-third", help="Optional path to lower-third PNG overlay")

    args = parser.parse_args()
    cfg_path = args.config
    auto_edit(args.input, args.output, config_path=cfg_path)


if __name__ == "__main__":
    main()
