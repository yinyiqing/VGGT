# VGGT 入门与论文路线规划

> 目标：从零理解 VGGT 所在的 3D vision 领域，跑通官方代码，建立失败案例直觉，并在一台 RTX 4090 的条件下收敛到一个有顶会潜力的研究方向。

## 0. 当前判断

VGGT 是一个面向多视角几何的 3D foundation model。它把一组同场景图片作为输入，一次前向传播预测相机参数、深度图、点云/point map 和点跟踪特征。它的重要性在于：把传统 SfM/MVS 里特征匹配、相机估计、三角化、稠密重建等步骤，部分统一进一个大 transformer。

你的硬件是一台 RTX 4090 24GB。这个配置适合：

- 跑 VGGT 官方 demo 和中小规模推理。
- 做 10-100 张图级别的实验。
- 冻结 VGGT 主干，训练轻量 head、校准模块、选择策略或 LoRA。
- 做 failure detection、uncertainty、active view selection、frame selection 等单卡友好方向。

不适合：

- 从头训练 VGGT 级别大模型。
- 大规模全量 fine-tuning。
- 拼数据规模或模型规模的 scaling paper。

## 1. 第一阶段：建立直觉，跑通闭环

时间：第 1 周

目标不是读懂所有公式，而是亲眼看到 VGGT 输入什么、输出什么、什么时候好、什么时候坏。

任务：

- 拉取官方仓库：`https://github.com/facebookresearch/vggt`
- 当前工作区中官方代码目录：`official-vggt/`
- 建立 Python 环境，安装依赖。
- 跑通官方 demo。
- 用官方样例图片得到相机、深度、点云输出。
- 用手机拍一组 10-20 张照片，跑一次自己的数据。

数据选择原则：

- 第一阶段只使用有选择的图片组，不直接上传或处理完整视频。
- 每组图片控制在 8-20 张，优先保证视角覆盖、清晰度和场景静态。
- 图片之间要有足够重叠，但不要几乎重复；相邻视角可以移动约 10-20 度。
- 避免一开始混入大量视频帧，因为视频通常包含冗余帧、运动模糊、曝光变化和动态干扰。
- 如果后续确实要用视频，先抽帧，再手动或自动筛掉模糊帧、重复帧和动态干扰明显的帧。

建议拍摄数据：

- 桌面物体，正常绕拍。
- 房间，纹理丰富。
- 白墙或低纹理区域。
- 反光、透明、金属物体。
- 有人或物体运动的场景。

阶段产物：

- 一个 `experiments/first_runs/` 文件夹，保存输入图、输出点云、截图和简单观察。
- 一个 `notes/failure_log.md`，记录每组数据的成功点和失败点。

## 2. 第二阶段：补齐领域基础

时间：第 2-3 周

需要理解的核心概念：

- Pinhole camera model：针孔相机模型。
- Intrinsics：内参，例如焦距、主点、视场角。
- Extrinsics：外参，即相机在世界坐标系中的位置和朝向。
- Depth map：每个像素距离相机的深度。
- Point map：每个像素对应的 3D 坐标。
- Correspondence：不同图片中同一个真实 3D 点的对应关系。
- SfM：Structure from Motion，从多张图恢复相机和稀疏结构。
- MVS：Multi-View Stereo，从多视角恢复稠密深度或点云。
- Bundle Adjustment：联合优化相机和 3D 点，使重投影误差最小。

推荐阅读顺序：

1. COLMAP / SfM 基础介绍。
2. DUSt3R：理解从两张图直接预测 dense 3D 的思想。
3. MASt3R：理解匹配和 3D 表征的增强。
4. VGGT 原论文：理解多图统一 transformer。
5. VGGT-Ω：理解后续 scaling、动态场景和效率方向。

读 VGGT 原论文时只抓四个问题：

- 输入是什么？
- 输出是什么？
- 相比传统 SfM/MVS，它省掉或替代了什么？
- 它在哪些情况下可能失败？

阶段产物：

- `notes/paper_reading_vggt.md`：按 Abstract、Introduction、Method、Experiments、Limitations 做阅读笔记。
- `notes/glossary.md`：整理所有 3D vision 术语，用自己的话解释。

## 3. 第三阶段：失败案例挖掘

时间：第 4 周

研究 idea 往往来自稳定、可复现、有规律的失败，而不是来自“再改一个模块”。

这一阶段仍然优先使用精选图片组。不要为了“数据多”而直接喂完整视频；我们要先控制变量，知道失败来自低纹理、反光、动态、低重叠，还是来自视频抽帧本身。

建议建立一个小型 benchmark：

- `data/phone_object_normal/`
- `data/phone_room_textured/`
- `data/phone_low_texture/`
- `data/phone_reflective/`
- `data/phone_dynamic/`
- `data/phone_low_overlap/`

对每组数据记录：

- 输入帧数。
- 分辨率。
- 推理时间。
- 峰值显存。
- 相机轨迹是否合理。
- 深度是否平滑。
- 点云是否破碎。
- 动态物体是否导致拉丝或错位。
- confidence 是否真的低在错误区域。

阶段产物：

- 一张 failure taxonomy 表格。
- 3-5 个最典型的可视化失败案例。
- 初步判断：VGGT 的 confidence 是否能预测错误。

## 4. 第四阶段：选择单卡友好的论文方向

时间：第 5-6 周

优先方向：VGGT 的可靠性与不确定性。

候选题目：

> Knowing When and Where to Look: Calibrated Uncertainty for Feed-Forward 3D Reconstruction

核心问题：

> VGGT 输出一个 3D 结果时，它是否知道哪里不可信？如果不知道，我们能否用轻量方法校准它，并进一步指导选帧或主动重建？

为什么适合 4090：

- 不需要重训 VGGT。
- 可以冻结主干，缓存中间结果。
- 训练对象是轻量 uncertainty head 或 calibration module。
- 实验可以在中小规模数据集和自采数据上完成。

可能贡献：

- 系统评估 VGGT confidence 与真实几何误差之间的关系。
- 提出一个轻量 uncertainty calibration 方法。
- 用校准后的 uncertainty 做 frame selection、bad frame rejection 或 active view selection。
- 在同样帧数或同样预算下提升重建质量。

## 5. 第五阶段：最小可行实验

时间：第 7-8 周

先做最小实验，不要一开始就设计复杂方法。

实验 A：confidence 是否可靠

- 输入多视角图像。
- 跑 VGGT 得到 depth、point map、camera、confidence。
- 计算重投影一致性误差或与已有 GT 比较。
- 画出 confidence 与真实误差的相关性。

判断标准：

- 如果 confidence 高但误差也高，这就是论文动机。
- 如果 confidence 已经很好，需要换方向或做更高阶任务。

实验 B：错误区域能否被预测

- 提取 VGGT 输出和中间特征。
- 训练一个小 MLP / CNN / transformer head 预测 error map。
- 比较原始 confidence、entropy、reprojection residual 和学习式 predictor。

实验 C：不确定性能否改善系统

- 用 uncertainty 做坏帧剔除。
- 用 uncertainty 做候选帧选择。
- 用 uncertainty 指导下一视角选择。
- 比较 random、farthest frame、overlap heuristic、原始 confidence 等 baseline。

阶段产物：

- 第一版实验表。
- 第一版方法图。
- 第一版 failure visualization。

## 6. 第六阶段：论文雏形

时间：第 9-12 周

论文结构建议：

- Introduction：VGGT 代表 feed-forward 3D reconstruction 的新范式，但可靠性仍未被系统解决。
- Related Work：SfM/MVS、DUSt3R/MASt3R/VGGT、uncertainty estimation、active reconstruction。
- Method：冻结 VGGT，构建 geometry risk predictor，再用于 selection/reconstruction。
- Experiments：failure prediction、calibration、frame selection、active view selection。
- Discussion：限制、泛化、真实部署意义。

关键实验指标：

- Depth error。
- Pose error。
- Chamfer distance / F-score。
- Reprojection error。
- Failure detection AUC。
- Calibration error。
- Same-quality fewer frames。
- Same-frame better reconstruction。

## 7. 每周检查点

第 1 周：

- 官方 demo 跑通。
- 自己手机数据跑通。

第 2-3 周：

- 看懂 VGGT 输入输出和主结构。
- 整理领域术语。

第 4 周：

- 建立 failure log。
- 找到 3 类稳定失败。

第 5-6 周：

- 完成 confidence-error 相关性实验。
- 决定主方向是否成立。

第 7-8 周：

- 完成轻量 uncertainty predictor。
- 得到第一版对比结果。

第 9-12 周：

- 扩展数据集。
- 补 baseline 和 ablation。
- 写第一版论文草稿。

## 8. 建议目录结构

```text
VGGT/
  VGGT_research_roadmap.md
  official-vggt/
    README.md
    demo_gradio.py
    demo_viser.py
    demo_colmap.py
    vggt/
  notes/
    glossary.md
    paper_reading_vggt.md
    failure_log.md
  data/
    phone_object_normal/
    phone_room_textured/
    phone_low_texture/
    phone_reflective/
    phone_dynamic/
  experiments/
    first_runs/
    confidence_calibration/
    frame_selection/
  scripts/
    run_vggt_batch.py
    evaluate_confidence.py
    visualize_failures.py
```

## 9. 当前最重要的下一步

不要先追求复杂方法。先完成：

1. 跑通官方 VGGT。
2. 拍 5 组手机数据。
3. 做第一版 failure log。
4. 验证 VGGT 原始 confidence 是否可靠。

如果第 4 点发现明显缺口，就可以围绕 reliability / uncertainty / active view selection 发展成论文方向。

## 10. 官方仓库启动命令

```bash
cd official-vggt
pip install -r requirements.txt
pip install -r requirements_demo.txt
python demo_gradio.py
```

第一次运行会自动从 Hugging Face 下载 VGGT 权重。之后可以用自己的图片文件夹测试 viser viewer：

```bash
python demo_viser.py --image_folder path/to/your/images/folder
```

如果要导出 COLMAP 格式，图片需要放在 `SCENE_DIR/images/` 下：

```bash
python demo_colmap.py --scene_dir=/YOUR/SCENE_DIR/
```
