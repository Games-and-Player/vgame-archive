# 项目当前状态

> 用途：会话被 `/compact` 或 `/clear` 后，新会话读此文件即可接续。
> 最后更新：2026-06-20（第 08 期全部正文 OCR + 整页扫描图完成）

## 项目目标

把 90 年代中文游戏杂志（《Game 集中营》《电子游戏软件》系列）数字化为可检索的静态网站归档。
已部署至 GitHub Pages：https://games-and-player.github.io/vgame-archive/

## 总进度

| 期号 | slug | 状态 | 文件数 |
|---|---|---|---|
| VOL.1（1994 试刊号） | 1994-vol1 | **全部完成** | 30 篇 + 72 张 webp |
| VOL.2（1994 第二辑） | 1994-vol2 | **全部完成** | 27 篇 + 72 张 webp |
| 第 01 期（1994.06 创刊号）| 1994-dianruan-01 | **全部完成** | — |
| 第 02 期（1994.07） | 1994-dianruan-02 | **全部完成** | 31 篇 + 73 张 webp |
| 第 03 期（1994.09） | 1994-dianruan-03 | **全部完成** | 35 篇 + 73 张 webp |
| 第 04 期（1994.11） | 1994-dianruan-04 | **全部完成** | 36 篇 + 73 张 webp |
| 第 05 期（1994.12） | 1994-dianruan-05 | **全部完成** | 18 篇 + 73 张 webp |
| 第 06 期（1995.01） | 1995-dianruan-06 | **全部完成** | 36 篇 + 73 张 webp |
| 第 07 期（1995.02） | 1995-dianruan-07 | **全部完成** | 35 篇 + 73 张 webp |
| 第 08 期（1995.03） | 1995-dianruan-08 | **全部完成** | 37 篇 + 88 张 webp |

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
- [x] **articles/kick-king.md** — 《踢王》PDF p.18-24（刊页 16-22）**全文完结**，作者"● 邱兆龙（撰文）/ ● 周志伟（摄影）"，附 p.22 右下"天堂任鸟飞"栏目方框由 ● 韩友本人署名 — 第二次 agent 试点（7 页，比 dice-king 长，仍稳定）
- [x] **CONVENTIONS.md frontmatter 规范**已落定（articles/ 字段顺序 + 类型 + status 字段；禁用 range 字符串），后续 agent 可直接复制模板

### 天舞三国志 + 爆炸俄罗斯已完结，下一篇起步

- [x] **articles/sangokushi.md** — 《天舞三国志》PDF p.25-26（刊页 23-24）**全文完结**，无署名。p.26 为共享页面（与爆炸俄罗斯）
- [x] **articles/bombliss.md** — 《俄罗斯方块 II ＋炸弹方块》PDF p.26-27（刊页 24-25）**全文完结**，无署名。目录标题"爆炸俄罗斯"

- [x] **articles/double-dragon.md** — 《双截龙》PDF p.28-31（刊页 26-29）**全文完结**，无署名。SFC 版 Return of Double Dragon，4 页招式详解 + 5 关攻略 + 敌方角色表

- [x] **articles/final-fight.md** — 《快打旋风 II》PDF p.32-33（刊页 30-31）**全文完结**，无署名。SFC 版 Final Fight 2，角色介绍（HAGGAR/MAKI/CARLOS）+ 剧情预览

### 后续 article（按目录）

- [x] **articles/super-fighter.md** — 《快打至尊》PDF p.34-35（刊页 32-33）**全文完结**，无署名。PC 游戏室栏目专题，含栏目引言 + 萨尔可夫/新角色档案 + 剧情预览
- [x] **articles/sonic2.md** — 《音速小子索尼克 II》PDF p.36-37（彩2-3）**全文完结**，无署名。彩色插页，Sonic 2 新要素介绍
- [x] **articles/tmnt.md** — 《忍者龟》PDF p.38-39（彩4 + 刊页 33）**全文完结**，无署名。SEGA 版 TMNT 角色 + 招式详解
- [x] **articles/mickey-donald.md** — 《米老鼠和唐老鸭》PDF p.40-41（刊页 34-35）**全文完结**，无署名。叙事式游戏介绍，World of Illusion Starring Mickey Mouse and Donald Duck
- [x] **articles/mazinger.md** — 《铁甲万能侠》PDF p.42-45（刊页 36-39）**全文完结**，作者：刘儒德。4 页长文，Mazin Saga: Mutant Fighter，含招式详解 + 五关攻略
- [x] **articles/bare-knuckle.md** — 《格斗四人组》PDF p.46-47（刊页 40-41）**全文完结**，无署名。Bare Knuckle II / Streets of Rage 2，角色介绍（MAX/AXEL/EOOLE/BLAZE）+ 剧情预览
- [x] **articles/midnight-resistance.md** — 《午夜克星攻略》PDF p.48-49（刊页 42-43）**全文完结**，无署名。Midnight Resistance（Data East 1990），9 关全攻略，港式中文行文
- [x] **articles/bio-hazard-battle.md** — 《亚生命战争》PDF p.50-51（刊页 44-45）**全文完结**，作者：刘儒德。Bio-Hazard Battle / Crying（Sega 1992），射击游戏赏析，生物造型评论
- [x] **articles/shikinjo.md** — 《紫禁城》PDF p.52-53（刊页 46-47）**全文完结**，无署名。Shikinjō（Sunsoft 1991），麻将牌消除益智游戏，500 关；p.53 与世界杯共享页面
- [x] **articles/world-cup-soccer.md** — 《世界杯超级足球赛》PDF p.53-54（刊页 47-48）**全文完结**，无署名。Tecmo World Cup '92，三种阵型介绍 + 球场风采
- [x] **articles/nba-basketball.md** — 《NBA 美国职业篮球赛》PDF p.55（刊页 49）**全文完结**，作者：刘儒德。NBA Action，操作表 + 球队选择 + 赛制介绍。**世嘉世家栏目全部完结**
- [x] **articles/sega-vs-nintendo.md** — 《SEGA世嘉大战任天堂 谁是老大》PDF p.56-57（刊页 50-51）**全文完结**，作者：林明正（译）。翻译文章，基于1992年CES的Sega vs Nintendo行业分析；台式中文行文
- [x] **articles/nintendo-decade.md** — 《十年辉煌任天堂》PDF p.58-59（刊页 52-53）**全文完结**，作者：邱兆龙。任天堂十年史（1983-1993），涵盖 FC/NES/Game Boy + NEC PC Engine 竞争史；磁碟机（备份器）详述为珍贵文化史料；[待续]标记
- [x] **articles/nintendo-secrets.md** — 《任天堂探秘》PDF p.60（刊页 54）**全文完结**，作者：明星。德文译文，记者实地探访任天堂 EAD 工作室；宫本茂专访 + Sega CD 竞争分析。**昨与今栏目全部完结**
- [x] **articles/dq5-wave.md** — 《勇者五代之潮》PDF p.61-62（刊页 55-56）**全文完结**，韩友编自台湾《星际》杂志。DQ5 社会现象 + 交响乐专辑制作 + 日本电玩音乐比赛；台湾视角文化评论
- [x] **articles/sega-vr.md** — 《世嘉VR 给你一个空间》PDF p.62（刊页 56）**全文完结**，作者：韩友。Sega VR 头盔介绍，Virtual Racing 对应，约200美元。p.56 与勇者五代之潮共享。**渗透波栏目全部完结**
- [x] **articles/detective-club.md** — 《大侦探俱乐部・秘技室》PDF p.63（刊页 57）**全文完结**，主持：笑书生 / 秘技室：王韵（人大附中高一）。7款游戏秘技 + 栏目介绍
- [x] **articles/gamer-tribe.md** — 《闯关族》PDF p.64（刊页 58）**全文完结**，作者：崔筱彤。青少年视角散文，小A/B/C/D四例讨论适度游戏
- [x] **articles/must-play.md** — 《不可不玩》PDF p.65（刊页 59）**全文完结**，作者：陈江。成人视角游戏辩护文，主张"应该玩"。**打余茶座栏目全部完结**
- [x] **articles/death-game.md** — 《死亡游戏》PDF p.66-67（刊页 60-61）**全文完结**，道格・霍尼格著/丁建民译/幻想者编选。美国科幻小说中译，虚拟游戏预言真实死亡；[待续]标记
- [x] **articles/beginner-workshop.md** — 《新手培训车间》PDF p.68（刊页 62）**全文完结**，无署名。FC兼容机选购指南：兼容性测试、品牌推荐（TM系列）、合卡vs单卡经济学
- [x] **articles/flea-market.md** — 《二手货市场》PDF p.69（刊页 63）**全文完结**，无署名。读者分类广告平台；第一位顾客为编委邱兆龙（出售世嘉卡带）
- [x] **articles/editors-note.md** — 《电玩大势——编后谈》PDF p.70（刊页 64）**全文完结**，作者：田松（主编）。主编编后语：市场现状（8位→16位地域差异）、RPG 至上论、文化辩护（叶丁/陈江实例 + 毛泽东语录）。附评刊表。**其他栏目全部完结**
- [x] PDF p.71（贴纸/插图页）、PDF p.72（封底）— 非正文内容，已记录于 editors-note.md 编辑备注

> **《Game 集中营》1994 试刊号（VOL.1）全 72 页 OCR 全部完成。10 个栏目、30 篇文章/页面全文转录完成。**

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

### 踢王（详见 `articles/kick-king.md` 文末"编辑备注"，27 条）

- 原作待考——文中无明确日 / 英文原标题，由文风 + "8 位任天堂"+ 10 招踢腿 + 12 件宝物 + 8 关 + 英文密码线索，agent 推测疑为 Culture Brain 的 FC 动作 RPG（《Flying Warriors》/ 飞翔战士系列同社作品），**未确认**
- p.21 第七 / 第八件宝物段落疑似**双段重复**——可能是版面问题，也可能原刊就是叙述重复
- 招式表中"连环脚→B 水平段 4"与"高腿→B 水平段 0"出招相同——疑印刷错误
- 密码花色字符（梅花 ♣、红心、黑桃等小图标）印刷不清——agent 用 ♣ 占位，需校对者按扫描件还原
- "减血酷髻"（屏幕宝物列表）真意不明——疑为"减血鬼盔/鬼髻"或全然另一词
- "亲和恩爱"（结局）疑漏字"**相**亲相爱"
- 第五件宝物原刊故意悬念"??这到底是什么呢？"——叙事手法，已保留原貌（非错印）
- **重要副产物**：本文 p.22 右下"天堂任鸟飞"栏目方框由 ● 韩友亲笔署名，**确证 dq5.md 的"● 韩"= 韩友**（已回填 dq5.md frontmatter 和编辑备注）

## 接续会话的提示词模板

新会话开局可以这样起步：

```
读 /home/pi/exdisk/ocr-workspace/STATE.md 接续上次的杂志数字化工作。
然后读 CONVENTIONS.md（注意 frontmatter 规范已写定）。
然后开始下一篇：天舞三国志（PDF p.25 / 刊页 23，疑似单页）。

可能的处理路径：
- 若实为单页：用 pages/p025.md（用 pdf_page / mag_page 单数 frontmatter）
- 若跨页：新建 articles/sangokushi.md
建议先 Read p.25 + p.26 各一页判定边界，再决定形态。

PDF 路径：/home/pi/exdisk/books/H-杂志书刊/电子游戏软件/1994年/试刊GAME集中营VOL.1.pdf
拆页用：pdfseparate -f N -l N <pdf> /tmp/game-zjy/page-%d.pdf

派 agent 处理时，可参考已完结的 articles/dq5.md / dice-king.md / kick-king.md 作为风格基线。
```

## 注意事项

- **勿污染原始 PDF**：所有处理都基于拆出的临时单页（`/tmp/game-zjy/`），原始 PDF 只读
- **不要读封面/已转录页**：已经转录到 md 的页（PDF p.1-24）不要再读 PDF，省 token
- **agent 工作流**：dice-king（4 页）+ kick-king（7 页）两次 agent 试点都稳定。流程是——主 session 写 self-contained prompt（含 PDF 路径、页码范围、CONVENTIONS 引用、已完结 article 作风格基线、边界验证页指示）→ 派 general-purpose agent → agent 在子上下文做 pdfseparate + Read + Write → 主 session 抽查 + 回填发现 + 同步 STATE/README + commit。**默认派 agent；系列首篇 / 长叙事 / 跨文章引用时主 session 处理**
- **提交点**：每完成一篇 article 或一组 pages，可以考虑 `git commit`（工作区已经 `uv init` 时建了 .git）
