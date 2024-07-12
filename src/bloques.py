import pygame
from random import randint
from settings import *


def create_block(imagen:pygame.Surface = None, left=0, top=0, width=50, height=50, color=(255, 255, 255), dir=3, borde=0, radio=-1):
    """
    Crea un bloque con opciones de imagen, color y atributos adicionales.

    Args:
    - imagen (pygame.Surface, opcional): Superficie de imagen para el bloque.
    - left (int): Posición izquierda del bloque.
    - top (int): Posición superior del bloque.
    - width (int): Ancho del bloque.
    - height (int): Altura del bloque.
    - color (tuple[int, int, int]): Color RGB del bloque (por defecto es blanco).
    - dir (int): Dirección del bloque (por defecto es 3).
    - borde (int): Borde del bloque (por defecto es 0).
    - radio (int): Radio del bloque (por defecto es -1).

    Returns:
    - dict: Un diccionario que representa el bloque con las siguientes claves:
        - 'rect' (pygame.Rect): Rectángulo que define la posición y tamaño del bloque.
        - 'color' (tuple[int, int, int]): Color RGB del bloque.
        - 'dir' (int): Dirección del bloque.
        - 'borde' (int): Borde del bloque.
        - 'radio' (int): Radio del bloque.
        - 'img' (pygame.Surface, opcional): Imagen escalada si se proporciona una.

    Nota:
    Si se proporciona una imagen (`imagen`), se escalará al tamaño especificado por `width` y `height`.
    """
    if imagen:
        imagen = pygame.transform.scale(imagen, (width, height))
    return {"rect": pygame.Rect(left, top, width, height), "color": color, "dir": dir, "borde": borde, "radio": radio, "img": imagen}


def create_player(imagen: pygame.Surface = None):
    """
    Crea un jugador como un bloque con imagen y atributos predeterminados.

    Args:
    - imagen (pygame.Surface, opcional): Superficie de imagen para el jugador.

    Returns:
    - dict: Un diccionario que representa al jugador como un bloque con los atributos predeterminados y una imagen opcional.
    """
    return create_block(imagen, randint(0, WIDTH - player_w), randint(0, HEIGHT - player_h), player_w, player_h, RED, radio= player_h // 2)

def create_enemy(imagen: pygame.Surface = None):
    """
    Crea un enemigo como un bloque con imagen, posición aleatoria en el borde derecho y velocidad aleatoria en el eje x.

    Args:
    - imagen (pygame.Surface, opcional): Superficie de imagen para el enemigo.

    Returns:
    - dict: Un diccionario que representa al enemigo como un bloque con imagen, posición en el borde derecho y velocidad en el eje x.
    """
    block = create_block(imagen, WIDTH, randint(0, HEIGHT - enemy_height), enemy_width, enemy_height, WHITE, radio= enemy_width // 2)
    block["speed_x"] = randint(min_speed_x_enemy, max_speed_x_enemy)  
    return block

def create_shot(midBottom: tuple[int, int], color:tuple [int, int, int] = WHITE):
    """
    Crea un objeto de disparo.

    Args:
    - midBottom (tuple[int, int]): Las coordenadas (x, y) del punto medio inferior del disparo.
    - color (tuple[int, int, int], opcional): La tupla de color RGB del disparo (por defecto es BLANCO).

    Returns:
    - dict: Un diccionario que representa el objeto de disparo con las claves:
        - 'rect' (pygame.Rect): Un rectángulo que representa la posición y tamaño del disparo.
        - 'color' (tuple[int, int, int]): El color RGB del disparo.
        - 'speed' (int): La velocidad del disparo.

    Nota:
    El atributo 'rect' del diccionario devuelto debe ajustarse después de la creación para colocar correctamente el disparo.
    """
    block = {"rect": pygame.Rect(0, 0, shot_width, shot_height), "color": color, "speed": shot_speed}
    block["rect"].midbottom = midBottom
    block["rect"].x += block["speed"]
    return block

def create_shot_special(midBottom: tuple[int, int], color:tuple [int, int, int] = RED):
    """
    Crea un objeto de disparo especial.

    Args:
    - midBottom (tuple[int, int]): Las coordenadas (x, y) del punto medio inferior del disparo especial.
    - color (tuple[int, int, int], opcional): La tupla de color RGB del disparo especial (por defecto es ROJO).

    Returns:
    - dict: Un diccionario que representa el objeto de disparo especial con las claves:
        - 'rect' (pygame.Rect): Un rectángulo que representa la posición y tamaño del disparo especial.
        - 'color' (tuple[int, int, int]): El color RGB del disparo especial.
        - 'speed' (int): La velocidad del disparo especial.
    """
    block = {"rect": pygame.Rect(0, 0, shot_width_special, shot_height_special), "color": color, "speed": shot_speed}
    block["rect"].midbottom = midBottom
    return block


def load_enemy_list(lista: list, qty_enemy: int, imagen:pygame.Surface = None):
    """
    Carga enemigos en una lista dada.

    Args:
    - lista (list): La lista en la que se cargarán los enemigos.
    - qty_enemy (int): La cantidad de enemigos que se deben cargar.
    - imagen (pygame.Surface, opcional): Superficie de imagen para los enemigos.

    Returns:
    - None

    Note:
    Esta función modifica la lista `lista` agregando `qty_enemy` nuevos enemigos creados con la función `create_enemy`.
    """
    try:
        for _ in range(qty_enemy):
            new_enemy = create_enemy(imagen)
            if new_enemy:
                lista.append(new_enemy)
    except Exception as e:
        print(f"Error al cargar lista de enemigos: {str(e)}")