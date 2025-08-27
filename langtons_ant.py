import sys

try:
    import pygame
except ImportError:
    print("Please install pygame first: pip install pygame")
    sys.exit(1)

rule = input("Rule (RL or LR): ").strip().upper()
if rule not in ("RL", "LR"):
    print("Invalid rule; using RL.")
    rule = "RL"

try:
    total_steps = int(input("Number of steps: ").strip())
    if total_steps <= 0:
        raise ValueError
except Exception:
    print("Invalid number; using 11000.")
    total_steps = 11000

# Directions: 0=Up, 1=Right, 2=Down, 3=Left
TURN = {"L": -1, "R": 1}


CELL = 6                     # pixel size of one cell (change if you want bigger/smaller squares)
W, H = 900, 900              # window size
BG = (240, 240, 240)         # background color (white-ish)
BLACK = (30, 30, 30)         # color for black cells
ANT = (200, 40, 40)          # ant color (red)
FPS = 60                     # max frames per second
STEPS_PER_FRAME = 50         # how many simulation steps to run per frame (speed-up)

pygame.init()
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Langton's Ant (RL/LR) - Pygame (close window to quit)")
clock = pygame.time.Clock()

cols = W // CELL
rows = H // CELL
half_cols = cols // 2
half_rows = rows // 2

# Grid state: store ONLY black cells (x, y) in a set. White cells are implicit.
black = set()

# Ant state
x, y = 0, 0    # grid coordinates (integers)
d = 0          # facing Up

# Rule mapping:
#   For "RL": white -> R, black -> L
#   For "LR": white -> L, black -> R
white_turn = rule[0]  # 'R' or 'L'
black_turn = rule[1]  # 'R' or 'L'

def is_black(cx, cy):
    return (cx, cy) in black

def flip(cx, cy):
    if (cx, cy) in black:
        black.remove((cx, cy))   # become white
    else:
        black.add((cx, cy))      # become black

def step():
    """Perform ONE Langton step using current rule and ant state."""
    global x, y, d
    on_black = is_black(x, y)

    # turn
    t = black_turn if on_black else white_turn
    d = (d + TURN[t]) % 4

    # flip color
    flip(x, y)

    # move forward 1 cell
    if d == 0:      # Up
        y -= 1
    elif d == 1:    # Right
        x += 1
    elif d == 2:    # Down
        y += 1
    else:           # Left
        x -= 1

def draw():
    screen.fill(BG)

    # Visible bounds (centered on ant)
    min_x = x - half_cols
    min_y = y - half_rows
    max_x = min_x + cols - 1
    max_y = min_y + rows - 1

    # Draw black cells that fall inside the current view
    # Convert grid (gx,gy) -> screen pixels
    for (gx, gy) in black:
        if min_x <= gx <= max_x and min_y <= gy <= max_y:
            sx = (gx - min_x) * CELL
            sy = (gy - min_y) * CELL
            pygame.draw.rect(screen, BLACK, (sx, sy, CELL, CELL))

    # Draw the ant as a red square at its cell
    ax = (x - min_x) * CELL
    ay = (y - min_y) * CELL
    pygame.draw.rect(screen, ANT, (ax, ay, CELL, CELL))

    pygame.display.flip()

steps_done = 0
running = True
while running:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if steps_done < total_steps:
        
        to_run = min(STEPS_PER_FRAME, total_steps - steps_done)
        for _ in range(to_run):
            step()
        steps_done += to_run

    # draw current frame
    draw()
    clock.tick(FPS)

pygame.quit()
