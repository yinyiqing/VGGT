# 文献排雷

目标：先判断哪些方向已经被做过，避免做成相似工作。

## 已经很拥挤

- VGGT 基础复现和普通 benchmark 对比。
- 只分析 VGGT confidence 是否可靠。
- 只做 point-level uncertainty calibration。
- 只用 VGGT confidence 过滤点云。
- 只做 outlier view rejection / distractor image removal。
- 只做 co-visibility / overlap prediction。
- 只做长序列 memory、token merging、加速。
- 只做 diversity-aware view partitioning。
- 只做 active view selection / next-best-view。
- 只做 token/frame selection 提速。
- 只判断多视角输入是否属于同一个静态场景。
- 只做通用 3D GFM benchmark。
- 只把 feed-forward 预测接到 SfM/BA 做全局优化。
- 只做传统 SfM/UAV 的在线采集反馈。
- 只做 LoRA/self-calibration 让模型适配单个场景。
- 只做大规模视频弱监督适配。
- 只做 next-best-image / next-best-view 策略。

## 关键相关工作

- VGGT：统一预测 camera、depth、point map、track。
- DUSt3R / MASt3R：feed-forward 3D reconstruction 的核心前序工作。
- Uncertainty Quality of VGGT：已经分析 VGGT uncertainty 质量。
- Trust3R：轻量 evidential uncertainty head，已经覆盖 VGGT cross-architecture 实验。
- RobustVGGT：利用 VGGT 内部信号做 outlier view rejection。
- Co-VGGT：探测 VGGT 内部 co-visibility 表征。
- Diversity-aware View Partitioning：处理冗余视角和 scalable VGGT。
- FrameVGGT / RetrieveVGGT：长视频/流式场景的 memory 和 frame selection。
- Good Token Hunting：inter-frame + intra-frame token selection，主打提速。
- AREA3D：把 VGGT confidence 和 VLM guidance 用到 active view selection。
- 传统 NBV / view planning：已经长期研究采集视角和重建质量。
- Can These Views Be One Scene：指出 VGGT/DUSt3R/MASt3R 会对无关图、重复图、噪声产生 3D 幻觉；用 COLMAP 式信号做一致性评估。
- E3D-Bench：综合评估 3D geometric foundation models。
- Glob3R：用 3D foundation model 初始化，再结合 tracks、motion averaging、BA 做全局 SfM。
- LoRA3D：用模型自身预测、confidence 重加权和 LoRA 做场景级自校准。
- SAGE：用互联网视频弱监督适配 3D geometric foundation model。
- RealX3D：真实退化 3D benchmark，覆盖 blur、low light、exposure、smoke、dynamic occlusion、reflection。
- 3DReflecNet：反光、透明、低纹理物体的大规模数据集。
- On-the-fly Feedback SfM：传统/UAV 场景的在线重建质量评估和路径反馈。
- VIN-NBV：用网络做 next-best-view selection，提高 3D reconstruction 资源效率。

## 暂时更有空间

- 面向真实手机采集的 capture-level reliability。
- 判断一组输入是否“值得重建”，而不只是判断单点是否可信。
- 区分坏帧类型：模糊、动态、低纹理、反光、低重叠、冗余帧。
- 给出重新拍摄建议：缺哪个方向、哪些帧应删、哪些区域不可信。
- 结合 VGGT 输出、跨视角一致性、图像质量和帧级几何稳定性。
- 不直接做机器人 NBV，而是做离线照片集的质量诊断和采集反馈。
- 不只回答“是不是一个场景”，还要回答“为什么差、删哪张、补拍什么”。
- 和传统在线 SfM 区分：我们关注离线手机照片集 + feed-forward 3D model。
- 和 LoRA/self-calibration 区分：我们先做诊断和采集反馈，不直接更新主模型。

## 当前判断

不要把主贡献放在“VGGT confidence 不可靠”。这已经有人做。

更稳的方向是：

> 真实不受控图像集合中的 feed-forward 3D reconstruction 可靠性诊断。

也就是从“点是否可信”提升到“这组输入为什么失败、该删哪张、该补拍什么”。

## 下一轮重点读

- 传统 SfM/MVS 的 image selection 和 quality prediction。
- 手机/无人机/文物扫描中的 capture guidance。
- blur、dynamic object、reflection、low texture 对重建失败的影响。
- feed-forward 3D 方法有没有公开的真实采集失败 benchmark。
- 能否把传统几何验证和 VGGT 输出结合成可解释诊断，而不是单一分数。

## 可借用的传统信号

- view graph 连通性。
- pairwise inlier 数和匹配覆盖。
- triangulation angle / baseline。
- reprojection error。
- 相机轨迹稳定性。
- 初始图像对和 next-best-image 的不确定性准则。
- 图像平面特征分布。
- planar / rotational / general motion 判断。

## 采集质量因素

- overlap 是否足够。
- baseline 是否太小或太大。
- 是否有低纹理大平面。
- 是否有反光、透明、金属、水面。
- 是否有运动物体或动态遮挡。
- 曝光、光照、白平衡是否变化大。
- 是否模糊、失焦、高 ISO 噪声。

## 可能可用数据

- 自采手机图片：最快，用来建立失败直觉。
- NAVI：casual image captures，有高质量 3D scan 和 2D-3D 对齐。
- OCRTOC / A Real World Dataset：真实桌面物体、多视角 RGB-D。
- RealX3D：真实退化条件，适合验证 blur / low light / reflection。
- 3DReflecNet：适合验证 reflective / transparent / low-texture。

## 参考链接

- VGGT: https://arxiv.org/abs/2503.11651
- Uncertainty Quality of VGGT: https://arxiv.org/html/2606.16479v1
- Trust3R: https://arxiv.org/abs/2605.19539
- RobustVGGT: https://arxiv.org/html/2512.04012v1
- Co-VGGT: https://arxiv.org/abs/2607.09503
- Good Token Hunting: https://arxiv.org/abs/2605.23892
- Can These Views Be One Scene: https://arxiv.org/abs/2605.18754
- SysCON3D code: https://github.com/mvp18/3DConsistency-metrics
- AREA3D: https://arxiv.org/html/2512.05131v1
- E3D-Bench: https://arxiv.org/abs/2506.01933
- Glob3R: https://arxiv.org/html/2607.09225v1
- LoRA3D: https://arxiv.org/abs/2412.07746
- SAGE: https://arxiv.org/abs/2602.07891
- NAVI: https://navidataset.github.io/
- A Real World Dataset for Multi-view 3D Reconstruction: https://arxiv.org/abs/2203.11397
- RealX3D: https://arxiv.org/html/2512.23437v2
- 3DReflecNet: https://arxiv.org/html/2605.10204v1
- Video-Based 3D Reconstruction Review: https://www.mdpi.com/2313-433X/12/3/128
- Structure-from-Motion Revisited: https://openaccess.thecvf.com/content_cvpr_2016/html/Schonberger_Structure-From-Motion_Revisited_CVPR_2016_paper.html
- View-graph Selection Framework for SfM: https://www.ecva.net/papers/eccv_2018/papers_ECCV/html/Rajvi_Shah_View-graph_Selection_Framework_ECCV_2018_paper.php
- On-the-fly Feedback SfM: https://arxiv.org/abs/2512.02375
- VIN-NBV: https://arxiv.org/html/2505.06219v1
