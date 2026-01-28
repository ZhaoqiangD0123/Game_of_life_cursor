import pygame
import random
import sys
import os

# 常量定义
WIDTH, HEIGHT = 800, 600
CELL_SIZE = 20
COLS = WIDTH // CELL_SIZE
ROWS = HEIGHT // CELL_SIZE

# 颜色定义
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (50, 50, 50)

def count_neighbors(grid, x, y):
    """计算 (x, y) 周围 8 个格子的活细胞数量（环绕边界）"""
    count = 0
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx == 0 and dy == 0:
                continue
            nx = (x + dx) % ROWS
            ny = (y + dy) % COLS
            count += grid[nx][ny]
    return count

def update_grid(grid):
    """根据康威生命游戏4条规则返回新网格，不修改原网格"""
    new_grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]
    for r in range(ROWS):
        for c in range(COLS):
            neighbors = count_neighbors(grid, r, c)
            if grid[r][c] == 1:
                # 规则1和3：少于2或多于3个邻居会死亡
                if neighbors < 2 or neighbors > 3:
                    new_grid[r][c] = 0
                else:
                    new_grid[r][c] = 1
            else:
                # 规则4：正好3个邻居时复活
                if neighbors == 3:
                    new_grid[r][c] = 1
                else:
                    new_grid[r][c] = 0
    return new_grid

# 功能1: 进程初始为暂停状态, 左键控制暂停/继续
# 功能2: 空格暂停并保存这一帧, 顺序命名, 保存在 image_save 文件夹

def ensure_image_save_directory():
    folder = "image_save"
    if not os.path.exists(folder):
        os.makedirs(folder)
    return folder

def get_next_image_num(folder):
    files = [f for f in os.listdir(folder) if f.startswith('image_') and f.endswith('.png')]
    nums = []
    for f in files:
        try:
            num = int(f[6:-4])
            nums.append(num)
        except Exception:
            continue
    if nums:
        return max(nums) + 1
    else:
        return 1

# 初始化
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Conway's Game of Life - Evolution")
clock = pygame.time.Clock()

grid = [[random.choice([0, 1]) for _ in range(COLS)] for _ in range(ROWS)]

paused = True
running = True

while running:
    save_image = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # 鼠标左键控制暂停/继续
            paused = not paused

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if not paused:
                    paused = True
                    save_image = True

    # 绘制背景
    screen.fill(BLACK)

    # 绘制细胞格子
    for r in range(ROWS):
        for c in range(COLS):
            if grid[r][c] == 1:
                pygame.draw.rect(
                    screen,
                    WHITE,
                    (c * CELL_SIZE, r * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                )

    # 绘制深灰色网格线（横线和竖线）
    for x in range(0, WIDTH + 1, CELL_SIZE):
        pygame.draw.line(screen, GRAY, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT + 1, CELL_SIZE):
        pygame.draw.line(screen, GRAY, (0, y), (WIDTH, y))

    pygame.display.flip()
    clock.tick(10)

    # 保存图像（如果需要）
    if save_image:
        folder = ensure_image_save_directory()
        img_num = get_next_image_num(folder)
        img_path = os.path.join(folder, f"image_{img_num}.png")
        pygame.image.save(screen, img_path)
        print(f"已经保存: {img_path}")

    # 更新网格状态
    if not paused:
        grid = update_grid(grid)

pygame.quit()
sys.exit()