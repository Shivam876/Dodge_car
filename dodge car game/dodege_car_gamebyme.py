from gzip import READ
import pygame
import random
# import os
# import time

# Initialize pygame
pygame.init()

# Game window
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Realistic Dodge Car Game")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Load images
def load_image(name, scale=1):
    try:
        image = pygame.image.load(name)
        if scale != 1:
            size = image.get_size()
            image = pygame.transform.scale(image, (int(size[0] * scale), int(size[1] * scale)))
        return image
    except:
        # Fallback rectangle if image fails to load
        surf = pygame.Surface((50, 80))
        surf.fill(BLUE if "player" in name else READ)
        return surf

# Try to load car images (replace with your own paths)
player_img = load_image("img/simple-travel-car-top_view.png", 0.1)
obstacle_imgs = [
    load_image("img/BuickerB.png", 1.5),
    load_image("img/JeepB.png", 1.5),
    load_image("img/simple-travel-car-top_view - Copy.png", 0.1),
    load_image("img/trashmaster.png", 0.9)
]

# Player car
player_width = player_img.get_width()
player_height = player_img.get_height()
player_x = WIDTH // 2 - player_width // 2
player_y = HEIGHT - player_height - 20
player_speed = 8

# Road settings
road_width = 500
road_x = (WIDTH - road_width) // 2
lane_width = road_width // 3
road_marker_height = 50
road_marker_width = 10

# Obstacles
obstacles = []
obstacle_speed = 5
obstacle_frequency = 60  # lower means more frequent

# Score
score = 0
high_score = 0
font = pygame.font.SysFont('Arial', 30)
big_font = pygame.font.SysFont('Arial', 50)

# Game clock
clock = pygame.time.Clock()
FPS = 60

# Road animation
road_marker_move_y = 0

def draw_road():
    # Draw grass
    screen.fill(GREEN)
    
    # Draw road
    pygame.draw.rect(screen, GRAY, [road_x, 0, road_width, HEIGHT])
    
    # Draw road markers
    road_marker_y = road_marker_move_y
    while road_marker_y < HEIGHT:
        pygame.draw.rect(screen, YELLOW, [WIDTH // 2 - road_marker_width // 2, road_marker_y, road_marker_width, road_marker_height])
        road_marker_y += road_marker_height * 2
    
    # Draw left and right road edges
    pygame.draw.rect(screen, YELLOW, [road_x, 0, road_marker_width, HEIGHT])
    pygame.draw.rect(screen, YELLOW, [road_x + road_width - road_marker_width, 0, road_marker_width, HEIGHT])
    
    # Draw lanes
    pygame.draw.rect(screen, WHITE, [road_x + lane_width, 0, road_marker_width, HEIGHT], 1)
    pygame.draw.rect(screen, WHITE, [road_x + lane_width * 2, 0, road_marker_width, HEIGHT], 1)

def draw_player(x, y):
    screen.blit(player_img, (x, y))

def create_obstacle():
    img = random.choice(obstacle_imgs)
    width = img.get_width()
    height = img.get_height()
    
    # Choose lane (0 = left, 1 = middle, 2 = right)
    lane = random.randint(0, 2)
    x = road_x + lane * lane_width + (lane_width - width) // 2
    
    return [x, -height, width, height, img]

def draw_obstacle(obstacle):
    screen.blit(obstacle[4], (obstacle[0], obstacle[1]))

def display_score(score, high_score):
    score_text = font.render(f"Score: {score}", True, WHITE)
    high_text = font.render(f"High Score: {high_score}", True, WHITE)
    screen.blit(score_text, (20, 20))
    screen.blit(high_text, (20, 60))

def check_collision(player_x, player_y, obstacle_x, obstacle_y, obstacle_w, obstacle_h):
    if (player_y < obstacle_y + obstacle_h and
        player_y + player_height > obstacle_y and
        player_x < obstacle_x + obstacle_w and
        player_x + player_width > obstacle_x):
        return True
    return False

# Game loop
running = True
game_over = False
game_started = False

while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and game_over:
                # Reset game
                game_over = False
                score = 0
                obstacles = []
                player_x = WIDTH // 2 - player_width // 2
                obstacle_speed = 5
                obstacle_frequency = 60
            if event.key == pygame.K_RETURN and not game_started:
                game_started = True

    if game_started and not game_over:
        # Player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > road_x:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < road_x + road_width - player_width:
            player_x += player_speed

        # Road animation
        road_marker_move_y += obstacle_speed * 0.5
        if road_marker_move_y >= road_marker_height * 2:
            road_marker_move_y = 0

        # Create obstacles
        if random.randrange(0, obstacle_frequency) == 0:
            obstacles.append(create_obstacle())

        # Move obstacles and check for collisions
        for obstacle in obstacles[:]:
            obstacle[1] += obstacle_speed
            
            if check_collision(player_x, player_y, obstacle[0], obstacle[1], obstacle[2], obstacle[3]):
                game_over = True
                if score > high_score:
                    high_score = score
            
            if obstacle[1] > HEIGHT:
                obstacles.remove(obstacle)
                score += 1
                
                # Increase difficulty
                if score % 10 == 0:
                    obstacle_speed += 0.5
                    if obstacle_frequency > 20:
                        obstacle_frequency -= 2

    # Drawing
    draw_road()
    
    if game_started:
        if not game_over:
            draw_player(player_x, player_y)
            for obstacle in obstacles:
                draw_obstacle(obstacle)
            display_score(score, high_score)
        else:
            game_over_text = big_font.render("GAME OVER", True, WHITE)
            restart_text = font.render("Press R to restart", True, WHITE)
            final_score_text = font.render(f"Final Score: {score}", True, WHITE)
            screen.blit(game_over_text, (WIDTH//2 - game_over_text.get_width()//2, HEIGHT//2 - 100))
            screen.blit(final_score_text, (WIDTH//2 - final_score_text.get_width()//2, HEIGHT//2))
            screen.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, HEIGHT//2 + 50))
    else:
        title_text = big_font.render("DODGE CAR GAME", True, WHITE)
        start_text = font.render("Press ENTER to start", True, WHITE)
        controls_text = font.render("Use LEFT and RIGHT arrow keys to move", True, WHITE)
        screen.blit(title_text, (WIDTH//2 - title_text.get_width()//2, HEIGHT//2 - 100))
        screen.blit(start_text, (WIDTH//2 - start_text.get_width()//2, HEIGHT//2))
        screen.blit(controls_text, (WIDTH//2 - controls_text.get_width()//2, HEIGHT//2 + 50))
        draw_player(WIDTH//2 - player_width//2, HEIGHT//2 + 100)

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()