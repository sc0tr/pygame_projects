# game options/settings
# pygame 'HOW TO THINK LIKE A COMP SCI'
# <http://openbookproject.net/thinkcs/python/english3e/pygame.html>


WIDTH = 480
HEIGHT = 600
FPS = 60
TITLE = 'JUMPY'
FONT_NAME = 'arial'
HS_FILE = "highscore.txt"
SPRITESHEET = 'spritesheet_jumper.png'


# player properties
"""
Friction sets a max speed, allows object to stop with key release, & 
affects how quickly it comes to a stop.
More negative number (further from zero) stops faster, but lowers the max
A number closer to 0 stops over longer streches, but has higher max speeds.
Bouncy direction changes with high/med-high speed (acc = 20, fric = -1.5)
Tight high speed controls use greater accel (5-10) more neg Frict(-0.8)

average/natural (2 >= acc <= 6) (-0.5 <= Fric >= -0.25)

Loose slow 		(0.5, -0.125)
Loose high speed (3 >= acc <= 5) (-0.25 <= Fric >= -0.08)

"""

PLAYER_ACC = 3
PLAYER_FRICTION = -0.325
PLAYER_GRAV = 0.75
PLAYER_JUMP = 22

# Game Properties
BOOST_POWER = 60  # How fast powerup moves player upward
POW_SPAWN_PCT = 7  # How often pow spawms How likely a platform will have Pow when spawm
MOB_FREQ = 5000  # frequency of mob spawns set to 5000 ms (5s)

"""
ADDED NEW VARS FOR LAYER UPDATE ORDER
"""
PLAYER_LAYER = 2
PLAT_LAYER = 1
POW_LAYER = 1
MOB_LAYER = 2

# Define colors
BLACK = (0,0,0)
WHITE = (250,250,250)
YELLOW = (244,244,30)
LTBLUE = (0, 155, 155)
CYAN = (80, 204, 255)
GREEN = (80, 255, 80)
TAN = (239, 135, 49)
BG_COLOR = (LTBLUE)

# starting platforms list  (x, y, w, h)
PLATFORM_LIST = [(WIDTH / 2 - 50, HEIGHT * 3 / 4),
				(0, HEIGHT - 20),
				(125, HEIGHT - 350),
				(350, 200),
				(175, 100),
				(20, HEIGHT + 200),
				]
