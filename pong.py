import pygame
import random

# Initialize pygame
pygame.init()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (173, 216, 230)
ORANGE = (255, 165, 0)

# Screen dimensions
WIDTH, HEIGHT = 800, 600

# Create the screen and clock
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong Game")
clock = pygame.time.Clock()

# Font for displaying score
font = pygame.font.SysFont(None, 55)

class Paddle:
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.velocity = 10

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

    def move(self, up_key, down_key):
        keys = pygame.key.get_pressed()
        if keys[up_key]:
            self.y -= self.velocity
        if keys[down_key]:
            self.y += self.velocity

        # Ensure paddle stays within screen bounds
        if self.y < 0:
            self.y = 0
        if self.y + self.height > HEIGHT:
            self.y = HEIGHT - self.height

class Ball:
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.velocity_x = random.choice([-4, 4])
        self.velocity_y = random.choice([-4, 4])

    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

    def move(self):
        self.x += self.velocity_x
        self.y += self.velocity_y

        # Ball collision with top and bottom
        if self.y - self.radius <= 0 or self.y + self.radius >= HEIGHT:
            self.velocity_y = -self.velocity_y

def display_score(score_a, score_b):
    score_text_a = font.render(f"Player 1: {score_a}", True, BLUE)
    score_text_b = font.render(f"Player 2: {score_b}", True, ORANGE)
    screen.blit(score_text_a, (50, 10))
    screen.blit(score_text_b, (WIDTH - 200, 10))


def display_winner(winner):
    winner_text = font.render(f"{winner} Wins!", True, WHITE)
    text_rect = winner_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(winner_text, text_rect)
    pygame.display.flip()
    pygame.time.wait(2000)  # Wait for 2 seconds to display the winner

def main():
    paddle_a = Paddle(10, HEIGHT // 2 - 70, 15, 140, BLUE)
    paddle_b = Paddle(WIDTH - 25, HEIGHT // 2 - 70, 15, 140, ORANGE)
    ball = Ball(WIDTH // 2, HEIGHT // 2, 10, WHITE)

    score_a = 0
    score_b = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        screen.fill(BLACK)

        paddle_a.move(pygame.K_w, pygame.K_s)
        paddle_b.move(pygame.K_UP, pygame.K_DOWN)

        ball.move()

        # Ball collision with paddles
        if ball.x - ball.radius <= paddle_a.x + paddle_a.width and ball.y > paddle_a.y and ball.y < paddle_a.y + paddle_a.height or \
           ball.x + ball.radius >= paddle_b.x and ball.y > paddle_b.y and ball.y < paddle_b.y + paddle_b.height:
            ball.velocity_x = -ball.velocity_x

        # Ball out of bounds
        if ball.x - ball.radius <= 0:
            score_b += 1
            ball.x = WIDTH // 2
            ball.y = HEIGHT // 2
            ball.velocity_x = random.choice([-4, 4])
            ball.velocity_y = random.choice([-4, 4])

        if ball.x + ball.radius >= WIDTH:
            score_a += 1
            ball.x = WIDTH // 2
            ball.y = HEIGHT // 2
            ball.velocity_x = random.choice([-4, 4])
            ball.velocity_y = random.choice([-4, 4])

        # Check if any player has reached 3 points
        if score_a == 3:
            display_winner("Player 1")
            pygame.quit()
            return
        elif score_b == 3:
            display_winner("Player 2")
            pygame.quit()
            return

        paddle_a.draw()
        paddle_b.draw()
        ball.draw()

        display_score(score_a, score_b)

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()