import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
FPS = 60

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Coin Plane")
clock = pygame.time.Clock()

# Initialize font
font = pygame.font.SysFont(None, 36)

# Load assets
def load_image(path, width, height):
    try:
        image = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(image, (width, height))
    except pygame.error as e:
        print(f"Error loading image: {e}")
        return None

# Classes
class Player:
    def __init__(self, image_path):
        self.image = load_image(image_path, 50, 50)
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT - 60))
        self.bullets = []
        self.bullet_image = load_image("bullet.png", 10, 20)  # Replace with your bullet image

    def move(self, keys):
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= 5
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += 5

    def shoot(self):
        bullet_rect = self.bullet_image.get_rect(center=(self.rect.centerx, self.rect.top))
        self.bullets.append(bullet_rect)

    def draw(self):
        screen.blit(self.image, self.rect)
        for bullet in self.bullets:
            screen.blit(self.bullet_image, bullet)

class Zombie:
    def __init__(self, x, y, image_path):
        self.image = load_image(image_path, 50, 50)
        self.rect = self.image.get_rect(topleft=(x, y))

    def move(self):
        self.rect.y += 2

    def draw(self):
        screen.blit(self.image, self.rect)

# Functions
def load_background(image_path):
    try:
        return pygame.image.load(image_path).convert()
    except pygame.error as e:
        print(f"Error loading background image: {e}")
        return None

def main(background_path=None):
    player = Player("warplane.png")  # Replace with your player image
    zombies = []
    zombie_image_path = "coin.png"  # Replace with your zombie image
    score = 0
    spawn_timer = 0

    # Load background
    background = None
    if background_path:
        background = load_background(background_path)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.shoot()

        keys = pygame.key.get_pressed()
        player.move(keys)

        # Update bullets
        for bullet in player.bullets[:]:
            bullet.y -= 10
            if bullet.bottom < 0:
                player.bullets.remove(bullet)

        # Spawn zombies
        spawn_timer += 1
        if spawn_timer >= 60:
            spawn_timer = 0
            zombie_x = random.randint(0, WIDTH - 50)
            zombies.append(Zombie(zombie_x, -50, zombie_image_path))

        # Update zombies
        for zombie in zombies[:]:
            zombie.move()
            if zombie.rect.top > HEIGHT:
                zombies.remove(zombie)
            for bullet in player.bullets[:]:
                if zombie.rect.colliderect(bullet):
                    zombies.remove(zombie)
                    player.bullets.remove(bullet)
                    score += 1

        # Draw everything
        if background:
            screen.blit(background, (0, 0))
        else:
            screen.fill((255, 255, 255))

        player.draw()
        for zombie in zombies:
            zombie.draw()

        # Display score
        score_text = font.render(f"Score: {score}", True, (0, 0, 0))
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main("anh.jpg")  # Replace with your background image path
