# 本地数据目录

这里放自采图片和外部数据集。真实图片不上传 Git。

建议结构：

```text
data/
└── desk_small_objects/
    └── images/
        ├── 000.jpg
        ├── 001.jpg
        └── ...
```

第一组数据建议见 `notes/data_collection.md`。

运行示例：

```bash
conda run --no-capture-output -n vggt python scripts/run_vggt_experiment.py \
  --image-folder data/desk_small_objects/images \
  --output-dir experiments/custom/desk_small_objects \
  --title desk_small_objects
```
