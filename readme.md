# LegalDocCraft - 多 Agent 法律文书生成与风险审查系统

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/)

**LegalDocCraft** 是一个基于多 Agent 协作的法律文书自动生成与风险审查原型系统。  
它专为中小律所设计，旨在将民间借贷、劳动仲裁等高发案由的起诉状/申请书撰写时间从数小时压缩至分钟级，同时通过对抗性辩论大幅降低风险遗漏率。

## 核心功能

- **长链推理生成**：从事实回溯、法律要件拆解到诉讼请求构建，形成严密逻辑链。
- **多 Agent 辩论式审查**：生成 Agent、审查 Agent（模拟对方律师）、合规 Agent 交替发言，由编排 Agent 消解冲突并迭代优化文书。
- **量化风险报告**：根据辩论历史自动评级，提示证据漏洞、时效、管辖等致命风险点。
- **全程上下文记录**：保留每一轮迭代的推理过程，便于审计与合规检查。

## 快速开始

### 1. 克隆仓库

```bash
git clone https://github.com/yourusername/legal-doc-craft.git
cd legal-doc-craft