# 
# 
# self.vel.y = -20  # This works if we were making flappy bird


# Sprite classes for platform game

# part 3 adding GRAVITY & PLATFORMS
# part 4 adding JUMPING
# part 5 scrolling up the screen 
# part 6 player death and game over
# part 8 File I/O and saving the game
# part 9 adding spritesheet and updating img
# part 10 adding animations!!
# part 12 adding graphics to the platforms
"""
Part 17 is about creating collision masks for pixel perfect collisions
Chris describes the difference between rectangular, circular and pixelPerfect
collision masks.
you create a mask within a sprite class using 
self.mask = pg.mask.from_surface(self.image)  
# add this at the end of the animate() or Update() Fx to match the current_frame
then in collision use add (pg.sprite.collide_mask) to the arguments in 
the hits sections

"""

import pygame as pg
from random import choice, randrange
from settings import *
vec = pg.math.Vector2


class Spritesheet:
	"""
	utility class for loading and parsing spritesheets (parsing-breakiong up into parts to understand)
	loads image and slices it up into animation frames
	"""
	def __init__(self, filename):
		self.spritesheet = pg.image.load(filename).convert()

	def get_img(self, x, y, width, height):
		# grab image out of larger spritesheet
		image = pg.Surface((width, height))
		# takes the (w,h) of self.spritesheet & blits it to image at loc (0,0)
		image.blit(self.spritesheet, (0,0), (x, y, width, height))
		image = pg.transform.scale(image, ((width // 3, height // 3)))
		return image


class Player(pg.sprite.Sprite):
	def __init__(self, game):
		self._layer = PLAYER_LAYER
		self.groups = game.all_sprites
		pg.sprite.Sprite.__init__(self, self.groups)
		self.game = game
		self.walking = False
		self.jumping = False
		self.current_frame = 0
		self.last_update = 0  # spaces framerate of anim based on FPS
		self.load_images()
		self.image = self.standing_frames[0]
		# self.image.set_colorkey(BLACK)
		self.rect = self.image.get_rect()
		self.rect.center = (WIDTH / 2, HEIGHT / 2)
		# # movement
		# self.vx = 0
		# self.vy = 0
		self.speed = PLAYER_ACC
		self.pos = vec(WIDTH / 2, HEIGHT / 2)
		self.vel = vec(0, 0) # x, y
		self.acc = vec(0, 0)

	def load_images(self):
		self.standing_frames = [self.game.spritesheet.get_img(614, 1063, 120, 191),
								self.game.spritesheet.get_img(690, 406, 120, 201)]
		for frame in self.standing_frames:
			frame.set_colorkey(BLACK)
		self.walk_frames_r = [self.game.spritesheet.get_img(678, 860, 120, 201),
								self.game.spritesheet.get_img(692, 1458, 120, 207)]
		self.walk_frames_l = []
		for frame in self.walk_frames_r:
			frame.set_colorkey(BLACK)
			self.walk_frames_l.append(pg.transform.flip(frame, True, False))
		self.jump_frame = self.game.spritesheet.get_img(382, 763, 150, 181)
		self.jump_frame.set_colorkey(BLACK)


	def jump_cut(self):
		if self.jumping:
			if self.vel.y < -5:
				self.vel.y = -3


	def jump(self):
		self.rect.x += 2  
		# but we need to allow jump only if standing on platform.
		# so we send the player a reference when it spawns (self.game=game)
		hits = pg.sprite.spritecollide(self, self.game.platforms, False)
		self.rect.y -= 2  # looks under player (add 1px lower)
		if hits and not self.jumping:
			self.game.jump_snd.play()
			self.jumping = True
			self.vel.y = -PLAYER_JUMP


	def update(self):
		# keeping clean make new method for animation:
		self.animate()

		# ADDING ACCELERATION
			# for gravity we want an accel in the Y direction
		self.acc = vec(0, PLAYER_GRAV)  # Next is to add GRAVITY! <--
		keys = pg.key.get_pressed()
		if keys[pg.K_LEFT]:
			self.acc.x = -self.speed
		if keys[pg.K_RIGHT]:
			self.acc.x = self.speed
		# if keys[pg.K_UP]:
		# 	self.acc.y = -self.speed
		if keys[pg.K_DOWN]:
			self.acc.y = self.speed

		# applies friction
		"""
		when we move, friction is slowing us down bc friction is a negative direction
		so accel & velocity is getting smaller but may never reach 0, & bc we are rounding
		so we need to set threshhold if abs(vel) is below certain level, then it should
		be set to zero. 
		"""
		# for gravity. only want friction in the x direction not y
		self.acc.x += self.vel.x * PLAYER_FRICTION
		# equations of motion
		self.vel += self.acc
		if abs(self.vel.x) < 0.1:
			self.vel.x = 0
		self.pos += self.vel + 0.5 * self.acc
		# wrap player around screen
		if self.pos.x > WIDTH + self.rect.width / 2:
			self.pos.x = 0 - self.rect.width / 2
		if self.pos.x < 0 - self.rect.width / 2:
			self.pos.x = WIDTH + self.rect.width / 2

		self.rect.midbottom = self.pos
		

	def animate(self):
		# 1st we need to find what time it is now
		now = pg.time.get_ticks()  # gets ticks since game start
		
		if self.vel.x != 0:
			self.walking = True
		else:
			self.walking = False
		# show walk animation
		if self.walking:
			if now - self.last_update > 120: # adjusts framess
				# is it time to update frame, now?
				self.last_update = now
				self.current_frame = (self.current_frame + 1) % len(self.walk_frames_l)
				bottom = self.rect.bottom
				if self.vel.x > 0:  # moving right
					self.image = self.walk_frames_r[self.current_frame]
				else:
					self.image = self.walk_frames_l[self.current_frame]
				self.rect = self.image.get_rect()
				self.rect.bottom = bottom

		if not self.jumping and not self.walking:
			if now - self.last_update > 350:
				self.last_update = now
				# if there are 2 frames, gets remainder
				self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
				# keeps track of bootom of rectangle, then need new rect for new frame
				bottom = self.rect.bottom
				self.image = self.standing_frames[self.current_frame]
				self.rect = self.image.get_rect()
				# gets new bottom for the new frame
				self.rect.bottom = bottom
		self.mask = pg.mask.from_surface(self.image)  


class Platform(pg.sprite.Sprite):

	def __init__(self, game, x, y):
		self._layer = PLAT_LAYER
		self.groups = game.all_sprites, game.platforms
		pg.sprite.Sprite.__init__(self, self.groups)
		self.game = game
		images = [self.game.spritesheet.get_img(0, 288, 380, 94),
		self.game.spritesheet.get_img(213, 1662, 201, 100)]
		self.image = choice(images)
		self.image.set_colorkey(BLACK)
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		if randrange(100) < POW_SPAWN_PCT:
			Pow(self.game, self)
		# after this add Group() to Game.new()

class Pow(pg.sprite.Sprite):
	def __init__(self, game, plat):
		self._layer = POW_LAYER
		self.groups = game.all_sprites, game.powerups
		pg.sprite.Sprite.__init__(self, self.groups)
		self.game = game
		self.plat = plat
		self.type = choice(['boost'])
		self.image = self.game.spritesheet.get_img(820, 1805, 71, 70)
		self.image.set_colorkey(BLACK)
		self.rect = self.image.get_rect()
		self.rect.centerx = self.plat.rect.centerx
		self.rect.bottom = self.plat.rect.top - 5  #hovers just above plat top

	def update(self):
		self.rect.bottom = self.plat.rect.top - 5
		if not self.game.platforms.has(self.plat):
			self.kill()

class Mob(pg.sprite.Sprite):
	"""
	This video is all about adding enemies and making them move.
	New info: randomizing mob spawn & setting movement direction based
	on the side of the screen. using a 
	adding an enemy and animation for the little yellow helicopter sprite
	'flyman'
	"""
	def __init__(self, game):
		self._layer = MOB_LAYER
		self.groups = game.all_sprites, game.mobs
		pg.sprite.Sprite.__init__(self, self.groups)
		self.game = game
		self.image_up = self.game.spritesheet.get_img(566, 510, 122, 139)
		self.image_up.set_colorkey(BLACK)
		self.image_down = self.game.spritesheet.get_img(568, 1534, 122, 135)
		self.image_down.set_colorkey(BLACK)
		self.image = self.image_up
		self.rect = self.image.get_rect()
		# have them somestimes spawn on left, and sometimes on right
		# start off screen
		self.rect.centerx = choice([-100, WIDTH + 100])
		self.vx = randrange(1, 4)  # positive x change speed 
		if self.rect.centerx > WIDTH:
			self.vx *= -1  # if spawns off screen right, changes x to negative
		self.rect.y = randrange(HEIGHT / 2)
		self.vy = 0  # velocity on y axis
		self.dy = 0.5  # amount of y acceleration for y movement

	def update(self):
		self.rect.x += self.vx  # increments x change
		self.vy += self.dy
		if self.vy > choice([1,2,3]) or self.vy < choice([-3,-2,-1]):  # boundary of 6 pixels
			self.dy *= -1  # changes y direction 
		if self.rect.top <= 0:  # keeps mobs from going off top screen
			self.dy = 0.5
		# decide which image to use (based on direction)
		center = self.rect.center
		if self.dy < 0:  # if neg Y up image
			self.image = self.image_up
		else:
			self.image = self.image_down
		self.rect = self.image.get_rect()
		self.mask = pg.mask.from_surface(self.image)
		self.rect.center = center
		self.rect.y += self.vy
		if self.rect.left > WIDTH +100 or self.rect.right < - 100:
			self.kill()
