import pygame
from random import choice

cell_size = 50
grid_width = 15
grid_height = 15
move_delay = 125

background = (18, 28, 38)
board_color = (31, 48, 57)
board_line = (38, 58, 66)
head_color = (112, 226, 126)
body_color = (55, 178, 94)
apple_color = (244, 91, 105)
text_color = (231, 243, 235)

directions = {
    pygame.K_UP: (0, -1),
    pygame.K_w: (0, -1),
    pygame.K_DOWN: (0, 1),
    pygame.K_s: (0, 1),
    pygame.K_LEFT: (-1, 0),
    pygame.K_a: (-1, 0),
    pygame.K_RIGHT: (1, 0),
    pygame.K_d: (1, 0),
}


def new_apple(snake):
    free_cells = [
        (x, y)
        for y in range(grid_height)
        for x in range(grid_width)
        if (x, y) not in snake
    ]
    return choice(free_cells) if free_cells else None


def reset_game():
    snake = [(7, 7), (6, 7), (5, 7)]
    return snake, (1, 0), [(1, 0)], new_apple(snake), 0, False


pygame.init()
pygame.display.set_caption("Snake")
screen = pygame.display.set_mode((grid_width * cell_size, grid_height * cell_size))
clock = pygame.time.Clock()
font = pygame.font.Font(None, 32)
large_font = pygame.font.Font(None, 58)
snake, direction, direction_queue, apple_position, score, game_over = reset_game()
previous_snake = snake[:]
time_since_move = 0
running = True

while running:
    elapsed = clock.tick(60)
    time_since_move += elapsed

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if game_over and event.key in (pygame.K_r, pygame.K_RETURN, pygame.K_SPACE):
                snake, direction, direction_queue, apple_position, score, game_over = reset_game()
                previous_snake = snake[:]
                time_since_move = 0
            elif event.key in directions and not game_over:
                new_direction = directions[event.key]
                last_direction = direction_queue[-1]
                if new_direction != (-last_direction[0], -last_direction[1]) and new_direction != last_direction:
                    direction_queue.append(new_direction)

    while time_since_move >= move_delay and not game_over:
        time_since_move -= move_delay
        previous_snake = snake[:]
        if len(direction_queue) > 1:
            direction_queue.pop(0)
        direction = direction_queue[0]
        head_x, head_y = snake[0]
        new_head = (head_x + direction[0], head_y + direction[1])
        hits_wall = not (0 <= new_head[0] < grid_width and 0 <= new_head[1] < grid_height)
        hits_body = new_head in snake[:-1]
        if hits_wall or hits_body:
            game_over = True
            break

        snake.insert(0, new_head)
        if new_head == apple_position:
            score += 1
            apple_position = new_apple(snake)
        else:
            snake.pop()

    screen.fill(background)
    for y in range(grid_height):
        for x in range(grid_width):
            rect = pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size)
            pygame.draw.rect(screen, board_color, rect)
            pygame.draw.rect(screen, board_line, rect, 1)

    if apple_position is not None:
        apple_center = (apple_position[0] * cell_size + cell_size // 2,
                        apple_position[1] * cell_size + cell_size // 2)
        pygame.draw.circle(screen, (255, 150, 130), apple_center, cell_size // 3 + 2)
        pygame.draw.circle(screen, apple_color, apple_center, cell_size // 3)

    interpolation = min(1, time_since_move / move_delay)
    for index, (x, y) in enumerate(snake):
        old_x, old_y = previous_snake[min(index, len(previous_snake) - 1)]
        draw_x = (old_x + (x - old_x) * interpolation) * cell_size
        draw_y = (old_y + (y - old_y) * interpolation) * cell_size
        inset = 5 if index == 0 else 7
        rect = pygame.Rect(draw_x + inset, draw_y + inset,
                           cell_size - inset * 2, cell_size - inset * 2)
        pygame.draw.rect(screen, head_color if index == 0 else body_color, rect, border_radius=10)

    score_surface = font.render(f"SCORE  {score:02d}", True, text_color)
    screen.blit(score_surface, (14, 12))
    if game_over:
        message = large_font.render("GAME OVER", True, text_color)
        prompt = font.render("R, Entree ou Espace pour rejouer", True, text_color)
        screen.blit(message, message.get_rect(center=screen.get_rect().center))
        screen.blit(prompt, prompt.get_rect(center=(screen.get_rect().centerx, screen.get_rect().centery + 45)))

    pygame.display.flip()

pygame.quit()