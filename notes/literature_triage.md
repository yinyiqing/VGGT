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

## 关键相关工作

- VGGT：统一预测 camera、depth、point map、track。
- DUSt3R / MASt3R：feed-forward 3D reconstruction 的核心前序工作。
- Uncertainty Quality of VGGT：已经分析 VGGT uncertainty 质量。
- Trust3R：轻量 evidential uncertainty head，已经覆盖 VGGT cross-architecture 实验。
- RobustVGGT：利用 VGGT 内部信号做 outlier view rejection。
- Co-VGGT：探测 VGGT 内部 co-visibility 表征。
- Diversity-aware View Partitioning：处理冗余视角和 scalable VGGT。
- FrameVGGT / RetrieveVGGT：长视频/流式场景的 memory 和 frame selection。

## 暂时更有空间

- 面向真实手机采集的 capture-level reliability。
- 判断一组输入是否“值得重建”，而不只是判断单点是否可信。
- 区分坏帧类型：模糊、动态、低纹理、反光、低重叠、冗余帧。
- 给出重新拍摄建议：缺哪个方向、哪些帧应删、哪些区域不可信。
- 结合 VGGT 输出、跨视角一致性、图像质量和帧级几何稳定性。

## 当前判断

不要把主贡献放在“VGGT confidence 不可靠”。这已经有人做。

更稳的方向是：

> 真实不受控图像集合中的 feed-forward 3D reconstruction 可靠性诊断。

也就是从“点是否可信”提升到“这组输入为什么失败、该删哪张、该补拍什么”。
