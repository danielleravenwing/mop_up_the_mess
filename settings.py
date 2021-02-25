#game options and settings
TITLE = "Mop Up the Mess"
TILE_SIZE = 32
TILES_WIDE = 15 # Mobile Phone size 11, small pc = 15
TILES_HIGH = 20 # Mobile Phone size 18, small pc = 20

WIDTH = TILE_SIZE * TILES_WIDE
HEIGHT = TILE_SIZE * TILES_HIGH
FPS = 60
FONT_NAME = 'arial'
END_LEVEL_DELAY = 1400

# Player properties
PLAYER_ACC = 0.5
PLAYER_FRICTION = -0.12

#Starting platforms
PLATFORM_LIST = [(0, HEIGHT - 40, WIDTH, 40),
                 (WIDTH / 2 - 50, HEIGHT * 3/4, 100, 20),
                 (125, HEIGHT - 350, 100, 20),
                 (350, 200, 100, 20),
                 (175, 100, 50, 20)]                 

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
LIGHTBLUE = (0, 155, 155)
BGCOLOR = LIGHTBLUE

# Sound effects
EFFECTS_SOUNDS = {'death': 'deathsplat.ogg', 'mop0': 'mop.ogg', 'mop1': 'mop2.ogg', 'multiply': 'drip.ogg', 'levelup': 'VictorySmall.ogg', 'invincible': 'invincible.ogg', 'explode': 'explode.ogg', 'shatter': 'shatter.ogg'}


# Mob properties
MESS_COLORS = ['green', 'yellow', 'red', 'blue', 'black']
MUSHROOM_COLORS = ['pink', 'brown', 'green', 'yellow', 'red', 'blue', 'black']
GIANT_SLIME_COLORS = ['green', 'yellow', 'red', 'blue']

SLIME_LEVEL = 20
SLIME_PROPS = {}
SLIME_PROPS['move speed'] = {'blue': 500, 'red': 1000, 'yellow': 1500, 'green': 2000, 'black': 4000}
SLIME_PROPS['hp'] = {'blue': 20, 'red': 12, 'yellow': 6, 'green': 2, 'black': 6}
SLIME_PROPS['acceleration'] = {'blue': 10, 'red': 20, 'yellow': 30, 'green': 40, 'black': 50}
SLIME_PROPS['defense'] = {'blue': 1000, 'red': 750, 'yellow': 500, 'green': 100, 'black': 2000}

GIANT_SLIME_PROPS = {}
GIANT_SLIME_PROPS['move speed'] = {'blue': 500, 'red': 1000, 'yellow': 1500, 'green': 2000, 'black': 4000}
GIANT_SLIME_PROPS['hp'] = {'blue': 500, 'red': 400, 'yellow': 300, 'green': 200, 'black': 600}
GIANT_SLIME_PROPS['acceleration'] = {'blue': 10, 'red': 20, 'yellow': 30, 'green': 40, 'black': 50}
GIANT_SLIME_PROPS['defense'] = {'blue': 1000, 'red': 750, 'yellow': 500, 'green': 100, 'black': 2000}

MESS_PROPS = {}
MESS_PROPS['growth rate'] = {'green': 1000, 'yellow': 750, 'red': 900, 'blue': 750, 'black': 2000}
MESS_PROPS['defense'] = {'green': 0, 'yellow': 0, 'red': 200, 'blue': 300, 'black': 700}

MUSHROOM_PROPS = {}
MUSHROOM_PROPS['growth rate'] = {'pink': 2000, 'brown': 1500, 'green': 1200, 'yellow': 1100, 'red': 1000, 'blue': 900, 'black': 3500}
MUSHROOM_PROPS['defense'] = {'pink': 300, 'brown': 500, 'green': 350, 'yellow': 300, 'red': 500, 'blue': 600, 'black': 1000}
MUSHROOM_PROPS['spore rate'] = {'pink': 20, 'brown': 10, 'green': 15, 'yellow': 7, 'red': 15, 'blue': 7, 'black': 25}
MUSHROOM_PROPS['spore speed'] = {'pink': 1, 'brown': 2, 'green': 1.5, 'yellow': 2.5, 'red': 1.5, 'blue': 3, 'black': .5}
MUSHROOM_PROPS['spore lifetime'] = {'pink': 2000, 'brown': 4000, 'green': 2500, 'yellow': 5000, 'red': 3000, 'blue': 5000, 'black': 3000}
