# 自采数据拍摄规范

目标：拍出能暴露 VGGT 成功/失败边界的图片，而不是只拍“最好看”的结果。

## 第一组建议

- 场景：桌面小物体，例如小车、杯子、书、反光物体。
- 数量：15-30 张。
- 路径：建议放到 `data/desk_small_objects/images/`。
- 拍法：绕物体慢慢移动，每张之间保持明显重叠。
- 光照：先用稳定光照，不要一开始就混合强反光和暗光。

## 必拍变化

- 正常环绕：作为基线。
- 少量低重叠：故意跳几个大角度。
- 少量模糊：轻微手抖或运动模糊。
- 小物体近景：检查小物体是否被高 confidence 过滤掉。

## 运行命令

```bash
conda run --no-capture-output -n vggt python scripts/run_vggt_experiment.py \
  --image-folder data/desk_small_objects/images \
  --output-dir experiments/custom/desk_small_objects \
  --title desk_small_objects
```

## 看结果顺序

1. 先看 `report.md`。
2. 再看 `artifacts/previews/images_grid.jpg`。
3. 对比 `pointcloud_clean_conf50.png` 和 `pointcloud_detail_conf10.png`。
4. 如果细小物体消失，再看 `frame00_pointcloud_conf10.png` 和对应 `.ply`。

每次只记录一句核心观察：哪里成功、哪里失败、怀疑原因是什么。
