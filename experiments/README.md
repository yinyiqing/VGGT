# 实验目录

这个目录只追踪轻量实验记录。大文件结果保留在本地，不提交 Git。

## 目录

- `first_runs/`：官方样例和环境验证。
- `custom/`：我们自己拍的数据。
- `diagnostics/`：失败诊断实验。
- `gsplat_trials/`：VGGT + 3DGS 对照实验。

每个具体实验目录建议包含：

- `README.md`：目的、命令、观察。
- `summary.json`：自动保存的运行摘要。
- `report.md`：标准检查报告。
- `artifacts/01_preview_images/`：本地 PNG/JPG 预览，不提交。
- `artifacts/02_pointcloud_files/`：本地 PLY/GLB，不提交。
