# Star Office UI

[English README](README.md)

一个给 AI 助手用的「像素办公室」状态 UI。

- 俯视像素办公室背景（可自定义；仓库内含示例背景 `office_bg.png`）
- 角色会根据 `state` 切换动作（walking / rushing / alert）
- 可选：气泡/打字机效果
- **内置 Gateway 日志 + TUI 状态侧边栏**
- 支持 Cloudflare Tunnel 远程访问

> 说明：英文版为 README.md。

## 效果预览

![UI Preview](frontend/office_bg.png)

**本分支新增：**
- 示例背景图
- Gateway 日志 + TUI 状态面板
- 多套角色动作与切换逻辑

- `idle / syncing` → 休息区
- `writing / researching` → 办公区
- `executing` → 执行区
- `error` → 报警区

UI 会轮询 `/status` 并渲染角色状态。

## 目录结构

```
star-office-ui/
  backend/        # Flask 后端（服务 index + status）
  frontend/       # Phaser 前端 + office_bg.png
  state.json      # 运行时状态文件
  set_state.py    # 状态更新脚本
```

## 依赖

- Python 3.9+
- Flask

## 快速开始（本地）

### 1) 安装依赖

```bash
pip install flask
```

### 2) 放置背景图

放一张 **800×600 PNG**：

```
star-office-ui/frontend/office_bg.png
```

### 3) 启动后端

```bash
cd star-office-ui/backend
python app.py
```

访问：
- http://127.0.0.1:18791

### 4) 更新状态

在项目根目录：

```bash
python3 star-office-ui/set_state.py writing "Working on a task..."
python3 star-office-ui/set_state.py idle "Standing by"
```

## 公网访问（Cloudflare quick tunnel）

```bash
cloudflared tunnel --url http://127.0.0.1:18791
```

得到 `https://xxx.trycloudflare.com` 访问地址。

## 安全提示

- quick tunnel URL 可能变化，不保证 uptime
- `/status` 对外公开，detail 不要写敏感信息
- 如需隐私：可给 `/status` 加 token / 不返回 detail
