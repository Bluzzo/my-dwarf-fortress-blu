import pygame
import constantes
from personajes import Personaje 
from personajes import Gallina
from mundo import Mundo
import csv

pygame.init()


pygame.display.set_caption("Tachiquin")

def escalar_img(image, scale):
    w = image.get_width()
    h = image.get_height()
    nueva_imagen = pygame.transform.scale(image, (w*scale, h*scale))
    return nueva_imagen


animaciones = []
for i in range(3):
    img = pygame.image.load(f"assets/images/characters/player/player {i} w.png")
    img = escalar_img(img, constantes.ESCALA_PERSONAJE)
    animaciones.append(img)


tile_list = []
for x in range(constantes.TILE_TYPES):
    tile_image = pygame.image.load(f"assets/images/tiles/tile_ ({x+1}).png")
    tile_image = pygame.transform.scale(tile_image,(constantes.TILE_SIZE,constantes.TILE_SIZE))
    tile_list.append(tile_image)

world_data = []     

for fila in range (constantes.FILLAS):
    filas = [0]  * constantes.COLUMNAS
    world_data.append(filas)

#mundo bello
with open("mundo_archivo/mapalol.csv",newline='') as csvfile:
    reader = csv.reader(csvfile,delimiter=',')
    for x, fila in enumerate(reader):
        for y, columna in enumerate(fila):
            world_data[x][y] = int(columna) 

world = Mundo()
world.process_data(world_data,tile_list)



def dibujar_grid():
    for x in range(30):
        pygame.draw.line(ventana,constantes.COLOR_BLANCO,(x*constantes.TILE_SIZE,0),(x*constantes.TILE_SIZE,constantes.ALTO_VENTANA))
        pygame.draw.line(ventana,constantes.COLOR_BLANCO,(0,x*constantes.TILE_SIZE),(constantes.ANCHO_VENTANA,x*constantes.TILE_SIZE))

player_image = pygame.image.load(f"assets/images/characters/player/player 2 w.png")
player_image = escalar_img(player_image,constantes.ESCALA_PERSONAJE)
jugador = Personaje(constantes.ANCHO_PERSONAJE,constantes.ANCHO_PERSONAJE,animaciones)
ventana = pygame.display.set_mode((constantes.ANCHO_VENTANA,constantes.ALTO_VENTANA))


#variables de movimiento
mover_arriba = False
mover_abajo = False
mover_derecha = False
mover_izquierda = False
deltaX = 0
deltaY = 0
reloj = pygame.time.Clock()

def ponerCasa(archivo, click_pos, nuevo_valor):
    x, y = click_pos
    fila = y // constantes.TILE_SIZE
    columna = x // constantes.TILE_SIZE

    # Leer todo el CSV
    with open("mundo_archivo/mapalol.csv", newline='', encoding='utf-8') as f:
        lector = csv.reader(f)
        datos = list(lector)

    # Reemplazar el valor en la posición calculada
    datos[fila][columna] = str(nuevo_valor)

    # Guardar los cambios de nuevo en el CSV
    with open("mundo_archivo/mapalol.csv", 'w', newline='', encoding='utf-8') as f:
        escritor = csv.writer(f)
        escritor.writerows(datos)
    world_data[fila][columna] = nuevo_valor
    
rangoGallina = pygame.Rect(100, 100, 400, 300)  # x, y, ancho, alto

gallina = Gallina(100,200,area = rangoGallina)
gallinas = [
    Gallina(100, 100, area=rangoGallina),
    Gallina(300, 300, area=rangoGallina), 
    Gallina(200, 400, area=rangoGallina)
]
gallinas.append(gallina)

###############################
run = True
while run:
    dt = reloj.tick(constantes.FPS)
    ventana.fill(constantes.COLOR_FONDO)
    
    dibujar_grid()

    deltaX = 0
    deltaY = 0
    #movimiento del jugador
    if mover_derecha == True:
        deltaX = constantes.VELOCIDAD
    if mover_izquierda == True:
        deltaX = -constantes.VELOCIDAD
    if mover_arriba == True:
        deltaY = -constantes.VELOCIDAD
    if mover_abajo == True:
        deltaY = constantes.VELOCIDAD

    #obtener posicion del click
    def obtener_casilla(pos):
        x, y = pos
        columna = x // constantes.TILE_SIZE
        fila = y // constantes.TILE_SIZE
        return fila, columna

    #moverme
    gallina.update(dt)
    jugador.movimiento(deltaX,deltaY)
    jugador.update()
    
    print(f"{deltaX}, {deltaY}")

    world.draw(ventana)

    for gallina in gallinas:
        gallina.update(dt)
        gallina.dibujar(ventana)

    jugador.dibujar(ventana)
    gallina.dibujar(ventana)


    for event in  pygame.event.get():
        #cerrar juego
        if event.type == pygame.QUIT:
            run = False

        # teclas presionadas
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                mover_izquierda = True
            if event.key == pygame.K_d:
                mover_derecha = True
            if event.key == pygame.K_w:
                mover_arriba = True
            if event.key == pygame.K_s:
                mover_abajo = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                mover_izquierda = False
            if event.key == pygame.K_d:
                mover_derecha = False
            if event.key == pygame.K_w:
                mover_arriba = False
            if event.key == pygame.K_s:
                mover_abajo = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                ponerCasa("mundo_archivo/mapalol.csv",event.pos,195)
                fila, columna = obtener_casilla(event.pos)
                print(f"Posicion del click [{fila}, {columna}]")
                
        if event.type == pygame.MOUSEWHEEL:
            if event.y > 0:
                pass
        

                


    pygame.display.update()
pygame.quit()