# official_kitchen

目的：验证官方 VGGT 样例能在本机完整跑通。

- 日期：2026-07-15
- 输入：`official-vggt/examples/kitchen/images`
- 图片数：25
- 权重：`weights/VGGT-1B/model.pt`
- 命令：

```bash
conda run --no-capture-output -n vggt python scripts/run_vggt_folder.py \
  --image-folder official-vggt/examples/kitchen/images \
  --output-dir experiments/first_runs/official_kitchen \
  --weights-path weights/VGGT-1B/model.pt
```

结果：

- 推理时间：19.752 秒
- 峰值显存：8.79 GB
- 输出：`summary.json`、`predictions.npz`
- 预览：`artifacts/previews/`
- 3D：`artifacts/3d/scene_conf50.glb`

备注：`predictions.npz` 约 196 MB，已被 Git 忽略。
