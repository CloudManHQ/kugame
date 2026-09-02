# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Stack

纯静态 HTML/CSS/JS。GTM/ 落地页为独立单文件夹交付，零构建依赖，可直接部署到任意静态托管。产品本体另有两套栈（CLI: Python/Rich；Web: FastAPI + vanilla JS + Tailwind），与 GTM 页互不依赖。

## Users

主要用户：正在学习或刚入门 Kubernetes 的开发者与运维工程师（含 SRE 初级岗）。
情境：面对 kubectl/YAML 的枯燥学习曲线，希望在碎片时间里用"玩"的方式系统性掌握 K8s 命令与概念。
任务（job）：坚持学完一套完整的 K8s 命令体系并形成肌肉记忆，而不是浅尝辄止的教程收藏。

## Product Purpose

KuGame 把 Kubernetes 学习做成武侠修仙风格的游戏：12 章武侠剧情对应 90+ kubectl/K8s 命令（12 大类），10 大修仙境界对应能力成长，配合装备/技能/天赋/副本/宠物/题库/成就/排行榜/PVP 等 RPG 系统。提供 CLI（终端 ASCII 艺术）与 Web（现代 UI + WebSocket 实时同步）双版本，存档互通。成功 = 用户真的通关：学完 12 章、命令形成长期记忆。

## Positioning

唯一机制：把 K8s 命令体系 1:1 映射为"修仙功法"——章节即剧情卷、命令即功法招式、能力成长即境界突破，且 CLI 与 Web 双版本同进度（存档互通）。竞品（教程站、刷题站、沙箱实验平台）无法照搬这套叙事-命令映射与双端进度同步。

## Operating Context

- 使用环境：终端（CLI 版，Python 3.8+/Rich 渲染）与浏览器（Web 版，FastAPI + WebSocket）。
- 学习模式：故事 / 挑战 / 测验 / 纯答题四种，支持错题集与智能组卷。
- 玩家数据：本地 JSON 存档（player_save.json）。
- 语言文化：界面与叙事为中文武侠/修仙语汇（境界、功法、副本）。

## Capabilities and Constraints

已确认能力：90+ 命令 / 12 章剧情 / 10 境界 / 四种学习模式 / 题库（complete_question_bank.json）/ 暗黑+明亮双主题 / 响应式 / 双端存档同步。
明确未决（GTM 页不得虚构）：定价与商业化形态、上线域名、GitHub Stars 数据、在线 Demo 地址、社区入口、用户证言、团队信息。GTM 页涉及以上内容一律使用清晰标记的占位符。

## Brand Commitments

- 名称：KuGame。
- 叙事语系：武侠修仙（境界体系：凡人→金仙；功法/副本/秘籍等词汇）。
- 双形态：CLI 终端美学 + Web 现代界面，二者并列是品牌事实。
- GTM 页语言：双语切换（中文默认，一键切换英文）。

## Evidence on Hand

- 仓库源码与题库（可自制真实功能演示素材：CLI ASCII 输出、界面元素复刻）。
- 无：公开 Star 数、在线 Demo、社区入口、证言、媒体报道。GTM 页所有外链与数据一律用明确标记的占位符，功能演示素材可自制但需标注为演示。

## Product Principles

1. 学习必须好玩且可坚持——游戏的奖励结构服务于真实的命令记忆。
2. 双端一体——终端与浏览器是同一份功法，不是两个产品。
3. 叙事即记忆法——每个命令都长在剧情里，不为虚构而虚构。
4. 真实可验证——不夸大能力与数据，未上线的证据不冒充已上线。

## Accessibility & Inclusion

GTM 页双语（zh 默认 / en 切换）、响应式（桌面+移动）、图片提供替代文本、色彩对比达标（WCAG AA）。
