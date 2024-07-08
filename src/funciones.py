import pygame
from random import *
from sys import *
from settings import *
from bloques import *
from pygame.locals import *



def terminar():
    pygame.quit()
    exit()


def detectar_colision(rect_1, rect_2):
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
    x, y = punto
    return x >= rect.left and x <= rect.right and y >= rect.top and y <= rect.bottom


def distancia_entre_puntos(pto_1:tuple[int, int], pto_2:tuple[int, int])-> float:
    return((pto_1[0] - pto_2[0]) ** 2 + (pto_1[1] - pto_2[1])** 2) ** 0.5

def calcular_radio(rect):
    return rect.width // 2

def detectar_colision_circulos(rect_1, rect_2)->bool:
    r1 = calcular_radio(rect_1)
    r2 = calcular_radio(rect_2)
    distancia = distancia_entre_puntos(rect_1.center, rect_2.center)
    return distancia <= r1 + r2

def mostrar_texto(superficie: pygame.Surface, coordenada: tuple[int, int], texto:str, fuente:pygame.font, color: tuple [int, int, int]= WHITE, background_color: tuple[int, int, int]= None):
    sup_texto = fuente.render(texto, True, color, background_color)
    rect_texto = sup_texto.get_rect(center = coordenada)
    superficie.blit(sup_texto, rect_texto)
    pygame.display.flip()

def mostrar_temporizador_habilidad(superficie: pygame.Surface, coordenada: tuple[int, int], tiempo_restante: int, fuente: pygame.font, color: tuple[int, int, int] = WHITE):
    texto = f"Ability Special: {tiempo_restante // 1000}"
    mostrar_texto(superficie, coordenada, texto, fuente, color)

def wait_user(tecla:int):
    flag_start = True
    while flag_start:
        for evento in pygame.event.get():
            if evento.type == QUIT:
                terminar()
            if evento.type == KEYDOWN:
                if evento.key == tecla:
                    flag_start = False 

def wait_user_click(rect_button: pygame.Rect):
    flag_start = True
    while flag_start:
        for evento in pygame.event.get():
            if evento.type == QUIT:
               terminar()
            if evento.type == MOUSEBUTTONDOWN:
                if evento.button == 1:
                    if punto_en_rectangulo(evento.pos, rect_button):
                        flag_start = False




