import pygame
from random import *
from sys import *
from settings import *
from bloques import *
from pygame.locals import *




def terminar():
    """
    Termina la ejecución de Pygame y sale del programa.
    """
    pygame.quit()
    exit()


def detectar_colision(rect_1, rect_2):
    """
    Detecta si hay colisión entre dos rectángulos.

    Args:
    - rect_1 (pygame.Rect): El primer rectángulo.
    - rect_2 (pygame.Rect): El segundo rectángulo.

    Returns:
    - bool: True si hay colisión, False de lo contrario.
    """
    if punto_en_rectangulo(rect_1.topleft, rect_2) or \
       punto_en_rectangulo(rect_1.topright, rect_2) or\
       punto_en_rectangulo(rect_1.bottomleft, rect_2) or\
       punto_en_rectangulo(rect_1.bottomright, rect_2) or\
       punto_en_rectangulo(rect_2.topleft, rect_1) or \
       punto_en_rectangulo(rect_2.topright, rect_1) or\
       punto_en_rectangulo(rect_2.bottomleft, rect_1) or\
       punto_en_rectangulo(rect_2.bottomright, rect_1):
        return True
    else:
        return False
        

def punto_en_rectangulo(punto, rect)->bool:
    """
    Determina si un punto está dentro de un rectángulo.

    Args:
    - punto (tuple[int, int]): Coordenadas (x, y) del punto.
    - rect (pygame.Rect): Rectángulo en el que se verifica la posición del punto.

    Returns:
    - bool: True si el punto está dentro del rectángulo, False de lo contrario.
    """
    x, y = punto
    return x >= rect.left and x <= rect.right and y >= rect.top and y <= rect.bottom


def distancia_entre_puntos(pto_1:tuple[int, int], pto_2:tuple[int, int])-> float:
    """
    Calcula la distancia euclidiana entre dos puntos.

    Args:
    - pto_1 (tuple[int, int]): Coordenadas (x, y) del primer punto.
    - pto_2 (tuple[int, int]): Coordenadas (x, y) del segundo punto.

    Returns:
    - float: La distancia euclidiana entre los dos puntos.
    """
    return((pto_1[0] - pto_2[0]) ** 2 + (pto_1[1] - pto_2[1])** 2) ** 0.5

def calcular_radio(rect):
    """
    Calcula el radio de un círculo inscrito en un rectángulo.

    Args:
    - rect (pygame.Rect): Rectángulo del que se calculará el radio.

    Returns:
    - int: El radio del círculo inscrito en el rectángulo.
    """
    return rect.width // 2

def detectar_colision_circulos(rect_1, rect_2)->bool:
    """
    Detecta si hay colisión entre dos círculos inscritos en rectángulos.

    Args:
    - rect_1 (pygame.Rect): El primer rectángulo que contiene al primer círculo.
    - rect_2 (pygame.Rect): El segundo rectángulo que contiene al segundo círculo.

    Returns:
    - bool: True si los círculos (inscritos en los rectángulos) están en colisión, False de lo contrario.
    """
    r1 = calcular_radio(rect_1)
    r2 = calcular_radio(rect_2)
    distancia = distancia_entre_puntos(rect_1.center, rect_2.center)
    return distancia <= r1 + r2

def mostrar_texto(superficie: pygame.Surface, coordenada: tuple[int, int], texto:str, fuente:pygame.font, color: tuple [int, int, int]= WHITE, background_color: tuple[int, int, int]= None):
    """
    Muestra texto en una superficie de Pygame.

    Args:
    - superficie (pygame.Surface): Superficie en la que se mostrará el texto.
    - coordenada (tuple[int, int]): Coordenadas (x, y) del centro del texto.
    - texto (str): Texto que se mostrará.
    - fuente (pygame.font): Fuente que se utilizará para el texto.
    - color (tuple[int, int, int], opcional): Color RGB del texto (por defecto es BLANCO).
    - background_color (tuple[int, int, int], opcional): Color de fondo RGB del texto (por defecto es None).

    Returns:
    - None
    """
    sup_texto = fuente.render(texto, True, color, background_color)
    rect_texto = sup_texto.get_rect(center = coordenada)
    superficie.blit(sup_texto, rect_texto)
    pygame.display.flip()

def mostrar_temporizador_habilidad(superficie: pygame.Surface, coordenada: tuple[int, int], tiempo_restante: int, fuente: pygame.font, color: tuple[int, int, int] = WHITE):
    """
    Muestra un temporizador de habilidad especial en una superficie de Pygame.

    Args:
    - superficie (pygame.Surface): Superficie en la que se mostrará el temporizador.
    - coordenada (tuple[int, int]): Coordenadas (x, y) del centro del temporizador.
    - tiempo_restante (int): Tiempo restante de la habilidad especial en milisegundos.
    - fuente (pygame.font): Fuente que se utilizará para el texto del temporizador.
    - color (tuple[int, int, int], opcional): Color RGB del texto del temporizador (por defecto es BLANCO).

    Returns:
    - None
    """
    texto = f"Ability Special: {tiempo_restante // 1000}"
    mostrar_texto(superficie, coordenada, texto, fuente, color)

def wait_user(tecla:int):
    """
    Espera a que el usuario presione una tecla específica para continuar.

    Args:
    - tecla (int): Código de tecla específico que se espera que el usuario presione.

    Returns:
    - None
    """
    flag_start = True
    while flag_start:
        for evento in pygame.event.get():
            if evento.type == QUIT:
                terminar()
            if evento.type == KEYDOWN:
                if evento.key == tecla:
                    flag_start = False 

def wait_user_click(rect_button: pygame.Rect):
    """
    Espera a que el usuario haga clic en un área rectangular específica para continuar.

    Args:
    - rect_button (pygame.Rect): Rectángulo del área en la que se espera que el usuario haga clic.

    Returns:
    - None
    """
    flag_start = True
    while flag_start:
        for evento in pygame.event.get():
            if evento.type == QUIT:
               terminar()
            if evento.type == MOUSEBUTTONDOWN:
                if evento.button == 1:
                    if punto_en_rectangulo(evento.pos, rect_button):
                        flag_start = False














