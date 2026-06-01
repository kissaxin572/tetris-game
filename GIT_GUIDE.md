# 🐙 Git 使用教程

> 从入门到进阶，全面掌握 Git 版本控制

---

## 📖 目录

1. [Git 是什么？](#1-git-是什么)
2. [核心概念](#2-核心概念)
3. [安装与配置](#3-安装与配置)
4. [基础命令](#4-基础命令)
5. [分支管理](#5-分支管理)
6. [远程协作](#6-远程协作)
7. [撤销与回退](#7-撤销与回退)
8. [进阶技巧](#8-进阶技巧)
9. [工作流程](#9-工作流程)
10. [最佳实践](#10-最佳实践)

---

## 1. Git 是什么？

**Git** 是一个**分布式版本控制系统**，由 Linus Torvalds 于 2005 年创建。它可以：

- 📝 **记录每一次代码变更**（谁、什么时候、改了啥）
- ⏪ **回退到任意历史版本**
- 🌿 **并行开发**（多人同时写不同功能，互不干扰）
- 🔗 **协作合并**（把多人的工作合在一起）

### Git  vs 手动备份

```
手动备份:  项目_v1.zip → 项目_v2.zip → 项目_v2_最终.zip → 项目_v2_真的最终.zip
Git:      每次 commit 就是一次快照，清晰可追溯
```

---

## 2. 核心概念

### 2.1 三个区域

Git 有**三个工作区**，理解它们是掌握 Git 的关键：

```
工作目录               暂存区                本地仓库             远程仓库
(Working Dir)   →    (Staging Area)   →   (Local Repo)   →   (Remote Repo)
     |                    |                     |                  |
  你的文件            git add 后           git commit 后       git push 后
  随意修改           准备提交的             永久保存的          分享给团队
                     "购物车"              "快照"              "云端"
```

| 区域 | 英文 | 作用 | 对应命令 |
|------|------|------|----------|
| 工作目录 | Working Directory | 你正在编辑的文件 | 直接修改文件 |
| 暂存区 | Staging Area / Index | 下次要提交的内容 | `git add` |
| 本地仓库 | Local Repository | 所有历史版本 | `git commit` |
| 远程仓库 | Remote Repository | 云端备份 & 协作 | `git push` / `git pull` |

### 2.2 文件的四种状态

```
Untracked  →  Staged  →  Committed  →  Modified
 (新文件)     (已暂存)    (已提交)      (已修改，需要重新 add)
```

用 `git status` 随时查看当前文件状态。

---

## 3. 安装与配置

### 3.1 安装

| 平台 | 方式 |
|------|------|
| **Windows** | 下载 [git-scm.com](https://git-scm.com/) 安装包，或 `winget install Git.Git` |
| **macOS** | `brew install git` 或 Xcode 自带 |
| **Linux** | `sudo apt install git` (Ubuntu) / `sudo yum install git` (CentOS) |

```bash
# 验证安装
git --version
# 输出: git version 2.x.x
```

### 3.2 初次配置

```bash
# 设置用户名和邮箱（必做！会记录在每次提交中）
git config --global user.name   "你的名字"
git config --global user.email  "你的邮箱@example.com"

# 查看当前配置
git config --list
```

> **⚡ 提示**：配置文件的三个级别
>
> | 级别 | 作用范围 | 文件位置 |
> |------|----------|----------|
> | `--local` | 当前仓库 | `.git/config` |
> | `--global` | 当前用户所有仓库 | `~/.gitconfig` |
> | `--system` | 本机所有用户 | `/etc/gitconfig` |

---

## 4. 基础命令

### 4.1 创建仓库

```bash
# 方式一：初始化新仓库
git init                    # 在当前目录创建 .git 文件夹
git init my-project         # 新建目录并初始化

# 方式二：克隆远程仓库
git clone https://github.com/user/repo.git            # HTTPS
git clone git@github.com:user/repo.git                # SSH (推荐)
git clone https://github.com/user/repo.git my-folder  # 指定目录名
```

### 4.2 `git status` — 查看状态

```bash
git status              # 简要状态
git status -s           # 精简输出 (--short)
git status -sb          # 精简 + 显示当前分支
```

**输出解读：**

```
On branch master                    ← 当前分支
Changes to be committed:            ← 暂存区（已 add，待 commit）
        modified:   README.md

Changes not staged for commit:      ← 已跟踪但未暂存（改了没 add）
        modified:   tetris.py

Untracked files:                    ← 新文件，从未 add 过
        GIT_GUIDE.md
```

### 4.3 `git add` — 添加到暂存区

```bash
git add <file>          # 添加指定文件
git add .               # 添加当前目录所有变更
git add -A              # 添加整个仓库所有变更 (--all)
git add -p              # 交互式选择，逐个确认每个改动块
git add *.py            # 通配符，添加所有 .py 文件
```

### 4.4 `git commit` — 提交到本地仓库

```bash
git commit -m "feat: 添加登录功能"                    # 最常用：一行消息提交
git commit -m "标题" -m "详细描述"                     # 标题 + 正文
git commit -a -m "fix: 修复bug"                       # 跳过 add，直接提交所有已跟踪文件的修改
git commit --amend -m "新的提交信息"                    # 修改最近一次提交的消息
git commit --amend --no-edit                          # 追加改动到上次提交，不改消息
```

**提交信息规范（推荐）：**

```
<type>: <subject>

type 类型:
  feat      — 新功能
  fix       — 修复 Bug
  docs      — 文档更新
  style     — 代码格式（不影响功能）
  refactor  — 重构（既不是新功能也不是修 Bug）
  perf      — 性能优化
  test      — 测试相关
  chore     — 构建/工具相关

示例:
  feat: 添加消行粒子特效
  fix: 修复旋转时越界问题
  docs: 更新 README 安装说明
```

### 4.5 `git log` — 查看历史

```bash
git log                     # 完整历史
git log --oneline           # 一行一条，精简输出
git log --graph             # 显示分支图谱
git log --graph --oneline --all   # 可视化所有分支（推荐！）
git log -3                  # 只显示最近 3 条
git log --author="张三"      # 按作者筛选
git log --since="2024-01-01" # 按日期筛选
git log --grep="fix"        # 搜索提交信息
git log -p                  # 显示每次提交的具体改动
git log -p <file>           # 查看某文件的所有提交历史
```

**输出示例（`--oneline`）：**

```
a1b2c3d (HEAD -> master, origin/master) feat: 添加粒子特效
e4f5g6h fix: 修复旋转碰撞检测
i7j8k9l docs: 更新操作说明
```

### 4.6 `git diff` — 查看差异

```bash
git diff                    # 工作目录 vs 暂存区（还没 add 的改动）
git diff --staged           # 暂存区 vs 最新提交（已经 add 但没 commit 的）
git diff HEAD               # 工作目录 vs 最新提交（所有未提交的改动）
git diff HEAD~1             # 工作目录 vs 上一次提交
git diff main..feature      # 两个分支之间的差异
git diff <commit1> <commit2> # 两个提交之间的差异
```

### 4.7 `git rm` & `git mv` — 删除与重命名

```bash
git rm <file>               # 删除文件（同时从工作目录和 Git 中删除）
git rm --cached <file>      # 只从 Git 跟踪中移除，保留本地文件
git mv <old> <new>          # 重命名文件（等价于 mv + git add + git rm）
```

---

## 5. 分支管理

### 5.1 理解分支

```
main ───●───●───●───●───●───●  (主分支)
              \
feature        ●───●───●        (功能分支)
                         \
                          ●  ←  HEAD（你当前的位置）
```

分支本质上是一个**指向某次提交的可移动指针**。创建分支 = 给你一个独立的"平行宇宙"，随便折腾不影响主线。

### 5.2 `git branch` — 分支操作

```bash
git branch                  # 列出本地分支（* 标记当前分支）
git branch -a               # 列出所有分支（含远程）
git branch -r               # 只列出远程分支
git branch <name>           # 创建新分支（不切换）
git branch -d <name>        # 删除分支（已合并的）
git branch -D <name>        # 强制删除分支（即使未合并）
git branch -m <new-name>    # 重命名当前分支
```

### 5.3 `git switch` / `git checkout` — 切换分支

```bash
# Git 2.23+ 推荐使用 switch（语义更清晰）
git switch <branch>         # 切换到已有分支
git switch -c <new-branch>  # 创建并切换到新分支
git switch -                # 切回上一个分支

# 传统方式
git checkout <branch>       # 切换到已有分支
git checkout -b <new-branch># 创建并切换到新分支
```

### 5.4 `git merge` — 合并分支

```bash
# 假设当前在 main，想把 feature 合并进来
git switch main
git merge feature           # 把 feature 合并到 main
```

**三种合并模式：**

| 模式 | 条件 | 结果 |
|------|------|------|
| **Fast-forward** | main 没有新提交 | 指针直接前移，历史是线性的 |
| **Merge commit** | 两个分支都有新提交 | 创建一个合并提交，保留分叉历史 |
| **Squash merge** | — | 把 feature 所有提交压缩成一个提交 |

```bash
git merge --no-ff feature   # 强制创建合并提交（保留分支痕迹）
git merge --squash feature  # 压缩合并（需要再 commit 一次）
```

### 5.5 `git rebase` — 变基

**把当前分支的提交"搬"到目标分支的最新提交之后**，让历史变成一条直线。

```bash
# 场景：feature 分支从 main 的 B 点分出，main 已经走到了 D
git switch feature
git rebase main
```

```
变基前:                        变基后:
main   A──B──C──D             A──B──C──D──E'──F'
            \            →
feature      E──F
```

```bash
# 交互式 rebase（最强大的历史编辑工具）
git rebase -i HEAD~3          # 编辑最近 3 次提交
# 可以: pick(保留) / reword(改消息) / squash(合并) / drop(删除) / edit(暂停修改)
```

> **⚠️ 黄金法则：不要 rebase 已经 push 过的分支！** 会改写历史导致队友的仓库混乱。

**merge vs rebase 对比：**

| 维度 | `git merge` | `git rebase` |
|------|-------------|--------------|
| 历史记录 | 保留真实分叉 | 线性、干净 |
| 安全性 | 安全，不改写历史 | 改写历史，有风险 |
| 适用场景 | 公共分支、主分支 | 个人分支整理 |
| 冲突解决 | 一次性解决 | 可能需要逐提交解决 |

### 5.6 解决合并冲突

冲突发生时的文件内容：

```
<<<<<<< HEAD
你当前分支的代码
=======
对方分支的代码
>>>>>>> feature
```

**解决步骤：**

```bash
# 1. 手动编辑文件，删除冲突标记，保留正确代码
# 2. 标记为已解决
git add <冲突文件>
# 3. 完成合并
git commit -m "merge: 解决与 feature 分支的冲突"

# 或者放弃合并
git merge --abort
```

---

## 6. 远程协作

### 6.1 `git remote` — 管理远程连接

```bash
git remote -v                       # 查看所有远程仓库地址
git remote add <name> <url>         # 添加远程仓库
git remote remove <name>            # 删除远程连接
git remote rename <old> <new>       # 重命名远程
git remote show origin              # 查看远程仓库详细信息
```

### 6.2 `git push` — 推送到远程

```bash
git push origin main                # 推送到 origin 的 main 分支
git push -u origin main             # 首次推送，建立追踪关系
git push                            # 建立追踪后直接 push
git push --all origin               # 推送所有分支
git push --tags                     # 推送所有标签
git push origin --delete <branch>   # 删除远程分支
git push --force                    # 强制推送 ⚠️ 危险！覆盖远程历史
git push --force-with-lease         # 更安全的强制推送（检测远程有无新提交）
```

### 6.3 `git fetch` — 获取远程更新（不合并）

```bash
git fetch                           # 获取所有远程分支的更新
git fetch origin                    # 指定远程仓库
git fetch --prune                   # 同时清理本地已删除的远程分支引用
```

> **fetch vs pull：**
> - `fetch` = 下载远程数据，但**不合并**，你可以先看看
> - `pull`  = fetch + merge（两步合一）

### 6.4 `git pull` — 获取并合并

```bash
git pull                            # = git fetch + git merge
git pull --rebase                   # = git fetch + git rebase（推荐！保持历史线性）
```

### 6.5 完整协作流程

```bash
# 一天的工作开始前
git pull --rebase                   # 拉取最新代码

# 创建功能分支
git switch -c feat/snake-mode

# 写代码...写代码...写代码...

# 暂存 & 提交
git add .
git commit -m "feat: 添加贪吃蛇模式"

# 结束前再拉一次，确保没有冲突
git pull --rebase origin main

# 推送
git push -u origin feat/snake-mode

# 去 GitHub 创建 Pull Request → 代码审查 → 合并到 main
```

---

## 7. 撤销与回退

### 7.1 工作目录级别

```bash
git restore <file>          # 丢弃工作目录的修改（回到上次 add/commit 的状态）
git restore .               # 丢弃所有文件的修改
git clean -fd               # 删除所有未跟踪的文件和目录
git clean -n                # 先看看会删什么（dry-run）
```

### 7.2 暂存区级别

```bash
git restore --staged <file> # 把文件从暂存区撤回到工作目录
git reset HEAD <file>       # 同上（传统写法）
git reset HEAD .            # 撤回所有暂存文件
```

### 7.3 `git reset` — 回退提交

```bash
# --soft：只移动 HEAD，保留暂存区和工作目录
git reset --soft HEAD~1     # 撤销最近一次 commit，改动回到暂存区
# 用途：合并多个提交、修改提交信息

# --mixed（默认）：移动 HEAD，清空暂存区，保留工作目录
git reset HEAD~1            # 撤销 commit + add，改动保留在工作目录
git reset --mixed HEAD~1    # 同上
# 用途：重新组织提交

# --hard：移动 HEAD，清空暂存区和工作目录 ⚠️
git reset --hard HEAD~1     # 彻底回到上一次提交，所有改动丢失！
# 用途：彻底放弃所有改动
```

**三种 reset 对比图：**

```
最初状态:  commit1 → commit2 → commit3 (HEAD)

git reset --soft HEAD~1
结果:      commit1 → commit2 (HEAD)   | commit3 的改动在暂存区

git reset --mixed HEAD~1
结果:      commit1 → commit2 (HEAD)   | commit3 的改动在工作目录（红色）

git reset --hard HEAD~1
结果:      commit1 → commit2 (HEAD)   | commit3 的改动彻底消失
```

### 7.4 `git revert` — 反向提交（安全回退）

```bash
git revert HEAD             # 创建一个新提交来"撤销"最近一次提交
git revert <commit-hash>    # 撤销指定提交
git revert HEAD~3..HEAD     # 撤销最近 3 次提交
```

> **reset vs revert：**
> - `reset` = 时间旅行，改写历史（危险但干净）
> - `revert` = 创建"反提交"，不改写历史（安全，适合已推送的分支）

### 7.5 `git reflog` — 后悔药

```bash
git reflog                  # 查看所有 HEAD 移动记录（包括已删除的提交！）
```

**用法：找回"被 reset --hard 删掉的提交"**

```bash
git reflog
# a1b2c3d HEAD@{0}: reset: moving to HEAD~1
# e4f5g6h HEAD@{1}: commit: 重要功能 ← 就是这个！

git reset --hard e4f5g6h    # 恢复！
```

> reflog 默认保存 90 天，只要 commit 过就不会真的丢失。

---

## 8. 进阶技巧

### 8.1 `git stash` — 暂存工作现场

```bash
git stash                   # 暂存当前所有改动，恢复干净的工作目录
git stash save "描述信息"    # 暂存并添加描述
git stash list              # 查看暂存列表
git stash pop               # 恢复最近一次暂存（同时从列表中删除）
git stash apply             # 恢复最近一次暂存（保留在列表中）
git stash apply stash@{2}   # 恢复指定暂存
git stash drop stash@{1}    # 删除指定暂存
git stash clear             # 清空所有暂存
```

**典型场景：**

```bash
# 正在写 feature-A，突然需要修一个紧急 bug
git stash                   # 把当前工作存起来
git switch main             # 切回主分支
# ... 修复 bug 并提交 ...
git switch feature-A        # 切回来
git stash pop               # 恢复之前的工作
```

### 8.2 `git cherry-pick` — 挑选提交

```bash
git cherry-pick <commit-hash>           # 把指定提交"复制"到当前分支
git cherry-pick <hash1>..<hash3>        # 批量挑选（不含 hash1）
git cherry-pick <hash1>^..<hash3>       # 批量挑选（含 hash1）
```

**场景：** 在 feature 分支上写了一个通用工具函数，想让 main 分支也能用，但又不想合并整个 feature。

### 8.3 `git tag` — 版本标签

```bash
git tag v1.0.0                      # 轻量标签（一个指针）
git tag -a v1.0.0 -m "正式发布"      # 附注标签（含作者、日期、消息）
git tag                             # 列出所有标签
git tag -l "v1.*"                   # 按模式筛选
git push origin v1.0.0              # 推送单个标签
git push --tags                     # 推送所有标签
git tag -d v1.0.0                   # 删除本地标签
```

**语义化版本：**

```
v主版本号.次版本号.修订号

v1.2.3  →  主版本 1，次版本 2，修订 3
  1     →  不兼容的 API 变更
   2    →  向后兼容的新功能
    3   →  向后兼容的 Bug 修复
```

### 8.4 `git blame` — 追溯代码作者

```bash
git blame <file>                    # 查看每一行是谁写的
git blame -L 10,30 <file>           # 只看 10-30 行
git blame -L "/def rotate/" <file>  # 搜索函数
```

### 8.5 `.gitignore` — 忽略文件

```gitignore
# 注释
*.log                   # 所有 .log 文件
__pycache__/            # 目录
.env                    # 特定文件
!important.log          # 但保留这个（! 取反）

# 常用模板
node_modules/
dist/
build/
*.pyc
.idea/
.vscode/
```

---

## 9. 工作流程

### 9.1 GitHub Flow（推荐，简单高效）

```
main ─────────────────────────────●──●──
       \                        /      \
        feat-A ●──●──●────────●        feat-B ●──●
                       ↑ PR →
```

1. 从 `main` 创建功能分支
2. 在分支上开发和提交
3. 推送到 GitHub，创建 Pull Request
4. 代码审查 + 讨论
5. 合并到 `main`，删除功能分支

### 9.2 Git Flow（适合有版本发布的项目）

```
main    ──●────────────●──────────●──  (只存发布版本)
            \         /
develop ──●──●──●──●──●──●──●──●──  (开发主线)
              \         /
feature-A      ●──●──●
                       \
release-v1.0              ●──●  (发布前修复)
```

- `main` — 生产环境代码
- `develop` — 开发主线
- `feature/*` — 新功能分支
- `release/*` — 发布准备分支
- `hotfix/*` — 紧急修复分支

---

## 10. 最佳实践

### 10.1 提交粒度

```
❌ 一个提交改了 20 个文件，消息写 "更新"
✅ 小而聚焦：一个提交只做一件事，消息说清楚做了什么、为什么
```

### 10.2 分支命名

```
feat/snake-mode          # 新功能
fix/login-error          # Bug 修复
docs/api-reference       # 文档
refactor/game-engine     # 重构
chore/update-deps        # 杂项
```

### 10.3 日常操作清单

```bash
# 开始工作前
git pull --rebase

# 开发中频繁做
git add -p               # 交互式暂存，检查每个改动
git commit -m "..."

# 推送前
git pull --rebase        # 确保没有冲突
git push

# 完成后清理
git branch -d feat/xxx   # 删除已合并的本地分支
```

### 10.4 常见问题速查

| 问题 | 命令 |
|------|------|
| 忘了加某个文件就提交了 | `git add forgotten.txt && git commit --amend --no-edit` |
| 提交信息写错了 | `git commit --amend -m "正确的消息"` |
| 不小心 add 了不该提交的文件 | `git restore --staged <file>` |
| 不小心 commit 到错误的分支 | `git reset --soft HEAD~1` → 切到正确分支 → commit |
| 本地改乱了想重来 | `git restore .` / `git clean -fd` |
| 想回退到某次提交看看 | `git checkout <hash>`（游离 HEAD）→ 看完 `git switch -` |
| 合并后后悔了 | `git reset --hard HEAD~1`（如果还没 push） |
| 找不到了之前的提交 | `git reflog` 一定能找到 |

### 10.5 速查图谱

```
                    git init / git clone
                           │
                    ┌──────▼──────┐
                    │  工作目录    │ ← 写代码
                    └──────┬──────┘
                      git add
                    ┌──────▼──────┐
                    │   暂存区     │ ← 准备提交
                    └──────┬──────┘
                     git commit
                    ┌──────▼──────┐
                    │  本地仓库    │ ← 永久记录
                    └──────┬──────┘
              git push │  │ git fetch
              ┌────────▼──▼────────┐
              │     远程仓库       │ ← GitHub / GitLab / Gitee
              └────────────────────┘
```

---

## 📚 推荐资源

- [Pro Git 中文版](https://git-scm.com/book/zh/v2) — 官方免费书籍
- [Learn Git Branching](https://learngitbranching.js.org/) — 可视化交互学习
- [Conventional Commits](https://www.conventionalcommits.org/zh-hans/) — 提交信息规范
