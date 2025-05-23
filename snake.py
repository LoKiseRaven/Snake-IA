import pygame
from random import randint

cell_size = 50
grid_width = 15
grid_height = 15

grass_color1 = (170, 215, 81)
grass_color2 = (162, 209, 73)

head_color = (0, 200, 0)
body_color = (0, 175, 0)

snake = [(7, 7), (6, 7), (5, 7)]
direction = (1, 0)

apple_exists = False
apple_position = (0, 0)

pygame.init()
pygame.display.set_caption("Snake")
screen = pygame.display.set_mode((grid_width*cell_size, grid_height*cell_size))
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    for y in range(grid_height):
        for x in range(grid_width):
            if (x + y) % 2 == 0:
                color = grass_color1
            else:
                color = grass_color2
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


    if not apple_exists:
        while True:
            apple_x = randint(0, grid_width - 1)
            apple_y = randint(0, grid_height - 1)
            if (apple_x, apple_y) not in snake:
                apple_position = (apple_x, apple_y)
                break
        apple_exists = True
    
    rect = pygame.Rect(apple_position[0] * cell_size, apple_position[1] * cell_size, cell_size, cell_size)
    pygame.draw.rect(screen, (255, 0, 0), rect)

    cpt = 0
    for (x, y) in snake:
        if cpt == 0:
            color = head_color
        else:
            color = body_color
        rect = pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size)
        pygame.draw.rect(screen, color, rect)
        cpt += 1

    if snake[0] == apple_position:
        snake.append(snake[-1])
        apple_exists = False

    pygame.display.flip()
    clock.tick(7)

pygame.quit()