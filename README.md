# 🎮 Tetris Game — 俄罗斯方块

A modern, visually stunning **Tetris game** built with **Python Flask** backend and **HTML5 Canvas** frontend. Features a neon-themed glassmorphism UI, ghost piece preview, wall-kick rotation, and particle effects on line clears.

基于 **Python Flask 后端 + HTML5 Canvas 前端** 的俄罗斯方块游戏。霓虹风格的玻璃拟态界面，支持幽灵方块预览、墙踢旋转和消行粒子特效。

---

## ✨ Features 特性

- 🎨 **Neon Glassmorphism UI** — 霓虹玻璃拟态视觉风格
- 👻 **Ghost Piece Preview** — 底部虚线预览落点位置
- 🎯 **7-Bag Randomizer** — 每 7 块各出现一次，避免连续重复
- 🧱 **Wall-Kick Rotation** — 旋转时自动尝试 7 种偏移，避免卡墙
- ✨ **Particle Effects** — 消行时炸裂粒子动画
- ⚡ **Level Speed Curve** — 每消 10 行升一级，下落速度加快
- 🏆 **Combo Scoring** — 1行100 / 2行300 / 3行500 / 4行800 × 等级倍率
- 📱 **Responsive Design** — 适配桌面和移动端

---

## 🚀 Quick Start 快速开始

### Prerequisites 环境要求

- Python **3.9+**
- pip (Python 包管理器)

### Installation 安装

```bash
# 1. 克隆仓库
git clone https://github.com/<your-username>/tetris-game.git
cd tetris-game

# 2. 安装依赖
pip install -r requirements.txt

# 3. 启动服务器
python tetris.py
```

### Play 开始游戏

在浏览器中打开 **http://127.0.0.1:5000**

---

## 🎮 Controls 操作

| Key | Action |
|-----|--------|
| `←` `→` | 左右移动 |
| `↓` | 加速下落 |
| `↑` | 旋转方块 |
| `Space` | 硬降（直接落底） |
| `P` | 暂停 / 继续 |

---

## 📁 Project Structure 项目结构

```
tetris-game/
├── tetris.py              # Flask 后端 + 游戏引擎
├── requirements.txt       # Python 依赖
├── templates/
│   └── index.html         # 前端 HTML/CSS/JS
├── .gitignore
└── README.md
```

---

## 🛠️ Tech Stack 技术栈

| Layer 层 | Technology 技术 |
|-----------|----------------|
| Backend   | Python / Flask |
| Frontend  | HTML5 Canvas + Vanilla JS |
| Styling   | CSS3 (Grid, Animations, Glassmorphism) |
| Communication | RESTful JSON API |

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET`  | `/` | 游戏页面 |
| `POST` | `/api/new_game` | 开始新游戏 |
| `GET`  | `/api/state` | 获取当前游戏状态 |
| `POST` | `/api/move` | 移动方块 `{direction: "left/right/down"}` |
| `POST` | `/api/rotate` | 旋转方块 |
| `POST` | `/api/hard_drop` | 硬降 |
| `POST` | `/api/tick` | 自然下落一帧 |

---

## 🎯 Scoring 计分规则

| Lines Cleared | Base Score |
|---------------|------------|
| 1 (Single)    | 100 |
| 2 (Double)    | 300 |
| 3 (Triple)    | 500 |
| 4 (Tetris)    | 800 |

最终得分 = 基础分 × 当前等级

---

## 📝 License

MIT — Feel free to use, modify, and share!
