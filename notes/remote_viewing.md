# 远程查看结果

这个项目主要在远程 GPU 机器上运行。我们的目标是：每次实验即使没有远程桌面，也能检查结果、保存证据、继续推进。

## 交互式查看

在本地机器上使用 SSH 端口转发。

查看 Gradio demo：

```bash
ssh -L 7860:127.0.0.1:7860 jiutian@REMOTE_HOST
cd /home/jiutian/vggt/official-vggt
conda run --no-capture-output -n vggt python demo_gradio.py
```

然后在本地浏览器打开：

```text
http://127.0.0.1:7860
```

查看 Viser demo：

```bash
ssh -L 8080:127.0.0.1:8080 jiutian@REMOTE_HOST
cd /home/jiutian/vggt/official-vggt
conda run --no-capture-output -n vggt python demo_viser.py --image_folder /path/to/images --port 8080
```

然后在本地浏览器打开：

```text
http://127.0.0.1:8080
```

如果使用 VS Code Remote SSH，可以在 Ports 面板里转发 `7860` 和 `8080`。

## 非交互式结果

每次可复现实验都应该保存足够的文件，方便之后检查：

- 输入图片列表或 manifest；
- 运行命令和环境摘要；
- 模型预测结果，通常是 `.npz`；
- 点云或网格导出，例如 `.ply` 或 `.glb`；
- depth、confidence 和失败案例的 2D 预览图；
- Markdown/CSV 格式的轻量指标和观察记录。

这样即使浏览器转发很慢或者暂时不可用，实验也不会卡住。

## 查看 3D 结果

VGGT 的原始输出是 `.npz`，不能直接用图片查看器打开。

导出浏览器友好的 `.glb`：

```bash
conda run --no-capture-output -n vggt python scripts/export_vggt_glb.py \
  --predictions experiments/first_runs/official_kitchen/predictions.npz \
  --output experiments/first_runs/official_kitchen/artifacts/3d/scene_conf50_500k.glb \
  --conf-percent 50 \
  --max-points 500000 \
  --also-ply
```

Mac 上查看 `.glb`：

- 直接拖到浏览器窗口。
- 或用 Blender / MeshLab 打开。
- VS Code Remote SSH 里可以右键下载到本地再看。

如果浏览器预览很淡或很碎，优先下载 `.ply` 用 MeshLab 或 CloudCompare 看。
不要依赖 macOS/VS Code 默认预览；它可能把点云错误显示成灰色三角片。

### 当前厨房样例的查看方式

同一个 VGGT 输出可以导出成不同“干净程度”的点云：

- `scene_conf50_500k.ply`：适合看整体结构，比较干净；可能丢掉小车这类细小物体。
- `scene_conf10_2m.ply`：能看到更多细节；也会带来很多噪声，所以画面会变乱。
- `frame00_conf10_500k.ply`：只看第 0 张图对应的点云，适合检查某个物体是不是被模型识别到。

结论：低 confidence 阈值不是“更正确”，只是“保留更多点”。如果目标是看整体，优先用 `conf50`；如果目标是找小物体，才临时看 `conf10` 或单帧结果。

## 建议规则

交互式 viewer 用来建立直觉；被追踪的笔记和轻量结果表才是研究记忆。只要在 viewer 里看到有意思的现象，就把它写进 `notes/failure_log.md`，并在 `experiments/` 下保存对应的小型结果记录或路径引用。
