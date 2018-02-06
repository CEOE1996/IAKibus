import pygame, sys
from pygame.locals import *

pygame.init()
Size = (1200, 600)
SizeCasilla = 30
Background = (40, 180, 99)
LineColor = (0, 0, 0)
Ventana = pygame.display.set_mode(Size)


while True:
    Ventana.fill(Background)

    i = SizeCasilla
    while i < Size[0]:
        pygame.draw.line(Ventana, LineColor, (i, 0), (i, Size[1]), 1)
        i += SizeCasilla

    i = SizeCasilla
    while i < Size[1]:
        pygame.draw.line(Ventana, LineColor, (0, i), (Size[0], i), 1)
        i += SizeCasilla

    for evento in pygame.event.get():
        if evento.type == QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()
