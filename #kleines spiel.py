#kleines spiel
import os
import pygame
import random

class Settings:
    WINDOW_WIDTH = 600
    WINDOW_HEIGHT = 700
    FPS = 60
    FILE_PATH = os.path.dirname(os.path.abspath(__file__))
    IMAGE_PATH = os.path.join(FILE_PATH, "images")

class Obstacle:
    def __init__(self, y_pos, speed_multiplier=1):
        self.image = pygame.image.load(os.path.join(Settings.IMAGE_PATH, "stein01.png")).convert()
        self.image.set_colorkey("white")
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect(midleft=(0, y_pos))
        self.speed = random.randint(3, 6) * speed_multiplier

        if y_pos < Settings.WINDOW_HEIGHT // 2:
            self.direction = 1  # Von links nach rechts
            self.rect.left = 0
        else:
            self.direction = -1  # Von rechts nach links
            self.rect.right = Settings.WINDOW_WIDTH

    def move(self):
        self.rect.x += self.speed * self.direction
        if self.rect.right < 0:  # Wenn links aus dem Bildschirm
            self.rect.left = Settings.WINDOW_WIDTH
        elif self.rect.left > Settings.WINDOW_WIDTH:  # Wenn rechts aus dem Bildschirm
            self.rect.right = 0

class Bunny:
    def __init__(self):
        self.image = pygame.image.load(os.path.join(Settings.IMAGE_PATH, "bunny.png")).convert_alpha()
        self.image.set_colorkey("white")
        self.image = pygame.transform.scale(self.image, (55, 55))
        self.rect = self.image.get_rect(midbottom=(Settings.WINDOW_WIDTH // 2, Settings.WINDOW_HEIGHT - 10))
        self.speed = 5

    def move(self, keys):
        current_speed = self.speed
        if keys[pygame.K_SPACE]:  # Beschleunigung mit der Leertaste
            current_speed *= 2

        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= current_speed
        if keys[pygame.K_DOWN] and self.rect.bottom < Settings.WINDOW_HEIGHT:
            self.rect.y += current_speed
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= current_speed
        if keys[pygame.K_RIGHT] and self.rect.right < Settings.WINDOW_WIDTH:
            self.rect.x += current_speed

def draw_text(screen, text, size, x, y, color=(255, 255, 255)):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)

def main():
    pygame.init()

    screen = pygame.display.set_mode((Settings.WINDOW_WIDTH, Settings.WINDOW_HEIGHT))
    pygame.display.set_caption("Bunny Game")
    clock = pygame.time.Clock()

    background_image = pygame.image.load(os.path.join(Settings.IMAGE_PATH, "background03.jpg")).convert()
    background_image = pygame.transform.scale(background_image, (Settings.WINDOW_WIDTH, Settings.WINDOW_HEIGHT))

    bunny = Bunny()
    speed_multiplier = 1
    obstacles = [Obstacle(y_pos, speed_multiplier) for y_pos in range(100, Settings.WINDOW_HEIGHT - 100, 150)]

    paused = False
    running = True
    score = 0
    round_count = 1
    esc_pressed = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = not paused
                if event.key == pygame.K_ESCAPE:
                    esc_pressed += 1
                    if esc_pressed == 2:
                        running = False

        if paused:
            screen.blit(background_image, (0, 0))
            draw_text(screen, "PAUSE", 50, Settings.WINDOW_WIDTH // 2, Settings.WINDOW_HEIGHT // 2, color=(200, 200, 200))
            pygame.display.flip()
            continue

        keys = pygame.key.get_pressed()
        bunny.move(keys)

        for obstacle in obstacles:
            obstacle.move()
            if bunny.rect.colliderect(obstacle.rect):
                print("Collision! Restarting position.")
                bunny.rect.midbottom = (Settings.WINDOW_WIDTH // 2, Settings.WINDOW_HEIGHT - 10)

        if bunny.rect.top <= 0:
            print("You Win!")
            score += 10
            round_count += 1
            speed_multiplier += 0.5
            bunny.rect.midbottom = (Settings.WINDOW_WIDTH // 2, Settings.WINDOW_HEIGHT - 10)
            obstacles = [Obstacle(y_pos, speed_multiplier) for y_pos in range(100, Settings.WINDOW_HEIGHT - 100, 150)]

        screen.blit(background_image, (0, 0))
        screen.blit(bunny.image, bunny.rect.topleft)

        for obstacle in obstacles:
            screen.blit(obstacle.image, obstacle.rect.topleft)

        draw_text(screen, f"Score: {score}", 30, 80, 30)
        draw_text(screen, f"Round: {round_count}", 30, 80, 60)

        pygame.display.flip()
        clock.tick(Settings.FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
