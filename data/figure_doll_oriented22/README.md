# figure_doll_oriented22 数据

这里是 `figure_doll` 的清理版。

处理方式：

- 取 `data/figure_doll/images/000.jpg` 到 `021.jpg`。
- 使用 EXIF 信息把图片真正转正。
- 统一保存为 jpg。
- 排除 `022.jpg` 和 `023.jpg`，因为它们没有 EXIF 且分辨率较低。

对应实验：

```text
experiments/custom/figure_doll_oriented22/
```

运行命令：

```bash
conda run --no-capture-output -n vggt python scripts/run_vggt_experiment.py \
  --image-folder data/figure_doll_oriented22/images \
  --output-dir experiments/custom/figure_doll_oriented22 \
  --title figure_doll_oriented22
```
