#!/usr/bin/env python
"""Export lightweight PNG/JPG previews from a VGGT predictions.npz file."""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
from PIL import Image


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--predictions", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--cols", type=int, default=5)
    return parser.parse_args()


def normalize(x: np.ndarray) -> np.ndarray:
    x = np.asarray(x, dtype=np.float32)
    finite = np.isfinite(x)
    if not finite.any():
        return np.zeros_like(x, dtype=np.uint8)
    lo, hi = np.percentile(x[finite], [2, 98])
    if hi <= lo:
        hi = lo + 1e-6
    y = np.clip((x - lo) / (hi - lo), 0, 1)
    return (y * 255).astype(np.uint8)


def make_grid(frames: list[np.ndarray], cols: int) -> Image.Image:
    images = [Image.fromarray(frame) for frame in frames]
    w, h = images[0].size
    rows = int(np.ceil(len(images) / cols))
    canvas = Image.new("RGB", (cols * w, rows * h), color=(255, 255, 255))
    for i, img in enumerate(images):
        canvas.paste(img.convert("RGB"), ((i % cols) * w, (i // cols) * h))
    return canvas


def gray_to_rgb(x: np.ndarray) -> np.ndarray:
    return np.repeat(x[..., None], 3, axis=-1)


def main() -> None:
    args = parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    data = np.load(args.predictions, allow_pickle=True)

    images = data["images"].transpose(0, 2, 3, 1)
    image_frames = [(np.clip(img, 0, 1) * 255).astype(np.uint8) for img in images]
    make_grid(image_frames, args.cols).save(args.output_dir / "images_grid.jpg", quality=90)

    depth = data["depth"][..., 0]
    depth_frames = [gray_to_rgb(normalize(frame)) for frame in depth]
    make_grid(depth_frames, args.cols).save(args.output_dir / "depth_grid.png")

    for key in ["depth_conf", "world_points_conf"]:
        if key in data:
            frames = [gray_to_rgb(normalize(frame)) for frame in data[key]]
            make_grid(frames, args.cols).save(args.output_dir / f"{key}_grid.png")

    print(f"Saved previews to {args.output_dir}")


if __name__ == "__main__":
    main()
