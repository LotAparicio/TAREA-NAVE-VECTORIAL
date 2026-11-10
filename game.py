import pygame
import math
import sys


pygame.init()
print("Pygame inicio exitosamente");
print("Version de Pygame: " + pygame.version.ver)

ANCHO, ALTO = 800, 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Mi juego con Pygame")
reloj = pygame.time.Clock()

def transformar_vertice(vertice, posx, posy, escala, angulo):
    x, y = vertice
    # Aplicar escala
    x_esc = x * escala
    y_esc = y * escala
    # Aplicar rotación
    rad = math.radians(angulo)
    x_rot = x_esc * math.cos(rad) - y_esc * math.sin(rad)
    y_rot = x_esc * math.sin(rad) + y_esc * math.cos(rad)
    # Aplicar traslación
    x_final = x_rot + posx
    y_final = y_rot + posy
    return (x_final, y_final)

# Modelo del triangulo, centrado en el origen
modelo_triangulo = [(0, -30), (-20, 20), (20, 20)] 

# Variables de posición y transformación
posx, posy = 400, 300
escala = 1.5
angulo = 0

# Configuracion de velocidad de la nave
VELOCIDAD = 250
VELOCIDAD_ROTACION = 180
VELOCIDAD_ESCALA = 1.5

# Configuracion de las balas
VELOCIDAD_BALA = 500
figura_bala = [(0, -5), (-2, 5), (2, 5)]
color_bala = (255, 50, 50)
balas = []

# Configuración de límites de escala y colores
ESCALA_MINIMA, ESCALA_MAXIMA = 0.25, 5
COLOR_FONDO = (18, 18, 28)
COLOR_TRIANGULO = (80, 220, 160)
fuente = pygame.font.Font(None, 24)

# Bucle principal del juego
ejecutando = True
while ejecutando:
    dt = reloj.tick(60) / 1000

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
        elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
            ejecutando = False
        elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:
            punta = transformar_vertice((0, -30), posx, posy, escala, angulo)
            balas.append([punta[0], punta[1], angulo])

# Controles del movimiento, rotación y escala del triangulo
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
        posx -= VELOCIDAD * dt
    if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
        posx += VELOCIDAD * dt
    if teclas[pygame.K_UP] or teclas[pygame.K_w]:
        posy -= VELOCIDAD * dt
    if teclas[pygame.K_DOWN] or teclas[pygame.K_s]:
        posy += VELOCIDAD * dt
    if teclas[pygame.K_q]:
        angulo -= VELOCIDAD_ROTACION * dt
    if teclas[pygame.K_e]:
        angulo += VELOCIDAD_ROTACION * dt
    if teclas[pygame.K_EQUALS] or teclas[pygame.K_KP_PLUS]:
        escala += VELOCIDAD_ESCALA * dt
    if teclas[pygame.K_MINUS] or teclas[pygame.K_KP_MINUS]:
        escala -= VELOCIDAD_ESCALA * dt
# Tamaño y posición de la nave 
    escala = max(ESCALA_MINIMA, min(ESCALA_MAXIMA, escala))
    margen = 30 * escala
    posx = max(margen, min(ANCHO - margen, posx))
    posy = max(margen, min(ALTO - margen, posy))

    for bala in balas[:]:
        rad = math.radians(bala[2])
        bala[0] += VELOCIDAD_BALA * dt * math.sin(rad)
        bala[1] -= VELOCIDAD_BALA * dt * math.cos(rad)
        if (
            bala[0] < -50
            or bala[0] > ANCHO + 50
            or bala[1] < -50
            or bala[1] > ALTO + 50
        ):
            balas.remove(bala)

    vertices = [
        transformar_vertice(vertice, posx, posy, escala, angulo)
        for vertice in modelo_triangulo
    ]
    vertices = [(round(x), round(y)) for x, y in vertices]

    pantalla.fill(COLOR_FONDO)
    for bala in balas:
        vertices_bala = [
            transformar_vertice(vertice, bala[0], bala[1], 1, bala[2])
            for vertice in figura_bala
        ]
        pygame.draw.polygon(
            pantalla,
            color_bala,
            [(round(x), round(y)) for x, y in vertices_bala],
        )
    pygame.draw.polygon(pantalla, COLOR_TRIANGULO, vertices)
    pygame.draw.polygon(pantalla, (220, 255, 240), vertices, 2)

    instrucciones = fuente.render(
        "Mover: WASD/flechas | Girar: Q/E | Escala: +/- | Salir: ESC | Disparar: SPACE",
        True,
        (230, 230, 240),
    )
    pantalla.blit(instrucciones, (12, ALTO - 30))
    pygame.display.flip()

pygame.quit()
sys.exit()
