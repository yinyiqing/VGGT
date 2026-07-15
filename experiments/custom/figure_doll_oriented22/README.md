# figure_doll_oriented22

目的：记录一次 VGGT 复现实验。

- 日期：2026-07-15
- 输入：`data/figure_doll_oriented22/images`
- 权重：`weights/VGGT-1B/model.pt`
- 命令：

```bash
conda run --no-capture-output -n vggt python scripts/run_vggt_experiment.py \
  --image-folder data/figure_doll_oriented22/images \
  --output-dir experiments/custom/figure_doll_oriented22 \
  --title figure_doll_oriented22
```

结果：

- 摘要：`summary.json`
- 报告：`report.md`
- 预览：`artifacts/01_preview_images/`
- 3D：`artifacts/02_pointcloud_files/`

人工观察：

- 成功现象：图片方向统一后，confidence 明显恢复；娃娃主体能聚成一团。
- 失败现象：桌面和背景噪声较多，低阈值点云更乱。
- 初步判断：当前主要问题从“方向错误”变成“背景/桌面噪声和小物体细节稳定性”。
- 下一步：打开 `artifacts/02_pointcloud_files/scene_conf50_500k.ply` 检查主体形状。
