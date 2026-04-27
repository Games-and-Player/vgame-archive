# 项目当前状态

> 用途：会话被 `/compact` 或 `/clear` 后，新会话读此文件即可接续。
> 最后更新：2026-04-27（赌神・双六全文转录完成，PDF p.14-17 / 刊页 12-15；首次 agent 试点成功）

## 项目目标

把 90 年代中文游戏杂志（首期为《Game 集中营》1994 试刊号）数字化为可检索的本地归档，
最终用于建一个**自用 / 小范围分享**的网站（局域网 / Tailscale 范围内）。

- 用户：自用 + 极小范围分享，不做公网
- 用户会做人工校对
- 版权：用户已确认在私域使用范围内可接受

## 工作流

- **OCR 方式**：用户机器（Pentium Silver J5005，无 AVX）跑不动 PaddleOCR。
  最终决定 **由 Claude（视觉模型）直接全文 OCR**，用户人工校对
- **分工**：Claude 全文转录 → 输出结构化 Markdown → 用户在 md 上直接改
- **批次**：每轮处理 3-5 页 PDF，避免单次对话塞太多附件触发请求大小上限
- **对话管理**：每读完一批就 `/compact`，避免历史里的页面图累积超过 32MB 请求上限

## 关键路径

| 路径 | 用途 |
|---|---|
| `/home/pi/exdisk/ocr-workspace/` | 工作区根目录 |
| `/home/pi/exdisk/ocr-workspace/CONVENTIONS.md` | **必读**——转录规范、Markdown 格式、命名约定 |
| `/home/pi/exdisk/ocr-workspace/issues/1994-vol1/` | 当前在做的这本杂志 |
| `/home/pi/exdisk/ocr-workspace/issues/1994-vol1/README.md` | 本期目录索引 + 编辑团队 + 进度 |
| `/home/pi/exdisk/ocr-workspace/issues/1994-vol1/pages/` | 短栏目（按 PDF 页归档）|
| `/home/pi/exdisk/ocr-workspace/issues/1994-vol1/articles/` | 跨多页的长文章 |
| `/home/pi/exdisk/books/H-杂志书刊/电子游戏软件/1994年/试刊GAME集中营VOL.1.pdf` | 原始扫描 PDF（72 页，192MB）|
| `/tmp/game-zjy/` | 单页拆分用的临时目录（`pdfseparate` 输出）|

## 转录规范要点（详见 CONVENTIONS.md）

- 文件名：`pages/pNNN.md` 或 `articles/<slug>.md`
- 命名以 **PDF 物理页码** 为准（pNNN，3 位数字补零）；frontmatter 同时记 `pdf_page` 和 `mag_page`
- 短栏目（卷首语、编辑手记、目录、版权）→ 逐字
- 长攻略 → **全文 OCR**（用户决定的，覆盖了 CONVENTIONS 原本的"摘要"建议）
- 操作表 / 必杀技 → Markdown 表格
- 广告 → 全文（算文化史料）

### Frontmatter 模板

```yaml
---
issue: 1994-vol1
pdf_page: NNN
mag_page: NN
section: 栏目名
title: 标题
author: 作者
games: [游戏 slug 列表]
---
```

### 校对处理原则

- 明显笔误（"干静"→"干净"）：直接改，在文末"编辑备注"里记录
- 有歧义的字：保留原文，加 `[?]`，等用户校对
- 艺术字、横竖排、boxed 文字：用 `<aside>` / Markdown 强调标记

## 进度

### 已完成

- [x] **CONVENTIONS.md** 已写
- [x] **issues/1994-vol1/README.md** 已写（含完整目录、编辑团队、版权信息）
- [x] **pages/p003.md** — PDF p.3，刊页 1，《闯关族的舞台》卷首语
- [x] **pages/p005.md** — PDF p.5，目录右半 + 版权页
- [x] **articles/dq5.md** — 《勇者斗恶龙 V 快速攻略》PDF p.6-13（刊页 4-11）**全文完结**，作者署名"● 韩"（疑为编委韩友）
- [x] **articles/dice-king.md** — 《赌神・双六》PDF p.14-17（刊页 12-15）**全文完结**，作者署名"● 熏风"（编委、本刊主任）— 首次 agent 试点

### 赌神已完结，下一篇起步

- [ ] **PDF p.18 起**（刊页 16+）— **踢王**（栏目：天堂任鸟飞）

### 后续 article（按目录）

- [ ] 天舞三国志（刊页 23）
- [ ] 爆炸俄罗斯（刊页 24+）
- [ ] 双截龙（刊页 26+）
- [ ] 快打旋风（刊页 30+）
- [ ] 快打至尊（PC 游戏室，刊页 32+）
- [ ] 世嘉世家系列（刊页 34-49）
- [ ] 昨与今 / 渗透波 / 大侦探俱乐部 / 打余茶座 / 死亡游戏 / 新手培训车间 / 二手货市场 / 编后谈

## 已识别但未解决的转录问题

### DQ5（详见 `articles/dq5.md` 文末"编辑备注"）

- "铜匙名人"——疑为"钥匙名人"
- "在桓台边不喝酒"——p.8 孤例笔误（p.9 同段印作"柜台"）
- "天空之及防具"——漏字，疑为"天空之**剑**及防具"（p.9 已印作"天空之**剑**"，确认）
- "天空之铠及盗"——疑为"天空之铠及**盾**"（p.9 已印作"天空之铠及**盾**"，确认）
- "因得亲具有通魔界的能力"——疑为"因**母亲**具有通魔界的能力"
- "波隆哥"译名来源——原作 プオーン，常见中译"普林"/"普乌"
- p.9 "亨利死围未表明身份"、"比斯达港船已可启了"
- p.10 "莱因哈特特城"（叠字）、"在泉水包转之处"
- p.11 "古巴尼亚" / "古兰巴尼亚" 不一致；"深人正喜获" 疑为"主人"

### 赌神・双六（详见 `articles/dice-king.md` 文末"编辑备注"）

- 原作待考——正文称"泰克诺公司"出品；"泰克诺"应指 **Technos Japan**（双截龙/热血发行商），但正文又把《洛克人》（Capcom）也归到泰克诺旗下，**编辑底层有混淆**
- "慕烈游戏"——疑为"剧烈/热烈/著名"之一，难辨
- "营菜"！"救命"！——"营菜"疑为"**要命**"（语境为大呼）
- "别出新裁"——成语应作"别出**心**裁"（同音误）
- "打开窗户"（A 键功能）——疑为"打开**窗口**"（菜单窗口）
- "特瓦著" = ドワーフ/Dwarf——本刊独特译法
- "基尔特" = Guild——90 年代音译变体
- "勇者的品质"表 5 项数值无标签——疑似排版漏排项目名
- "按着掷怪兽移动的骰子"——疑为"**接**着掷"
- "则被预先告之使用的结果"——"告之"应为"**告知**"

## 接续会话的提示词模板

新会话开局可以这样起步：

```
读 /home/pi/exdisk/ocr-workspace/STATE.md 接续上次的杂志数字化工作。
然后读 CONVENTIONS.md。
然后开始下一篇 article：踢王（PDF p.18 起，刊页 16 起），新建 articles/kick-king.md（slug 待定）。
建议：派 agent 处理（参考 dice-king 的 agent 试点已成功；以 dq5.md / dice-king.md 为风格基线）。

PDF 路径：/home/pi/exdisk/books/H-杂志书刊/电子游戏软件/1994年/试刊GAME集中营VOL.1.pdf
拆页用：pdfseparate -f N -l N <pdf> /tmp/game-zjy/page-%d.pdf
```

## 注意事项

- **勿污染原始 PDF**：所有处理都基于拆出的临时单页（`/tmp/game-zjy/`），原始 PDF 只读
- **不要读封面/已转录页**：已经转录到 md 的页（PDF p.1-17）不要再读 PDF，省 token
- **agent 试点**：dice-king 是首次 agent 试点，效果良好——把 4 页 PDF 读取留在子上下文，主 session 只做抽查 + 同步。后续可继续 per-article 派 agent
- **提交点**：每完成一篇 article 或一组 pages，可以考虑 `git commit`（工作区已经 `uv init` 时建了 .git）
