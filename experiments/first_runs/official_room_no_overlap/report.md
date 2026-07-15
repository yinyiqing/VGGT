# official_room_no_overlap VGGT 检查报告

这份报告由 `scripts/make_vggt_report.py` 生成，用来快速判断一次 VGGT 输出是否值得继续分析。

## 基本信息

- predictions：`experiments/first_runs/official_room_no_overlap/predictions.npz`
- 图片数量：8
- 输出目录：`experiments/first_runs/official_room_no_overlap`
- 单帧检查：第 0 张

## 置信度分布

- `depth_conf`：`{'min': 1.0, 'p05': 3.3366, 'p10': 3.8453, 'p25': 4.3885, 'p50': 5.1331, 'p75': 7.3319, 'p90': 8.2573, 'p95': 8.609, 'max': 10.9889}`
- `world_points_conf`：`{'min': 1.0, 'p05': 1.266, 'p10': 1.5349, 'p25': 2.1417, 'p50': 2.9019, 'p75': 3.7898, 'p90': 4.9822, 'p95': 5.6455, 'max': 8.0601}`

## 推荐查看顺序

1. 输入图：`experiments/first_runs/official_room_no_overlap/artifacts/previews/images_grid.jpg`
2. depth：`experiments/first_runs/official_room_no_overlap/artifacts/previews/depth_grid.png`
3. confidence：`experiments/first_runs/official_room_no_overlap/artifacts/previews/world_points_conf_grid.png`
4. 干净点云 PNG：`experiments/first_runs/official_room_no_overlap/artifacts/previews/pointcloud_clean_conf50.png`
5. 细节点云 PNG：`experiments/first_runs/official_room_no_overlap/artifacts/previews/pointcloud_detail_conf10.png`
6. 单帧点云 PNG：`experiments/first_runs/official_room_no_overlap/artifacts/previews/frame00_pointcloud_conf10.png`

## 3D 文件

- `experiments/first_runs/official_room_no_overlap/artifacts/3d/scene_conf50_500k.glb`
- `experiments/first_runs/official_room_no_overlap/artifacts/3d/scene_conf50_500k.ply`
- `experiments/first_runs/official_room_no_overlap/artifacts/3d/scene_conf10_2m.glb`
- `experiments/first_runs/official_room_no_overlap/artifacts/3d/scene_conf10_2m.ply`
- `experiments/first_runs/official_room_no_overlap/artifacts/3d/frame00_conf10_500k.glb`
- `experiments/first_runs/official_room_no_overlap/artifacts/3d/frame00_conf10_500k.ply`

## 人工观察

- 成功现象：模型能正常输出 depth、相机、点云和 confidence。
- 失败现象：输入视角重叠不足，整体几何拼接可信度存疑。
- 初步判断：低重叠场景可能产生“看似有输出，但空间关系不可靠”的失败。
- 下一步：增加相机轨迹和跨视角一致性检查。
