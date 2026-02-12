<p align="center">
  <img src="https://img.shields.io/badge/OpenClaw-Swarm-blue?style=for-the-badge" alt="OpenClaw Swarm"/>
  <img src="https://img.shields.io/badge/version-1.0.0-green?style=for-the-badge" alt="Version"/>
  <img src="https://img.shields.io/badge/license-MIT-orange?style=for-the-badge" alt="License"/>
</p>

<h1 align="center">🐝 OpenClaw Swarm</h1>

<p align="center">
  <strong>让你的 OpenClaw 从"单打独斗🦞"进化为"团队作战🦞🦞🦞"！</strong>
</p>

<p align="center">
  <a href="README.md">🇨🇳 中文</a> | <a href="README_EN.md">🇺🇸 English</a>
</p>

---

## 📖 项目简介

OpenClaw 在处理简单和自动化任务上非常有效，但在处理复杂任务时存在几个痛点：

| 问题 | 描述 |
|------|------|
| ⏱️ **任务耗时极长** | 默认线性串行执行，处理超长任务时耗时极长 |
| 📄 **鲁棒性较差** | 长任务链条中单一任务报错可能导致整体失败，中间过程不透明 |
| 🔥💰 **非常烧钱** | 默认使用 Opus 4.5 模型，一天复杂任务可能烧掉几百元 |

**OpenClaw Swarm 解决方案：**

将复杂任务拆解为多个子任务，指派合适的子智能体**并行**完成，高难度任务用强模型，简单任务用便宜模型。

> 💡 **一句话总结**：把 OpenClaw 从"一个人干活"变成"带领一支团队干活"。就像公司里的项目经理，接到复杂任务后不是自己从头干到尾，而是把任务拆成小块，分配给不同专业人员（研究员搜资料、程序员写代码、设计师画图），大家并行工作，最后汇总结果。

## ✨ 核心优势

| 能力 | 说明 |
|------|------|
| 🔀 **任务并行** | 多个无依赖的子任务同时执行，不再排队等 |
| 💰 **成本优化** | 简单任务用便宜模型(GLM)，复杂任务才用昂贵模型(Claude)，**实测节省 50-70% 成本** |
| 🔧 **完全可定制** | 每个智能体有独立人格文件(SOUL.md)，可随时添加/删除/修改，工具权限精细控制 |
| 📚 **经验积累** | 智能体记录有效经验，下次执行类似任务时自动注入，越用越聪明，不是每次从零开始 |
| 🏠 **本地优先** | 完全运行在你自己的 OpenClaw 实例，数据不经过第三方，可离线使用 |

## 📦 智能体团队

| 智能体 | 角色 | 核心能力 |
|--------|------|----------|
| 📋 pm | 产品经理 | 需求分析、任务拆解、优先级排序 |
| 🔍 researcher | 研究员 | 信息搜集、资料整理、多源验证 |
| 👨‍💻 coder | 程序员 | 编码、调试、测试、重构 |
| ✍️ writer | 写作者 | 文档、报告、文案、翻译 |
| 🎨 designer | 设计师 | 配图、插画、数据可视化 |
| 📊 analyst | 分析师 | 数据处理、统计分析、趋势预测 |
| 🔎 reviewer | 审核员 | 代码审查、内容审核、合规检查 |
| 💬 assistant | 助手 | 简单问答、消息转发、提醒 |
| 🤖 automator | 自动化 | 定时任务、网页自动化、脚本 |
| 🔥 github-tracker | GitHub追踪 | 热门项目追踪、趋势分析 |

> 💡 目前实现的是静态多智能体集群，后续我们也会尝试动态生成团队的配置

## 🚀 快速开始

### 方式一：Skill 形式安装（⭐ 推荐）

直接将以下指令发送给您的 bot 或在 openclaw 后台输入：

```bash
npx skills add https://gitlab.chehejia.com/ai-market/lixiang-skills-marketplace/-/tree/master/packages/agent-swarm
```

> ⚠️ **注意**: 目前该技能主要适配在公司数智云内部部署的 OpenClaw，外部环境可能会出现报错。
>
> 🛒 **技能集市地址**: [ai-market.chehejia.com](https://ai-market.chehejia.com)

### 方式二：文档配置（不推荐）

让你的 OpenClaw 读取配置文档进行 swarm 集群配置：
- 📄 [OpenClaw Swarm 多智能体系统配置教程](https://li.feishu.cn/wiki/SVw0wIj5viweM9kqd70c2SlDnAg)

> 通过文档配置得到的 swarm 集群设定不稳定，且不方便更新版本，但教程有助于了解 Swarm 的设计理念。

### 方式三：文件安装

如果 skill 下载失败，可以直接将 `agent-swarm.skill` 文件发送给你的机器人。

### 安装后验证

```bash
# 1. 检查智能体团队
openclaw agents list

# 2. 重启对话
/new

# 3. 重启网关
openclaw gateway restart
```

> 📞 安装遇到问题请联系 @李大鹏，OpenClaw 本身问题请联系数智云团队

## 📚 使用案例

### Case 1: 🔬 技术调研报告

> "调研强化学习技术并写一篇分析报告"

**执行流程：**
```
├── 🔍 researcher × 3 (并行)
│   ├── 搜索 Arxiv 论文
│   ├── 搜索 GitHub 项目
│   └── 搜索飞书内部文档
├── ✍️ writer (串行)
│   └── 整合资料，撰写分析报告
└── 🎨 designer (串行)
    └── 生成技术发展路线图
```

---

### Case 2: 📊 市场调研 & 网页可视化

> "帮我调研白银价格走势，生成可交互的网页展示"

**执行流程：**
```
├── 🔍 researcher × 3 (并行)
│   ├── 客观数据调研
│   ├── 看多观点收集
│   └── 看空观点收集
├── ✍️ writer → 🔎 reviewer (串行)
└── 👨‍💻 coder (串行)
    └── 开发交互式网页
```

---

### Case 3: 🐙 GitHub 项目调研

> "调研主流 AI Agent 框架（LangChain、AutoGPT、CrewAI），对比分析"

---

### Case 4: 📚 批量资料处理

> "帮我处理这 50 封邮件，提取关键信息并生成汇总报告"

**效率分析：**
- ⏱️ 时间节省：从串行数小时缩短到并行十几分钟
- 💰 Token 成本：简单任务用 GLM 替代 Claude，节省 50-70%

---

### Case 5: 🐱 图像生成

> "画一只可爱的猫猫！"

配置 Gemini 图像模型后支持图片生成。

---

### Case 6: 🎬 动画分镜绘制

> "根据剧本生成动画分镜"

## 🎯 适用场景

### ✅ 适合用 Swarm

- **技术调研报告** — 多框架并行调研
- **代码项目** — 分析 → 编码 → 审核
- **数据分析报告** — 处理 → 分析 → 可视化 → 撰写
- **内容创作** — 调研 → 写作 → 配图 → 审核

### ❌ 不适合 Swarm

- **简单问答** — 直接问就行
- **单一任务** — 没必要拆解
- **实时对话** — 延迟要求高

## 🔧 高级配置

### 🎨 定制化智能体

根据需求和 OpenClaw 对话来新增定制化的子智能体，或通过调用 skill 修改智能体配置。

示例对话：
> "冒险小理，帮我在 agent swarm 中增加一个子智能体，专门用来检测每天最新的 github 热门项目"

### 🖼️ 图像生成模型配置

申请 Gemini API 后（[申请地址](https://li.chj.cloud/apihub/abilitysquare)），在 `openclaw.json` 中配置：

```json
{
  "vendor-gemini-3-pro-image": {
    "baseUrl": "https://llm-gateway-proxy.inner.chj.cloud/llm-gateway/v1beta",
    "apiKey": "Your API Key",
    "api": "google-generative-ai",
    "authHeader": "x-goog-api-key",
    "models": [
      {
        "id": "gemini-3-pro-image-preview",
        "name": "CHJ Gemini 3 Pro Image",
        "reasoning": false,
        "input": ["text", "image"],
        "cost": { "input": 0, "output": 0 },
        "contextWindow": 1000000,
        "maxTokens": 65536
      }
    ]
  }
}
```

配置完成后测试：`帮我生成一张小猫的图片`

## 🆚 竞品对比

| 特性 | OpenClaw Swarm | Kimi K2.5 Swarm | Claude Code Swarm |
|------|----------------|-----------------|-------------------|
| 状态 | ✅ 可用 | 🔬 实验阶段 | 🔬 实验阶段 |
| 会员要求 | 无 | 最高级会员 | - |
| 模型可选 | ✅ 完全自定义 | ❌ 固定 | - |
| 定制性 | ✅ 高度可定制 | ❌ 受限 | - |
| 二次开发 | ✅ 低成本 | ❌ 不支持 | - |

使用 OpenClaw 具有高度可定制性，可以根据自己的需求进行低成本且高定制化的二次开发，欢迎大家在我们的 skill 上进行优化和提供 feature。

## 🔮 开发中 Feature

- 📺 **前端可视化**：任务进展、子智能体描述、任务拆解都可在网页直观查看和修改
- 👤 **人在回路机制**：每次使用后可提供专家建议，子智能体记录经验，避免重复错误
- 🤖 **动态团队生成**：根据任务自动生成最优团队配置

## 📁 目录结构

```
agent-swarm/
├── SKILL.md              # 主技能文档（必读）
├── README.md             # 项目说明（本文件）
├── scripts/
│   ├── setup_wizard.py   # 配置向导
│   ├── agent_manager.py  # 智能体管理
│   └── init_agents.py    # 初始化脚本
└── references/
    └── setup-guide.md    # 详细部署指南
```

## 👥 团队 & 联系

**技术团队：**
- @李大鹏（负责人）
- @韩纪飞
- @曾令铭
- @张升涛

**鸣谢：** 感谢数智云团队提供的 OpenClaw 技术支持

## 📢 加入社区

欢迎加入话题群交流使用心得，或加入内测群提供改进建议和分享使用案例！

## ⚠️ 声明

目前关于 OpenClaw Swarm 的配置和优化我们还在探索中，使用中该能力可能存在不稳定性，后续会不断优化和升级，并分享相关使用经验。欢迎有相关需求或成功探索了使用案例的同事进行交流！

## 📄 许可证

MIT License

---

<p align="center">
  Made with ❤️ for <a href="https://github.com/anthropics/claude-code">OpenClaw</a>
</p>

📚 **项目文档**: [飞书文档](https://li.feishu.cn/wiki/SVw0wIj5viweM9kqd70c2SlDnAg)
