# 老杂志数字化归档项目

90 年代中文游戏杂志（《Game 集中营》《电子游戏软件》等）的 OCR 全文转录 + 静态网站归档。

## 构建 & 测试

```bash
uv run python -m web.build              # 本地构建 → dist/
uv run python -m web.build --base /X/   # 指定 base path（GitHub Pages 用）
uv run python -m pytest tests/ -q       # 12 个测试
uv run python -m web.serve              # 本地预览（8000 端口）
```

**不要用 `python` 直接执行**——pyenv 版本不匹配，必须通过 `uv run`。

### OCR 提交前检查

转录完成后、提交前，务必检查 ASCII 双引号泄漏（正文必须用 `""` 不用 `"`）：

```bash
# 扫描正文中的 ASCII 双引号（frontmatter 内的不算）
grep -rn '"' issues/*/articles/*.md issues/*/pages/*.md | grep -v '^.*:---$'
```

如有输出，用 `/tmp/fix-quotes.py` 批量修复（脚本会跳过 frontmatter）。

## 目录结构

```
issues/1994-vol1/           # 当前已完成的唯一一期
  README.md                 # 本期目录索引 + 编辑团队 + 进度
  articles/*.md             # 长文章（30 篇，全文 OCR 完成）
  pages/*.md                # 短栏目页（卷首语、目录等）
  assets/page-NNN.webp      # 72 张整页扫描图（150 DPI，自动裁白边）
web/                        # 静态站点构建器（Jinja2 + Markdown）
  build.py                  # 构建入口，支持 --base 参数
  parser.py                 # Markdown 解析（frontmatter + md_in_html）
  models.py                 # Issue / Article / Page 数据模型
  search.py                 # 搜索索引生成
  templates/                # Jinja2 模板
  static/                   # CSS + JS
tests/                      # pytest 测试
CONVENTIONS.md              # 转录规范（frontmatter 格式、字段约束、校对原则）
STATE.md                    # 项目进度跟踪（会话间接续用）
```

## 转录规范要点

- **全文 OCR**——不做摘要，逐字转录
- Frontmatter 字段顺序固定：articles/ 用 `issue → title → section → pdf_pages → mag_pages → author → games → status`
- `pdf_pages` 用 int list `[6, 7, 8]`，禁止 range 字符串
- 难辨字标 `[?]`，明显笔误在编辑备注中记录
- 引号用中文全角 `""`，不用 ASCII `"`
- 每篇文末必须有 `## 编辑备注` 段

## PDF 源文件 & 页码偏移

```
原始 PDF：/home/pi/exdisk/books/H-杂志书刊/电子游戏软件/1994年/试刊GAME集中营VOL.1.pdf
拆页命令：pdfseparate -f N -l N <pdf> /tmp/game-zjy/page-%d.pdf
页码关系：PDF 页 = 刊页 + 2（无彩页区域）/ 刊页 + 6（彩页后，因 PDF p.35-38 为 4 张彩色插页）
```

## 整页扫描图生成

```bash
# 批量导出（已完成，存于 assets/）
# 150 DPI + 自动裁白边（bg_threshold=225, blank_ratio=0.95）
# 模板自动在文章底部显示对应扫描图，支持点击放大
```

## 部署

- 仓库：`Games-and-Player/vgame-archive`
- GitHub Pages：https://games-and-player.github.io/vgame-archive/
- Action 在 push master 时自动构建部署（`.github/workflows/pages.yml`）
- `--base` 从 `${{ github.event.repository.name }}` 自动推导，换仓库无需改代码

## 当前状态

《Game 集中营》1994 试刊号（VOL.1）**全 72 页 OCR 完成**，10 个栏目、30 篇文章/页面全文转录。详见 `STATE.md` 和 `issues/1994-vol1/README.md`。
