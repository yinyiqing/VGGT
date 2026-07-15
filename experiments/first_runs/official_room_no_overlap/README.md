# official_room_no_overlap

目的：测试官方低重叠房间样例，建立第一条失败案例基线。

- 日期：2026-07-15
- 输入：`official-vggt/examples/room/images`
- 图片数：8
- 权重：`weights/VGGT-1B/model.pt`
- 命令：

```bash
conda run --no-capture-output -n vggt python scripts/run_vggt_folder.py \
  --image-folder official-vggt/examples/room/images \
  --output-dir experiments/first_runs/official_room_no_overlap \
  --weights-path weights/VGGT-1B/model.pt
```

结果：

- 推理时间：10.564 秒
- 峰值显存：8.43 GB
- 输出：`summary.json`、`predictions.npz`
- 预览：`artifacts/previews/`
- 3D：`artifacts/3d/scene_conf50_500k.glb`、`artifacts/3d/scene_conf50_500k.ply`

初步观察：输入视角覆盖房间不同局部，重叠不足；VGGT 仍会输出深度和相机，需要后续检查几何一致性。
