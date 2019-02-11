import pygame
import random
from os import path

img_dir = path.join(path.dirname(__file__), "img")
aud_dir = path.join(path.dirname(__file__), "aud")

width = 480
height = 600
fps = 60
power_time = 5000

# Define color
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)

# Initialize and create a window
pygame.init()
pygame.mixer.init() # for sound, source: https://www.bfxr.net/
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Shoot_up")
clock = pygame.time.Clock()

font_name = pygame.font.match_font('arial')
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, white)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

def newmob():
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)

def draw_shield_bar(surf, x, y, pct):
    if pct < 0:
        pct = 0
    bar_length = 100
    bar_height = 10
    fill = (pct / 100) * bar_length
    outline_rect = pygame.Rect(x, y, bar_length, bar_height)
    fill_rect = pygame.Rect(x, y, fill, bar_height)
    pygame.draw.rect(surf, green, fill_rect)
    pygame.draw.rect(surf, white, outline_rect, 2)

def draw_lives(surf, x, y, lives, img):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 30 + i
        img_rect.y = y
        surf.blit(img, img_rect)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (50,30))
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.radius = 20
        # pygame.draw.circle(self.image, red, self.rect.center, self.radius)
        self.rect.centerx = width / 2
        self.rect.bottom = height - 10
        self.speedx = 0
        self.shield = 100
        self.shoot_delay = 250
        self.last_shot = pygame.time.get_ticks()
        self.lives = 3
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()
        self.power = 1
        self.power_time = pygame.time.get_ticks()

    def update(self):
        # timeout for powerup
        if self.power >= 2 and pygame.time.get_ticks() - self.power_time > powerup_time:
            self.power -= 1
            self.power_time = pygame.time.get_ticks()

        # unhide if hidden
        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1000:
            self.hidden = False
            self.rect.center = width / 2
            self.rect.bottom = height - 10

        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -5
        if keystate[pygame.K_RIGHT]:
            self.speedx = 5
        if keystate[pygame.K_SPACE]:
            self.shoot()
        self.rect.x += self.speedx
        if self.rect.right > width:
            self.rect.right = width
        if self.rect.left < 0:
            self.rect.left = 0

    def powerup(self):
        self.power += 1
        self.power_time = pygame.time.get_ticks()

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            if self.power == 1:
                bullet = Bullet(self.rect.centerx, self.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)
                shoot_sound.play()
            if self.power >= 2:
                bullet1 = Bullet(self.rect.left, self.rect.centery)
                bullet2 = Bullet(self.rect.right, self.rect.centery)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                bullets.add(bullet1)
                bullets.add(bullet2)
                shoot_sound.play()

    def hide(self):
        # hide the player temporarily
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (width / 2, height + 200)

class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = random.choice(meteor_images)
        self.image_orig.set_colorkey(black)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .85 / 2)
        # pygame.draw.circle(self.image, red, self.rect.center, self.radius)
        self.rect.x = random.randrange(width - self.rect.width)
        self.rect.y = random.randrange(-150, -100)
        self.speedy = random.randrange(1, 8)
        self.speedx = random.randrange(-3, 3)
        self.rot = 0
        self.rot_speed = random.randrange(-8, 8)
        self.last_update = pygame.time.get_ticks()
    
    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def update(self):
        self.rotate()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > height + 10 or self.rect.left < -25 or self.rect.right > width + 10:
            self.rect.x = random.randrange(width - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x 
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        # Kill it if it moves off the top of the screen
        if self.rect.bottom < 0:
            self.kill()
class Pow(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(['shield', 'bolt'])
        self.image = powerup_images[self.type]
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 5

    def update(self):
        self.rect.y += self.speedy
        # Kill it if it moves off the top of the screen
        if self.rect.bottom < 0:
            self.kill()

class Exploision(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0 
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 75

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

# Load all game graphics
background = pygame.image.load(path.join(img_dir, "purple.png")).convert()
bg_fix = pygame.transform.scale(background, (width, height))
background_rect = bg_fix.get_rect()
player_img = pygame.image.load(path.join(img_dir, "playerShip1_orange.png")).convert()
# meteor_img = pygame.image.load(path.join(img_dir, "meteorBrown_big1.png")).convert()
player_mini_img = pygame.transform.scale(player_img, (25, 19))
player_mini_img.set_colorkey(black)
bullet_img = pygame.image.load(path.join(img_dir, "laserRed01.png")).convert()
meteor_images = []
meteor_list = ['meteorBrown_big1.png', 'meteorBrown_big2.png', 'meteorBrown_big3.png', 'meteorGrey_big1.png']
for img in meteor_list:
    meteor_images.append(pygame.image.load(path.join(img_dir, img)).convert())

explosion_anim = {}
explosion_anim['lg'] = []
explosion_anim['sm'] = []
explosion_anim['player'] = []
for i in range(9):
    filename = 'regularExplosion0{}.png'.format(i)
    img = pygame.image.load(path.join(img_dir, filename)).convert()
    img.set_colorkey(black)
    img_lg = pygame.transform.scale(img, (75, 75))
    explosion_anim['lg'].append(img_lg)
    img_sm = pygame.transform.scale(img, (32, 32))
    explosion_anim['sm'].append(img_sm)
    #filename = 'sonicExplosion0{}.png'.format(i)
    #img = pygame.image.load(path.join(img_dir, filename)).convert()
    explosion_anim['player'].append(img)
powerup_images = {}
powerup_images['shield'] = pygame.image.load(path.join(img_dir, 'shield_gold.png')).convert()
powerup_images['bolt'] = pygame.image.load(path.join(img_dir, 'bolt_gold.png')).convert()

# Load all game sound
shoot_sound = pygame.mixer.Sound(path.join(aud_dir, 'Hit_Hurt.wav'))  
expl_sounds = []
for aud in ['Blip_Select.wav', 'Hit_Hurt.wav']:
    expl_sounds.append(pygame.mixer.Sound(path.join(aud_dir, aud)))
player_die_sound = pygame.mixer.Sound(path.join(aud_dir, 'sfx_lose.ogg'))
pygame.mixer.music.load(path.join(aud_dir, 'sfx_lose.ogg'))
pygame.mixer.music.set_volume(0.4)

all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()
powerups = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
for i in range(8):
    newmob()

score = 0
pygame.mixer.music.play(loops=-1)
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

    # check to see if a bullet hit a mob
    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
    for hit in hits:
        score += int(50 - hit.radius)
        random.choice(expl_sounds).play()
        expl = Exploision(hit.rect.center, 'lg')
        all_sprites.add(expl)
        if random.random() > 0.1:
            pow = Pow(hit.rect.center)
            all_sprites.add(pow)
            powerups.add(pow)
            pow
        newmob()

    # Check to see if a mob hit player
    hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle)
    for hit in hits:
        player.shield -= hit.radius * 2
        expl = Exploision(hit.rect.center, 'sm')
        all_sprites.add(expl)
        newmob()
        if player.shield <= 0:
            player_die_sound.play()
            death_explosion = Exploision(player.rect.center, 'player')
            all_sprites.add(death_explosion)
            player.hide()
            player.lives -= 1
            player.shield = 100
    # Check to see if player hit a powerup
    hits = pygame.sprite.spritecollide(player, powerups, True)
    for hit in hits:
        if hit.type == 'shield':
            player.shield += random.randrange(10, 30)
            if player.shield >= 100:
                player.shield = 100
        if hit.type == 'bolt':
            player.powerup

        # if the player died and the explosion has finished playing
        if not player.lives == 0 and not death_explosion.alive():
            running = False
        
    # Draw/ render
    # screen.fill(black)
    screen.blit(bg_fix, background_rect)
    all_sprites.draw(screen)
    draw_text(screen, str(score), 18, width / 2, 10)
    draw_shield_bar(screen, 5, 5, player.shield)
    draw_lives(screen, width - 100, 5, player.lives, player_mini_img)

    # after drawing everything, flip the display
    pygame.display.flip()

pygame.quit()

