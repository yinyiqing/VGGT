# VGGT Research Workspace

This repository tracks our research code, experiment notes, configs, and compact
results for VGGT-based 3D reconstruction research.

The official VGGT source tree is kept locally at `official-vggt/` and is ignored
by Git. Treat it as a third-party dependency: we run it, import from it, and may
generate patches against it, but we do not vendor the whole upstream codebase
into this repository.

## What We Track

- `VGGT_research_roadmap.md`: research plan and milestones.
- `scripts/`: our reproducible wrappers, probes, evaluation scripts, and tools.
- `notes/`: reading notes, glossary, failure logs, and experiment observations.
- `experiments/`: lightweight experiment manifests, configs, and summary tables.
- `patches/`: small patches against `official-vggt/` if modifying upstream code
  becomes necessary.

## What We Do Not Track

- `official-vggt/`: full upstream VGGT checkout.
- `data/`, model weights, checkpoints, and downloaded assets.
- large generated outputs, caches, point clouds, logs, and visualization dumps.

This keeps the repository publishable and readable while preserving enough
information for others to reproduce our experiments with their own official VGGT
checkout.
