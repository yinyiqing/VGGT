# figure_doll_oriented22 VGGT 检查报告

这份报告由 `scripts/make_vggt_report.py` 生成，用来快速判断一次 VGGT 输出是否值得继续分析。

## 基本信息

- predictions：`experiments/custom/figure_doll_oriented22/predictions.npz`
- 图片数量：22
- 输出目录：`experiments/custom/figure_doll_oriented22`
- 单帧检查：第 0 张

## 置信度分布

- `depth_conf`：`{'min': 1.0, 'p05': 1.0, 'p10': 1.0, 'p25': 1.0, 'p50': 2.4133, 'p75': 6.9859, 'p90': 10.7403, 'p95': 12.2519, 'max': 32.1921}`
- `world_points_conf`：`{'min': 1.0, 'p05': 1.0, 'p10': 1.0, 'p25': 1.0, 'p50': 4.7609, 'p75': 11.2454, 'p90': 14.3681, 'p95': 16.054, 'max': 24.4841}`

## 推荐查看顺序

1. 输入图：`experiments/custom/figure_doll_oriented22/artifacts/01_preview_images/images_grid.jpg`
2. depth：`experiments/custom/figure_doll_oriented22/artifacts/01_preview_images/depth_grid.png`
3. confidence：`experiments/custom/figure_doll_oriented22/artifacts/01_preview_images/world_points_conf_grid.png`
4. 干净点云 PNG：`experiments/custom/figure_doll_oriented22/artifacts/01_preview_images/pointcloud_clean_conf50.png`
5. 细节点云 PNG：`experiments/custom/figure_doll_oriented22/artifacts/01_preview_images/pointcloud_detail_conf10.png`
6. 单帧点云 PNG：`experiments/custom/figure_doll_oriented22/artifacts/01_preview_images/frame00_pointcloud_conf10.png`

## 3D 文件

- `experiments/custom/figure_doll_oriented22/artifacts/02_pointcloud_files/scene_conf50_500k.glb`
- `experiments/custom/figure_doll_oriented22/artifacts/02_pointcloud_files/scene_conf50_500k.ply`
- `experiments/custom/figure_doll_oriented22/artifacts/02_pointcloud_files/scene_conf10_2m.glb`
- `experiments/custom/figure_doll_oriented22/artifacts/02_pointcloud_files/scene_conf10_2m.ply`
- `experiments/custom/figure_doll_oriented22/artifacts/02_pointcloud_files/frame00_conf10_500k.glb`
- `experiments/custom/figure_doll_oriented22/artifacts/02_pointcloud_files/frame00_conf10_500k.ply`

## 手动截图

- `manual_views/meshlab_scene_conf50_overview.png`：主体较完整，适合作为当前展示结果。
- `manual_views/meshlab_scene_conf10_noisy.png`：低阈值带入更多背景和错误点，整体更乱。

## 人工观察

- 成功现象：图片方向统一后，confidence 明显恢复；娃娃主体能聚成一团，头发和金色装饰大致可见。
- 失败现象：桌面和背景仍有大量雾状噪声；`conf10` 比 `conf50` 更乱，说明低阈值主要放进了背景/桌面噪声。
- 初步判断：这组数据可以作为“预处理修复后仍存在小物体/背景噪声”的自采基线。
- 下一步：优先查看 `scene_conf50_500k.ply`；如果要继续优化，下一组拍摄应减少背景杂物、保持娃娃占画面更大。
