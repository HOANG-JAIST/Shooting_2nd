# main program

import pygame as pg
import random
from settings import *

class Game:
    def __init__(self):
        # Initialize game
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((width, height))
        pg.display.set_caption(Title)
        self.clock = pg.time.Clock()
        self.running = True
    
    def new(self):
        # Start a new game
        self.all_sprites = pg.sprite.Group()
        self.run()

    def run(self):
        # Game loop
        self.playing = True
        while self.playing:
            self.clock.tick(fps)
            self.events()
            self.update()
            self.draw()

    def update(self):
        # Game loop - update
        self.all_sprites.update()

    def events(self):
        # Game loop - vents
        for event in pg.event.get():
            # Check for closing window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False

    def draw(self):
        # Game loop - draw
        self.screen.fill(black)
        self.all_sprites.draw(self.screen)
        # after draw everything, flip screen
        pg.display.flip()
    
    def show_start_screen(self):
        # Game start screen
        pass

    def show_go_screen(self):
        # Game over
        pass

g = Game()
g.show_start_screen()

while g.running:
    g.new()
    g.show_go_screen()

pg.guit()  
    