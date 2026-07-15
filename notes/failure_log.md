# VGGT 失败案例日志

每组图片单独记录一节。记录要短、直观、可复现。

## 模板

- 日期：
- 场景：
- 图片目录：
- 图片数量：
- 分辨率：
- 运行命令：
- 推理时间：
- 峰值显存：
- 输出文件：
- 成功现象：
- 失败现象：
- confidence/error 观察：
- 初步假设：
- 下一步：

## 环境备注

- `nvidia-smi` 报告的 GPU：NVIDIA GeForce RTX 4090，49140 MiB。
- roadmap 最初按 24 GB 显存估计；正式报告实验硬件时需要记录这个差异。

## 2026-07-15 official_room_no_overlap

- 场景：官方房间低重叠样例。
- 图片目录：`official-vggt/examples/room/images`
- 图片数量：8
- 运行命令：见 `experiments/first_runs/official_room_no_overlap/README.md`
- 推理时间：10.564 秒
- 峰值显存：8.43 GB
- 输出文件：`experiments/first_runs/official_room_no_overlap/summary.json`
- 成功现象：模型正常输出 depth、camera、point map、confidence。
- 失败现象：输入图覆盖房间不同局部，重叠明显不足；输出深度不等于整组几何可靠。
- confidence/error 观察：待做几何一致性检查。
- 初步假设：VGGT 会对低重叠输入生成看似完整的局部几何，但整组相机/点云可能不可靠。
- 下一步：增加相机轨迹和点云预览，检查是否存在场景拼接错误。
