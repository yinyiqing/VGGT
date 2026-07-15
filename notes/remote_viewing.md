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
  --output experiments/first_runs/official_kitchen/artifacts/3d/scene_conf50.glb \
  --conf-percent 50
```

Mac 上查看 `.glb`：

- 直接拖到浏览器窗口。
- 或用 Blender / MeshLab 打开。
- VS Code Remote SSH 里可以右键下载到本地再看。

## 建议规则

交互式 viewer 用来建立直觉；被追踪的笔记和轻量结果表才是研究记忆。只要在 viewer 里看到有意思的现象，就把它写进 `notes/failure_log.md`，并在 `experiments/` 下保存对应的小型结果记录或路径引用。
