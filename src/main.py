import pygame
from random import *
from sys import *
from settings import *
from bloques import *
from pygame.locals import *
from funciones import *
import time


pygame.init() 

clock = pygame.time.Clock()

# configuracion pantalla principal
screen = pygame.display.set_mode(SIZE_SCREEN)
pygame.display.set_caption("Cazador")
pygame.display.set_icon(pygame.image.load("./src/assets/images/logo.png"))

#configuro la fuente
fuente_1 = pygame.font.Font("./src/assets/font/dash-horizon.otf", 48)

#cargo imagen
imagen_fondo = pygame.transform.scale(pygame.image.load("./src/assets/images/fondo.jpg"), SIZE_SCREEN)
imagen_player = pygame.image.load("./src/assets/images/player.png")
imagen_enemy = pygame.image.load("./src/assets/images/enemy.png")
start_button = pygame.transform.scale(pygame.image.load("./src/assets/images/start_button.png"), START_BUTTON_SIZE)

#cargo sonidos
disparo = pygame.mixer.Sound("./src/assets/sounds/disparo.mp3")
game_over_sound = pygame.mixer.Sound("./src/assets/sounds/game_over.mp3")
game_over_sound.set_volume(0.2)
level_sound = pygame.mixer.Sound("./src/assets/sounds/exito.mp3")
collision_sound = pygame.mixer.Sound("./src/assets/sounds/enemy.mp3")

#cargo musica
pygame.mixer.music.load("./src/assets/sounds/musica.mp3")
pygame.mixer.music.set_volume(0.1) 

high_score = 0


while True:
    #Pantalla inicio
    pygame.mouse.set_visible(True)
    screen.fill(BLACK)
    mostrar_texto(screen, POS_TITLE, "Cazador", fuente_1, RED)
    rect_start_button = start_button.get_rect(center = CENTER_SCREEN)
    screen.blit(start_button, rect_start_button)
    pygame.display.flip()
    wait_user_click(rect_start_button)

    pygame.mouse.set_visible(False)

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
                    if current_time - last_special_ability_time > special_ability_cooldown:
                        if not shot_special:
                            shot_special = create_shot_special(block["rect"].midright)
                            special_ability_active = True
                        last_special_ability_time = current_time
                if evento.key == K_DOWN or evento.key == K_s:
                    move_down = True
                    move_up = False  
                if evento.key == K_UP or evento.key == K_w:
                    move_up = True
                    move_down = False               
                if evento.key == K_LEFT or evento.key == K_a:
                    move_left = True
                    move_right = False
                if evento.key == K_RIGHT or evento.key == K_d:
                    move_right = True
                    move_left = False
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
                
    
            if evento.type == KEYUP:
                if evento.key == K_DOWN or evento.key == K_s:
                    move_down = False
                if evento.key == K_UP or evento.key == K_w:
                    move_up = False              
                if evento.key == K_LEFT or evento.key == K_a:
                    move_left = False
                if evento.key == K_RIGHT or evento.key == K_d:
                    move_right = False

            if evento.type == MOUSEBUTTONDOWN:
                if evento.button == 1:
                    new_enemy = create_enemy()
                    new_enemy["color"] = MAGENTA
                    new_enemy["rect"].center =evento.pos
                    enemys.append(new_enemy)

            if evento.type == MOUSEMOTION:
                block["rect"].center = evento.pos   


        # muevo el bloque de acuerdo a su direccion

        if move_left and block ["rect"].left > 0:
            block["rect"].x -= SPEED
            if block ["rect"].left < 0:
                block ["rect"].left = 0
        if move_right and block ["rect"].right < WIDTH:
            block["rect"].x += SPEED
            if block ["rect"].right > WIDTH:
                block ["rect"].right = WIDTH
        if move_up and block ["rect"].top > 0:
            block["rect"].y -= SPEED
            if block ["rect"].top < 0:
                block ["rect"].top = 0
        if move_down and block ["rect"].bottom < HEIGHT:
            block["rect"].y += SPEED
            if block ["rect"].bottom > HEIGHT:
                block ["rect"].bottom = HEIGHT
            
        pygame.mouse.set_pos(block["rect"].center)

        for enemy in enemys:
            enemy["rect"].move_ip(-enemy["speed_x"], 0)  # Mueve el enemigo hacia la izquierda
            if enemy["rect"].right < 0:  # Si el enemigo sale de la pantalla por la izquierda
                enemy["rect"].left = WIDTH  # Reposiciona el enemigo en el borde derecho
            
        if shot:
            shot["rect"].move_ip(shot["speed"], 0)  
            if shot["rect"].left > WIDTH:
                shot = None

        if shot_special:
            shot_special["rect"].move_ip(shot_special["speed"], 0)  
            if shot_special["rect"].left > WIDTH:
                shot_special = None 

        if shot:
            for enemy in enemys:  
                if shot and detectar_colision(shot["rect"], enemy["rect"]):
                        collision_sound.play()
                        enemys.remove(enemy)
                        disparo.play()
                        shot = None
                        score += 1
                        if len(enemys) == 0: 
                            load_enemy_list(enemys, INITIAL_ENEMYS, imagen_enemy)
                            level_sound.play()                        
        else:
            for enemy in enemys.copy():
                if shot_special and detectar_colision(shot_special["rect"], enemy["rect"]):
                    enemys.remove(enemy)
                    shot_special = None
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
                    is_running = False
                    
            
        if counter_collision > 0:
            counter_collision -= 1
            block["rect"].width = player_w + 5
            block["rect"].height = player_h + 5
        else:
            block["rect"].width = player_w 
            block["rect"].height = player_h                       

        # dibujar pantalla

        screen.blit(imagen_fondo, ORIGIN)

        screen.blit(block["img"], block["rect"])
            
        if shot:
            pygame.draw.rect(screen, shot["color"], shot["rect"])

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
    screen.fill(BLACK)
    mostrar_texto(screen, POS_LAST_SCORE, f"Last score: {score}", fuente_1, BLUE)
    mostrar_texto(screen, POS_HIGH_SCORE, f"High score: {high_score}", fuente_1, BLUE)
    mostrar_texto(screen, CENTER_SCREEN, "Game Over", fuente_1, RED)
    mostrar_texto(screen, (WIDTH // 2, HEIGHT - 50), "Presione SPACE para comenzar", fuente_1, BLUE)
    pygame.display.flip()
    wait_user(K_SPACE)

terminar()
