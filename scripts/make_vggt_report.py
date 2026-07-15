#!/usr/bin/env python
"""Generate a standard VGGT inspection report from predictions.npz."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

import numpy as np


REPO_ROOT = Path(__file__).resolve().parents[1]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--predictions", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, default=None)
    parser.add_argument("--title", type=str, default=None)
    parser.add_argument("--single-frame", type=int, default=0)
    parser.add_argument("--clean-conf", type=float, default=50.0)
    parser.add_argument("--detail-conf", type=float, default=10.0)
    parser.add_argument("--clean-max-points", type=int, default=500000)
    parser.add_argument("--detail-max-points", type=int, default=2000000)
    parser.add_argument("--preview-max-points", type=int, default=120000)
    parser.add_argument("--point-size", type=float, default=0.25)
    parser.add_argument("--background", choices=["white", "dark"], default="white")
    parser.add_argument("--skip-3d", action="store_true")
    return parser.parse_args()


def run(cmd: list[str]) -> None:
    print(" ".join(cmd))
    subprocess.run(cmd, cwd=REPO_ROOT, check=True)


def fmt_conf(value: float) -> str:
    return str(int(value)) if float(value).is_integer() else str(value).replace(".", "p")


def quantiles(x: np.ndarray) -> dict[str, float]:
    x = np.asarray(x, dtype=np.float32)
    finite = x[np.isfinite(x)]
    if len(finite) == 0:
        return {}
    qs = np.percentile(finite, [0, 5, 10, 25, 50, 75, 90, 95, 100])
    names = ["min", "p05", "p10", "p25", "p50", "p75", "p90", "p95", "max"]
    return {name: round(float(value), 4) for name, value in zip(names, qs)}


def rel(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(REPO_ROOT))
    except ValueError:
        return str(path)


def main() -> None:
    args = parse_args()
    predictions = args.predictions.resolve()
    output_dir = args.output_dir.resolve() if args.output_dir else predictions.parent.resolve()
    title = args.title or output_dir.name

    previews_dir = output_dir / "artifacts" / "01_preview_images"
    three_d_dir = output_dir / "artifacts" / "02_pointcloud_files"
    report_path = output_dir / "report.md"

    data = np.load(predictions, allow_pickle=True)
    image_count = int(data["images"].shape[0])
    if args.single_frame < 0 or args.single_frame >= image_count:
        raise ValueError(f"--single-frame must be in [0, {image_count - 1}]")

    previews_dir.mkdir(parents=True, exist_ok=True)
    if not args.skip_3d:
        three_d_dir.mkdir(parents=True, exist_ok=True)

    run(
        [
            sys.executable,
            "scripts/export_vggt_previews.py",
            "--predictions",
            rel(predictions),
            "--output-dir",
            rel(previews_dir),
        ]
    )

    clean_conf = fmt_conf(args.clean_conf)
    detail_conf = fmt_conf(args.detail_conf)
    frame_tag = f"frame{args.single_frame:02d}"

    preview_jobs = [
        (
            previews_dir / f"pointcloud_clean_conf{clean_conf}.png",
            args.clean_conf,
            None,
            args.preview_max_points,
        ),
        (
            previews_dir / f"pointcloud_detail_conf{detail_conf}.png",
            args.detail_conf,
            None,
            args.preview_max_points,
        ),
        (
            previews_dir / f"{frame_tag}_pointcloud_conf{detail_conf}.png",
            args.detail_conf,
            args.single_frame,
            args.preview_max_points,
        ),
    ]
    for output, conf, frame_index, max_points in preview_jobs:
        cmd = [
            sys.executable,
            "scripts/render_vggt_pointcloud_preview.py",
            "--predictions",
            rel(predictions),
            "--output",
            rel(output),
            "--conf-percent",
            str(conf),
            "--max-points",
            str(max_points),
            "--point-size",
            str(args.point_size),
            "--background",
            args.background,
        ]
        if frame_index is not None:
            cmd.extend(["--frame-index", str(frame_index)])
        run(cmd)

    three_d_files: list[Path] = []
    if not args.skip_3d:
        export_jobs = [
            (
                three_d_dir / f"scene_conf{clean_conf}_{args.clean_max_points // 1000}k.glb",
                args.clean_conf,
                None,
                args.clean_max_points,
            ),
            (
                three_d_dir / f"scene_conf{detail_conf}_{args.detail_max_points // 1000000}m.glb",
                args.detail_conf,
                None,
                args.detail_max_points,
            ),
            (
                three_d_dir / f"{frame_tag}_conf{detail_conf}_{args.clean_max_points // 1000}k.glb",
                args.detail_conf,
                args.single_frame,
                args.clean_max_points,
            ),
        ]
        for output, conf, frame_index, max_points in export_jobs:
            cmd = [
                sys.executable,
                "scripts/export_vggt_glb.py",
                "--predictions",
                rel(predictions),
                "--output",
                rel(output),
                "--conf-percent",
                str(conf),
                "--max-points",
                str(max_points),
                "--also-ply",
            ]
            if frame_index is not None:
                cmd.extend(["--frame-index", str(frame_index)])
            run(cmd)
            three_d_files.extend([output, output.with_suffix(".ply")])

    lines = [
        f"# {title} VGGT 检查报告",
        "",
        "这份报告由 `scripts/make_vggt_report.py` 生成，用来快速判断一次 VGGT 输出是否值得继续分析。",
        "",
        "## 基本信息",
        "",
        f"- predictions：`{rel(predictions)}`",
        f"- 图片数量：{image_count}",
        f"- 输出目录：`{rel(output_dir)}`",
        f"- 单帧检查：第 {args.single_frame} 张",
        "",
        "## 置信度分布",
        "",
    ]

    for key in ["depth_conf", "world_points_conf"]:
        if key in data:
            lines.append(f"- `{key}`：`{quantiles(data[key])}`")
    lines.extend(
        [
            "",
            "## 推荐查看顺序",
            "",
            f"1. 输入图：`{rel(previews_dir / 'images_grid.jpg')}`",
            f"2. depth：`{rel(previews_dir / 'depth_grid.png')}`",
            f"3. confidence：`{rel(previews_dir / 'world_points_conf_grid.png')}`",
            f"4. 干净点云 PNG：`{rel(previews_dir / f'pointcloud_clean_conf{clean_conf}.png')}`",
            f"5. 细节点云 PNG：`{rel(previews_dir / f'pointcloud_detail_conf{detail_conf}.png')}`",
            f"6. 单帧点云 PNG：`{rel(previews_dir / f'{frame_tag}_pointcloud_conf{detail_conf}.png')}`",
            "",
            "## 3D 文件",
            "",
        ]
    )

    if three_d_files:
        for path in three_d_files:
            lines.append(f"- `{rel(path)}`")
    else:
        lines.append("- 本次跳过 3D 导出。")

    lines.extend(
        [
            "",
            "## 人工观察",
            "",
            "- 成功现象：",
            "- 失败现象：",
            "- 初步判断：",
            "- 下一步：",
            "",
        ]
    )
    report_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Saved report: {report_path}")


if __name__ == "__main__":
    main()
