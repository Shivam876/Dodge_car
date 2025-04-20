import pygame
import random
import asyncio
import platform

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH = 400
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dodge Car Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GRAY = (128, 128, 128)

# Car settings
CAR_WIDTH = 50
CAR_HEIGHT = 80
car_x = WIDTH // 2 - CAR_WIDTH // 2
car_y = HEIGHT - CAR_HEIGHT - 20
car_speed = 5

# Obstacle settings
OBSTACLE_WIDTH = 50
OBSTACLE_HEIGHT = 50
obstacle_speed = 7
obstacles = []
spawn_rate = 60  # Frames between obstacle spawns
frame_count = 0

# Road settings
road_y = 0
road_speed = 10

# Score
score = 0
font = pygame.font.SysFont("arial", 30)

# Game state
game_over = False

def setup():
    global road_y, obstacles, car_x, score, game_over, frame_count
    road_y = 0
    obstacles = []
    car_x = WIDTH // 2 - CAR_WIDTH // 2
    score = 0
    game_over = False
    frame_count = 0
    pygame.display.set_caption("Dodge Car Game")

def draw_road():
    global road_y
    screen.fill(BLACK)
    # Draw road
    pygame.draw.rect(screen, GRAY, (50, road_y, WIDTH - 100, HEIGHT))
    pygame.draw.rect(screen, GRAY, (50, road_y - HEIGHT, WIDTH - 100, HEIGHT))
    # Draw lane markings
    for i in range(-HEIGHT, HEIGHT, 100):
        pygame.draw.rect(screen, WHITE, (WIDTH // 2 - 5, road_y + i, 10, 50))
        pygame.draw.rect(screen, WHITE, (WIDTH // 2 - 5, road_y + i - HEIGHT, 10, 50))
    road_y += road_speed
    if road_y >= HEIGHT:
        road_y = 0

def draw_car():
    pygame.draw.rect(screen, RED, (car_x, car_y, CAR_WIDTH, CAR_HEIGHT))

def spawn_obstacle():
    x = random.randint(50, WIDTH - 50 - OBSTACLE_WIDTH)
    obstacles.append(pygame.Rect(x, -OBSTACLE_HEIGHT, OBSTACLE_WIDTH, OBSTACLE_HEIGHT))

def update_obstacles():
    for obs in obstacles[:]:
        obs.y += obstacle_speed
        if obs.y > HEIGHT:
            obstacles.remove(obs)
        if obs.colliderect(pygame.Rect(car_x, car_y, CAR_WIDTH, CAR_HEIGHT)):
            return True  # Collision detected
    return False

def draw_obstacles():
    for obs in obstacles:
        pygame.draw.rect(screen, WHITE, obs)

def draw_score():
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

def draw_game_over():
    game_over_text = font.render(f"Game Over! Score: {score}", True, WHITE)
    restart_text = font.render("Press R to Restart", True, WHITE)
    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 20))
    screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 20))

async def main():
    global car_x, frame_count, score, game_over
    setup()
    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN and game_over:
                if event.key == pygame.K_r:
                    setup()

        if not game_over:
            # Handle input
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and car_x > 50:
                car_x -= car_speed
            if keys[pygame.K_RIGHT] and car_x < WIDTH - 50 - CAR_WIDTH:
                car_x += car_speed

            # Spawn obstacles
            frame_count += 1
            if frame_count % spawn_rate == 0:
                spawn_obstacle()

            # Update
            if update_obstacles():
                game_over = True
            score += 1

        # Draw
        draw_road()
        draw_car()
        draw_obstacles()
        draw_score()
        if game_over:
            draw_game_over()

        pygame.display.flip()
        await asyncio.sleep(1.0 / 60)  # 60 FPS

if platform.system() == "Emscripten":
    asyncio.ensure_future(main())
else:
    if __name__ == "__main__":
        asyncio.run(main())