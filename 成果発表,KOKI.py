import pygame
import random

# Initialize Pygame
pygame.init()

# Initialize the mixer for sound
pygame.mixer.init()

# Constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
GOLD = (255, 215, 0)
PURPLE = (160, 32, 240)

# Load sounds
break_sound = pygame.mixer.Sound('break_sound.wav')

item_sound = pygame.mixer.Sound('ブロック崩し_2.mp3')  # 新たに追加する効果音ファイル

# Set up display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Block Breaker with Power-Ups")

# Paddle
PADDLE_WIDTH, PADDLE_HEIGHT = 100, 10
paddle = pygame.Rect(WIDTH // 2 - PADDLE_WIDTH // 2, HEIGHT - 40, PADDLE_WIDTH, PADDLE_HEIGHT)
paddle_speed = 10

# Ball
BALL_SIZE = 10
balls = [pygame.Rect(WIDTH // 2, HEIGHT // 2, BALL_SIZE, BALL_SIZE)]
ball_speed = [[5, -5]]

# Blocks
BLOCK_WIDTH, BLOCK_HEIGHT = 60, 20
blocks = []
block_colors = []
block_scores = []

for j in range(5):
    for i in range(10):
        blocks.append(pygame.Rect(10 + i * (BLOCK_WIDTH + 10), 10 + j * (BLOCK_HEIGHT + 10), BLOCK_WIDTH, BLOCK_HEIGHT))
        if j == 0:
            block_colors.append(YELLOW)
            block_scores.append(50)  # Score for top row
        elif j == 1:
            block_colors.append(GREEN)
            block_scores.append(40)  # Score for second row
        elif j == 2:
            block_colors.append(BLUE)
            block_scores.append(30)  # Score for third row
        elif j == 3:
            block_colors.append(PURPLE)
            block_scores.append(20)  # Score for fourth row
        else:
            block_colors.append(RED)
            block_scores.append(10)  # Score for fifth row

# Items
items = []
ITEM_SIZE = 15
ITEM_DROP_CHANCE = 0.2  # 20% chance to drop an item

# Score
score = 0
font = pygame.font.SysFont(None, 36)

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Paddle movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and paddle.left > 0:
        paddle.move_ip(-paddle_speed, 0)
    if keys[pygame.K_RIGHT] and paddle.right < WIDTH:
        paddle.move_ip(paddle_speed, 0)

    # Ball movement
    for i, ball in enumerate(balls):
        ball.move_ip(ball_speed[i])
        # Ball collision with walls
        if ball.left <= 0 or ball.right >= WIDTH:
            ball_speed[i][0] = -ball_speed[i][0]
        if ball.top <= 0:
            ball_speed[i][1] = -ball_speed[i][1]
        if ball.bottom >= HEIGHT:
            balls.pop(i)
            ball_speed.pop(i)
            if len(balls) == 0:
                # Play game over sound
                game_over_sound.play()
                running = False  # Game over

        # Ball collision with paddle
        if ball.colliderect(paddle):
            ball_speed[i][1] = -ball_speed[i][1]

        # Ball collision with blocks
        for j, block in enumerate(blocks[:]):
            if ball.colliderect(block):
                blocks.remove(block)
                block_colors.pop(j)
                score += block_scores.pop(j)  # Add score based on block's position
                ball_speed[i][1] = -ball_speed[i][1]
                # Play break sound
                break_sound.play()
                # Drop item with certain probability
                if random.random() < ITEM_DROP_CHANCE:
                    # Decide item type
                    if random.random() < 1/3:
                        item_color = GOLD  # 1/3 chance
                    else:
                        item_color = GREEN  # 2/3 chance
                    items.append((pygame.Rect(block.x, block.y, ITEM_SIZE, ITEM_SIZE), item_color))
                break

    # Item movement
    for item in items[:]:
        item_rect, item_color = item
        item_rect.move_ip(0, 5)
        if item_rect.top >= HEIGHT:
            items.remove(item)
        if item_rect.colliderect(paddle):
            items.remove(item)
            if item_color == GREEN:
                # Play item sound
                item_sound.play()
                # Add a new ball
                new_ball = pygame.Rect(paddle.centerx, paddle.centery - BALL_SIZE, BALL_SIZE, BALL_SIZE)
                balls.append(new_ball)
                ball_speed.append([random.choice([5, -5]), -5])
            elif item_color == GOLD:
                # Play item sound
                item_sound.play()
                # Multiply the number of balls by 3
                current_ball_count = len(balls)
                for _ in range(2 * current_ball_count):  # Adding 2 more balls for each existing one
                    new_ball = pygame.Rect(paddle.centerx, paddle.centery - BALL_SIZE, BALL_SIZE, BALL_SIZE)
                    balls.append(new_ball)
                    ball_speed.append([random.choice([5, -5]), random.choice([5, -5])])

    # Draw everything
    screen.fill(BLACK)
    pygame.draw.rect(screen, WHITE, paddle)
    for ball in balls:
        pygame.draw.ellipse(screen, RED, ball)
    for block, color in zip(blocks, block_colors):
        pygame.draw.rect(screen, color, block)
    for item_rect, item_color in items:
        pygame.draw.rect(screen, item_color, item_rect)

    # Display score
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
