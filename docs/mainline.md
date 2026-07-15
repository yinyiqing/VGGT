# 项目主线

目标：围绕 VGGT 做一个有论文潜力的“真实输入可靠性诊断”项目。

核心问题不是“让 VGGT 重建得更好看”，而是：

> 给一组真实拍摄图片，VGGT 输出什么时候不可信？为什么不可信？用户应该删哪张、补哪个视角、重拍哪里？

## 主线阶段

### 1. 复现基线

目录：`experiments/first_runs/`

目的：确认官方样例、权重、脚本、可视化流程都稳定。

当前样例：

- `official_kitchen`：小物体和 confidence 过滤。
- `official_room_no_overlap`：低重叠输入。

### 2. 自采数据

目录：`data/`、`experiments/custom/`

目的：收集真实、轻微不受控的图片组，观察 VGGT 在普通拍摄条件下的失败方式。

第一组建议：桌面小物体。

### 3. 失败诊断

目录：`experiments/diagnostics/`

目的：把失败从“看起来乱”拆成可记录的信号。

优先信号：

- confidence 分布；
- 小物体是否被高 confidence 过滤掉；
- 低重叠 / 大视角跳变；
- 模糊、反光、低纹理；
- 单帧能看到，但多帧融合后丢失。

### 4. 3DGS 对照

目录：`experiments/gsplat_trials/`

目的：测试 `VGGT -> COLMAP -> 3DGS` 是否能改善视觉质量，以及它是否掩盖几何失败。

注意：3DGS 是对照和分析工具，不是当前论文主贡献。

### 5. 论文沉淀

目录：`ideas/`、`paper/`

目的：把实验现象转成可投稿的问题定义、方法草图和实验设计。

当前候选方向：

> 面向 feed-forward 3D reconstruction 的 capture-level / region-level 可靠性诊断。

## 每次实验的最小闭环

1. 跑 `scripts/run_vggt_experiment.py`。
2. 看 `report.md` 和 `artifacts/01_preview_images/`。
3. 必要时打开 `artifacts/02_pointcloud_files/`。
4. 把一句核心失败写进 `notes/failure_log.md`。
5. 如果现象有论文价值，写进 `ideas/candidate_directions.md`。
