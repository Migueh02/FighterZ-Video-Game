import pygame

class Fighter():
  def __init__(self, player, x, y, flip, data, sprite_sheet, animation_steps, sound, screen_width, screen_height):
    self.screen_width = screen_width
    self.screen_height = screen_height
    self.player = player
    self.size = data[0]
    self.image_scale = data[1]
    self.offset = data[2]
    self.flip = flip
    self.animation_list = self.load_images(sprite_sheet, animation_steps)
    self.action = 0#0:quieto #1:correr #2:saltar #3:ataque1 #4: ataque2 #5:golpe #6:muerte
    self.frame_index = 0
    self.image = self.animation_list[self.action][self.frame_index]
    self.update_time = pygame.time.get_ticks()
    self.rect = pygame.Rect((x, y, 80, 180))
    self.vel_y = 0
    self.running = False
    self.jump = False
    self.attacking = False
    self.attack_type = 0
    self.attack_cooldown = 0
    self.attack_sound = sound
    self.hit = False
    self.health = 100
    self.alive = True
  
  def adjust_position(self, new_width, new_height, old_width, old_height):
    ratio_x = new_width / old_width
    ratio_y = new_height / old_height
    self.rect.x = int(self.rect.x * ratio_x)
    self.rect.y = int(self.rect.y * ratio_y)

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


  def move(self, screen_width, screen_height, surface, target, round_over):
    SPEED = 7
    GRAVITY = 2
    dx = 0
    dy = 0
    self.running = False
    self.attack_type = 0

    #get keypresses
    key = pygame.key.get_pressed()

    if self.attacking == False and self.alive == True and round_over == False:
      #controles del player
      if self.player == 1:
        #movimientps
        if key[pygame.K_a]:
          dx = -SPEED
          self.running = True
        if key[pygame.K_d]:
          dx = SPEED
          self.running = True
        #salto
        if key[pygame.K_w] and self.jump == False:
          self.vel_y = -30
          self.jump = True
        #ataque
        if key[pygame.K_r] or key[pygame.K_t]:
          self.attack(target)
          #botones de atque 1 y 2
          if key[pygame.K_r]:
            self.attack_type = 1
          if key[pygame.K_t]:
            self.attack_type = 2


      #Controles del player 2
      if self.player == 2:
        #movimientos
        if key[pygame.K_LEFT]:
          dx = -SPEED
          self.running = True
        if key[pygame.K_RIGHT]:
          dx = SPEED
          self.running = True
        #Salto
        if key[pygame.K_UP] and self.jump == False:
          self.vel_y = -30
          self.jump = True
        #ataque
        if key[pygame.K_o] or key[pygame.K_p]:
          self.attack(target)
          #atque 1 y aque 2
          if key[pygame.K_o]:
            self.attack_type = 1
          if key[pygame.K_p]:
            self.attack_type = 2


    #aplicar gravedad
    self.vel_y += GRAVITY
    dy += self.vel_y

    #limites de pantalla
    if self.rect.left + dx < 0:
      dx = -self.rect.left
    if self.rect.right + dx > screen_width:
      dx = screen_width - self.rect.right
    if self.rect.bottom + dy > screen_height - 110:
      self.vel_y = 0
      self.jump = False
      dy = screen_height - 110 - self.rect.bottom

    #cuando los dos jugadores estan serca el perfil de mirda cambia
    if target.rect.centerx > self.rect.centerx:
      self.flip = False
    else:
      self.flip = True

    #aplicar tiempo de ataque
    if self.attack_cooldown > 0:
      self.attack_cooldown -= 1

    #actulizacion de posicionamiento de jugador 
    self.rect.x += dx
    self.rect.y += dy


  #Animacion de los sprints de los personajes
  def update(self):
    #comprobar qué acción está realizando el jugador
    if self.health <= 0:
      self.health = 0
      self.alive = False
      self.update_action(6)#6:Muerte
    elif self.hit == True:
      self.update_action(5)#5:Golpe
    elif self.attacking == True:
      if self.attack_type == 1:
        self.update_action(3)#3:attack1
      elif self.attack_type == 2:
        self.update_action(4)#4:attack2
    elif self.jump == True:
      self.update_action(2)#2:salto
    elif self.running == True:
      self.update_action(1)#1:correr
    else:
      self.update_action(0)#0:quieto

    animation_cooldown = 130
    #actulizacion de imagen
    self.image = self.animation_list[self.action][self.frame_index]
    #comprobar si ha pasado suficiente tiempo desde la última actualización
    if pygame.time.get_ticks() - self.update_time > animation_cooldown:
      self.frame_index += 1
      self.update_time = pygame.time.get_ticks()
    #comprobar si la animación ha terminado
    if self.frame_index >= len(self.animation_list[self.action]):
      #Si el jugador está muerto, entonces termina la animación
      if self.alive == False:
        self.frame_index = len(self.animation_list[self.action]) - 1
      else:
        self.frame_index = 0
        #comprobar si se ejecutó un ataque
        if self.action == 3 or self.action == 4:
          self.attacking = False
          self.attack_cooldown = 10
        #comprobar si se sufrió daño
        if self.action == 5:
          self.hit = False
          #si el jugador estaba en medio de un ataque, entonces el ataque se detiene
          self.attacking = False
          self.attack_cooldown = 10


  def attack(self, target):
    if self.attack_cooldown == 0:
      #ejecutar ataque
      self.attacking = True
      self.attack_sound.play()
      attacking_rect = pygame.Rect(self.rect.centerx - (0.7 * self.rect.width * self.flip), self.rect.y, 0.7 * self.rect.width, self.rect.height)
      if attacking_rect.colliderect(target.rect):
        target.health -= 10
        target.hit = True


  def update_action(self, new_action):
    #comprobar si la nueva acción es diferente a la anterior
    if new_action != self.action:
      self.action = new_action
      #actualizar la configuración de animación
      self.frame_index = 0
      self.update_time = pygame.time.get_ticks()


  def draw(self, surface):
    img = pygame.transform.flip(self.image, self.flip, False)
    surface.blit(img, (self.rect.x - (self.offset[0] * self.image_scale), self.rect.y - (self.offset[1] * self.image_scale)))