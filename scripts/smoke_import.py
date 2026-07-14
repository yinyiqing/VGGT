#!/usr/bin/env python
"""Minimal import and model-construction smoke test for the local VGGT checkout."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--official-root",
        type=Path,
        default=Path("official-vggt"),
        help="Path to the local official VGGT checkout.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    official_root = args.official_root.resolve()
    if not official_root.exists():
        raise FileNotFoundError(f"Official VGGT checkout not found: {official_root}")

    sys.path.insert(0, str(official_root))

    import torch
    from vggt.models.vggt import VGGT

    print(f"official_root={official_root}")
    print(f"python={sys.version.split()[0]}")
    print(f"torch={torch.__version__}")
    print(f"cuda_available={torch.cuda.is_available()}")
    if torch.cuda.is_available():
        print(f"cuda_device={torch.cuda.get_device_name(0)}")
        print(f"cuda_capability={torch.cuda.get_device_capability(0)}")

    model = VGGT()
    param_count = sum(p.numel() for p in model.parameters())
    print(f"model=VGGT")
    print(f"parameters={param_count:,}")


if __name__ == "__main__":
    main()
