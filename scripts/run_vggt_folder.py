#!/usr/bin/env python
"""Run VGGT on an image folder and save remote-friendly artifacts."""

from __future__ import annotations

import argparse
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import numpy as np


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--image-folder", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--official-root", type=Path, default=Path("official-vggt"))
    parser.add_argument("--weights-url", default="https://huggingface.co/facebook/VGGT-1B/resolve/main/model.pt")
    return parser.parse_args()


def image_files(image_folder: Path) -> list[Path]:
    suffixes = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}
    return sorted(p for p in image_folder.iterdir() if p.is_file() and p.suffix.lower() in suffixes)


def main() -> None:
    args = parse_args()
    official_root = args.official_root.resolve()
    image_folder = args.image_folder.resolve()
    output_dir = args.output_dir.resolve()

    if not official_root.exists():
        raise FileNotFoundError(f"Official VGGT checkout not found: {official_root}")
    if not image_folder.exists():
        raise FileNotFoundError(f"Image folder not found: {image_folder}")

    names = image_files(image_folder)
    if not names:
        raise ValueError(f"No images found in {image_folder}")

    output_dir.mkdir(parents=True, exist_ok=True)
    sys.path.insert(0, str(official_root))

    import torch
    from vggt.models.vggt import VGGT
    from vggt.utils.geometry import unproject_depth_map_to_point_map
    from vggt.utils.load_fn import load_and_preprocess_images
    from vggt.utils.pose_enc import pose_encoding_to_extri_intri

    if not torch.cuda.is_available():
        raise RuntimeError("CUDA is not available. VGGT reproduction expects a CUDA GPU.")

    device = "cuda"
    dtype = torch.bfloat16 if torch.cuda.get_device_capability()[0] >= 8 else torch.float16

    started = time.perf_counter()
    torch.cuda.reset_peak_memory_stats()

    print("Loading VGGT weights...")
    model = VGGT()
    state_dict = torch.hub.load_state_dict_from_url(args.weights_url)
    model.load_state_dict(state_dict)
    model.eval().to(device)

    print(f"Loading {len(names)} images from {image_folder}")
    images = load_and_preprocess_images([str(p) for p in names]).to(device)

    print("Running inference...")
    with torch.no_grad():
        with torch.cuda.amp.autocast(dtype=dtype):
            predictions = model(images)

    extrinsic, intrinsic = pose_encoding_to_extri_intri(predictions["pose_enc"], images.shape[-2:])
    predictions["extrinsic"] = extrinsic
    predictions["intrinsic"] = intrinsic

    for key, value in list(predictions.items()):
        if isinstance(value, torch.Tensor):
            predictions[key] = value.detach().cpu().numpy().squeeze(0)
    predictions["pose_enc_list"] = None

    world_points = unproject_depth_map_to_point_map(
        predictions["depth"], predictions["extrinsic"], predictions["intrinsic"]
    )
    predictions["world_points_from_depth"] = world_points

    prediction_path = output_dir / "predictions.npz"
    np.savez_compressed(prediction_path, **predictions)

    elapsed = time.perf_counter() - started
    peak_vram_gb = torch.cuda.max_memory_allocated() / 1024**3
    summary = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "image_folder": str(image_folder),
        "image_count": len(names),
        "images": [p.name for p in names],
        "output_dir": str(output_dir),
        "prediction_file": str(prediction_path),
        "python": sys.version.split()[0],
        "torch": torch.__version__,
        "cuda_device": torch.cuda.get_device_name(0),
        "cuda_capability": torch.cuda.get_device_capability(0),
        "dtype": str(dtype),
        "elapsed_seconds": round(elapsed, 3),
        "peak_vram_gb": round(peak_vram_gb, 3),
        "prediction_keys": sorted(k for k, v in predictions.items() if v is not None),
    }

    summary_path = output_dir / "summary.json"
    summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    print(f"Saved predictions: {prediction_path}")
    print(f"Saved summary: {summary_path}")
    print(f"Elapsed seconds: {summary['elapsed_seconds']}")
    print(f"Peak VRAM GB: {summary['peak_vram_gb']}")


if __name__ == "__main__":
    main()
