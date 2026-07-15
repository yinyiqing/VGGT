# figure_doll

目的：测试 VGGT 在手办娃娃这类小物体、细节丰富目标上的表现。

图片目录：

```text
data/figure_doll/images/
```

运行：

```bash
conda run --no-capture-output -n vggt python scripts/run_vggt_experiment.py \
  --image-folder data/figure_doll/images \
  --output-dir experiments/custom/figure_doll \
  --title figure_doll
```

重点观察：

- 脸、头发、手指、衣服边缘是否保留。
- `conf50` 是否丢细节。
- `conf10` 是否能找回细节但变乱。
- 单帧能看到的细节，多帧融合后是否消失。
