import pygame

cell_size = 50
grid_width = 15
grid_height = 15

color1 = (170, 215, 81)
color2 = (162, 209, 73)

snake = [(7, 7), (6, 7), (5, 7)]
direction = (1, 0)


pygame.init()
pygame.display.set_caption("Snake")
screen = pygame.display.set_mode((grid_width*cell_size, grid_height*cell_size))
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Dessiner le damier
    for y in range(grid_height):
        for x in range(grid_width):
            if (x + y) % 2 == 0:
                color = color1
            else:
                color = color2
            rect = pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size)
            pygame.draw.rect(screen, color, rect)

    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_UP and direction != (0, 1):
            direction = (0, -1)
        elif event.key == pygame.K_DOWN and direction != (0, -1):
            direction = (0, 1)
        elif event.key == pygame.K_LEFT and direction != (1, 0):
            direction = (-1, 0)
        elif event.key == pygame.K_RIGHT and direction != (-1, 0):
            direction = (1, 0)
    
    head_x, head_y = snake[0]
    dx, dy = direction
    new_head = (head_x + dx, head_y + dy)
    snake.insert(0, new_head)
    snake.pop()

    for (x, y) in snake:
        rect = pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size)
        pygame.draw.rect(screen, (0, 100, 0), rect)  # vert foncé



    pygame.display.flip()
    clock.tick(7)

pygame.quit()