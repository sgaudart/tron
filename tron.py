import pygame
import sys

# --- Configuration ---
TILE_SIZE = 20
PLAYER_COLOR = (0, 150, 255)
TRACE_COLOR = (0, 255, 255)
BG_COLOR = (0, 0, 0)
WALL_COLOR = (100, 100, 100)
NORMAL_SPEED = 5
BOOSTED_SPEED = 2
MAX_POWER_TIME = 5.0  # secondes

# --- Charger la carte depuis un fichier texte ---
def charger_carte(nom_fichier):
    with open(nom_fichier, "r") as f:
        lignes = [line.rstrip("\n") for line in f]
    return [[1 if char == '#' else 0 for char in ligne] for ligne in lignes]

game_map = charger_carte("carte.txt")
MAP_HEIGHT = len(game_map)
MAP_WIDTH = len(game_map[0])

# --- Initialisation Pygame ---
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tron - Carte depuis fichier")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 28)

# --- Joueur ---
player_x, player_y = 1, 1  # Départ dans un espace vide
trace = set()
move_timer = 0
game_over = False

# --- Pouvoirs ---
invincible = False
boosted = False
invincibility_time_left = MAX_POWER_TIME
boost_time_left = MAX_POWER_TIME

last_time = pygame.time.get_ticks()

# --- Boucle principale ---
running = True
while running:
    dt = (pygame.time.get_ticks() - last_time) / 1000.0
    last_time = pygame.time.get_ticks()

    screen.fill(BG_COLOR)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    # --- Activation des pouvoirs ---
    if keys[pygame.K_i] and invincibility_time_left > 0:
        invincible = True
    else:
        invincible = False

    if keys[pygame.K_SPACE] and boost_time_left > 0:
        boosted = True
    else:
        boosted = False

    # --- Consommation des pouvoirs ---
    if invincible:
        invincibility_time_left -= dt
        if invincibility_time_left <= 0:
            invincibility_time_left = 0
            invincible = False

    if boosted:
        boost_time_left -= dt
        if boost_time_left <= 0:
            boost_time_left = 0
            boosted = False

    # --- Déplacement ---
    current_speed = BOOSTED_SPEED if boosted else NORMAL_SPEED

    if not game_over:
        move_timer += 1
        if move_timer >= current_speed:
            dx, dy = 0, 0
            if keys[pygame.K_LEFT]:
                dx = -1
            elif keys[pygame.K_RIGHT]:
                dx = 1
            elif keys[pygame.K_UP]:
                dy = -1
            elif keys[pygame.K_DOWN]:
                dy = 1

            if dx != 0 or dy != 0:
                new_x = player_x + dx
                new_y = player_y + dy

                if 0 <= new_x < MAP_WIDTH and 0 <= new_y < MAP_HEIGHT:
                    is_wall = game_map[new_y][new_x] == 1
                    hits_trace = (new_x, new_y) in trace

                    if (is_wall or hits_trace) and not invincible:
                        game_over = True
                    else:
                        trace.add((player_x, player_y))
                        player_x = new_x
                        player_y = new_y

            move_timer = 0

    # --- Caméra centrée ---
    cam_x = player_x * TILE_SIZE - SCREEN_WIDTH // 2
    cam_y = player_y * TILE_SIZE - SCREEN_HEIGHT // 2

    # --- Affichage des murs ---
    for y in range(MAP_HEIGHT):
        for x in range(MAP_WIDTH):
            if game_map[y][x] == 1:
                rect = pygame.Rect(x * TILE_SIZE - cam_x, y * TILE_SIZE - cam_y, TILE_SIZE, TILE_SIZE)
                pygame.draw.rect(screen, WALL_COLOR, rect)

    # --- Affichage des traces ---
    for (x, y) in trace:
        rect = pygame.Rect(x * TILE_SIZE - cam_x, y * TILE_SIZE - cam_y, TILE_SIZE, TILE_SIZE)
        pygame.draw.rect(screen, TRACE_COLOR, rect)

    # --- Affichage du joueur ---
    if not game_over:
        color = PLAYER_COLOR
        if invincible:
            color = (255, 255, 0)
        elif boosted:
            color = (255, 100, 255)
        rect = pygame.Rect(player_x * TILE_SIZE - cam_x, player_y * TILE_SIZE - cam_y, TILE_SIZE, TILE_SIZE)
        pygame.draw.rect(screen, color, rect)

    # --- Affichage compteurs ---
    text1 = font.render(f"Invincibilité: {invincibility_time_left:.1f}s", True, (255, 255, 0))
    text2 = font.render(f"Accélération: {boost_time_left:.1f}s", True, (255, 100, 255))
    screen.blit(text1, (10, 10))
    screen.blit(text2, (10, 40))

    # --- Fin de partie ---
    if game_over:
        text = font.render("GAME OVER", True, (255, 0, 0))
        screen.blit(text, (SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2 - 20))

    pygame.display.flip()
    clock.tick(60)

    if game_over:
        pygame.time.delay(3000)
        running = False

pygame.quit()
sys.exit()
