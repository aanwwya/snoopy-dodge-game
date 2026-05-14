import pygame
import time
import random

pygame.init()
pygame.font.init()

# ---------------- SCREEN ----------------
WIDTH, HEIGHT = 1000, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snoopy Duo Dodge")

# ---------------- IMAGES ----------------
BG = pygame.transform.scale(pygame.image.load("bg.jpeg"), (WIDTH, HEIGHT))

PLAYER_SIZE = (70, 70)
HEART_SIZE = (35, 35)

SNOOPY1 = pygame.transform.scale(
    pygame.image.load("snoopy1.png").convert_alpha(),
    PLAYER_SIZE
)

SNOOPY2 = pygame.transform.scale(
    pygame.image.load("snoopy2.png").convert_alpha(),
    PLAYER_SIZE
)

HEART = pygame.transform.scale(
    pygame.image.load("heart.png").convert_alpha(),
    HEART_SIZE
)

# ---------------- SETTINGS ----------------
PLAYER_VEL = 6
HEART_VEL = 5
FONT = pygame.font.SysFont("comicsans", 30)


def draw(p1, p2, hearts, elapsed_time):
    WIN.blit(BG, (0, 0))

    text = FONT.render(f"Time: {int(elapsed_time)}s", True, "white")
    WIN.blit(text, (10, 10))

    WIN.blit(SNOOPY1, (p1.x, p1.y))
    WIN.blit(SNOOPY2, (p2.x, p2.y))

    for h in hearts:
        WIN.blit(HEART, (h.x, h.y))

    pygame.display.update()


def game_over_screen():
    WIN.fill((0, 0, 0))

    msg = FONT.render("Oopsies, you lost 💔", True, "white")
    sub = FONT.render("Press ESC to exit", True, "gray")

    WIN.blit(msg, (WIDTH // 2 - msg.get_width() // 2,
                   HEIGHT // 2 - 40))
    WIN.blit(sub, (WIDTH // 2 - sub.get_width() // 2,
                   HEIGHT // 2 + 10))

    pygame.display.update()


def main():
    run = True
    clock = pygame.time.Clock()

    # ---------------- PLAYERS ----------------
    p1 = pygame.Rect(50, HEIGHT // 2, *PLAYER_SIZE)
    p2 = pygame.Rect(WIDTH - 120, HEIGHT // 2, *PLAYER_SIZE)

    hearts = []
    start_time = time.time()

    spawn_timer = 0
    spawn_delay = 1200

    hit = False

    while run:
        clock.tick(60)
        spawn_timer += clock.get_time()
        elapsed_time = time.time() - start_time

        # ---------------- SPAWN HEARTS (SAFE) ----------------
        if spawn_timer > spawn_delay:
            y = random.randint(0, HEIGHT - HEART_SIZE[1])

            # prevent spawning too close to players
            if abs(y - p1.y) > 120 and abs(y - p2.y) > 120:
                heart = pygame.Rect(-HEART_SIZE[0], y, *HEART_SIZE)
                hearts.append(heart)

            spawn_timer = 0
            spawn_delay = max(400, spawn_delay - 15)

        # ---------------- EVENTS ----------------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # ---------------- MOVEMENT ----------------
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w] and p1.y > 0:
            p1.y -= PLAYER_VEL
        if keys[pygame.K_s] and p1.y + PLAYER_SIZE[1] < HEIGHT:
            p1.y += PLAYER_VEL

        if keys[pygame.K_UP] and p2.y > 0:
            p2.y -= PLAYER_VEL
        if keys[pygame.K_DOWN] and p2.y + PLAYER_SIZE[1] < HEIGHT:
            p2.y += PLAYER_VEL

        # ---------------- HEART MOVEMENT ----------------
        for h in hearts[:]:
            h.x += HEART_VEL

            if h.x > WIDTH:
                hearts.remove(h)

        # ---------------- COLLISION CHECK ----------------
        for h in hearts:
            if h.colliderect(p1) or h.colliderect(p2):
                hit = True
                break

        # ---------------- GAME OVER ----------------
        if hit:
            game_over_screen()

            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        waiting = False
                        run = False

                keys = pygame.key.get_pressed()
                if keys[pygame.K_ESCAPE]:
                    waiting = False
                    run = False

            break

        draw(p1, p2, hearts, elapsed_time)

    pygame.quit()


if __name__ == "__main__":
    main()