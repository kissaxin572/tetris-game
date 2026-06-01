# -*- coding: utf-8 -*-
"""
俄罗斯方块 — Flask 后端 + 游戏引擎
Tetris Game with Python Flask Backend
"""

import sys
import io
import random
from flask import Flask, render_template, request, jsonify

# 修复 Windows 控制台 GBK 编码问题
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

app = Flask(__name__)

# ============================================================
# 游戏常量
# ============================================================
COLS = 10
ROWS = 20

# 经典七种方块 (使用相对坐标，以旋转中心为原点)
SHAPES = {
    'I': [(0, -1), (0, 0), (0, 1), (0, 2)],
    'O': [(0, 0), (0, 1), (1, 0), (1, 1)],
    'T': [(0, -1), (0, 0), (0, 1), (1, 0)],
    'S': [(0, 0), (0, 1), (1, -1), (1, 0)],
    'Z': [(0, -1), (0, 0), (1, 0), (1, 1)],
    'J': [(0, -1), (0, 0), (0, 1), (1, -1)],
    'L': [(0, -1), (0, 0), (0, 1), (1, 1)],
}

# 方块颜色 (霓虹风格)
COLORS = {
    'I': '#00f0f0',
    'O': '#f0f000',
    'T': '#a000f0',
    'S': '#00f000',
    'Z': '#f00000',
    'J': '#0000f0',
    'L': '#f0a000',
}

# 得分规则: 1行100, 2行300, 3行500, 4行800
SCORE_TABLE = {1: 100, 2: 300, 3: 500, 4: 800}
LINES_PER_LEVEL = 10


class TetrisGame:
    """俄罗斯方块游戏引擎"""

    def __init__(self):
        self.board = [[None for _ in range(COLS)] for _ in range(ROWS)]
        self.score = 0
        self.level = 1
        self.lines_cleared = 0
        self.game_over = False
        self.current_piece = None
        self.current_pos = (0, 0)
        self.next_piece = None
        self.bag = []
        self._spawn_piece()

    # ---- 7-bag 随机系统 ----
    def _refill_bag(self):
        """每7块各出现一次，避免连续重复"""
        self.bag = list(SHAPES.keys())
        random.shuffle(self.bag)

    def _next_from_bag(self):
        if not self.bag:
            self._refill_bag()
        return self.bag.pop()

    # ---- 生成方块 ----
    def _spawn_piece(self):
        if self.next_piece is None:
            self.next_piece = self._next_from_bag()

        piece_type = self.next_piece
        self.current_piece = piece_type
        self.current_pos = (0, COLS // 2 - 1)
        self.next_piece = self._next_from_bag()

        # 生成即碰撞 → 游戏结束
        if self._collision(self.current_piece, self.current_pos):
            self.game_over = True

    # ---- 获取方块在世界坐标中的格子 ----
    def _get_cells(self, piece_type, pos):
        r0, c0 = pos
        return [(r0 + dr, c0 + dc) for dr, dc in SHAPES[piece_type]]

    # ---- 碰撞检测 ----
    def _collision(self, piece_type, pos):
        for r, c in self._get_cells(piece_type, pos):
            if c < 0 or c >= COLS or r >= ROWS:
                return True
            if r >= 0 and self.board[r][c] is not None:
                return True
        return False

    # ---- 移动 ----
    def move(self, dr, dc):
        r, c = self.current_pos
        new_pos = (r + dr, c + dc)
        if not self._collision(self.current_piece, new_pos):
            self.current_pos = new_pos
            return True
        return False

    # ---- 旋转 (顺时针 90°) + 墙踢 ----
    def rotate(self):
        if self.current_piece == 'O':
            return True  # O 无需旋转

        cells = SHAPES[self.current_piece]
        # (r, c) -> (c, -r)
        rotated = [(c, -r) for r, c in cells]

        r, c = self.current_pos
        kicks = [(0, 0), (-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, 1)]

        for kr, kc in kicks:
            new_pos = (r + kr, c + kc)
            rotated_cells = [(new_pos[0] + dr, new_pos[1] + dc) for dr, dc in rotated]
            if all(
                0 <= col < COLS and row < ROWS and (row < 0 or self.board[row][col] is None)
                for row, col in rotated_cells
            ):
                SHAPES[self.current_piece] = rotated
                self.current_pos = new_pos
                return True
        return False

    # ---- 硬降 ----
    def hard_drop(self):
        dropped = 0
        while self.move(1, 0):
            dropped += 1
        self._lock_piece()
        return dropped

    # ---- 锁定方块 ----
    def _lock_piece(self):
        color = COLORS[self.current_piece]
        for r, c in self._get_cells(self.current_piece, self.current_pos):
            if r >= 0:
                self.board[r][c] = color

        self._clear_lines()
        self._spawn_piece()

    # ---- 消行 & 计分 ----
    def _clear_lines(self):
        cleared = 0
        new_board = []
        for row in self.board:
            if all(cell is not None for cell in row):
                cleared += 1
            else:
                new_board.append(row)

        for _ in range(cleared):
            new_board.insert(0, [None for _ in range(COLS)])

        self.board = new_board

        if cleared > 0:
            self.lines_cleared += cleared
            self.score += SCORE_TABLE.get(cleared, 0) * self.level
            self.level = self.lines_cleared // LINES_PER_LEVEL + 1

    # ---- 自然下落一格 ----
    def tick(self):
        if self.game_over:
            return False
        if not self.move(1, 0):
            self._lock_piece()
        return True

    # ---- 序列化为 JSON 状态 ----
    def get_state(self):
        # 构建显示棋盘 (含活动方块 & 幽灵方块)
        display_board = [row[:] for row in self.board]

        if self.current_piece and not self.game_over:
            piece_color = COLORS[self.current_piece]

            # 幽灵方块 (落点预览)
            ghost_r, ghost_c = self.current_pos
            while not self._collision(self.current_piece, (ghost_r + 1, ghost_c)):
                ghost_r += 1
            ghost_pos = (ghost_r, ghost_c)

            # 绘制当前活动方块
            for r, c in self._get_cells(self.current_piece, self.current_pos):
                if 0 <= r < ROWS and 0 <= c < COLS:
                    display_board[r][c] = piece_color

            # 绘制幽灵方块
            if ghost_pos != self.current_pos:
                for r, c in self._get_cells(self.current_piece, ghost_pos):
                    if 0 <= r < ROWS and 0 <= c < COLS and display_board[r][c] is None:
                        display_board[r][c] = 'ghost'

        # 下一块信息
        np_type = self.next_piece
        next_data = None
        if np_type:
            next_data = {
                'type': np_type,
                'color': COLORS.get(np_type, '#fff'),
                'cells': SHAPES[np_type],
            }

        return {
            'board': display_board,
            'score': self.score,
            'level': self.level,
            'lines': self.lines_cleared,
            'gameOver': self.game_over,
            'nextPiece': next_data,
        }


# ============================================================
# 全局游戏实例 (单例，生产环境建议用 session/redis)
# ============================================================
games = {}

def get_game():
    return games.get('default')


# ============================================================
# Flask 路由
# ============================================================

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/new_game', methods=['POST'])
def new_game():
    games['default'] = TetrisGame()
    return jsonify(games['default'].get_state())


@app.route('/api/state', methods=['GET'])
def get_state():
    game = get_game()
    if game is None:
        return jsonify({'error': 'No game started'}), 400
    return jsonify(game.get_state())


@app.route('/api/move', methods=['POST'])
def move():
    game = get_game()
    if game is None:
        return jsonify({'error': 'No game started'}), 400
    direction = request.get_json().get('direction', '')
    if direction == 'left':
        game.move(0, -1)
    elif direction == 'right':
        game.move(0, 1)
    elif direction == 'down':
        game.move(1, 0)
    return jsonify(game.get_state())


@app.route('/api/rotate', methods=['POST'])
def rotate():
    game = get_game()
    if game is None:
        return jsonify({'error': 'No game started'}), 400
    game.rotate()
    return jsonify(game.get_state())


@app.route('/api/hard_drop', methods=['POST'])
def hard_drop():
    game = get_game()
    if game is None:
        return jsonify({'error': 'No game started'}), 400
    game.hard_drop()
    return jsonify(game.get_state())


@app.route('/api/tick', methods=['POST'])
def tick():
    game = get_game()
    if game is None:
        return jsonify({'error': 'No game started'}), 400
    game.tick()
    return jsonify(game.get_state())


# ============================================================
# 启动入口
# ============================================================
if __name__ == '__main__':
    print('=' * 50)
    print('  Tetris Server Starting...')
    print('  Open: http://127.0.0.1:5000')
    print('=' * 50)
    app.run(host='127.0.0.1', port=5000, debug=True)
