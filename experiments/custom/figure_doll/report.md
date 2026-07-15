# figure_doll VGGT 检查报告

这份报告由 `scripts/make_vggt_report.py` 生成，用来快速判断一次 VGGT 输出是否值得继续分析。

## 基本信息

- predictions：`experiments/custom/figure_doll/predictions.npz`
- 图片数量：24
- 输出目录：`experiments/custom/figure_doll`
- 单帧检查：第 0 张

## 置信度分布

- `depth_conf`：`{'min': 1.0, 'p05': 1.0, 'p10': 1.0, 'p25': 1.0, 'p50': 1.0, 'p75': 1.0, 'p90': 1.1249, 'p95': 1.8287, 'max': 5.2872}`
- `world_points_conf`：`{'min': 1.0, 'p05': 1.0, 'p10': 1.0, 'p25': 1.0, 'p50': 1.0, 'p75': 1.0106, 'p90': 1.673, 'p95': 2.07, 'max': 4.6264}`

## 推荐查看顺序

1. 输入图：`experiments/custom/figure_doll/artifacts/01_preview_images/images_grid.jpg`
2. depth：`experiments/custom/figure_doll/artifacts/01_preview_images/depth_grid.png`
3. confidence：`experiments/custom/figure_doll/artifacts/01_preview_images/world_points_conf_grid.png`
4. 干净点云 PNG：`experiments/custom/figure_doll/artifacts/01_preview_images/pointcloud_clean_conf50.png`
5. 细节点云 PNG：`experiments/custom/figure_doll/artifacts/01_preview_images/pointcloud_detail_conf10.png`
6. 单帧点云 PNG：`experiments/custom/figure_doll/artifacts/01_preview_images/frame00_pointcloud_conf10.png`

## 3D 文件

- `experiments/custom/figure_doll/artifacts/02_pointcloud_files/scene_conf50_500k.glb`
- `experiments/custom/figure_doll/artifacts/02_pointcloud_files/scene_conf50_500k.ply`
- `experiments/custom/figure_doll/artifacts/02_pointcloud_files/scene_conf10_2m.glb`
- `experiments/custom/figure_doll/artifacts/02_pointcloud_files/scene_conf10_2m.ply`
- `experiments/custom/figure_doll/artifacts/02_pointcloud_files/frame00_conf10_500k.glb`
- `experiments/custom/figure_doll/artifacts/02_pointcloud_files/frame00_conf10_500k.ply`

## 人工观察

- 成功现象：流程正常跑通，生成 summary、report、PNG 预览和 PLY/GLB。
- 失败现象：输入图方向混乱；前 22 张依赖 EXIF 旋转，模型读取后显示为横倒，最后 2 张又是低分辨率正向图。点云明显发散，confidence 大量卡在 1.0。
- 初步判断：这是一个“图像方向 / 混合分辨率导致 VGGT 低置信”的预处理失败案例。
- 下一步：查看 `experiments/custom/figure_doll_oriented22/`，那里使用 EXIF 转正后的前 22 张图。
