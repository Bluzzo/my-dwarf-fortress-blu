import pygame
import constantes
import random as rd

class Personaje:
    def __init__(self,x,y,animaciones):
        #self.shape es la posicion del mono
        self.flip = False
        self.animaciones = animaciones
        #imagen de la animacion
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.image = animaciones[self.frame_index]
        self.shape = pygame.Rect(constantes.ALTO_PERSONAJE,constantes.ANCHO_PERSONAJE,20,20)
        self.shape.center = (x,y)
    
    def update(self):
        cooldown_animacion = 100
        self.image = self.animaciones[self.frame_index]
        if pygame.time.get_ticks() - self.update_time >= cooldown_animacion:
            self.frame_index = self.frame_index + 1
            self.update_time = pygame.time.get_ticks()
        if self.frame_index >= len(self.animaciones):
            self.frame_index = 0
        
    def dibujar(self,interfaz):
        imagen_flip = pygame.transform.flip(self.image, self.flip, False)
        interfaz.blit(imagen_flip,self.shape)
        #pygame.draw.rect(interfaz,constantes.COLOR_PERSONAJE,self.shape,1)
        
    def movimiento(self,deltaX,deltaY):
        if deltaX < 0:
            self.flip = True
        if deltaX > 0:
            self.flip = False
        self.shape.x = self.shape.x + deltaX
        self.shape.y = self.shape.y + deltaY


# 1 cerdo , 2 vaca , 3 gallina

class Animal:
    def __init__(self, x, y, frames, area=None, velocidad=None, escala=0.5):
        # Escalar todas las imágenes
        self.frames = [
            pygame.transform.scale(
                frame,
                (
                    int(frame.get_width() * escala),
                    int(frame.get_height() * escala)
                )
            )
            for frame in frames
        ]
        
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(topleft=(x, y))
        
        # control de animacion
        self.anim_delay = 150
        self.anim_timer = 0
        self.facing_right = False

        # movimiento aleatorio
        self.velocidad = velocidad if velocidad is not None else constantes.VELOCIDAD_ANIMALES
        self.dx = rd.choice([-1, 1])
        self.dy = rd.choice([-1, 1])
        self.area = area if area else pygame.Rect(0, 0, 800, 600)
    
    def actualizar_animacion(self,dt):
        #cambiar el frame en automatico 
        self.anim_timer += dt
        if self.anim_timer >= self.anim_delay:
            self.anim_timer = 0
            self.frame_index = (self.frame_index + 1) % len(self.frames)
            self.image = self.frames[self.frame_index]

    def mover_aleatorio(self,dt):
        self.rect.x += self.dx * self.velocidad * (dt/16)
        self.rect.y += self.dy * self.velocidad * (dt/16)

        #cambiar direccion
        if self.dx > 0:
            self.facing_right = False
        elif self.dx < 0:
            self.facing_right = True

        # Rebotar dentro del área (considerando tamaño de la imagen)
        if self.rect.left < self.area.left:
            self.rect.left = self.area.left
            self.dx *= -1
        if self.rect.right > self.area.right:
            self.rect.right = self.area.right
            self.dx *= -1

        if self.rect.top < self.area.top:
            self.rect.top = self.area.top
            self.dy *= -1
        if self.rect.bottom > self.area.bottom:
            self.rect.bottom = self.area.bottom
            self.dy *= -1


    def update(self,dt):
        self.actualizar_animacion(dt)
        self.mover_aleatorio(dt)

    def dibujar(self,surface):
        img = self.image
        if not self.facing_right:
            img = pygame.transform.flip(img,True ,False)
        surface.blit(img,self.rect)
    
class Gallina(Animal):
    def __init__(self, x, y, area = None):
        frames = [
            pygame.image.load(f"assets/images/animales/gallina/gallina (1).png"),
            pygame.image.load(f"assets/images/animales/gallina/gallina (2).png") , 
            pygame.image.load(f"assets/images/animales/gallina/gallina (3).png"),
            pygame.image.load(f"assets/images/animales/gallina/gallina (4).png"),
            pygame.image.load(f"assets/images/animales/gallina/gallina (5).png")
            ]
        super().__init__(x,y,frames,area)

class Vaca(Animal):
    def __init__(self,x,y, area = None):
        frames = [
            pygame.image.load(f"assets/images/animales/vaca/vaca_01.png"),
            pygame.image.load(f"assets/images/animales/vaca/vaca_02.png"),
            pygame.image.load(f"assets/images/animales/vaca/vaca_03.png")
        ]
        super().__init__(x,y,frames,area, escala=0.3)

class Cerdo(Animal):
    def __init__(self,x,y, area = None):
        frames = [
            pygame.image.load(f"assets/images/animales/cerdo/cerdo_02.png"),
            pygame.image.load(f"assets/images/animales/cerdo/cerdo_01.png"),
            pygame.image.load(f"assets/images/animales/cerdo/cerdo_03.png"),
            pygame.image.load(f"assets/images/animales/cerdo/cerdo_04.png")
            ]
        super().__init__(x,y,frames,area,escala=0.1)

class Personaje:
    def __init__(self, x, y, animaciones, area=None, velocidad=2, escala=0.6):
        # animaciones: diccionario con "idle", "mover", "atacar"
        self.animaciones = {}
        for estado, frames in animaciones.items():
            self.animaciones[estado] = [
                pygame.transform.scale(
                    frame,
                    (
                        int(frame.get_width() * escala),
                        int(frame.get_height() * escala)
                    )
                ) for frame in frames
            ]
        
        self.estado = "idle"
        self.frame_index = 0
        self.image = self.animaciones[self.estado][self.frame_index]
        self.rect = self.image.get_rect(center=(x, y))
        
        self.area = area if area else pygame.Rect(0, 0, 800, 600)
        self.velocidad = velocidad
        self.flip = False
        self.tiempo_anim = 0
        self.delay = 120

        # movimiento automático
        self.dx = rd.choice([-1, 1])
        self.dy = rd.choice([-1, 1])
        self.cambio_direccion_timer = 0
        self.cambio_direccion_delay = 2000  # cada 2 seg cambia de dirección

        # control ataque
        self.atacando = False
        self.modo_auto = True  # True = se mueve solo, False = controlado por jugador

    # -------------------
    def manejar_entrada(self, teclas):
        """Si se presiona una tecla, el personaje pasa a modo jugador."""
        if teclas[pygame.K_SPACE]:
            self.atacar()
            self.modo_auto = False
        elif teclas[pygame.K_LEFT]:
            self.rect.x -= self.velocidad
            self.flip = True
            self.estado = "mover"
            self.modo_auto = False
        elif teclas[pygame.K_RIGHT]:
            self.rect.x += self.velocidad
            self.flip = False
            self.estado = "mover"
            self.modo_auto = False
        else:
            if not self.atacando:
                self.estado = "idle"

    # -------------------
    def atacar(self):
        if not self.atacando:
            self.atacando = True
            self.estado = "atacar"
            self.frame_index = 0
            self.tiempo_anim = 0

    # -------------------
    def mover_aleatorio(self, dt):
        """Movimiento automático dentro del área."""
        self.rect.x += self.dx * self.velocidad * (dt / 16)
        self.rect.y += self.dy * self.velocidad * (dt / 16)

        # Rebotar en los límites del área
        if self.rect.left < self.area.left or self.rect.right > self.area.right:
            self.dx *= -1
        if self.rect.top < self.area.top or self.rect.bottom > self.area.bottom:
            self.dy *= -1

        # cambiar de dirección cada cierto tiempo
        self.cambio_direccion_timer += dt
        if self.cambio_direccion_timer >= self.cambio_direccion_delay:
            self.cambio_direccion_timer = 0
            self.dx = rd.choice([-1, 0, 1])
            self.dy = rd.choice([-1, 0, 1])

        # actualizar flip según dirección
        if self.dx > 0:
            self.flip = False
        elif self.dx < 0:
            self.flip = True

        if not self.atacando:
            self.estado = "mover"

    # -------------------
    def actualizar_animacion(self, dt):
        self.tiempo_anim += dt
        if self.tiempo_anim >= self.delay:
            self.tiempo_anim = 0
            self.frame_index = (self.frame_index + 1) % len(self.animaciones[self.estado])
            self.image = self.animaciones[self.estado][self.frame_index]

    # -------------------
    def update(self, dt, teclas):
        # Control jugador
        self.manejar_entrada(teclas)

        # Movimiento automático si no se está controlando
        if self.modo_auto and not self.atacando:
            self.mover_aleatorio(dt)

        # Cuando termina ataque, vuelve a idle
        if self.atacando:
            if self.frame_index == len(self.animaciones["atacar"]) - 1:
                self.atacando = False
                self.estado = "idle"

        self.actualizar_animacion(dt)

    # -------------------
    def dibujar(self, surface):
        img = self.image
        if self.flip:
            img = pygame.transform.flip(img, True, False)
        surface.blit(img, self.rect)
    
class Japones(Personaje):
    def __init__(self, x, y, area=None):
        animaciones = {
            "mover": [
                pygame.image.load("assets/images/characters/japanese/runnning/japanese (1).png"),
                pygame.image.load("assets/images/characters/japanese/runnning/japanese (2).png"),
                pygame.image.load("assets/images/characters/japanese/runnning/japanese (3).png"),
                pygame.image.load("assets/images/characters/japanese/runnning/japanese (4).png"),
                pygame.image.load("assets/images/characters/japanese/runnning/japanese (5).png"),
                pygame.image.load("assets/images/characters/japanese/runnning/japanese (6).png"),
                pygame.image.load("assets/images/characters/japanese/runnning/japanese (7).png"),
                pygame.image.load("assets/images/characters/japanese/runnning/japanese (8).png")
            ],
            "atacar": [
                pygame.image.load("assets/images/characters/japanese/attack/japaneseA_01.png"),
                pygame.image.load("assets/images/characters/japanese/attack/japaneseA_02.png"),
                pygame.image.load("assets/images/characters/japanese/attack/japaneseA_03.png"),
                pygame.image.load("assets/images/characters/japanese/attack/japaneseA_04.png"),
                pygame.image.load("assets/images/characters/japanese/attack/japaneseA_05.png"),
                pygame.image.load("assets/images/characters/japanese/attack/japaneseA_06.png"),
                pygame.image.load("assets/images/characters/japanese/attack/japaneseA_07.png")
            ],
            "idle": [
                pygame.image.load("assets/images/characters/japanese/runnning/japanese (1).png")
            ]
        }
        super().__init__(x, y, animaciones, area, velocidad=2)
        self.atacando = False
        self.tiempo_ataque = 0
        self.duracion_ataque = 300  # ms que dura el ataque
        self.dx = rd.choice([-1, 1])
        self.dy = rd.choice([-1, 1])

    def update(self, dt, teclas):
        # Si no está atacando, se mueve aleatoriamente
        if not self.atacando:
            self.x += self.dx * self.velocidad
            self.y += self.dy * self.velocidad

            # Cambiar dirección de vez en cuando
            if rd.random() < 0.02:  # 2% de probabilidad por frame
                self.dx = rd.choice([-1, 0, 1])
                self.dy = rd.choice([-1, 0, 1])

            # Limitar a su área (si tiene una)
            if self.area:
                if self.x < self.area.left:
                    self.x = self.area.left
                    self.dx *= -1
                if self.x > self.area.right:
                    self.x = self.area.right
                    self.dx *= -1
                if self.y < self.area.top:
                    self.y = self.area.top
                    self.dy *= -1
                if self.y > self.area.bottom:
                    self.y = self.area.bottom
                    self.dy *= -1

            # cambiar animación a mover
            self.cambiar_animacion("mover")

        # si presionas espacio → ataca
        if teclas[pygame.K_SPACE] and not self.atacando:
            self.atacando = True
            self.tiempo_ataque = pygame.time.get_ticks()
            self.cambiar_animacion("atacar")

        # controlar duración del ataque
        if self.atacando:
            if pygame.time.get_ticks() - self.tiempo_ataque > self.duracion_ataque:
                self.atacando = False  # termina el ataque

        super().update(dt, teclas)
