#!/usr/bin/env python
"""Render simple PNG previews from a VGGT point cloud prediction."""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--predictions", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--conf-percent", type=float, default=50.0)
    parser.add_argument("--max-points", type=int, default=120000)
    parser.add_argument("--seed", type=int, default=0)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    data = np.load(args.predictions, allow_pickle=True)

    points = data["world_points"].reshape(-1, 3)
    conf = data["world_points_conf"].reshape(-1)
    colors = (np.clip(data["images"].transpose(0, 2, 3, 1), 0, 1) * 255).astype(np.uint8).reshape(-1, 3)

    threshold = np.percentile(conf, args.conf_percent)
    mask = np.isfinite(points).all(axis=1) & (conf >= threshold) & (conf > 1e-5)
    points = points[mask]
    colors = colors[mask] / 255.0

    if len(points) > args.max_points:
        rng = np.random.default_rng(args.seed)
        keep = rng.choice(len(points), size=args.max_points, replace=False)
        points = points[keep]
        colors = colors[keep]

    points = points - np.median(points, axis=0)

    fig = plt.figure(figsize=(12, 6), dpi=160)
    views = [(20, -60, "view_a"), (30, 35, "view_b")]
    for i, (elev, azim, title) in enumerate(views, start=1):
        ax = fig.add_subplot(1, 2, i, projection="3d")
        ax.scatter(points[:, 0], points[:, 1], points[:, 2], c=colors, s=0.15, linewidths=0)
        ax.view_init(elev=elev, azim=azim)
        ax.set_title(title)
        ax.set_axis_off()
        ax.set_box_aspect(np.ptp(points, axis=0))

    args.output.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(args.output, bbox_inches="tight", pad_inches=0.02)
    print(f"Saved preview: {args.output}")


if __name__ == "__main__":
    main()
