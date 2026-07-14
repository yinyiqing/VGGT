# Official VGGT Patches

Store small patches here if we need to modify the local `official-vggt/`
checkout for reproduction or experiments.

Suggested workflow:

```bash
cd official-vggt
git diff > ../patches/official-vggt/YYYYMMDD-short-description.patch
```

This lets us keep the full upstream source out of our repository while still
tracking any local changes that matter for reproducibility.
