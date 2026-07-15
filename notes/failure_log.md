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

## 2026-07-15 official_kitchen 小物体丢失

- 场景：官方厨房样例。
- 图片目录：`official-vggt/examples/kitchen/images`
- 图片数量：25
- 输出文件：`experiments/first_runs/official_kitchen/`
- 成功现象：`scene_conf50_500k.ply` 能看出主要桌面、餐垫和厨房结构。
- 失败现象：高 confidence 过滤后，小车这类小物体明显变少或消失。
- confidence/error 观察：`conf10 + 2m points` 会保留更多小物体点，但全场景明显变乱；单帧 `frame00_conf10_500k.ply` 更适合检查局部细节。
- 初步假设：细小、局部、遮挡多的物体更容易落在低 confidence 区间；confidence 过滤会在“干净整体”和“保留细节”之间产生取舍。
- 下一步：在自采数据里专门记录“小物体是否被保留”和对应 confidence 分布。

## 2026-07-15 figure_doll 图像方向问题

- 场景：自采手办娃娃。
- 图片目录：`data/figure_doll/images`
- 图片数量：24
- 输出文件：`experiments/custom/figure_doll/`
- 成功现象：流程正常跑通。
- 失败现象：前 22 张依赖 EXIF 旋转，模型读取后方向横倒；最后 2 张低分辨率正向图混入。点云发散，confidence 大量卡在 1.0。
- confidence/error 观察：raw 版 `world_points_conf` p50=1.0，p95=2.07；转正并排除低分辨率图后 p50=4.7609，p95=16.054。
- 初步假设：VGGT 对 EXIF 方向和混合画幅比较敏感；输入方向错误会直接触发低置信和点云发散。
- 下一步：以后自采图先做 EXIF 转正；当前推荐查看 `experiments/custom/figure_doll_oriented22/`。
