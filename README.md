# VGGT 研究工作区

这个仓库用于保存我们围绕 VGGT 做 3D 重建研究时产生的研究代码、实验笔记、配置文件和轻量结果。

官方 VGGT 源码保存在本地的 `official-vggt/`，并被 Git 忽略。它在这个项目里被当作第三方依赖：我们会运行它、从中导入模型和工具，也可能针对它生成小补丁，但不会把整份上游源码复制进自己的仓库。

## 我们会追踪什么

- `VGGT_research_roadmap.md`：研究路线和阶段目标。
- `scripts/`：我们自己写的复现脚本、探针、评估脚本和辅助工具。
- `notes/`：论文笔记、术语表、失败案例日志和实验观察。
- `experiments/`：轻量实验记录、配置、命令和结果表。
- `ideas/`：论文 idea、方向取舍和决策记录。
- `paper/`：论文大纲和后续草稿。
- `docs/`：项目主线和结构说明。
- `patches/`：如果后续必须修改 `official-vggt/`，就在这里保存小补丁。

## 我们不会追踪什么

- `official-vggt/`：完整上游 VGGT 源码。
- `data/`、模型权重、checkpoint 和下载资源。
- 大体积生成结果、缓存、点云、日志和可视化导出。

这样做的目标是让仓库保持干净、可读、可公开，同时保留足够信息，让别人可以用自己的官方 VGGT checkout 复现我们的实验。

## 当前工作流

1. 把图片放到一个 `images/` 目录。
2. 用 `scripts/run_vggt_experiment.py` 一键跑 VGGT 和标准检查报告。
3. 先看 `report.md`，再按报告里的路径打开 PNG / PLY。
4. 把失败现象写进 `notes/failure_log.md`。

示例：

```bash
conda run --no-capture-output -n vggt python scripts/run_vggt_experiment.py \
  --image-folder data/desk_small_objects/images \
  --output-dir experiments/custom/desk_small_objects \
  --title desk_small_objects
```

自采数据怎么拍，见 `notes/data_collection.md`。

## 主线目录

```text
docs/mainline.md          # 当前研究主线
data/                     # 本地图片，不上传
experiments/first_runs/   # 官方样例复现
experiments/custom/       # 自采数据实验
experiments/diagnostics/  # 失败诊断实验
experiments/gsplat_trials/# 3DGS 对照实验
ideas/                    # 候选方向和决策
paper/                    # 论文草稿
```
