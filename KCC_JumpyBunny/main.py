# Jumpy Platformer
#



# File I/O  saving a high score

import pygame as pg
import random
from settings import *
from sprites import *
from os import path

class Game:

    def __init__(self):
        """ initialize game window, sounds, clock """
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.font_name = pg.font.match_font(FONT_NAME)
        ## you want to load data at the start of the game (initialization)
        self.load_data()  #new function to add high_score, snds & imgs

    def load_data(self):
        # load high score
        """you need to make sure to close the file after opening """
        self.dir = path.dirname(__file__)
        img_dir = path.join(self.dir, 'img')
        # WHEN OPENING A FILE YOU HAVE OPTIONS ('r'=read, 'w'=write, 't'=text)
        # to do both make var:
        self.file_exist = 'r+' if path.isfile(path.join(self.dir, HS_FILE)) else 'w'
        with open(path.join(self.dir, HS_FILE), self.file_exist) as f:
            # within the with block the file is conditioned
            # if no hs_file exists the 'w' automatically creates one
            # below int(f.read()) will read the score in HS_FILE, but if no
            # file, then there is nothing to convert to int and Error(use try:)
            try:
                self.highscore = int(f.read())
            except:
                self.highscore = 0
        # load spritesheet image
        self.spritesheet = Spritesheet(path.join(img_dir, SPRITESHEET))
        # load sounds
        self.snd_dir = path.join(self.dir, 'snd')
        self.jump_snd = pg.mixer.Sound(path.join(self.snd_dir, "jump.wav"))
        self.jump_snd2 = pg.mixer.Sound(path.join(self.snd_dir, "jump3.wav"))
        self.jump_snd3 = pg.mixer.Sound(path.join(self.snd_dir, "jump3.wav"))
        self.die_snd = pg.mixer.Sound(path.join(self.snd_dir, 'die_snd.wav'))
        self.boost_sound = pg.mixer.Sound(path.join(self.snd_dir, 'boost16.wav'))

    def new(self):
        # start game play
        """
        create the mobs group, and set a mob timer to 0
        """
        self.score = 0
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.platforms = pg.sprite.Group()
        self.powerups = pg.sprite.Group()
        self.player = Player(self)
        self.mobs = pg.sprite.Group()
        # self.all_sprites.add(self.player)
        for plat in PLATFORM_LIST:
            Platform(self, *plat)  # exploding the list
        self.mob_timer = 0
        pg.mixer.music.load(path.join(self.snd_dir,'happytune.ogg'))
        self.run()


    def run(self):
        # Game loop
        pg.mixer.music.play(loops=-1)
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
        pg.mixer.music.fadeout(500)

    def show_start_screen(self):
        #
        pg.mixer.music.load(path.join(self.snd_dir, 'Town.ogg'))
        pg.mixer.music.play(loops=-1)
        self.screen.fill(BG_COLOR)
        self.draw_text(TITLE, 48, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text("Arrow Keys: move\nSpace Bar: Jump", 
                        22, WHITE, WIDTH / 2, HEIGHT / 3)
        self.draw_text("Press Any Key to Play", 18, WHITE, WIDTH / 2, HEIGHT / 2)
        self.draw_text("HIGH SCORE: " + str(self.highscore), 22, WHITE, WIDTH/2, 15)
        pg.display.flip()
        self.wait_to_play()
        pg.mixer.music.fadeout(500)
    
    def wait_to_play(self):
        """ LOOP that checks for KEYUP or pg.quit() event"""
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pg.KEYUP:
                    waiting = False


    def show_go_screen(self):
        # game over/continue screen
        if not self.running:
            return
        pg.mixer.music.load(path.join(self.snd_dir, 'Town.ogg'))
        pg.mixer.music.play(loops=-1)
        self.screen.fill(BLACK)
        self.draw_text("GAME OVER", 72, TAN, WIDTH / 2, HEIGHT / 4)
        self.draw_text("Arrow Keys: move\nSpace Bar: Jump", 
                        22, WHITE, WIDTH / 2, HEIGHT / 3)
        self.draw_text("Press Any Key to Play", 18, WHITE, WIDTH / 2, HEIGHT / 2)
        if self.score > self.highscore:
            self.highscore = self.score
            self.draw_text("NEW HIGH SCORE! " + str(self.highscore), 22, WHITE, WIDTH / 2, HEIGHT /2+ 40)
            with open(path.join(self.dir, HS_FILE), 'w') as f:
                f.write(str(self.score))
        else:
            self.draw_text("HIGH SCORE: " + str(self.highscore), 22, WHITE, WIDTH / 2, HEIGHT / 2 + 40)
        pg.display.flip()
        self.wait_to_play()
        pg.mixer.music.fadeout(500)

    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

    def update(self):
        # screen and sprite animation updates
        self.all_sprites.update()
        
        """
        Here we spawn mobs according to the mob timer
        by defining 'now' and assigning it to get_ticks()
        that way if the timer passes 5000 a new mob will spawn
        but in order to randomize the interval use random.choice in 500ms

        then in the 'if player reaches top 1/4 of screen' section
        we added a loop to collect all mobs and set their y + the 
        max of either the absolute value of the player velocity or 2

        finally we updated the draw order in the draw function using 
        a new type of group called layeredupdates in the new function
        LayeredUpdates() allows you to assign an order value to each 
        of your sprites 

        Created constant vars in the settings.py for layer order
        putting the player and mobs on the same layer (2) and the
        plats and the pows on the same layer (1)

        next you don't need the screen.blit for player image any more
        due to the LayeredUpdates() in the draw function
        instead the all_sprites group will handle all the layers
        """
        # Spawn a mob?
        now = pg.time.get_ticks()
        if now - self.mob_timer > 5000 + random.choice([-1000, -500, 0, 500, 1000]):
            self.mob_timer = now
            Mob(self)

        #hit mobs?
        mob_hits = pg.sprite.spritecollide(self.player, self.mobs, False, pg.sprite.collide_mask)
        if mob_hits:
            self.playing = False

        # check if player hits platform (only if falling)
        if self.player.vel.y > 0:
            hits = pg.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                lowest = hits[0]
                for hit in hits:
                    if hit.rect.bottom > lowest.rect.bottom:
                        lowest = hit
                if self.player.pos.x < lowest.rect.right + 8 and \
                    self.player.pos.x > lowest.rect.left - 8:
                    if self.player.pos.y -8 < lowest.rect.bottom:
                        self.player.pos.y = hits[0].rect.top
                        self.player.vel.y = 0
                        self.player.jumping = False
        
        # if player reaches top 25% of screen - MOVE SCREEN UP -
        if self.player.rect.top <= HEIGHT / 4:
            # screen "follows player" (velocity slows down)
            self.player.pos.y += max(abs(self.player.vel.y), 2)  # absoluteVal
            for mob in self.mobs:
                mob.rect.y += max(abs(self.player.vel.y), 2)
            for plat in self.platforms:
                plat.rect.y += max(abs(self.player.vel.y), 2)
                if plat.rect.top >= HEIGHT:
                    plat.kill()
                    self.score += random.randint(8, 15)

        # if player hits powerup
        pow_hits = pg.sprite.spritecollide(self.player, self.powerups, True)
        for pow in pow_hits:
            if pow.type == 'boost':
                self.boost_sound.play()
                self.player.vel.y = -BOOST_POWER
                self.player.jumping = False

        # Player Death
        if self.player.rect.bottom > HEIGHT:
            for sprite in self.all_sprites:
                sprite.rect.y -= max(self.player.vel.y, 10)
                if sprite.rect.bottom < 0:
                    # self.die_snd.play()
                    sprite.kill()

        if len(self.platforms) == 0:
            self.playing = False

        # spawn new platforms to keep avg number
        while len(self.platforms) < 6:
            width = random.randint(40, 120)
            p = Platform(self, random.randrange(0, WIDTH-width), 
                        random.randrange(-75, -30))
            self.platforms.add(p)
            self.all_sprites.add(p)

    def draw(self):
        # 
        self.screen.fill(BG_COLOR)
        self.all_sprites.draw(self.screen)
        self.draw_text(str(self.score), 22, (255,255,255), WIDTH / 2, 15)
        pg.display.flip()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            # ADDING JUMP EVENT
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.player.jump()
            if event.type == pg.KEYUP:
                if event.key == pg.K_SPACE:
                    self.player.jump_cut()


g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.show_go_screen()

pg.quit()
