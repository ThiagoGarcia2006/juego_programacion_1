import pygame
from random import randint
from settings import *


def create_block(imagen:pygame.Surface = None, left=0, top=0, width=50, height=50, color=(255, 255, 255), dir=3, borde=0, radio=-1):
    if imagen:
        imagen = pygame.transform.scale(imagen, (width, height))
    return {"rect": pygame.Rect(left, top, width, height), "color": color, "dir": dir, "borde": borde, "radio": radio, "img": imagen}


def create_player(imagen: pygame.Surface = None):
    return create_block(imagen, randint(0, WIDTH - player_w), randint(0, HEIGHT - player_h), player_w, player_h, RED, radio= player_h // 2)

def create_enemy(imagen: pygame.Surface = None):
    block = create_block(imagen, WIDTH, randint(0, HEIGHT - enemy_height), enemy_width, enemy_height, WHITE, radio= enemy_width // 2)
    block["speed_x"] = randint(min_speed_x_enemy, max_speed_x_enemy)  
    return block

def create_shot(midBottom: tuple[int, int], color:tuple [int, int, int] = WHITE):

    block = {"rect": pygame.Rect(0, 0, shot_width, shot_height), "color": color, "speed": shot_speed}
    block["rect"].midbottom = midBottom
    block["rect"].x += block["speed"]
    return block

def create_shot_special(midBottom: tuple[int, int], color:tuple [int, int, int] = RED):
    block = {"rect": pygame.Rect(0, 0, shot_width_special, shot_height_special), "color": color, "speed": shot_speed}
    block["rect"].midbottom = midBottom
    return block


def load_enemy_list(lista: list, qty_enemy: int, imagen:pygame.Surface = None):
    for _ in range (qty_enemy):
        new_enemy = create_enemy(imagen)
        lista.append(new_enemy)