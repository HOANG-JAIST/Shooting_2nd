import pygame
import random

width = 360
height = 480
fps = 30

# Define color
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
# Initialize and create a window
pygame.init()
pygame.mixer.init() # for sound
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Anhh Game")
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()
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
    screen.fill(black)
    all_sprites.draw(screen)
    # after drawing everything, flip the display
    pygame.display.flip()

pygame.quit()

