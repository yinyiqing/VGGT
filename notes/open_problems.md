# 开放问题

目标：记录最新论文明确承认还没解决、或只在内部管线中处理但没有系统研究的问题。

## 值得关注

- 真实输入会触发 3D hallucination。
- learned backbone 可能给无效输入生成看似完整的几何。
- confidence 不能保证 correctness。
- point-level uncertainty 不能表示多种可能几何解释。
- depth branch 容易 overconfidence。
- dynamic / reflection / transparent / low-texture 仍然困难。
- 只做 view-level rejection 不够，patch/token/region-level 诊断仍有空间。
- COLMAP 式验证可解释，但会在低纹理、反光、模糊、低重叠场景失败。
- 训练数据标注对 window、thin structure、dynamic regions 有歧义。
- 数据管线需要过滤 unsuitable videos，但这通常是内部工程，不是用户级诊断。
- VGGT-Ω 已用 VLM 过滤 unsuitable videos，但没有把它变成用户级反馈系统。
- VGGT-Ω 标注管线用几何特征过滤失败重建：trajectory smoothness、parallax、point-cloud PCA、depth completeness、noise ratio。

## 对我们有用的切口

- 从“这个结果不可信”推进到“为什么不可信”。
- 从 point-level uncertainty 推进到 frame / region / capture-level diagnosis。
- 输出简洁采集反馈：删哪张、缺哪个视角、哪里不可靠。
- 把 VGGT 输出、传统几何验证、图像质量因素组合起来。
- 不更新主模型，先做诊断和建议系统。
- 借用 VGGT-Ω 数据过滤标准，转成用户可读的 capture diagnosis。

## 需要小心避开

- 不做单纯 uncertainty head。
- 不做单纯 outlier view rejection。
- 不做 active view selection / NBV。
- 不做通用 benchmark。
- 不做 VGGT + BA refinement。

## 参考来源

- Trust3R：unimodal point uncertainty 不能表达多重几何解释；安全场景仍需额外验证。
- Uncertainty Quality of VGGT：depth uncertainty overconfidence；metric uncertainty quantification 仍未解决。
- RobustVGGT：当前是 view-level filtering，patch/token-wise filtering 留作未来工作。
- Can These Views Be One Scene：learned 3D backbone 会 hallucinate geometric support；COLMAP 验证也不是万能。
- VGGT-Ω supplement：训练数据管线需要拒绝 blur、rotation-only、reflection、low texture、dynamic dominance 等 unsuitable videos。
- VGGT-Ω supplement：还明确使用 trajectory smoothness、parallax、PCA degeneracy、depth completeness、point-cloud noise 检测重建失败。
