# 遊戲誌 — 中文游戏杂志数字归档

中文游戏杂志（《Game 集中营》《电子游戏软件》《游戏机实用技术》等）的 OCR 全文转录 + 静态网站归档。

## 构建 & 部署

本地不做构建。push 后 GitHub Actions 自动构建部署，构建失败会有通知。

本地预览（仅调试用）：`uv run python -m web.serve`

**不要用 `python` 直接执行**——pyenv 版本不匹配，必须通过 `uv run`。
**不要在本地运行 `pytest` 或 `web.build`**——会产生数十 GB 临时文件撑满磁盘。

## OCR 工作流（每期完整流程）

### 1. 拆页 & 准备

```bash
mkdir -p issues/{slug}/{articles,pages,assets} /tmp/dianruan-{N}
pdfseparate "源PDF路径" /tmp/dianruan-{N}/page-%d.pdf
```

### 2. 结构扫描

直接读取封面 + 目录页（通常 PDF 1 和 PDF 11-12），从目录获取栏目和页码。
结合历史规律推断结构（三段式彩插、对调页），只在边界不确定时额外读 2-3 页验证。
手动编制 README.md 目录。

### 3. WebP 生成

```bash
# pdftoppm → PIL 裁白边 → WebP quality=82
# 生成到 issues/{slug}/assets/page-NNN.webp（本地保留，不提交到 git）
```

### 4. OCR 转录（串行）

主 session 直接按顺序读取 PDF 页面，输出 Markdown 到 articles/ 和 pages/。
不派子 agent，全部在当前 session 中串行完成。

**转录约束：**
- ❌ 不要运行 pytest 或 web.build（构建由 GitHub Actions 完成）
- ❌ 不要运行引号修复脚本（完成后统一修复）
- ✅ 直接用 Write 工具写文件，一次写完一个文件
- ✅ 转录规则：全文逐字转录，中文全角引号 ""，frontmatter 字段顺序 issue→title→section→pdf_pages→mag_pages→author→games→status，每篇末尾 `## 编辑备注`
- ✅ 图片位置用 `【图】` 描述，**禁止**使用 Hugo shortcode `{{< img >}}` 或任何模板语法

### 5. 提交前检查

```bash
# ASCII 双引号检查（正文必须用 "" 不用 "）
grep -rn '"' issues/{slug}/articles/*.md issues/{slug}/pages/*.md | grep -v '^.*:---$'
# 用 fix-quotes 脚本批量修复
```

**不要在本地跑 pytest 或 web.build**——构建验证由 GitHub Actions 完成。

### 6. 提交 & 推送

```bash
git add issues/{slug}/ STATE.md
git commit -m "dianruan-{N}: 完结全文转录（...）"
git push
```

### 7. 清理临时文件（每期必做！）

```bash
rm -rf /tmp/dianruan-{N}/          # 拆页临时 PDF
```

**⚠️ 不要删除本地 WebP！** 图片由本地 Nginx 直接服务，删除会导致线上图片 404。

## 图片托管

- **存储**：本地 `issues/{slug}/assets/*.webp`，由 Nginx（端口 8787）直接服务
- **反代**：Cloudflare Tunnel → `localhost:8787`
- **域名**：`https://game-magazine.nerdliu.cyou/`
- **URL 格式**：`https://game-magazine.nerdliu.cyou/{slug}/page-{NNN}.webp`
- **模板变量**：`assets_base`（在 `web/build.py` 中设置，域名不变）
- **Git 不追踪 WebP**：`.gitignore` 已排除 `issues/*/assets/`
- **备份**：历史数据仍保留在 Cloudflare R2 桶 `game-magazine`（已停止同步）
- **⚠️ 不要删除本地 WebP**——它们是线上图片的唯一来源

## 目录结构

```
issues/{slug}/
  README.md                 # 本期目录索引 + 编辑团队 + 进度
  articles/*.md             # 长文章（全文 OCR）
  pages/*.md                # 短栏目页（封面、目录、封三、封底等）
  assets/page-NNN.webp      # 整页扫描图（本地保留，不进 git）
web/                        # 静态站点构建器（Jinja2 + Markdown）
  build.py                  # 构建入口，含 assets_base 域名配置
  templates/                # Jinja2 模板（图片 src 指向域名）
tests/                      # pytest 测试
CONVENTIONS.md              # 转录规范
STATE.md                    # 项目进度跟踪（会话间接续用）
```

## 转录规范要点

- **全文 OCR**——不做摘要，逐字转录
- Frontmatter 字段顺序固定：articles/ 用 `issue → title → section → pdf_pages → mag_pages → author → games → status`
- `pdf_pages` 用 int list `[6, 7, 8]`，禁止 range 字符串
- 难辨字标 `[?]`，明显笔误在编辑备注中记录
- 引号用中文全角 `""`，不用 ASCII `"`
- 每篇文末必须有 `## 编辑备注` 段

## 部署

- 仓库：`Games-and-Player/vgame-archive`
- GitHub Pages：https://games-and-player.github.io/vgame-archive/
- Action 在 push master 时自动构建部署（`.github/workflows/pages.yml`）
- `--base` 从 `${{ github.event.repository.name }}` 自动推导

## Token 预算注意事项

- 每期 116 页串行约消耗 **8-12 万 token**
- 每次定时触发只做 **1 期**，不要连续追赶多期
- 结构扫描只读 2-3 页，不多读

**Rate limit 处理规则：**
- 如果因 rate limit 中断，**不要当场重试**
- 立即检查已完成的页面覆盖率，提交已有成果（commit message 标注 partial）
- 等下次定时触发时继续处理缺失页面

## 定时配置（pi-schedule-prompt）

定时自动执行 OCR 转录任务。使用 `schedule_prompt` 扩展管理定时任务。
**注意：定时任务只在 pi session 保持打开时才会触发。**

```
schedule: 0 3 2 * * *
name: ocr-daily
prompt: 继续执行任务，如果上一个任务已完成，可以继续下一期内容的转录。如果不知道下一期是哪一期，可以自己从目录中寻找并推测。
```

Job 创建一次即可持久运行，无需每次删除重建。
首次设置：`schedule_prompt(action="add", name="ocr-daily", schedule="0 3 2 * * *", type="cron", prompt="...")`
查看状态：`schedule_prompt(action="list")`

**cron 格式说明：** pi-schedule-prompt 使用 6 字段格式（秒 分 时 日 月 周），`0 3 2 * * *` = 每天 02:03:00。

## 当前状态

详见 `STATE.md`。
