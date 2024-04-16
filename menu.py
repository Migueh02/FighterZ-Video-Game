import pygame
from pygame import mixer
import sys

mixer.init()
pygame.init()

infoObject = pygame.display.Info()
SCREEN_WIDTH = infoObject.current_w
SCREEN_HEIGHT = infoObject.current_h
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption("Singel Player")

#Musica
pygame.mixer.music.load("assets/audio/y2mate.com - TODAS LAS CANCIONES DE DRAGON BALLZ KAIGT.mp3")
pygame.mixer.music.set_volume(0)
pygame.mixer.music.play(-1, 0.0, 5000)

#FPS del juego
Clock = pygame.time.Clock()
FPS = 60

main_font = pygame.font.Font("Menu/bg/Saiyan-Sans Right Oblique.ttf", 30)

bg_image = pygame.image.load("Menu/bg/gb.png")

abc_sheet = pygame.image.load("Menu/bg/sprints.png").convert_alpha()

Titulo= pygame.image.load("Menu/bg/logo.png")

ABC_SIZE = 200
ABC_SCALE = 1.8
ABC_OFFSET =[120, 230]
ABC_DATA = [ABC_SIZE, ABC_SCALE, ABC_OFFSET]

ABC_ANIMATION_STEPS = [14]

class Button():
    def __init__(self, image, x_pos, y_pos, text_input):

        self.image = image
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_input = text_input
        self.text = main_font.render(self.text_input, True, "white")
        # Ajuste del rectángulo del texto para tener un área más grande
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect.topleft = (self.x_pos - self.text_rect.width // 2, self.y_pos - self.text_rect.height // 2)

    def update(self):
        screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def draw(self, screen):
        current_frame = 0 # Puedes cambiar esto para hacer la animación más dinámica
        screen.blit(self.animation_list[0][current_frame], (200, 310)) # Cambia las coordenadas según tu necesidad

    def checkForInput(self, position):
        if self.text_rect.collidepoint(position):
            print(f"{self.text_input} Button Press!")

    def changeColor(self, position):
        if self.text_rect.collidepoint(position):
            self.text = main_font.render(self.text_input, True, "red")
        else:
            self.text = main_font.render(self.text_input, True, "white")

class Sprits():
    def __init__(self, x, y, data, sprite_sheet, animation_steps):
       self.size = data[0]
       self.image_scale = data[1]
       self.offset = data[2]
       self.action = 0
       self.frame_index = 0    
       self.animation_list = self.load_images(sprite_sheet, animation_steps) 
       self.image = self.animation_list[self.action][self.frame_index]
       self.update_time = pygame.time.get_ticks()
       self.rect = pygame.Rect((x, y, 80, 180))

    def load_images(self, sprite_sheet, animation_steps):
      #secuencia constante de los sprits
      animation_list = []
      for y, animation in enumerate(animation_steps):
        temp_img_list = []
        for x in range(animation):
          temp_img = sprite_sheet.subsurface(x * self.size, y * self.size, self.size, self.size)
          temp_img_list.append(pygame.transform.scale(temp_img, (self.size * self.image_scale, self.size * self.image_scale)))
        animation_list.append(temp_img_list)
      return animation_list
    
    def update(self):
        animation_cooldown = 400
        self.image = self.animation_list[self.action][self.frame_index]
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index = 0

    def draw(self,surface):
        surface.blit(self.image, (self.rect.x -(self.offset[0] * self.image_scale), self.rect.y - (self.offset[1] * self.image_scale)))


button_surface = pygame.image.load("Menu/bg/buttom.png")

Titulo = pygame.transform.scale(Titulo, (600, 526))

button_surface = pygame.transform.scale(button_surface, (400, 240))

button1_x = int(0.781 * SCREEN_WIDTH)
button2_x = int(0.781 * SCREEN_WIDTH)
button3_x = int(0.781 * SCREEN_WIDTH)
button4_x = int(0.781 * SCREEN_WIDTH)
button_y = int(0.444 * SCREEN_HEIGHT) 

button1 = Button(button_surface, button4_x, button_y -100, "Single Player")
button2 = Button(button_surface, button4_x, button_y, "Two Players")
button3 = Button(button_surface, button4_x, button_y + 100, "Options")
button4 = Button(button_surface, button4_x, button_y + 200, "EXIT")

abc = Sprits(int(0.156 * SCREEN_WIDTH), int(0.400 * SCREEN_HEIGHT), ABC_DATA, abc_sheet, ABC_ANIMATION_STEPS)
Titulo = pygame.transform.scale(Titulo, (int(SCREEN_WIDTH * 0.469), int(SCREEN_HEIGHT * 0.731)))

def draw_bg():
  scaled_bg = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
  screen.blit(scaled_bg, (0, 0))

run_game = False
run = True
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Eventos para el botón "Single Player"
        if event.type == pygame.MOUSEBUTTONDOWN:
            if button1.rect.collidepoint(event.pos):
                run_game = True

        # Eventos para el botón "Two Players"
        if event.type == pygame.MOUSEBUTTONDOWN:
            if button2.rect.collidepoint(event.pos):
                print("Two Players Button Pressed!")  # Aquí puedes poner la lógica correspondiente

        # Eventos para el botón "Options"
        if event.type == pygame.MOUSEBUTTONDOWN:
            if button3.rect.collidepoint(event.pos):
                print("Options Button Pressed!")  # Aquí puedes poner la lógica correspondiente

        # Eventos para el botón "EXIT"
        if event.type == pygame.MOUSEBUTTONDOWN:
            if button4.rect.collidepoint(event.pos):
                pygame.quit()
                sys.exit()

    if run_game:
        try:
            exec(open('main.py').read())
        except FileNotFoundError:
            print("El archivo no fue encontrado.")
        run_game = False
    
    Clock.tick(FPS)
    draw_bg()

    abc.update()

    abc.draw(screen)

    screen.blit(Titulo, (30, 80))

    button1.update()
    button2.update()
    button3.update()
    button4.update()


    button1.changeColor(pygame.mouse.get_pos())
    button2.changeColor(pygame.mouse.get_pos())
    button3.changeColor(pygame.mouse.get_pos())
    button4.changeColor(pygame.mouse.get_pos())

    pygame.display.update()
