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

- 推理时间：16.135 秒
- 峰值显存：8.79 GB
- 输出：`summary.json`、`predictions.npz`
- 报告：`report.md`
- 预览：`artifacts/01_preview_images/`
- 3D：`artifacts/02_pointcloud_files/scene_conf50_500k.glb`、`artifacts/02_pointcloud_files/scene_conf50_500k.ply`

当前保留的查看文件：

- `artifacts/02_pointcloud_files/scene_conf50_500k.ply`：干净整体。
- `artifacts/02_pointcloud_files/scene_conf10_2m.ply`：更多细节，也更乱。
- `artifacts/02_pointcloud_files/frame00_conf10_500k.ply`：单帧检查小车。
