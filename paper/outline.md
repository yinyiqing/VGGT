# 论文大纲草稿

暂定题目：

> Diagnosing Reliability of Feed-Forward 3D Reconstruction on In-the-Wild Image Collections

## 1. Introduction

- Feed-forward 3D reconstruction 很快，但用户不知道结果什么时候可信。
- VGGT 这类模型会输出 confidence，但 confidence 不等于 correctness。
- 真实拍摄中常见失败：低重叠、小物体、模糊、反光、低纹理。

## 2. Problem

输入：一组无序或弱有序图片，以及 VGGT 输出。

输出：

- 哪些 frame / region / capture 条件不可靠；
- 为什么不可靠；
- 用户应该如何补救。

## 3. Method

待定。先从无需训练的诊断信号开始。

## 4. Experiments

- 官方样例 sanity check。
- 自采桌面小物体。
- 低重叠 / 模糊 / 反光扰动。
- 3DGS 对照。

## 5. Limitations

- 不保证修复重建。
- 不替代几何优化。
- 诊断信号需要和更多场景验证。
