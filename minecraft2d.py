import pygame
import random

# Inizializza Pygame
pygame.init()

# Dimensioni della finestra
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Minecraft 2D")

# Definisci i colori
WHITE = (255, 255, 255)
BROWN = (139, 69, 19)
GREEN = (34, 177, 76)
BLUE = (0, 0, 255)

# Dimensioni dei blocchi
TILE_SIZE = 40

# Definisci il numero di righe e colonne in base alle dimensioni della finestra
ROWS = SCREEN_HEIGHT // TILE_SIZE
COLS = SCREEN_WIDTH // TILE_SIZE

# Genera una semplice mappa: 1 = erba, 2 = terra, 3 = acqua
def generate_world():
    world = []
    for row in range(ROWS):
        world_row = []
        for col in range(COLS):
            if row < ROWS // 2:
                world_row.append(1)  # Erba
            else:
                world_row.append(random.choice([1, 2, 3]))  # Terreno casuale
        world.append(world_row)
    return world

# Disegna il mondo a schermo
def draw_world(world_data):
    for row in range(ROWS):
        for col in range(COLS):
            if world_data[row][col] == 1:
                color = GREEN  # Erba
            elif world_data[row][col] == 2:
                color = BROWN  # Terra
            elif world_data[row][col] == 3:
                color = BLUE  # Acqua
            pygame.draw.rect(screen, color, (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE))

# Classe Giocatore
class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
        self.color = (255, 0, 0)
        self.velocity_y = 0
        self.on_ground = False

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def apply_gravity(self):
        if not self.on_ground:
            self.velocity_y += 1  # Gravità costante
            self.rect.y += self.velocity_y

    def check_collision(self, world_data):
        self.on_ground = False
        # Controlla le collisioni verticali
        for row in range(ROWS):
            for col in range(COLS):
                if world_data[row][col] != 0:  # Blocchi solidi
                    block_rect = pygame.Rect(col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                    if self.rect.colliderect(block_rect):
                        if self.velocity_y > 0:
                            self.rect.bottom = block_rect.top
                            self.on_ground = True
                            self.velocity_y = 0
                        elif self.velocity_y < 0:
                            self.rect.top = block_rect.bottom
                            self.velocity_y = 0

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

# Genera il mondo
world_data = generate_world()

# Inizializza il giocatore
player = Player(100, 100)

# Ciclo di gioco
running = True
clock = pygame.time.Clock()

while running:
    # Eventi di uscita
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Controlli del giocatore
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.move(-5, 0)
    if keys[pygame.K_RIGHT]:
        player.move(5, 0)
    if keys[pygame.K_UP] and player.on_ground:
        player.velocity_y = -15  # Salto

    # Applica la gravità
    player.apply_gravity()

    # Controlla le collisioni del giocatore con il mondo
    player.check_collision(world_data)

    # Colora lo schermo di bianco
    screen.fill(WHITE)

    # Disegna il mondo
    draw_world(world_data)

    # Disegna il giocatore
    player.draw(screen)

    # Aggiorna lo schermo
    pygame.display.update()

    # Limita i fotogrammi al secondo
    clock.tick(30)

# Chiude Pygame
pygame.quit()

