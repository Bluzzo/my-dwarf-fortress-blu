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
    def __init__(self,x,y,frames,area = None,velocidad = None):
        #imagen solamente
        self.frames = frames
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(topleft=(x, y))
        

        #control de animacion
        self.anim_delay = 150
        self.anim_timer = 0
        self.facing_right = False

        #movimiento aleatorio 
        self.velocidad = velocidad
        self.dx = rd.choice([-1,1])
        self.dy = rd.choice([-1,1])
        self.area = area if area else pygame.Rect(0,0,800,600)

        #velocidad 
        self.velocidad = velocidad if velocidad is not None else constantes.VELOCIDAD_ANIMALES
    
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
            pygame.image.load(f"EDATACHI/assets/images/animales/gallina/gallina (1).png"),
            pygame.image.load(f"EDATACHI/assets/images/animales/gallina/gallina (2).png") , 
            pygame.image.load(f"EDATACHI/assets/images/animales/gallina/gallina (3).png"),
            pygame.image.load(f"EDATACHI/assets/images/animales/gallina/gallina (4).png"),
            pygame.image.load(f"EDATACHI/assets/images/animales/gallina/gallina (5).png")
            ]
        super().__init__(x,y,frames)