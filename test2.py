import pygame

pygame.init()

# Pantalla
H, W = 900, 675
pantalla = pygame.display.set_mode((H, W))
# icono y titulo
pygame.display.set_caption('Videogame')
icono = pygame.image.load('img/icont/icont.png')
pygame.display.set_icon(icono)

# Fondo del juego
fondo = pygame.image.load('img/fondos/CellArena.png')

class enemigo:
    def __init__(self, pantalla):
        # Pantalla
        self.pantalla = pantalla
        
        # Movimientos de imagen
        self.quieto = pygame.image.load('img/character/vegetta/Vegeta_10_1.png')

        # Cargar imágenes de caminar como listas
        self.caminar_derecha =  [pygame.image.load('img/character/vegetta/Vegeta_11_1.png'),
                 pygame.image.load('img/character/vegetta/Vegeta_11_1.png'),
                 pygame.image.load('img/character/vegetta/Vegeta_11_1.png'),
                 pygame.image.load('img/character/vegetta/Vegeta_11_1.png'),
                 pygame.image.load('img/character/vegetta/Vegeta_11_1.png'),
                 pygame.image.load('img/character/vegetta/Vegeta_11_1.png')]
        
        self.caminar_izquierda = [pygame.image.load('img/character/vegetta/Vegeta_13_1.png'), 
                 pygame.image.load('img/character/vegetta/Vegeta_13_1.png'),
                 pygame.image.load('img/character/vegetta/Vegeta_13_1.png'),
                 pygame.image.load('img/character/vegetta/Vegeta_13_1.png'),
                 pygame.image.load('img/character/vegetta/Vegeta_13_1.png'),
                 pygame.image.load('img/character/vegetta/Vegeta_13_1.png')]
        
        self.Volar = [pygame.image.load('img/character/vegetta/Vegeta_09_1.png'),
                      pygame.image.load('img/character/vegetta/Vegeta_09_1.png'), 
                      pygame.image.load('img/character/vegetta/Vegeta_09_1.png')]

        self.abajo = [pygame.image.load('img/character/vegetta/Vegeta_09_1.png'),
                      pygame.image.load('img/character/vegetta/Vegeta_09_1.png'), 
                      pygame.image.load('img/character/vegetta/Vegeta_09_1.png')]
        
        self.saltar = [pygame.image.load('img/character/vegetta/Vegeta_19_1.png'),
         pygame.image.load('img/character/vegetta/Vegeta_20_1.png')]

        # Posición del personaje
        self.px = 800
        self.py = 550
        self.velocidad = 10
        
        self.Volar_ = False
        self.abajo_ = False

        # Variable salto
        self.salto = False
        # Altura de salto
        self.cuantosalto = 10

        # Variable izquierda
        self.izquierda = False
        self.derecha = False

        # Pasos
        self.cuenta_pasos = 0
        

    def dibujar(self):
     if self.izquierda:
        self.pantalla.blit(self.caminar_izquierda[0], (int(self.px), int(self.py)))
        self.cuenta_pasos += 1
        
     elif self.derecha:
          self.pantalla.blit(self.caminar_derecha[0], (int(self.px), int(self.py)))
          self.cuenta_pasos += 1
        
     elif self.salto + 1 >= 2:
          self.pantalla.blit(self.saltar[0], (int(self.px), int(self.py)))
          self.cuenta_pasos += 1
          
     elif self.Volar_ + 1 >= 2:
          self.pantalla.blit(self.Volar[0], (int(self.px), int(self.py)))
          self.cuenta_pasos +=1
      
     elif self.abajo_ + 1 >= 2:
          self.pantalla.blit(self.abajo[0], (int(self.px), int(self.py)))
          self.cuenta_pasos +=1
          
     else:
          self.pantalla.blit(self.quieto, (int(self.px), int(self.py)))


    def actualizar_posicion(self, keys):
        # Tecla A - Movimiento a la izquierda
        if keys[pygame.K_LEFT] and self.px > self.velocidad:
            self.px -= self.velocidad
            self.izquierda = True
            self.derecha = False

        # Tecla D - Movimiento a la Derecha
        elif keys[pygame.K_RIGHT] and self.px < 860 - self.velocidad - 40:
            self.px += self.velocidad
            self.izquierda = False
            self.derecha = True

        # personaje quieto
        else:
            self.izquierda = False
            self.derecha = False
            self.cuenta_pasos = 0
            
        #Abajo
        if keys[pygame.K_DOWN] and self.py < 550:
           self.py += self.velocidad
           self.abajo_ = True
        else:
           self.abajo_ = False
      
        # Tecla W - Volar   
        if keys[pygame.K_UP] and self.py > 20:
           self.py -= self.velocidad
           self.Volar_ = True
        else:
           self.Volar_ = False

        # Tecla Space - salto
        if not self.salto:
            if keys[pygame.K_RCTRL]:
                self.salto = True
                self.izquierda = False
                self.derecha = False
                self.cuenta_pasos = 0
        else:
            if self.cuantosalto >= -10:
                self.py -= (self.cuantosalto * abs(self.cuantosalto)) * 0.5
                self.cuantosalto -= 1
            else:
                self.cuantosalto = 10
                self.salto = False

class jugador_:
    def __init__(self, pantalla):
        # Pantalla
        self.pantalla = pantalla
        
        # Movimientos de imagen
        self.quieto = pygame.image.load('img/character/goku/Goku_12.png')

        # Cargar imágenes de caminar como listas
        self.caminar_derecha =  [pygame.image.load('img/character/goku/Goku_15.png'),
                 pygame.image.load('img/character/goku/Goku_15.png'),
                 pygame.image.load('img/character/goku/Goku_15.png'),
                 pygame.image.load('img/character/goku/Goku_15.png'),
                 pygame.image.load('img/character/goku/Goku_15.png'),
                 pygame.image.load('img/character/goku/Goku_15.png')]
        
        self.caminar_izquierda = [pygame.image.load('img/character/goku/Goku_14.png'), 
                 pygame.image.load('img/character/goku/Goku_14.png'),
                 pygame.image.load('img/character/goku/Goku_14.png'),
                 pygame.image.load('img/character/goku/Goku_14.png'),
                 pygame.image.load('img/character/goku/Goku_14.png'),
                 pygame.image.load('img/character/goku/Goku_14.png')]
        
        self.Volar = [pygame.image.load('img/character/goku/Goku_11.png'), 
                      pygame.image.load('img/character/goku/Goku_11.png')]

        self.abajo = [pygame.image.load('img/character/goku/Goku_11.png'), 
                      pygame.image.load('img/character/goku/Goku_11.png')]
        
        self.saltar = [pygame.image.load('img/character/goku/Goku_13.png'),
                      pygame.image.load('img/character/goku/Goku_13.png'),
                      pygame.image.load('img/character/goku/Goku_13.png')]

        # Posición del personaje
        self.px = 100
        self.py = 550
        self.velocidad = 10
        
        self.Volar_ = False
        self.abajo_ = False
        # Variable salto
        self.salto = False
        # Altura de salto
        self.cuantosalto = 10

        # Variable izquierda
        self.izquierda = False
        self.derecha = False

        # Pasos
        self.cuenta_pasos = 0
        

    def dibujar(self):
     if self.izquierda:
        self.pantalla.blit(self.caminar_izquierda[0], (int(self.px), int(self.py)))
        self.cuenta_pasos += 1
        
     elif self.derecha:
          self.pantalla.blit(self.caminar_derecha[0], (int(self.px), int(self.py)))
          self.  cuenta_pasos += 1
        
     elif self.salto + 1 >= 2:
          self.pantalla.blit(self.saltar[0], (int(self.px), int(self.py)))
          self.cuenta_pasos += 1
          
     elif self.Volar_ + 1 >= 2:
          self.pantalla.blit(self.Volar[0], (int(self.px), int(self.py)))
          self.cuenta_pasos +=1
      
     elif self.abajo_ + 1 >= 2:
          self.pantalla.blit(self.abajo[0], (int(self.px), int(self.py)))
          self.cuenta_pasos +=1
          
     else:
          self.pantalla.blit(self.quieto, (int(self.px), int(self.py)))


    def actualizar_posicion(self, keys):
        # Tecla A - Movimiento a la izquierda
        if keys[pygame.K_a] and self.px > self.velocidad:
            self.px -= self.velocidad
            self.izquierda = True
            self.derecha = False

        # Tecla D - Movimiento a la Derecha
        elif keys[pygame.K_d] and self.px < 860 - self.velocidad - 40:  # 40 es el ancho del personaje
            self.px += self.velocidad
            self.izquierda = False
            self.derecha = True

        # personaje quieto
        else:
           self.izquierda = False
           self.derecha = False
           self.cuenta_pasos = 0
        #Abajo
        if keys[pygame.K_s] and self.py < 550:
           self.py += self.velocidad
           self.abajo_ = True
        else:
           self.abajo_ = False
      
        # Tecla W - Volar   
        if keys[pygame.K_w] and self.py > 20:
           self.py -= self.velocidad
           self.Volar_ = True
        else:
           self.Volar_ = False
        # Movientos del Teclado

        # Tecla W - Movimiento salto
        if keys[pygame.K_w] and self.py > 20:
            self.py -= self.velocidad

        # Tecla S - Movimiento a la izquierda
        if keys[pygame.K_s] and self.py < 550:
            self.py += self.velocidad

        # Tecla Space - salto
        if not self.salto:
            if keys[pygame.K_SPACE]:
                self.salto = True
                self.izquierda = False
                self.derecha = False
                self.cuenta_pasos = 0
        else:
            if self.cuantosalto >= -10:
                self.py -= (self.cuantosalto * abs(self.cuantosalto)) * 0.5
                self.cuantosalto -= 1
            else:
                self.cuantosalto = 10
                self.salto = False

reloj = pygame.time.Clock()

enemigo1 = enemigo(pantalla)
jugador1 = jugador_(pantalla)

ejecute = True

while ejecute:
    reloj.tick(18)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            ejecute = False

    # Obtener teclas presionadas
    keys = pygame.key.get_pressed()

    # Actualizar posición de los personajes
    enemigo1.actualizar_posicion(keys)
    jugador1.actualizar_posicion(keys)

    # Dibujar los personajes y actualizar la pantalla
    pantalla.blit(fondo, (0, 0))  # Dibuja el fondo en la posición (0, 0)
    enemigo1.dibujar()
    jugador1.dibujar()
    pygame.display.update()

# Salida del juego
pygame.quit()