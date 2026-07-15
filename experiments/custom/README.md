# 自采数据实验

这里放我们自己拍摄图片后的 VGGT 结果记录。

第一组建议：

```text
experiments/custom/desk_small_objects/
```

对应图片建议放在：

```text
data/desk_small_objects/images/
```

运行：

```bash
conda run --no-capture-output -n vggt python scripts/run_vggt_experiment.py \
  --image-folder data/desk_small_objects/images \
  --output-dir experiments/custom/desk_small_objects \
  --title desk_small_objects
```
