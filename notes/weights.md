# 权重准备

VGGT 第一次推理需要 `model.pt`。

自动下载地址：

```text
https://huggingface.co/facebook/VGGT-1B/resolve/main/model.pt
```

如果 Hugging Face 访问失败，可以用 ModelScope：

```bash
conda run --no-capture-output -n vggt python -m pip install modelscope
mkdir -p weights/VGGT-1B
conda run --no-capture-output -n vggt python - <<'PY'
from modelscope import snapshot_download
snapshot_download(
    'facebook/VGGT-1B',
    allow_file_pattern='model.pt',
    local_dir='weights/VGGT-1B',
)
PY
```

如果远程机器访问 Hugging Face 失败，可以在本地 Mac 下载后传到远程：

```bash
scp model.pt jiutian@REMOTE_HOST:/home/jiutian/vggt/weights/VGGT-1B/model.pt
```

然后运行：

```bash
conda run --no-capture-output -n vggt python scripts/run_vggt_folder.py \
  --image-folder official-vggt/examples/kitchen/images \
  --output-dir experiments/first_runs/official_kitchen \
  --weights-path weights/VGGT-1B/model.pt
```

`weights/` 已被 Git 忽略，不会上传。
