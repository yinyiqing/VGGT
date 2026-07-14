# Remote Viewing Notes

This project is expected to run on a remote GPU machine. We should make every
experiment inspectable without requiring a desktop session on that machine.

## Interactive Viewing

Use SSH port forwarding from your local machine.

For the Gradio demo:

```bash
ssh -L 7860:127.0.0.1:7860 jiutian@REMOTE_HOST
cd /home/jiutian/vggt/official-vggt
conda run --no-capture-output -n vggt python demo_gradio.py
```

Then open this URL locally:

```text
http://127.0.0.1:7860
```

For the Viser demo:

```bash
ssh -L 8080:127.0.0.1:8080 jiutian@REMOTE_HOST
cd /home/jiutian/vggt/official-vggt
conda run --no-capture-output -n vggt python demo_viser.py --image_folder /path/to/images --port 8080
```

Then open this URL locally:

```text
http://127.0.0.1:8080
```

If using VS Code Remote SSH, use the Ports panel to forward ports 7860 and 8080.

## Non-Interactive Artifacts

Every reproducible run should save enough files to inspect results later:

- input image list or manifest;
- run command and environment summary;
- model predictions, usually `.npz`;
- point cloud or mesh export, such as `.ply` or `.glb`;
- 2D preview images for depth, confidence, and failure cases;
- compact metrics or observations in Markdown/CSV.

This lets us keep experiments moving even when browser forwarding is slow or
unavailable.

## Suggested Rule

Interactive viewers are for intuition. Tracked notes and compact result tables
are for research memory. When a result looks interesting in the viewer, write it
down in `notes/failure_log.md` and save a small artifact reference under
`experiments/`.
