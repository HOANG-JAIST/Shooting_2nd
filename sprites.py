import pygame
import random
import os

width = 360
height = 480
fps = 30

# Define color
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

# set up assets
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, "img")

class Player(pygame.sprite.Sprite):
    # sprite for the Player
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(img_folder, "p1_stand.png")).convert()
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.center = (width / 2, height / 2)
        self.y_speed = 5

    def update(self):
        self.rect.x += 5
        self.rect.y += self.y_speed
        if self.rect.bottom > height - 200:
            self.y_speed = -5
        if self.rect.top < 200:
            self.y_speed = 5
        if self.rect.left > width:
            self.rect.right = 0

# Initialize and create a window
pygame.init()
pygame.mixer.init() # for sound
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Anhh Game")
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
# Game loop
running = True
while running:
    # keep running at the right speed
    clock.tick(fps)
    # Process input/ events
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False
    
    # Updata
    all_sprites.update()
    
    # Draw/ render
    screen.fill(blue)
    all_sprites.draw(screen)
    # after drawing everything, flip the display
    pygame.display.flip()

pygame.quit()

