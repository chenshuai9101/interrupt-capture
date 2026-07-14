# Interrupt Capture — MVP Spec (三 Agent 共识)

## 一句话
被打断时,一个命令把"我刚在干嘛"抓进本地纯文本,之后用 grep 秒回现场。

## 约束
- 纯本地、免注册、无 API key、无外部依赖(Python 3 标准库 only)
- 无 GUI;flat-file 存储;grep 恢复

## 命令
- `ic "note text"`  → 追加一条记录到 ~/.interrupt-capture/YYYY-MM-DD.md
    自动附带: 时间戳 / cwd / git 分支(若在 repo) / macOS 前台窗口标题(osascript, 拿不到就跳过)
- `ic`(无参数)   → 交互式读一行 note(便于绑热键)
- `ic resume [kw]` → 显示今天(或最近)的记录; 有 kw 则 grep 过滤; 高亮 file:line 与路径
- `ic list`        → 列出所有日期的 log
- `ic --help`

## 存储格式(每行一条, 便于 grep)
`- [HH:MM] {note}  ::cwd={path} ::branch={b} ::win={title}`

## 恢复体验
- 提供 shell alias 建议: `alias resume='ic resume'`
- resume 输出里若含 `path:line` 或存在的文件路径, 给出可直接粘贴的打开命令提示

## 交付物
- interrupt_capture.py (单文件, 可 chmod +x)
- install.sh (软链到 /usr/local/bin/ic 或 ~/bin/ic, 并打印 alias 建议)
- README.md (安装 + 热键绑定说明: macOS 用 Automator/skhd)
