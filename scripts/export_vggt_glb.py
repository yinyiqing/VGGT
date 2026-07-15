#!/usr/bin/env python
"""Export VGGT predictions to lightweight point-cloud files."""

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
    parser.add_argument("--max-points", type=int, default=500000)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--also-ply", action="store_true")
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

    points_out = points_flat[mask]
    colors_out = colors_flat[mask]
    if len(points_out) > args.max_points:
        rng = np.random.default_rng(args.seed)
        keep = rng.choice(len(points_out), size=args.max_points, replace=False)
        points_out = points_out[keep]
        colors_out = colors_out[keep]

    center = np.median(points_out, axis=0)
    points_out = points_out - center

    point_cloud = trimesh.PointCloud(vertices=points_out, colors=colors_out)
    scene = trimesh.Scene(point_cloud)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    scene.export(file_obj=args.output)
    print(f"Saved GLB: {args.output}")
    print(f"Exported points: {len(points_out)}")

    if args.also_ply:
        ply_path = args.output.with_suffix(".ply")
        point_cloud.export(file_obj=ply_path)
        print(f"Saved PLY: {ply_path}")


if __name__ == "__main__":
    main()
