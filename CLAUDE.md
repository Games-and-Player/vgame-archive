# 遊戲誌 — 中文游戏杂志数字归档

中文游戏杂志（《Game 集中营》《电子游戏软件》《游戏机实用技术》等）的 OCR 全文转录 + 静态网站归档。

## 构建 & 测试

```bash
uv run python -m web.build              # 本地构建 → dist/
uv run python -m web.build --base /X/   # 指定 base path（GitHub Pages 用）
uv run python -m pytest tests/ -q       # 测试
uv run python -m web.serve              # 本地预览（8000 端口）
```

**不要用 `python` 直接执行**——pyenv 版本不匹配，必须通过 `uv run`。

## OCR 工作流（每期完整流程）

### 1. 拆页 & 准备

```bash
mkdir -p issues/{slug}/{articles,pages,assets} /tmp/dianruan-{N}
pdfseparate "源PDF路径" /tmp/dianruan-{N}/page-%d.pdf
```

### 2. 结构扫描（主循环直接做，不派 agent）

直接读取封面 + 目录页（通常 PDF 1 和 PDF 11-12），从目录获取栏目和页码。
结合历史规律推断结构（三段式彩插、对调页），只在边界不确定时额外读 2-3 页验证。
手动编制 README.md 目录。**不要为此派独立 agent。**

### 3. WebP 生成

```bash
# pdftoppm → PIL 裁白边 → WebP quality=82
# 生成到 issues/{slug}/assets/page-NNN.webp（本地保留，不提交到 git）
```

### 4. OCR 转录

派 **2 个** agent 并行读取 PDF，输出 Markdown 到 articles/ 和 pages/。

**agent 提示词必须包含以下约束（节省 token）：**
- ❌ 不要派出子 agent（subagent），自己完成所有文件
- ❌ 不要运行 pytest 测试或 web.build 构建
- ❌ 不要运行引号修复脚本（主循环统一修复）
- ❌ 不要读取 CONVENTIONS.md（关键规则已内联在提示词中）
- ✅ 直接用 Write 工具写文件，一次写完一个文件
- ✅ 转录规则：全文逐字转录，中文全角引号 ""，frontmatter 字段顺序 issue→title→section→pdf_pages→mag_pages→author→games→status，每篇末尾 `## 编辑备注`
- ✅ 图片位置用 `【图】` 描述，**禁止**使用 Hugo shortcode `{{< img >}}` 或任何模板语法

### 5. 提交前检查

```bash
# ASCII 双引号检查（正文必须用 "" 不用 "）
grep -rn '"' issues/{slug}/articles/*.md issues/{slug}/pages/*.md | grep -v '^.*:---$'
# 用 fix-quotes 脚本批量修复
# 运行测试 + 构建
uv run python -m pytest tests/ -q
uv run python -m web.build
```

### 6. 提交 & 推送

```bash
git add issues/{slug}/ STATE.md
git commit -m "dianruan-{N}: 完结全文转录（...）"
git push
```

### 7. WebP 上传到 R2

```bash
# ⚠️ 必须用 copy 不用 sync —— sync 会在本地文件被清理后把 R2 也清空！
rclone copy issues/{slug}/assets/ r2:game-magazine/{slug}/ --include "*.webp"
# 上传完成后验证（必须有 116 个文件）：
rclone ls r2:game-magazine/{slug}/ | wc -l
```

### 8. 清理临时文件（每期必做！）

**⚠️ 必须在第 7 步 R2 上传完成并验证后，才能清理本地 WebP！**

```bash
rm -rf /tmp/dianruan-{N}/          # 拆页临时 PDF
rm -rf /tmp/pytest-of-pi/          # pytest 构建缓存（每次约 3GB）
rm -f issues/{slug}/assets/*.webp  # 本地 WebP（已上传到 R2）
# 每 2-3 期清理一次 agent 日志：
# rm -rf ~/.claude/projects/.../subagents/ ~/.claude/projects/.../tool-results/
```

## 图片托管

- **存储**：Cloudflare R2 桶 `game-magazine`
- **域名**：`https://game-magazine.nerdliu.cyou/`
- **URL 格式**：`https://game-magazine.nerdliu.cyou/{slug}/page-{NNN}.webp`
- **同步工具**：`rclone sync ... r2:game-magazine/{slug}/`
- **模板变量**：`assets_base`（在 `web/build.py` 中设置）
- **Git 不追踪 WebP**：`.gitignore` 已排除 `issues/*/assets/`

## 目录结构

```
issues/{slug}/
  README.md                 # 本期目录索引 + 编辑团队 + 进度
  articles/*.md             # 长文章（全文 OCR）
  pages/*.md                # 短栏目页（封面、目录、封三、封底等）
  assets/page-NNN.webp      # 整页扫描图（本地保留，上传到 R2，不进 git）
web/                        # 静态站点构建器（Jinja2 + Markdown）
  build.py                  # 构建入口，含 assets_base R2 域名配置
  templates/                # Jinja2 模板（图片 src 指向 R2）
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

- 每期 116 页用 2 个 agent 约消耗 **10-13 万 token**
- 每次 cron 触发只做 **1 期**，不要连续追赶多期
- 如果 session limit 快到了（agent 开始失败），立即停止，等下次 cron 触发继续
- 周限额约 100 万 token，控制在每天不超过 1 期
- 结构扫描自己做（读 2-3 页），不派 agent
- OCR agent 不允许派子 agent、不允许跑测试/构建/引号修复

## Loop 配置

定时自动执行 OCR 转录任务。Prompt 和 cron 表达式存于此处，作为唯一真实来源。

```
cron: 3 2 * * *
prompt: 继续执行任务，如果上一个任务已完成，可以继续下一期内容的转录。如果不知道下一期是哪一期，可以自己从目录中寻找并推测。任务完成后，从 CLAUDE.md 的「Loop 配置」段读取 cron 和 prompt，先用 CronList 检查现有 job，如有则 CronDelete，再 CronCreate 新 job（重置 7 天过期）。注意：必须先 CronList 确认只删除本 loop 的 job，避免重复创建。
```

**执行规则：**
1. Cron 触发 → 执行 prompt 中的转录任务
2. 完成后（commit + push + R2 + cleanup）→ 读取本段配置
3. `CronList` → 找到现有 job → `CronDelete` 该 job
4. `CronCreate` 用上面的 cron 和 prompt → 重置 7 天计时器
5. 如果 `CronList` 为空（已过期），跳过删除直接创建

## 当前状态

详见 `STATE.md`。
