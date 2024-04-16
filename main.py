import pygame
from pygame import mixer
from fighter import Fighter
from pygame.locals import *

mixer.init()
pygame.init()

#pantalla
infoObject = pygame.display.Info()
SCREEN_WIDTH = infoObject.current_w
SCREEN_HEIGHT = infoObject.current_h

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN, pygame.RESIZABLE)
pygame.display.set_caption("FighterZ")

#FPS del juego
clock = pygame.time.Clock()
FPS = 60

#color bar
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)

#Definir variables de juego
intro_count = 3
last_count_update = pygame.time.get_ticks()
score = [0, 0]#player scores. [P1, P2]
round_over = False
ROUND_OVER_COOLDOWN = 2000

#Definir la variables de los peleadore
GOKU_SIZE = 162
GOKU_SCALE = 2.5
GOKU_OFFSET = [72, 2.5]
GOKU_DATA = [GOKU_SIZE, GOKU_SCALE, GOKU_OFFSET]

VEGETA_SIZE = 162
VEGETA_SCALE = 2.5
VEGETA_OFFSET = [72, 2.5]
VEGETA_DATA = [VEGETA_SIZE, VEGETA_SCALE, VEGETA_OFFSET]


#Musica
pygame.mixer.music.load("assets/audio\Canciones de dragon ball z peleas.mp3")
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play(-1, 0.0, 5000)
sword_fx = pygame.mixer.Sound("assets/audio\Weak Melee Impact (DBZ Sound Effects)(MP3_320K).mp3")
sword_fx.set_volume(0.3)
magic_fx = pygame.mixer.Sound("assets/audio/Dragon Ball Z   Heavy Kick sound effect(MP3_320K).mp3")
magic_fx.set_volume(0.3)

#mapas
bg_image = pygame.image.load("assets/images/background/CellArena.png").convert_alpha()

#cargar sprints
goku_sheet = pygame.image.load("assets/images/goku/goku.png").convert_alpha()
vegeta_sheet = pygame.image.load("assets/images/vegeta/vegeta.png").convert_alpha()

#imagen de victoria
victory_img = pygame.image.load("assets/images/icons/victory.png").convert_alpha()

#definir el numero de animaciones
GOKU_ANIMATION_STEPS = [10, 8, 1, 7, 7, 3, 7]
VEGETA_ANIMATION_STEPS = [10, 8, 1, 7, 7, 3, 7]

#font lentras
count_font = pygame.font.Font("assets/fonts/turok.ttf", 80)
score_font = pygame.font.Font("assets/fonts/turok.ttf", 30)

#funcion para poner texto
def draw_text(text, font, text_col, x_ratio, y_ratio):
    img = font.render(text, True, text_col)
    x = int(x_ratio * SCREEN_WIDTH)
    y = int(y_ratio * SCREEN_HEIGHT)
    screen.blit(img, (x, y))

# Función para dibujar la barra de vida
def draw_health_bar(health, x_ratio, y_ratio, width_ratio, height_ratio):
    x = int(x_ratio * SCREEN_WIDTH)
    y = int(y_ratio * SCREEN_HEIGHT)
    width = int(width_ratio * SCREEN_WIDTH)
    height = int(height_ratio * SCREEN_HEIGHT)
    ratio = health / 100
    pygame.draw.rect(screen, WHITE, (x - 2, y - 2, width + 4, height + 4))
    pygame.draw.rect(screen, RED, (x, y, width, height))
    pygame.draw.rect(screen, YELLOW, (x, y, width * ratio, height))
    
#Funcion para dibujar la pantalla
def draw_bg():
  scaled_bg = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
  screen.blit(scaled_bg, (0, 0))

#distacias de inicio
fighter_1_x = int(0.15625 * SCREEN_WIDTH)  # 0.15625 representa aproximadamente el 20% del ancho de la pantalla
fighter_1_y = int(0.6230 * SCREEN_HEIGHT)  # 0.4305 representa aproximadamente el 40% de la altura de la pantalla
fighter_2_x = int(0.800000 * SCREEN_WIDTH)  # 0.546875 representa aproximadamente el 60% del ancho de la pantalla
fighter_2_y = int(0.6230 * SCREEN_HEIGHT)  # 0.4305 representa aproximadamente el 40% de la altura de la pantalla

fighter_1 = Fighter(1, fighter_1_x, fighter_1_y, False, GOKU_DATA, goku_sheet, GOKU_ANIMATION_STEPS, sword_fx, SCREEN_WIDTH, SCREEN_HEIGHT)
fighter_2 = Fighter(2, fighter_2_x, fighter_2_y, True, VEGETA_DATA, vegeta_sheet, VEGETA_ANIMATION_STEPS, magic_fx, SCREEN_WIDTH, SCREEN_HEIGHT)

#Motro de juego
run = True
while run:

  clock.tick(FPS)

  #dibujo de fondo
  draw_bg()

  #Mostra la barra de vida y stadisticas
  draw_health_bar(fighter_1.health, 0.02, 0.02, 0.4, 0.05)
  draw_health_bar(fighter_2.health, 0.58, 0.02, 0.4, 0.05)
  draw_text("P1: " + str(score[0]), score_font, RED, 0.02, 0.1)
  draw_text("P2: " + str(score[1]), score_font, RED, 0.58, 0.1)

  #pantalla de tiempo regresivo
  if intro_count <= 0:
    fighter_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_2, round_over)
    fighter_2.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_1, round_over)
  else:
    draw_text(str(intro_count), count_font, RED, 0.5, 0.3)
  if (pygame.time.get_ticks() - last_count_update) >= 1000:
      intro_count -= 1
      last_count_update = pygame.time.get_ticks()

  #actulizarcion de movimiento
  fighter_1.update()
  fighter_2.update()

  #dibujo de luchadores
  fighter_1.draw(screen)
  fighter_2.draw(screen)

  #contador de puntos
  if round_over == False:
    if fighter_1.alive == False:
      score[1] += 1
      round_over = True
      round_over_time = pygame.time.get_ticks()
    elif fighter_2.alive == False:
      score[0] += 1
      round_over = True
      round_over_time = pygame.time.get_ticks()
  else:
      screen.blit(victory_img, (int(0.36 * SCREEN_WIDTH), int(0.25 * SCREEN_HEIGHT)))
      if pygame.time.get_ticks() - round_over_time > ROUND_OVER_COOLDOWN:
        round_over = False
        intro_count = 3
        fighter_1 = Fighter(1, fighter_1_x, fighter_1_y, False, GOKU_DATA, goku_sheet, GOKU_ANIMATION_STEPS, sword_fx, SCREEN_WIDTH, SCREEN_HEIGHT)
        fighter_2 = Fighter(2, fighter_2_x, fighter_2_y, True, VEGETA_DATA, vegeta_sheet, VEGETA_ANIMATION_STEPS, magic_fx, SCREEN_WIDTH, SCREEN_HEIGHT)

  #bucle de juego
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()
      run = False

    if event.type == VIDEORESIZE:
        new_width, new_height = event.w, event.h
        old_width, old_height = SCREEN_WIDTH, SCREEN_HEIGHT
        for fighter in [fighter_1, fighter_2,]:
            fighter.adjust_position(new_width, new_height, old_width, old_height)
        SCREEN_WIDTH, SCREEN_HEIGHT = new_width, new_height
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)

    if event.type == KEYDOWN:
      if event.key == K_f:
        pygame.quit()


  #actulizador de pantalla
  pygame.display.update()

#salir de juego
pygame.quit()