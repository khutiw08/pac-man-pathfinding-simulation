import sys
import random
import pygame
import heapq
from collections import deque
import asyncio   # 👈 required for pygbag

# ====== Config ======
ROWS, COLS = 25, 25
TILE = 15
GAP = 1
BORDER = 2

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
YELLOW = (251, 255, 0)
RED = (255, 0, 0)
CYAN = (0, 255, 255)
BUTTON_BLUE = (0, 60, 255)
BUTTON_HOVER = (255, 191, 0)

TITLE_TEXT = "Pac-Man Arena"
WIN_TEXT = "🎉 You Win!"
LOSE_TEXT = "💀 Game Over"
RESTART_TEXT = "Restart"

Tile_WALL = 1
Tile_PELLET = 0
Tile_EMPTY = 3

play_mode = "manual"

class Pos:
    def __init__(self, r, c):
        self.r = r
        self.c = c
    def copy(self):
        return Pos(self.r, self.c)
    def __iter__(self):
        return iter((self.r, self.c))
    def __repr__(self):
        return f"Pos(r={self.r}, c={self.c})"

def make_initial_maze():
    grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]
    for r in range(ROWS):
        for c in range(COLS):
            if r == 0 or r == ROWS - 1 or c == 0 or c == COLS - 1 or (r % 2 == 0 and c % 2 == 0):
                grid[r][c] = Tile_WALL
            else:
                grid[r][c] = Tile_PELLET
    pellet_count = sum(1 for r in range(ROWS) for c in range(COLS) if grid[r][c] == Tile_PELLET)
    return grid, pellet_count

def manhattan(a: Pos, b: Pos) -> int:
    return abs(a.r - b.r) + abs(a.c - b.c)

def astar_next_move(start: Pos, goal: Pos, maze):
    dirs = [(-1,0),(1,0),(0,-1),(0,1)]
    open_set = []
    
    nodes_explored = 0
    
    heapq.heappush(open_set, (0 + manhattan(start, goal), 0, (start.r, start.c), None))
    came_from = {}
    g_score = {(start.r, start.c): 0}
    while open_set:
        _, cost, current, parent = heapq.heappop(open_set)
        
        nodes_explored += 1 
        
        if current in came_from:
            continue
        came_from[current] = parent
        if current == (goal.r, goal.c):
            break
        for dr, dc in dirs:
            nr, nc = current[0] + dr, current[1] + dc
            if not (0 <= nr < ROWS and 0 <= nc < COLS):
                continue
            if maze[nr][nc] == Tile_WALL:
                continue
            new_cost = cost + 1
            if (nr, nc) not in g_score or new_cost < g_score[(nr, nc)]:
                g_score[(nr, nc)] = new_cost
                f_score = new_cost + manhattan(Pos(nr, nc), goal)
                heapq.heappush(open_set, (f_score, new_cost, (nr, nc), current))
    path = []
    node = (goal.r, goal.c)
    if node not in came_from:
        return start.copy(), nodes_explored 
    while node != (start.r, start.c):
        path.append(node)
        node = came_from[node]
    path.reverse()
    next_move =  Pos(path[0][0], path[0][1]) if path else start.copy()
    return next_move, nodes_explored

def bfs_next_move(start: Pos, goal: Pos, maze):
    dirs = [(-1,0),(1,0),(0,-1),(0,1)]
    queue = deque([start])
    parent = {(start.r, start.c): None}
    
    nodes_explored = 0   
    
    while queue:
        pos = queue.popleft()
        
        nodes_explored += 1
        
        if (pos.r, pos.c) == (goal.r, goal.c):
            break
        for dr, dc in dirs:
            nr, nc = pos.r + dr, pos.c + dc
            if not (0 <= nr < ROWS and 0 <= nc < COLS):
                continue
            if maze[nr][nc] != Tile_WALL and (nr, nc) not in parent:
                parent[(nr, nc)] = (pos.r, pos.c)
                queue.append(Pos(nr, nc))
    path = []
    node = (goal.r, goal.c)
    if node not in parent:
        return start.copy(), nodes_explored
    while node != (start.r, start.c):
        path.append(node)
        node = parent[node]
    path.reverse()
    next_move = Pos(path[0][0], path[0][1]) if path else start.copy()
    return next_move, nodes_explored

def find_nearest_pellet(pacman, maze):
    queue = deque([pacman])
    visited = {(pacman.r, pacman.c)}
    while queue:
        pos = queue.popleft()
        if maze[pos.r][pos.c] == Tile_PELLET:
            return Pos(pos.r, pos.c)
        for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
            nr, nc = pos.r + dr, pos.c + dc
            if 0 <= nr < ROWS and 0 <= nc < COLS and maze[nr][nc] != Tile_WALL and (nr, nc) not in visited:
                visited.add((nr, nc))
                queue.append(Pos(nr, nc))
    return pacman

def draw_maze(surface, maze, offset_x, offset_y):
    surface.fill(BLACK)
    maze_w = COLS * TILE + (COLS - 1) * GAP
    maze_h = ROWS * TILE + (ROWS - 1) * GAP
    pygame.draw.rect(surface, WHITE, (offset_x - BORDER, offset_y - BORDER, maze_w + 2*BORDER, maze_h + 2*BORDER), width=2)
    for r in range(ROWS):
        for c in range(COLS):
            x = offset_x + c * (TILE + GAP)
            y = offset_y + r * (TILE + GAP)
            if maze[r][c] == Tile_WALL:
                pygame.draw.rect(surface, BLUE, (x, y, TILE, TILE))
            elif maze[r][c] == Tile_PELLET:
                pygame.draw.rect(surface, BLACK, (x, y, TILE, TILE))
                pygame.draw.rect(surface, WHITE, (x+7, y+7, 5, 5))
            else:
                pygame.draw.rect(surface, BLACK, (x, y, TILE, TILE))

def draw_pacman(surface, pos: Pos, offset_x, offset_y):
    x = offset_x + pos.c * (TILE + GAP)
    y = offset_y + pos.r * (TILE + GAP)
    pygame.draw.circle(surface, YELLOW, (x + TILE//2, y + TILE//2), 9)

def draw_ghost(surface, pos: Pos, offset_x, offset_y, color):
    x = offset_x + pos.c * (TILE + GAP)
    y = offset_y + pos.r * (TILE + GAP)
    body_rect = pygame.Rect(x + 1, y + 1, 18, 18)
    pygame.draw.ellipse(surface, color, (body_rect.x, body_rect.y - 5, body_rect.w, body_rect.h))
    pygame.draw.rect(surface, color, (body_rect.x, body_rect.y + 4, body_rect.w, body_rect.h - 4))
    stripe_y = body_rect.bottom - 5
    pygame.draw.rect(surface, color, (body_rect.x, stripe_y, body_rect.w, 5))
    for i in range(3, body_rect.w, 6):
        pygame.draw.rect(surface, WHITE, (body_rect.x + i, stripe_y, 3, 5))

async def main():   # 👈 now async
    global play_mode
    pygame.init()
    pygame.display.set_caption("Pac-Man Arena")
    font_title = pygame.font.SysFont(None, 40)
    font_info = pygame.font.SysFont("Arial", 16, bold=False)

    font_overlay_h2 = pygame.font.SysFont(None, 48)
    font_button = pygame.font.SysFont(None, 32)

    maze_w = COLS * TILE + (COLS - 1) * GAP
    maze_h = ROWS * TILE + (ROWS - 1) * GAP
    top_margin = 80
    side_margin = 20
    width = maze_w + side_margin * 2
    height = top_margin + maze_h + 20
    screen = pygame.display.set_mode((width, height))

    lives, score, gameOver, win = 3, 0, False, False
    pacman = Pos(1, 1)
    ghosts = [Pos(6, 6), Pos(6, 7)]
    maze, totalPellets = make_initial_maze()

    overlay_rect = pygame.Rect(width//2 - 200, height//2 - 100, 400, 200)
    button_rect = pygame.Rect(overlay_rect.centerx - 80, overlay_rect.bottom - 70, 160, 40)

    GHOST_MOVE_EVENT_BFS = pygame.USEREVENT + 1
    GHOST_MOVE_EVENT_ASTAR = pygame.USEREVENT + 2
    PACMAN_MOVE_EVENT_AI = pygame.USEREVENT + 3

    pygame.time.set_timer(GHOST_MOVE_EVENT_BFS, 500)
    pygame.time.set_timer(GHOST_MOVE_EVENT_ASTAR, 700)
    if play_mode == "ai":
        pygame.time.set_timer(PACMAN_MOVE_EVENT_AI, 200)

    clock = pygame.time.Clock()

    def restart_game():
        nonlocal lives, score, gameOver, win, pacman, ghosts, maze
        lives, score, gameOver, win = 3, 0, False, False
        pacman = Pos(1, 1)
        ghosts = [Pos(6, 6), Pos(6, 7)]
        maze, _ = make_initial_maze()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Spacebar toggle
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and not gameOver:
                if play_mode == "manual":
                    play_mode = "ai"
                    pygame.time.set_timer(PACMAN_MOVE_EVENT_AI, 200)
                else:
                    play_mode = "manual"
                    pygame.time.set_timer(PACMAN_MOVE_EVENT_AI, 0)

            if play_mode == "manual" and event.type == pygame.KEYDOWN and not gameOver:
                next_pos = pacman.copy()
                if event.key == pygame.K_UP: next_pos.r -= 1
                elif event.key == pygame.K_DOWN: next_pos.r += 1
                elif event.key == pygame.K_LEFT: next_pos.c -= 1
                elif event.key == pygame.K_RIGHT: next_pos.c += 1
                if maze[next_pos.r][next_pos.c] != Tile_WALL:
                    if maze[next_pos.r][next_pos.c] == Tile_PELLET:
                        score += 1
                        maze[next_pos.r][next_pos.c] = Tile_EMPTY
                    pacman = next_pos

            if event.type == PACMAN_MOVE_EVENT_AI and not gameOver:
                target = find_nearest_pellet(pacman, maze)
                # pacman = bfs_next_move(pacman, target, maze)
                bfs_move, bfs_nodes = bfs_next_move(pacman, target, maze)
                astar_move, astar_nodes = astar_next_move(pacman, target, maze)

                # 👇 comparison
                if bfs_nodes > 0:
                    reduction = ((bfs_nodes - astar_nodes) / bfs_nodes) * 100
                    print(f"BFS: {bfs_nodes}, A*: {astar_nodes}, Reduction: {reduction:.2f}%")

                pacman = bfs_move  # keep same behavior
                if maze[pacman.r][pacman.c] == Tile_PELLET:
                    score += 1
                    maze[pacman.r][pacman.c] = Tile_EMPTY

            if event.type == pygame.KEYDOWN and gameOver and event.key == pygame.K_r:
                restart_game()
            if event.type == pygame.MOUSEBUTTONDOWN and gameOver and button_rect.collidepoint(event.pos):
                restart_game()

            if event.type == GHOST_MOVE_EVENT_BFS and not gameOver:
                next_pos, _ = bfs_next_move(ghosts[0], pacman, maze)
                ghosts[0]= next_pos
            if event.type == GHOST_MOVE_EVENT_ASTAR and not gameOver:
                next_pos, _ = astar_next_move(ghosts[1], pacman, maze)
                ghosts[1] = next_pos

        if not gameOver:
            for g in ghosts:
                if g.r == pacman.r and g.c == pacman.c:
                    lives -= 1
                    if lives <= 0:
                        gameOver = True
                    pacman = Pos(1, 1)
                    break
            if score >= totalPellets:
                win, gameOver = True, True

        screen.fill(BLACK)
        screen.blit(font_title.render(TITLE_TEXT, True, WHITE), (width//2 - 100, 10))
        offset_x, offset_y = side_margin, top_margin
        draw_maze(screen, maze, offset_x, offset_y)
        draw_pacman(screen, pacman, offset_x, offset_y)
        draw_ghost(screen, ghosts[0], offset_x, offset_y, RED)
        draw_ghost(screen, ghosts[1], offset_x, offset_y, CYAN)

        # HUD
        mode_text = font_info.render(f"Mode: {play_mode.upper()}", True, WHITE)
        screen.blit(mode_text, (20, 45))

        # Prevent overlap
        mode_width = mode_text.get_width()
        score_text = font_info.render(f"Score: {score}    Lives: {lives}", True, WHITE)
        screen.blit(score_text, (30 + mode_width, 45))

        if gameOver:
            overlay_surf = pygame.Surface((overlay_rect.w, overlay_rect.h), pygame.SRCALPHA)
            overlay_surf.fill((0, 0, 0, int(0.85 * 255)))
            screen.blit(overlay_surf, overlay_rect.topleft)
            result_text = WIN_TEXT if win else LOSE_TEXT
            screen.blit(font_overlay_h2.render(result_text, True, WHITE), (overlay_rect.centerx - 80, overlay_rect.y + 25))
            mouse_pos = pygame.mouse.get_pos()
            btn_color = BUTTON_HOVER if button_rect.collidepoint(mouse_pos) else BUTTON_BLUE
            pygame.draw.rect(screen, btn_color, button_rect, border_radius=5)
            screen.blit(font_button.render(RESTART_TEXT, True, BLACK), (button_rect.centerx - 40, button_rect.centery - 10))

        pygame.display.flip()
        clock.tick(60)

        await asyncio.sleep(0)   # 👈 yield to browser

    pygame.quit()
    return   # 👈 instead of sys.exit()

if __name__ == "__main__":
    asyncio.run(main())   # 👈 run async loop
