import pygame

cell_size = 50
grid_width = 15
grid_height = 15

pygame.init()
pygame.display.set_caption("Snake")
screen = pygame.display.set_mode((grid_width*cell_size, grid_height*cell_size))
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    screen.fill((0, 0, 0))
    # Dessiner les lignes verticales
    for x in range(grid_width + 1):
        pygame.draw.line(screen, (40, 40, 40), (x * cell_size, 0), (x * cell_size, grid_height * cell_size))

    # Dessiner les lignes horizontales
    for y in range(grid_height + 1):
        pygame.draw.line(screen, (40, 40, 40), (0, y * cell_size), (grid_width * cell_size, y * cell_size))
    pygame.display.flip()
    clock.tick(60)

pygame.quit()