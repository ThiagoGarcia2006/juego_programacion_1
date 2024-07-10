import pygame
from random import *
from sys import *
from settings import *
from bloques import *
from pygame.locals import *
from funciones import *
import time
import csv
import json


pygame.init() 

clock = pygame.time.Clock()

# configuracion pantalla principal
screen = pygame.display.set_mode(SIZE_SCREEN)
pygame.display.set_caption("Cazador")
pygame.display.set_icon(pygame.image.load(LOGO_TYPE))

#configuro la fuente
fuente_1 = pygame.font.Font(FONT_TYPE, FONT_SIZE)


#cargo imagen
imagen_fondo = pygame.transform.scale(pygame.image.load(SCREEN_TYPE), SIZE_SCREEN)
imagen_fondo_menu = pygame.transform.scale(pygame.image.load(SCREEN_MENU_TYPE), SIZE_SCREEN)
imagen_player = pygame.image.load(IMAGE_PLAYER_TYPE)
imagen_enemy = pygame.image.load(IMAGE_ENEMY_TYPE)
start_button = pygame.transform.scale(pygame.image.load(START_BUTTON_TYPE), START_BUTTON_SIZE)

#cargo sonidos
shot_sound = pygame.mixer.Sound(SHOT_TIPE)
shot_sound.set_volume(0.2)
game_over_sound = pygame.mixer.Sound(GAME_OVER_TYPE)
game_over_sound.set_volume(0.2)
level_sound = pygame.mixer.Sound(LEVEL_TYPE)
collision_sound = pygame.mixer.Sound(COLLISION_TYPE)
collision_sound.set_volume(0.2)


#cargo musica
pygame.mixer.music.load(MUSIC_TYPE)
pygame.mixer.music.set_volume(0.1) 

with open("src/config.json") as f:
    config = json.load(f)


def draw_button(text, rect, color, hover_color, action=None):
    mouse_pos = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    hovered = rect.collidepoint(mouse_pos)
    
    if hovered:
        pygame.draw.rect(screen, hover_color, rect)
        if click[0] == 1 and action:
            pygame.time.delay(200)
            action()
    else:
        pygame.draw.rect(screen, color, rect)
    
    text_surf = fuente_1.render(text, True, BLACK)
    screen.blit(text_surf, (rect.x + (rect.width - text_surf.get_width()) // 2, rect.y + (rect.height - text_surf.get_height()) // 2))

# Acciones de los botones
def go_to_screen1():
    screen1()

def go_to_screen2():
    screen2()

def quit_game():
    pygame.quit()
    exit()

def main_menu():   
    while True:
        screen.fill(WHITE)
        mouse_over_button = False

        # Manejar eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()

        # Dibujar la imagen de fondo del menú
        screen.blit(imagen_fondo_menu, ORIGIN)

        # Dibujar los botones y manejar eventos
        if draw_button("Jugar", pygame.Rect(300, 200, 200, 50), RED, YELLOW, go_to_screen1):
            mouse_over_button = True
        if draw_button("Opciones", pygame.Rect(300, 300, 200, 50), RED, YELLOW, go_to_screen2):
            mouse_over_button = True
        if draw_button("Salir", pygame.Rect(300, 500, 200, 50), RED, YELLOW, quit_game):
            mouse_over_button = True

        # Cambiar el cursor según si se está sobre un botón o no
        if mouse_over_button:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        # Actualizar la pantalla
        pygame.display.flip()

def screen1():
    high_score = 0
    while True:       
        pygame.mouse.set_visible(False)
      
        #inicializo estas variables booleanas al principio de la función
        move_left = False
        move_right = False
        move_up = False
        move_down = False

        #creo al jugador
        block = create_player(imagen_player)
    
        #creo y cargo la lista de enemys
        enemys = []
        load_enemy_list(enemys, INITIAL_ENEMYS, imagen_enemy)

        #puntaje
        lives = 3
        shot = None
        shot_special = None
        score = 0
        counter_collision = 0
        
        #Habilidad especial
        special_ability_active = False
        last_special_ability_time = 0

        #musica 
        pygame.mixer.music.play()
        playing_music = True
        in_pause = False

        #inicio del juego
        is_running = True

        while is_running:
            clock.tick(FPS)
            current_time = pygame.time.get_ticks()  # Obtén el tiempo actual en milisegundos
            tiempo_restante = max(0, special_ability_cooldown - (current_time - last_special_ability_time))  # Calcula el tiempo restante del cooldown
            # ----> detectar los eventos
            for evento in pygame.event.get():
                if evento.type == QUIT:
                    terminar()
                if evento.type == KEYDOWN:
                    if evento.key == K_f:
                            if not shot:
                                shot = create_shot(block["rect"].midright)
                    if evento.key == K_g:
                        if current_time - last_special_ability_time >= special_ability_cooldown:
                            if not shot_special:
                                shot_special = create_shot_special(block["rect"].midright)
                                special_ability_active = True
                            last_special_ability_time = current_time
                    if evento.key == K_m:
                        if playing_music:
                            pygame.mixer.music.pause()
                        else:
                            pygame.mixer.music.unpause()
                        playing_music = not playing_music  
                    if evento.key == K_p:
                        pygame.mixer.music.pause()
                        mostrar_texto(screen, CENTER_SCREEN, "PAUSE", fuente_1, RED)
                        wait_user(K_p)
                        if playing_music:
                            pygame.mixer.music.unpause()                   
                    

                if evento.type == MOUSEBUTTONDOWN:
                    if evento.button == 1:
                        new_enemy = create_enemy()
                        new_enemy["color"] = MAGENTA
                        new_enemy["rect"].center =evento.pos
                        enemys.append(new_enemy)

                if evento.type == MOUSEMOTION:
                    block["rect"].center = evento.pos   



            # Muevo el bloque de acuerdo a su dirección
            if move_left:
                block["rect"].x -= SPEED
            if move_right:
                block["rect"].x += SPEED
            if move_up:
                block["rect"].y -= SPEED
            if move_down:
                block["rect"].y += SPEED

            # Asegurarse de que el bloque no sobresalga de la pantalla
            if block["rect"].left < 0:
                block["rect"].left = 0
            if block["rect"].right > WIDTH:
                block["rect"].right = WIDTH
            if block["rect"].top < 0:
                block["rect"].top = 0
            if block["rect"].bottom > HEIGHT:
                block["rect"].bottom = HEIGHT
                
            pygame.mouse.set_pos(block["rect"].center)

            for enemy in enemys:
                enemy["rect"].move_ip(-enemy["speed_x"], 0)  
                if enemy["rect"].right < 0:  
                    enemy["rect"].left = WIDTH  
                
            if shot:
                shot["rect"].move_ip(shot["speed"], 0)  
                if shot["rect"].left > WIDTH:
                    shot = None

            elif shot_special:
                shot_special["rect"].move_ip(shot_special["speed"], 0)  
                if shot_special["rect"].left > WIDTH:
                    shot_special = None 

            if shot:
                for enemy in enemys:  
                    if shot and detectar_colision(shot["rect"], enemy["rect"]):
                            collision_sound.play()
                            enemys.remove(enemy)
                            shot_sound.play()
                            shot = None
                            score += 1
                            if len(enemys) == 0: 
                                load_enemy_list(enemys, INITIAL_ENEMYS, imagen_enemy)
                                level_sound.play()                        
            else:
                for enemy in enemys.copy():
                    if shot_special and detectar_colision(shot_special["rect"], enemy["rect"]):
                        enemys.remove(enemy)
                        score += 1  
                        collision_sound.play()
                        if len(enemys) == 0:
                            special_ability_active = False
                            load_enemy_list(enemys, INITIAL_ENEMYS, imagen_enemy)
                            level_sound.play()                       
                            
            for enemy in enemys.copy():
                if detectar_colision_circulos(block["rect"], enemy["rect"]):
                    enemys.remove(enemy)
                    lives -= 1
                    if lives == 0:
                        special_ability_active = False
                        last_special_ability_time = pygame.time.get_ticks() + special_ability_cooldown * 1000
                        is_running = False
                        
                
            if counter_collision > 0:  # Comprueba si el contador de colisiones es mayor que 0
                counter_collision -= 1  # Disminuye el contador de colisiones en 1
                block["rect"].width = player_w + 5  # Aumenta el ancho del bloque del jugador en 5 unidades
                block["rect"].height = player_h + 5  # Aumenta la altura del bloque del jugador en 5 unidades
            else:  # Si el contador de colisiones es 0 o menor
                block["rect"].width = player_w  # Restaura el ancho original del bloque del jugador
                block["rect"].height = player_h  # Restaura la altura original del bloque del jugador
                       

            # dibujar pantalla

            screen.blit(imagen_fondo, ORIGIN)

            screen.blit(block["img"], block["rect"])
                
            if shot:
                pygame.draw.rect(screen, shot["color"], shot["rect"])

            if shot_special:
                pygame.draw.rect(screen, shot_special["color"], shot_special["rect"])    

            for enemy in enemys:  
                if enemy ["img"]:
                    screen.blit(enemy["img"], enemy["rect"])
                else:
                    pygame.draw.rect(screen, enemy["color"], enemy["rect"], border_radius = enemy ["radio"])
                
            mostrar_texto(screen, POS_SCORE, f"Score: {score}", fuente_1, RED)
            mostrar_texto(screen, POS_LAST_SCORE, f"Lives: {lives}", fuente_1, RED)
            mostrar_temporizador_habilidad(screen, (WIDTH - 200, HEIGHT - 50), tiempo_restante, fuente_1, WHITE) 

            if not playing_music:
                mostrar_texto(screen, POS_MUTE, "MUTE", fuente_1, RED)


            # actualizo la pantalla

            pygame.display.flip()

        #pantalla fin
        if score > high_score:
            high_score = score
        pygame.mixer.music.stop()
        game_over_sound.play()
        screen.blit(imagen_fondo_menu, ORIGIN)
        mostrar_texto(screen, POS_LAST_SCORE, f"Last score: {score}", fuente_1, BLUE)
        mostrar_texto(screen, POS_HIGH_SCORE, f"High score: {high_score}", fuente_1, BLUE)
        mostrar_texto(screen, CENTER_SCREEN, "Game Over", fuente_1, RED)
        mostrar_texto(screen, (WIDTH // 2, HEIGHT - 50), "Presione SPACE para comenzar", fuente_1, BLUE)
        pygame.display.flip()
        wait_user(K_SPACE)

        # Guardar la puntuación al finalizar el juego
        save_score("Player", score)

        #volver al menú
        pygame.mouse.set_visible(True)
        return main_menu()
               

def screen2():
    while True:
        screen.blit(imagen_fondo_menu, ORIGIN)
        mouse_over_button = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()

        text_surf = fuente_1.render("Opciones", True, BLACK)
        screen.blit(text_surf, (WIDTH // 2 - text_surf.get_width() // 2, HEIGHT // 2 - text_surf.get_height() // 2))

        if draw_button("Volver", pygame.Rect(300, 500, 200, 50), GREEN, YELLOW, main_menu):
            mouse_over_button = True

        if mouse_over_button:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        pygame.display.flip()
     
def save_score(username, final_score):
    """
    Guarda la puntuación del jugador en un archivo CSV.

    Parameters:
    username (str): Nombre de usuario del jugador.
    final_score (int): Puntuación final obtenida por el jugador.

    Raises:
    IOError: Si hay algún problema al intentar abrir o escribir en el archivo CSV.

    """
    try:  
        with open("src/scores.csv", "a", newline="") as f:  # Abre el archivo 'scores.csv' en modo de append (agregar al final) y sin líneas en blanco adicionales
            writer = csv.writer(f)  # Crea un objeto writer para escribir en el archivo CSV
            writer.writerow([username, final_score])  # Escribe una nueva fila en el archivo CSV con el nombre de usuario y la puntuación final
    except IOError as e:  # Si ocurre un error de entrada/salida (IOError), ejecuta el bloque de código dentro del except
        print(f"Error al guardar la puntuación: {e}")  # Imprime un mensaje de error indicando que hubo un problema al guardar la puntuación


# Iniciar la pantalla principal
main_menu()       

