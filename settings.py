# Settings for the game
import math

# screen settings
Res = WIDTH, HEIGHT = 1600, 900
HALF_WIDTH = WIDTH // 2
HALF_HEIGHT = HEIGHT // 2
FPS = 60

# player settings
PLAYER_POSITION = 1.5, 1.5
PLAYER_ANGLE = 0
PLAYER_SPEED = 0.005
PLAYER_ROTATION_SPEED = 0.002
PLAYER_SIZE = 60
PLAYER_MAX_HEALTH = 100
PLAYER_MAX_ARMOUR = 50
MAX_SHOTGUN_MUNITION = 20

# mouse settings
MOUSE_SENSITIVITY = 0.0002
MOUSE_MAX_REL = 40
MOUSE_BORDER_LEFT = 400
MOUSE_BORDER_RIGHT = WIDTH - MOUSE_BORDER_LEFT

# FOV and ray casting settings
FOV = math.pi / 3
HALF_FOV = FOV / 2
NUM_RAYS = WIDTH // 2
HALF_NUM_RAYS = NUM_RAYS // 2
DELTA_ANGLE = FOV / NUM_RAYS
MAX_DEPTH = 20

# 3D
SCREEN_DIST = HALF_WIDTH / math.tan(HALF_FOV)
SCALE = WIDTH // NUM_RAYS

TEXTURE_SIZE = 256
HALF_TEXTURE_SIZE = TEXTURE_SIZE // 2
FLOOR_COLOUR = (30, 30, 30)
