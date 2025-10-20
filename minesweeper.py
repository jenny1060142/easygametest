# minesweeper.py - clean single implementation
import random
import argparse
import sys
import re


def make_board(n, bombs):
    """Return board where -1 are bombs and other cells contain neighbor counts."""
    board = [[0] * n for _ in range(n)]
    coords = [(r, c) for r in range(n) for c in range(n)]
    bomb_coords = random.sample(coords, bombs)
    for r, c in bomb_coords:
        board[r][c] = -1
    for r in range(n):
        for c in range(n):
            if board[r][c] == -1:
                continue
            cnt = 0
            for dr in (-1, 0, 1):
                for dc in (-1, 0, 1):
                    if dr == 0 and dc == 0:
                        continue
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < n and 0 <= nc < n and board[nr][nc] == -1:
                        cnt += 1
            board[r][c] = cnt
    return board


def print_view(view):
    n = len(view)
    w = max(2, len(str(n - 1)))
    header = ' ' * (w + 1) + ' ' + ' '.join(f'{i:>{w}}' for i in range(n))
    print(header)
    for r in range(n):
        row = f'{r:>{w}} '
        for c in range(n):
            row += ' ' + f'{view[r][c]:>{w}}'
        print(row)


def reveal(board, view, r, c):
    """Reveal a cell; flood-fill zeros (4-directional)."""
    n = len(board)
    # don't reveal flags
    if view[r][c] == 'x':
        return
    if view[r][c] != '.':
        return
    if board[r][c] == -1:
        view[r][c] = '!'
        return
    if board[r][c] > 0:
        view[r][c] = str(board[r][c])
        return
    # zero -> flood fill (4 directions)
    stack = [(r, c)]
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    while stack:
        x, y = stack.pop()
        if view[x][y] != '.':
            continue
        if board[x][y] == 0:
            view[x][y] = ' '
            for dr, dc in dirs:
                nx, ny = x + dr, y + dc
                if 0 <= nx < n and 0 <= ny < n and view[nx][ny] == '.':
                    if board[nx][ny] == 0:
                        stack.append((nx, ny))
                    elif board[nx][ny] > 0:
                        view[nx][ny] = str(board[nx][ny])
        else:
            view[x][y] = str(board[x][y])


def check_win(board, view):
    n = len(board)
    for r in range(n):
        for c in range(n):
            if board[r][c] != -1 and view[r][c] == '.':
                return False
    return True


def play(n, bombs, auto=False):
    board = make_board(n, bombs)
    view = [['.'] * n for _ in range(n)]
    if auto:
        cells = [(r, c) for r in range(n) for c in range(n)]
        random.shuffle(cells)
        for r, c in cells:
            reveal(board, view, r, c)
            if view[r][c] == '!':
                print_view(view)
                print('\n你踩到炸彈了! 遊戲結束')
                return
            if check_win(board, view):
                for i in range(n):
                    for j in range(n):
                        if board[i][j] == -1:
                            view[i][j] = '!'
                print_view(view)
                print('\n你贏了!')
                return
        print_view(view)
        print('\n自動模式結束')
        return

    help_text = (
        "指令格式：\n"
        "  r c        -> 揭露座標 (row col)\n"
        "  m r c      -> 標記/取消標記該格 (flag/unflag)\n"
        "              範例：\n"
        "                m 1 2    -> 標記列 1、欄 2\n"
        "                m12 或 m1,2 -> 緊湊格式也會被解析為 (1,2)\n"
        "  q          -> 離開遊戲\n"
        "註：標記格子用 x 顯示；未揭露格用 . 顯示。"
    )

    print('=== Minesweeper ===')
    print(help_text)

    while True:
        print_view(view)
        cmd = input('> ').strip()
        if not cmd:
            continue
        if cmd.lower() == 'q':
            print('離開遊戲')
            return
        parts = cmd.split()
        # handle mark/flag commands in multiple formats: 'm r c', 'm r,c', 'mrc', 'm1,2', etc.
        if parts[0].lower().startswith('m'):
            # extract everything after the first 'm' (allow uppercase M too)
            after = cmd.lstrip()
            if after and after[0].lower() == 'm':
                after = after[1:].strip()

            # try to find integers anywhere (handles 'm 1 2', 'm1,2', 'm:1,2')
            nums = re.findall(r'-?\d+', after)
            r = c = None
            if len(nums) >= 2:
                try:
                    r = int(nums[0]); c = int(nums[1])
                except ValueError:
                    r = c = None
            else:
                # special-case compact two-digit like '12' meaning r=1,c=2 (only safe for single-digit indices)
                compact = ''.join(ch for ch in after if ch.isdigit() or ch == '-')
                s = compact.lstrip('-')
                if len(s) == 2 and s.isdigit():
                    r = int(s[0]); c = int(s[1])

            if r is None or c is None:
                print('無法解析標記座標，請使用: m row col 或 m row,col（例如: m 1 2 或 m1,2）')
                continue

            if not (0 <= r < n and 0 <= c < n):
                print('座標超出範圍')
                continue

            if view[r][c] == '.':
                view[r][c] = 'x'
            elif view[r][c] == 'x':
                view[r][c] = '.'
            else:
                print('該格已揭露，無法標記')
            continue

        if len(parts) < 2:
            print('請輸入座標或指令')
            continue
        try:
            r = int(parts[0]); c = int(parts[1])
        except ValueError:
            print('請輸入數字座標')
            continue
        if not (0 <= r < n and 0 <= c < n):
            print('座標超出範圍')
            continue

        reveal(board, view, r, c)
        if view[r][c] == '!':
            for i in range(n):
                for j in range(n):
                    if board[i][j] == -1:
                        view[i][j] = '!'
            print_view(view)
            print('\n你踩到炸彈了! 遊戲結束')
            return
        if check_win(board, view):
            for i in range(n):
                for j in range(n):
                    if board[i][j] == -1:
                        view[i][j] = '!'
            print_view(view)
            print('\n你贏了!')
            return


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--size', '-n', type=int, default=9)
    parser.add_argument('--bombs', '-b', type=int, default=10)
    parser.add_argument('--auto', action='store_true')
    args = parser.parse_args()
    n = args.size
    bombs = args.bombs
    if bombs >= n * n:
        print('炸彈數必須小於格子總數')
        sys.exit(1)
    play(n, bombs, auto=args.auto)


if __name__ == '__main__':
    main()
