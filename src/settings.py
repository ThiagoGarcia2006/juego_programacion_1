
WIDTH = 800
HEIGHT = 600
MID_WIDTH_SCREEN = WIDTH // 2
MID_HEIGHT_SCREEN = HEIGHT // 2
SIZE_SCREEN = (WIDTH, HEIGHT)
CENTER_SCREEN = (WIDTH // 2, HEIGHT// 2)
ORIGIN = (0, 0)


START_BUTTON_SIZE = (200,200)

POS_SCORE = (MID_WIDTH_SCREEN, 50)
POS_HIGH_SCORE = (150, 50)
POS_LAST_SCORE = (WIDTH - 150, 50)
POS_MUTE = (50, HEIGHT - 50)
POS_TITLE = (MID_WIDTH_SCREEN, 50)

FPS = 60

INITIAL_ENEMYS = 10

SPEED = 5

FONT_SIZE = 40

FONT_TYPE = "./src/assets/font/dash-horizon.otf"
SCREEN_TYPE = "./src/assets/images/fondo.jpg"
SCREEN_MENU_TYPE = "./src/assets/images/fondo_menu.jpg"
IMAGE_PLAYER_TYPE = "./src/assets/images/player.png"
IMAGE_ENEMY_TYPE = "./src/assets/images/enemy.png"
START_BUTTON_TYPE = "./src/assets/images/start_button.png"
LOGO_TYPE = "./src/assets/images/logo.png"
SHOT_TIPE = "./src/assets/sounds/disparo.mp3"
GAME_OVER_TYPE = "./src/assets/sounds/game_over.mp3"
LEVEL_TYPE = "./src/assets/sounds/exito.mp3"
COLLISION_TYPE = "./src/assets/sounds/enemy.mp3"
MUSIC_TYPE = "./src/assets/sounds/musica.mp3"



#colors
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
CYAN = (0, 255, 255)
YELLOW = (255, 255, 0)
MAGENTA = (255, 0, 255)


#dimenciones player
player_w = 70
player_h = 70

#dimensiones enemy
enemy_width = 80
enemy_height = 80

#configuro la direccion
move_left = False
move_right = False
move_up = False
move_down = False

min_speed_y_enemy = 3
max_speed_y_enemy = 7
min_speed_x_enemy = 3
max_speed_x_enemy = 7


shot_width = 10
shot_height = 10
shot_speed = 15
shot_width_special = 50
shot_height_special = 50

last_special_ability_time = 0
special_ability_cooldown = 10000  

