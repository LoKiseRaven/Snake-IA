import pygame
from random import choice, random

cell_size = 50
grid_width = 15
grid_height = 15
move_delay = 100
restart_delay = 450
min_move_delay = 1
max_move_delay = 100
speed_step = 25

background = (18, 28, 38)
board_color = (31, 48, 57)
board_line = (38, 58, 66)
head_color = (112, 226, 126)
body_color = (55, 178, 94)
apple_color = (244, 91, 105)
text_color = (231, 243, 235)
muted_text = (157, 180, 177)

actions = (0, 1, 2)
turn_right = {
    (0, -1): (1, 0),
    (1, 0): (0, 1),
    (0, 1): (-1, 0),
    (-1, 0): (0, -1),
}
turn_left = {value: key for key, value in turn_right.items()}


def new_apple(snake):
    free_cells = [
        (x, y)
        for y in range(grid_height)
        for x in range(grid_width)
        if (x, y) not in snake
    ]
    return choice(free_cells) if free_cells else None


class SnakeGame:
    def reset(self):
        self.snake = [(7, 7), (6, 7), (5, 7)]
        self.direction = (1, 0)
        self.apple = new_apple(self.snake)
        self.score = 0
        self.steps = 0
        self.done = False

    def state(self):
        head_x, head_y = self.snake[0]
        checks = (self.direction, turn_right[self.direction], turn_left[self.direction])
        danger = tuple(
            self.is_danger((head_x + dx, head_y + dy))
            for dx, dy in checks
        )
        apple_dx = 0 if self.apple is None else self.apple[0] - head_x
        apple_dy = 0 if self.apple is None else self.apple[1] - head_y
        return danger + (
            apple_dx < 0,
            apple_dx > 0,
            apple_dy < 0,
            apple_dy > 0,
            self.direction == (1, 0),
            self.direction == (-1, 0),
            self.direction == (0, -1),
            self.direction == (0, 1),
        )

    def is_danger(self, position):
        x, y = position
        return (
            x < 0
            or x >= grid_width
            or y < 0
            or y >= grid_height
            or position in self.snake[:-1]
        )

    def step(self, action):
        if action == 1:
            self.direction = turn_right[self.direction]
        elif action == 2:
            self.direction = turn_left[self.direction]

        head_x, head_y = self.snake[0]
        new_head = (head_x + self.direction[0], head_y + self.direction[1])
        self.steps += 1
        if self.is_danger(new_head):
            self.done = True
            return -10, True, False

        self.snake.insert(0, new_head)
        ate_apple = new_head == self.apple
        if ate_apple:
            self.score += 1
            self.apple = new_apple(self.snake)
            reward = 10
        else:
            self.snake.pop()
            reward = -0.1

        if self.apple is None:
            self.done = True
        return reward, self.done, ate_apple


class QLearningAgent:
    def __init__(self):
        self.q_table = {}
        self.learning_rate = 0.15
        self.discount = 0.9
        self.epsilon = 1.0
        self.minimum_epsilon = 0.05
        self.episodes = 0

    def values(self, state):
        if state not in self.q_table:
            self.q_table[state] = [0.0, 0.0, 0.0]
        return self.q_table[state]

    def choose_action(self, state):
        values = self.values(state)
        if random() < self.epsilon:
            return choice(actions)
        best_value = max(values)
        best_actions = [action for action, value in enumerate(values) if value == best_value]
        return choice(best_actions)

    def learn(self, state, action, reward, next_state, done):
        values = self.values(state)
        next_best = 0 if done else max(self.values(next_state))
        target = reward + self.discount * next_best
        values[action] += self.learning_rate * (target - values[action])

    def end_episode(self):
        self.episodes += 1
        self.epsilon = max(self.minimum_epsilon, self.epsilon * 0.98)


def draw_game(screen, game, previous_snake, interpolation):
    screen.fill(background)
    for y in range(grid_height):
        for x in range(grid_width):
            rect = pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size)
            pygame.draw.rect(screen, board_color, rect)
            pygame.draw.rect(screen, board_line, rect, 1)

    if game.apple is not None:
        center = (game.apple[0] * cell_size + cell_size // 2,
                  game.apple[1] * cell_size + cell_size // 2)
        pygame.draw.circle(screen, (255, 150, 130), center, cell_size // 3 + 2)
        pygame.draw.circle(screen, apple_color, center, cell_size // 3)

    for index, (x, y) in enumerate(game.snake):
        old_x, old_y = previous_snake[min(index, len(previous_snake) - 1)]
        draw_x = (old_x + (x - old_x) * interpolation) * cell_size
        draw_y = (old_y + (y - old_y) * interpolation) * cell_size
        inset = 5 if index == 0 else 7
        rect = pygame.Rect(draw_x + inset, draw_y + inset,
                           cell_size - inset * 2, cell_size - inset * 2)
        pygame.draw.rect(screen, head_color if index == 0 else body_color,
                         rect, border_radius=10)


pygame.init()
pygame.display.set_caption("Snake IA - Q-learning")
screen = pygame.display.set_mode((grid_width * cell_size, grid_height * cell_size))
clock = pygame.time.Clock()
font = pygame.font.Font(None, 28)
game = SnakeGame()
game.reset()
agent = QLearningAgent()
previous_snake = game.snake[:]
time_since_move = 0
restart_timer = 0
running = True

while running:
    elapsed = clock.tick(60)
    time_since_move += elapsed
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                move_delay = max(min_move_delay, move_delay - speed_step)
            elif event.key == pygame.K_DOWN:
                move_delay = min(max_move_delay, move_delay + speed_step)

    if game.done:
        restart_timer += elapsed
        if restart_timer >= restart_delay:
            agent.end_episode()
            game.reset()
            previous_snake = game.snake[:]
            restart_timer = 0
            time_since_move = 0

    while time_since_move >= move_delay and not game.done:
        time_since_move -= move_delay
        previous_snake = game.snake[:]
        state = game.state()
        action = agent.choose_action(state)
        reward, _, _ = game.step(action)
        agent.learn(state, action, reward, game.state(), game.done)

    interpolation = min(1, time_since_move / move_delay)
    draw_game(screen, game, previous_snake, interpolation)
    score_surface = font.render(
        f"SCORE  {game.score:02d}    EPISODES  {agent.episodes:04d}",
        True,
        text_color,
    )
    exploration_surface = font.render(
        f"EXPLORATION  {agent.epsilon:.0%}", True, muted_text
    )
    speed_surface = font.render(
        f"VITESSE  {1000 / move_delay:.1f} mouvements/s", True, muted_text
    )
    screen.blit(score_surface, (14, 12))
    screen.blit(exploration_surface, (14, 40))
    screen.blit(speed_surface, (14, 68))
    if game.done:
        message = font.render("Mort - nouvelle partie automatique", True, text_color)
        screen.blit(message, message.get_rect(center=screen.get_rect().center))
    pygame.display.flip()

pygame.quit()