# 官方 VGGT 补丁

如果为了复现或实验必须修改本地 `official-vggt/`，就在这里保存小补丁。

建议流程：

```bash
cd official-vggt
git diff > ../patches/official-vggt/YYYYMMDD-short-description.patch
```

这样可以避免把整份上游源码放进自己的仓库，同时保留对复现有影响的本地改动。
