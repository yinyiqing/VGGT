#!/usr/bin/env python
"""Export a VGGT predictions.npz file to a browser-friendly point-cloud GLB."""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import trimesh


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--predictions", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--conf-percent", type=float, default=50.0)
    parser.add_argument("--mode", choices=["pointmap", "depth"], default="pointmap")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    predictions = dict(np.load(args.predictions, allow_pickle=True))
    if args.mode == "pointmap":
        points = predictions["world_points"]
        conf = predictions["world_points_conf"]
    else:
        points = predictions["world_points_from_depth"]
        conf = predictions["depth_conf"]

    images = predictions["images"].transpose(0, 2, 3, 1)
    colors = (np.clip(images, 0, 1) * 255).astype(np.uint8)

    points_flat = points.reshape(-1, 3)
    colors_flat = colors.reshape(-1, 3)
    conf_flat = conf.reshape(-1)

    threshold = np.percentile(conf_flat, args.conf_percent)
    mask = np.isfinite(points_flat).all(axis=1) & (conf_flat >= threshold) & (conf_flat > 1e-5)

    point_cloud = trimesh.PointCloud(vertices=points_flat[mask], colors=colors_flat[mask])
    scene = trimesh.Scene(point_cloud)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    scene.export(file_obj=args.output)
    print(f"Saved GLB: {args.output}")


if __name__ == "__main__":
    main()
