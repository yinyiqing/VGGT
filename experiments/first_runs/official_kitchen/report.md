# official_kitchen VGGT 检查报告

这份报告由 `scripts/make_vggt_report.py` 生成，用来快速判断一次 VGGT 输出是否值得继续分析。

## 基本信息

- predictions：`experiments/first_runs/official_kitchen/predictions.npz`
- 图片数量：25
- 输出目录：`experiments/first_runs/official_kitchen`
- 单帧检查：第 0 张

## 置信度分布

- `depth_conf`：`{'min': 1.0, 'p05': 1.0, 'p10': 1.0, 'p25': 1.001, 'p50': 11.299, 'p75': 17.0084, 'p90': 19.1963, 'p95': 21.8989, 'max': 33.0607}`
- `world_points_conf`：`{'min': 1.0, 'p05': 1.0, 'p10': 1.0, 'p25': 1.749, 'p50': 12.2518, 'p75': 17.2171, 'p90': 20.3639, 'p95': 22.0751, 'max': 31.2859}`

## 推荐查看顺序

1. 输入图：`experiments/first_runs/official_kitchen/artifacts/01_preview_images/images_grid.jpg`
2. depth：`experiments/first_runs/official_kitchen/artifacts/01_preview_images/depth_grid.png`
3. confidence：`experiments/first_runs/official_kitchen/artifacts/01_preview_images/world_points_conf_grid.png`
4. 干净点云 PNG：`experiments/first_runs/official_kitchen/artifacts/01_preview_images/pointcloud_clean_conf50.png`
5. 细节点云 PNG：`experiments/first_runs/official_kitchen/artifacts/01_preview_images/pointcloud_detail_conf10.png`
6. 单帧点云 PNG：`experiments/first_runs/official_kitchen/artifacts/01_preview_images/frame00_pointcloud_conf10.png`

## 3D 文件

- `experiments/first_runs/official_kitchen/artifacts/02_pointcloud_files/scene_conf50_500k.glb`
- `experiments/first_runs/official_kitchen/artifacts/02_pointcloud_files/scene_conf50_500k.ply`
- `experiments/first_runs/official_kitchen/artifacts/02_pointcloud_files/scene_conf10_2m.glb`
- `experiments/first_runs/official_kitchen/artifacts/02_pointcloud_files/scene_conf10_2m.ply`
- `experiments/first_runs/official_kitchen/artifacts/02_pointcloud_files/frame00_conf10_500k.glb`
- `experiments/first_runs/official_kitchen/artifacts/02_pointcloud_files/frame00_conf10_500k.ply`

## 人工观察

- 成功现象：整体桌面、餐垫、植物和小车位置能看出来。
- 失败现象：高置信点云更干净，但小车这类细小物体容易变少；低阈值会变乱。
- 初步判断：confidence 过滤存在“整体干净”和“保留细节”的取舍。
- 下一步：自采桌面小物体数据，记录小物体是否被过滤掉。
