import pygame
import os # usa un módulo que interactúa con los archivos del programa
import time

pygame.init()


WIDTH, HEIGHT = 900, 500 # lo vamos a usar varias veces
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Fighters") # título de la ventana


# asignamos los colores (los paréntesis son tuplas, listas no modificables)
WHITE = pygame.Color(255, 255, 255)
BLACK = pygame.Color(0, 0, 0)
RED = pygame.Color(255, 0, 0)
YELLOW = pygame.Color(255, 255, 0)
WINDOW_COLOR = pygame.Color(6, 90, 126)
WINDOW_BORDER_COLOR = pygame.Color(11, 68, 93)

# línea de borde para diferenciar la línea de cada bando
BORDER = pygame.Rect(WIDTH//2 - 2.5, 0, 5, HEIGHT)

# Obtenemos los archivos de sonido
BULLET_HIT_SOUND = pygame.mixer.Sound('Assets/Grenade+1.mp3')
BULLET_FIRE_SOUND = pygame.mixer.Sound('Assets/Gun+Silencer.mp3')

# Agregamos formatos de texto
NORMAL_FONT = pygame.font.Font('Assets/PressStart2P-vaV7.ttf', 30)
WINNER_FONT = pygame.font.Font('Assets/PressStart2P-vaV7.ttf', 60)
TITLE_FONT = pygame.font.Font('Assets/PixemonTrialRegular-p7nLK.ttf', 100)

# Asignamos estos datos
FPS = 60
VEL = 5
BULLET_VEL = 7
MAX_BULLETS = 3
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

# Agregamos el disfraz del amarillo
YELLOW_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('Assets', 'spaceship_yellow.png'))
# La rotamos para que mire la dirección correcta
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)

# Lo mismo con el rojo
RED_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('Assets', 'spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)

# Creamos el icono del videojuego
ICON = pygame.image.load(
    os.path.join('Assets', 'favicon.ico'))

pygame.display.set_icon(ICON)

# Agregamos los fondos de espacio
SPACE = pygame.transform.scale(pygame.image.load(
    os.path.join('Assets', 'space.png')), (WIDTH, HEIGHT))

START_BG = pygame.transform.scale(pygame.image.load(
    os.path.join('Assets', 'startBackground.jpg')), (WIDTH, HEIGHT))

# Fondo del juego
def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health, display_red_spaceship, display_yellow_spaceship):
    WIN.blit(SPACE, (0, 0))
    pygame.draw.rect(WIN, WHITE, BORDER)

    red_health_text = NORMAL_FONT.render(
        "Health: " + str(red_health), 1, WHITE)
    yellow_health_text = NORMAL_FONT.render(
        "Health: " + str(yellow_health), 1, WHITE)
    WIN.blit(red_health_text, (WIDTH // 4 * 3 - red_health_text.get_width() // 2, 20))
    WIN.blit(yellow_health_text, (WIDTH // 4 - red_health_text.get_width() // 2, 20))

    if display_yellow_spaceship:
        WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    if display_red_spaceship:
        WIN.blit(RED_SPACESHIP, (red.x, red.y))

    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    pygame.display.update()


def yellow_handle_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0:  # LEFT
        yellow.x -= VEL
    if keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.width < BORDER.x:  # RIGHT
        yellow.x += VEL
    if keys_pressed[pygame.K_w] and yellow.y - VEL > NORMAL_FONT.get_height() + 20:  # UP
        yellow.y -= VEL
    if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT - 15:  # DOWN
        yellow.y += VEL


def red_handle_movement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width:  # LEFT
        red.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH:  # RIGHT
        red.x += VEL
    if keys_pressed[pygame.K_UP] and red.y - VEL > NORMAL_FONT.get_height() + 20:  # UP
        red.y -= VEL
    if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT - 15:  # DOWN
        red.y += VEL


def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            yellow_bullets.remove(bullet)
            pygame.event.post(pygame.event.Event(RED_HIT))
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)

def draw_winner(text):
    if text == "Yellow Wins!":
        winner_color = YELLOW
    else:
        winner_color = RED
    draw_text = WINNER_FONT.render(text, 1, winner_color)
    WIN.blit(draw_text, (WIDTH // 2 - draw_text.get_width() // 2, HEIGHT // 2 - draw_text.get_height() // 2))
    
    pygame.display.update()
    pygame.time.delay(3000)

def start():
    start = True
    while start:

        clock = pygame.time.Clock()
        clock.tick(FPS)

        start_text = NORMAL_FONT.render("PRESS 'ENTER' TO START", 1, YELLOW)
        title_text = TITLE_FONT.render("SPACE FIGHTERS", 1, YELLOW)

        WIN.blit(START_BG, (0, 0))
        WIN.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, HEIGHT // 2 - start_text.get_height() + 100)) # crear función a parte
        WIN.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 2 - title_text.get_height() - 30))
        time.sleep(0.5)
        pygame.display.update()
        WIN.blit(START_BG, (0, 0))
        WIN.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 2 - title_text.get_height() - 30))
        time.sleep(0.5)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit() # podrías poner pygame.quit(), start = False... si este no fuese el programa principal, esto termina el programa directamente
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    start = False
                    main()
                    break

def new_match():
    clock = pygame.time.Clock()
    run = True
    restart_option = True

    while run:
        clock.tick(FPS)

        ASK_WINDOW = pygame.Rect(WIDTH//2 - 250, HEIGHT//2 - 150, 500, 300)
        pygame.draw.rect(WIN, WINDOW_COLOR, ASK_WINDOW)
        pygame.draw.rect(WIN, WINDOW_BORDER_COLOR, ASK_WINDOW, 5)
        # Play again?
        ASK_TEXT = NORMAL_FONT.render("PLAY AGAIN?", 1, WHITE)
        WIN.blit(ASK_TEXT, (WIDTH // 2 - ASK_TEXT.get_width() // 2, HEIGHT // 2 - ASK_TEXT.get_height() // 2 - 50))
        # Options
        yes_font, no_font = NORMAL_FONT, NORMAL_FONT
        yes_color, no_color = WHITE, WHITE

        if restart_option:
            no_color = WINDOW_BORDER_COLOR
        if restart_option == False:
            yes_color = WINDOW_BORDER_COLOR

        yes_text = yes_font.render("YES", 1, yes_color)
        no_text = no_font.render("NO", 1, no_color)

        WIN.blit(yes_text, (WIDTH // 2 - yes_text.get_width() // 2 - 125, HEIGHT // 2 - yes_text.get_height() // 2 + 50))
        WIN.blit(no_text, (WIDTH // 2 - no_text.get_width() // 2 + 125, HEIGHT // 2 - no_text.get_height() // 2 + 50))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                        restart_option = False
                        
                elif event.key == pygame.K_LEFT:
                        restart_option = True

                elif event.key == pygame.K_RETURN:
                    if restart_option:
                        main()
                        break
                    else:
                        quit()
        
        
def main():

    red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    hit_red_cd = 0
    hit_yellow_cd = 0

    blink_red_cd = 0
    blink_yellow_cd = 0

    display_red_spaceship = True
    display_yellow_spaceship = True
    
    red_bullets = []
    yellow_bullets = []

    red_health = 10
    yellow_health = 10

    clock = pygame.time.Clock()
    run = True
    
    #Mecanismo del juego
    while run:
        clock.tick(FPS)
        time_now = pygame.time.get_ticks()

        # Si ha terminado el tiempo de recuperación tras ser golpeado, volverá a ser tangible
        if time_now >= hit_red_cd:
            red.width = SPACESHIP_WIDTH
            display_red_spaceship = True # Por si al terminar el tiempo de parpadeo termina en False
        # Si no, pero ha terminado el tiempo de parpadeo
        elif time_now >= blink_red_cd:
            # cambia de elección de disfraz
            display_red_spaceship = not display_red_spaceship
            # cambia el tiempo de parpadeo
            blink_red_cd = time_now + 200

        if time_now >= hit_yellow_cd:
            yellow.width = SPACESHIP_WIDTH
            display_yellow_spaceship = True
        elif time_now >= blink_yellow_cd:
            # cambia de disfraz
            display_yellow_spaceship = not display_yellow_spaceship
            # cambia el tiempo de parpadeo
            blink_yellow_cd = time_now + 200

        keys_pressed = pygame.key.get_pressed()
        yellow_handle_movement(keys_pressed, yellow)
        red_handle_movement(keys_pressed, red)

        handle_bullets(yellow_bullets, red_bullets, yellow, red)

        draw_window(red, yellow, red_bullets, yellow_bullets,
                    red_health, yellow_health, display_red_spaceship, display_yellow_spaceship)
        

        winner_text = ""
        if red_health <= 0:
            winner_text = "Yellow Wins!"

        if yellow_health <= 0:
            winner_text = "Red Wins!"

        if winner_text != "":
            draw_winner(winner_text)
            new_match()
            break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit() # podrías poner pygame.quit(), run = False... si este no fuese el programa principal, esto termina el programa directamente

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10, 5)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        red.x, red.y + red.height//2 - 2, 10, 5)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            if event.type == RED_HIT:
                hit_red_cd = time_now + 3000
                red_health -= 1
                red.width = 0
                BULLET_HIT_SOUND.play()   

            if event.type == YELLOW_HIT:
                hit_yellow_cd = time_now + 3000
                yellow_health -= 1
                yellow.width = 0
                BULLET_HIT_SOUND.play()

# Básicamente indica que la función solo se ejecuta si es
# el programa principal (no funciona si lo ejecutas como módulo de otro código)
if __name__ == "__main__":
    start()
    quit()