#!/usr/bin/env python
"""Run one VGGT experiment and generate the standard inspection report."""

from __future__ import annotations

import argparse
import subprocess
import sys
from datetime import datetime
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--image-folder", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--title", type=str, default=None)
    parser.add_argument("--weights-path", type=Path, default=Path("weights/VGGT-1B/model.pt"))
    parser.add_argument("--official-root", type=Path, default=Path("official-vggt"))
    parser.add_argument("--single-frame", type=int, default=0)
    parser.add_argument("--background", choices=["white", "dark"], default="white")
    parser.add_argument("--point-size", type=float, default=0.3)
    parser.add_argument("--skip-3d", action="store_true")
    return parser.parse_args()


def rel(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(REPO_ROOT))
    except ValueError:
        return str(path)


def run(cmd: list[str]) -> None:
    print(" ".join(cmd))
    subprocess.run(cmd, cwd=REPO_ROOT, check=True)


def write_readme_if_missing(args: argparse.Namespace, title: str) -> None:
    readme_path = args.output_dir / "README.md"
    if readme_path.exists():
        return

    lines = [
        f"# {title}",
        "",
        "目的：记录一次 VGGT 复现实验。",
        "",
        f"- 日期：{datetime.now().strftime('%Y-%m-%d')}",
        f"- 输入：`{rel(args.image_folder)}`",
        f"- 权重：`{rel(args.weights_path)}`",
        "- 命令：",
        "",
        "```bash",
        "conda run --no-capture-output -n vggt python scripts/run_vggt_experiment.py \\",
        f"  --image-folder {rel(args.image_folder)} \\",
        f"  --output-dir {rel(args.output_dir)} \\",
        f"  --title {title}",
        "```",
        "",
        "结果：",
        "",
        "- 摘要：`summary.json`",
        "- 报告：`report.md`",
        "- 预览：`artifacts/01_preview_images/`",
        "- 3D：`artifacts/02_pointcloud_files/`",
        "",
        "人工观察：",
        "",
        "- 成功现象：",
        "- 失败现象：",
        "- 初步判断：",
        "- 下一步：",
        "",
    ]
    readme_path.parent.mkdir(parents=True, exist_ok=True)
    readme_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Saved README: {readme_path}")


def main() -> None:
    args = parse_args()
    args.image_folder = args.image_folder.resolve()
    args.output_dir = args.output_dir.resolve()
    args.weights_path = args.weights_path.resolve()
    args.official_root = args.official_root.resolve()
    title = args.title or args.output_dir.name

    run(
        [
            sys.executable,
            "scripts/run_vggt_folder.py",
            "--image-folder",
            rel(args.image_folder),
            "--output-dir",
            rel(args.output_dir),
            "--weights-path",
            rel(args.weights_path),
            "--official-root",
            rel(args.official_root),
        ]
    )

    report_cmd = [
        sys.executable,
        "scripts/make_vggt_report.py",
        "--predictions",
        rel(args.output_dir / "predictions.npz"),
        "--output-dir",
        rel(args.output_dir),
        "--title",
        title,
        "--single-frame",
        str(args.single_frame),
        "--background",
        args.background,
        "--point-size",
        str(args.point_size),
    ]
    if args.skip_3d:
        report_cmd.append("--skip-3d")
    run(report_cmd)

    write_readme_if_missing(args, title)


if __name__ == "__main__":
    main()
