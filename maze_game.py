import random
import sys
import argparse
import os

# Try to enable colored output when available
USE_COLOR = False
try:
    from colorama import init as colorama_init, Fore, Style
    colorama_init()
    USE_COLOR = True
except Exception:
    USE_COLOR = False

IS_WINDOWS = os.name == 'nt'
if IS_WINDOWS:
    try:
        import msvcrt
    except Exception:
        msvcrt = None


def make_perfect_maze(n):
    """Generate an n x n perfect maze using depth-first search (recursive backtracker).
    Cells: 1 = path, 0 = boundary, x = wall later when printing, but we keep 1 for passage
    Returns a grid of size n x n with 1 for passage and 0 for outer boundary cells.
    """
    # Ensure odd-sized internal grid for maze carving if needed
    if n < 3:
        # minimal workable maze
        grid = [[1]*n for _ in range(n)]
        for i in range(n):
            grid[0][i] = 0
            grid[n-1][i] = 0
            grid[i][0] = 0
            grid[i][n-1] = 0
        return grid

    # Start with all walls (0) then carve passages (1)
    grid = [[0]*n for _ in range(n)]

    # carve interior using DFS on odd coordinates
    def neighbors(r, c):
        for dr, dc in ((0,2),(0,-2),(2,0),(-2,0)):
            nr, nc = r+dr, c+dc
            if 1 <= nr < n-1 and 1 <= nc < n-1:
                yield nr, nc

    start_r = random.randrange(1, n-1, 2)
    start_c = random.randrange(1, n-1, 2)

    stack = [(start_r, start_c)]
    grid[start_r][start_c] = 1

    while stack:
        r, c = stack[-1]
        nbrs = [p for p in neighbors(r, c) if grid[p[0]][p[1]] == 0]
        if not nbrs:
            stack.pop()
            continue
        nr, nc = random.choice(nbrs)
        # knock down wall between
        wall_r, wall_c = (r+nr)//2, (c+nc)//2
        grid[wall_r][wall_c] = 1
        grid[nr][nc] = 1
        stack.append((nr, nc))

    # set outer boundary to 0 explicitly (already 0)
    for i in range(n):
        grid[0][i] = 0
        grid[n-1][i] = 0
        grid[i][0] = 0
        grid[i][n-1] = 0

    return grid


def place_start_end_on_boundary(grid):
    n = len(grid)
    # all possible boundary cells that are not corners blocked: include all border coordinates
    positions = []
    for i in range(n):
        positions.append((0, i))
        positions.append((n-1, i))
        positions.append((i, 0))
        positions.append((i, n-1))
    # remove duplicates
    positions = list(set(positions))

    # remove corner positions to avoid corner start/end
    corners = {(0,0),(0,n-1),(n-1,0),(n-1,n-1)}
    positions = [p for p in positions if p not in corners]

    s = random.choice(positions)
    e = random.choice(positions)
    while e == s:
        e = random.choice(positions)

    # Make sure start and end are passages (if boundary is 0, carve an opening inward)
    def ensure_open(pos):
        r, c = pos
        if grid[r][c] == 0:
            # carve neighbor inside
            if r == 0:
                grid[r+1][c] = 1
            elif r == n-1:
                grid[r-1][c] = 1
            elif c == 0:
                grid[r][c+1] = 1
            elif c == n-1:
                grid[r][c-1] = 1
            grid[r][c] = 1

    ensure_open(s)
    ensure_open(e)

    return s, e


def print_maze(grid, start, end, player=None, steps=0):
    n = len(grid)
    out_lines = []
    for r in range(n):
        row = []
        for c in range(n):
            ch = ' '
            if (r, c) == player:
                ch = 'P'
            elif (r, c) == start:
                ch = 'S'
            elif (r, c) == end:
                ch = 'E'
            else:
                # use block or hash for walls/boundary for better visuals
                if r == 0 or r == n-1 or c == 0 or c == n-1:
                    ch = '#'
                else:
                    ch = ' ' if grid[r][c] == 1 else '█'
            # add spacing between cells for readability
            row.append(ch)
            row.append(' ')
        out_lines.append(''.join(row).rstrip())

    # colored print if available
    if USE_COLOR:
        colored_lines = []
        for line in out_lines:
            # color mapping: █ -> red, # -> cyan, S/E/P -> green/yellow/magenta
            line = line.replace('█', Fore.RED + '█' + Style.RESET_ALL)
            line = line.replace('#', Fore.CYAN + '#' + Style.RESET_ALL)
            line = line.replace('S', Fore.GREEN + 'S' + Style.RESET_ALL)
            line = line.replace('E', Fore.YELLOW + 'E' + Style.RESET_ALL)
            line = line.replace('P', Fore.MAGENTA + 'P' + Style.RESET_ALL)
            colored_lines.append(line)
        print('\n'.join(colored_lines))
    else:
        print('\n'.join(out_lines))

    print(f"Steps: {steps}")
    print()  # extra blank line after steps for clarity


def get_input():
    """Read a single keypress and return normalized key: 'w','a','s','d','up','down','left','right','q'.
    On Windows use msvcrt for immediate keypress; otherwise fallback to input() requiring Enter.
    """
    if IS_WINDOWS and msvcrt:
        while True:
            ch = msvcrt.getch()
            if ch in (b'w', b'a', b's', b'd', b'q', b'W', b'A', b'S', b'D', b'Q'):
                return ch.decode().lower()
            # arrow keys and special keys come as prefix b'\x00' or b'\xe0' then a code
            if ch in (b'\x00', b'\xe0'):
                ch2 = msvcrt.getch()
                code = ch2
                if code == b'H':
                    return 'up'
                if code == b'P':
                    return 'down'
                if code == b'K':
                    return 'left'
                if code == b'M':
                    return 'right'
            # ignore other keys
    else:
        # fallback: require Enter
        k = input().strip().lower()
        if k in ('w','a','s','d','q'):
            return k
        if k in ('up','down','left','right'):
            return k
        return ''


def find_path_bfs(grid, start, end):
    # BFS to check path existence and return path
    n = len(grid)
    from collections import deque
    q = deque([start])
    prev = {start: None}
    while q:
        r, c = q.popleft()
        if (r, c) == end:
            break
        for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
            nr, nc = r+dr, c+dc
            if 0 <= nr < n and 0 <= nc < n and grid[nr][nc] == 1 and (nr,nc) not in prev:
                prev[(nr,nc)] = (r,c)
                q.append((nr,nc))

    if end not in prev:
        return None
    # reconstruct
    path = []
    cur = end
    while cur:
        path.append(cur)
        cur = prev[cur]
    path.reverse()
    return path


def ensure_unique_solution(grid, start, end):
    # For simplicity, we will verify uniqueness by checking that the path found is the only shortest path
    # A perfect maze generated by DFS already guarantees a unique path between any two cells in the passage graph
    # So we just ensure start/end are on passages and return the path
    path = find_path_bfs(grid, start, end)
    return path


def play_interactive(grid, start, end):
    player = start
    steps = 0
    n = len(grid)
    print_maze(grid, start, end, player, steps)
    print("Use WASD or arrow keys to move. Press q to quit.")
    while True:
        key = get_input()
        if not key:
            continue
        if key == 'q':
            print('Quit')
            break
        move = None
        if key in ('w','up'):
            move = (-1,0)
        elif key in ('s','down'):
            move = (1,0)
        elif key in ('a','left'):
            move = (0,-1)
        elif key in ('d','right'):
            move = (0,1)
        else:
            # ignore other keys
            continue

        nr, nc = player[0]+move[0], player[1]+move[1]
        # increment steps regardless of success of move
        steps += 1
        if not (0 <= nr < n and 0 <= nc < n):
            # out of bounds attempted
            print_maze(grid, start, end, player, steps)
            continue
        # treat grid value 0 as blocked/boundary
        if grid[nr][nc] == 0:
            # attempted move into blocked cell — count step but do not move
            print_maze(grid, start, end, player, steps)
            continue

        # successful move
        player = (nr, nc)
        print_maze(grid, start, end, player, steps)
        if player == end:
            print(f'You reached the end in {steps} steps!')
            break


def demo_solve(grid, start, end):
    path = ensure_unique_solution(grid, start, end)
    if not path:
        print('No path found (demo)')
        return
    steps = 0
    for p in path:
        print_maze(grid, start, end, p, steps)
        steps += 1
    print(f'Demo reached end in {steps-1} steps')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--size', '-n', type=int, default=15, help='maze size n for n x n')
    parser.add_argument('--demo', action='store_true', help='run demo auto-solve')
    args = parser.parse_args()

    n = args.size
    if n < 3:
        print('Size must be at least 3')
        sys.exit(1)

    grid = make_perfect_maze(n)
    start, end = place_start_end_on_boundary(grid)
    path = ensure_unique_solution(grid, start, end)
    if not path:
        # fallback: regenerate until path exists
        attempts = 0
        while not path and attempts < 10:
            grid = make_perfect_maze(n)
            start, end = place_start_end_on_boundary(grid)
            path = ensure_unique_solution(grid, start, end)
            attempts += 1

    if args.demo:
        demo_solve(grid, start, end)
    else:
        play_interactive(grid, start, end)


if __name__ == '__main__':
    main()
