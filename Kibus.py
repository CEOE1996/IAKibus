import pygame, sys
from pygame.locals import *
from bresenham import bresenham
from random import randint

def SetDifficulty(Dif):
    NumberBombs = 0
    while NumberBombs < int(((NX * NY) * Difficulty / 100)):
        BX, BY = randint(0, NX - 1), randint(0, NY - 1)
        if Matriz[BX][BY] != 1 and Matriz[BX][BY] != 2:
            Matriz[BX][BY] = 3
            NumberBombs+= 1

def DrawImg(x, y, img):
    DX = InitPlane + (x * SizeCasilla)
    DY = y * SizeCasilla
    Ventana.blit(img, (DX, DY))

StartGame = 0
RunnerPos = (0, 0)
HousePos = (15, 15)
Difficulty = 10
NumberBombs = 0

pygame.init()

#Tamaño de las Casillas
SizeCasilla = 30

#Numero de Casillas X, Y
NX, NY = 35, 20

#Inicio de Tablero
InitPlane = SizeCasilla * 6

#Tamaño Ventana Incluyendo Panel de Configuración y Tablero
Size = (InitPlane + (SizeCasilla * NX), (NY * SizeCasilla))

#Colores
Background = (41, 128, 185)
LineColor = (0, 0, 0)
PanelColor = (255, 255, 255)

#Declaración de Ventana
Ventana = pygame.display.set_mode(Size)

#Matriz de Posiciones
Matriz = [[0 for x in range(NY)] for y in range(NX)]
Matriz[RunnerPos[0]][RunnerPos[1]] = 1
Matriz[HousePos[0]][HousePos[1]] = 2

#Imagenes
ImgRunner = pygame.image.load("img/run.png")
ImgHouse = pygame.image.load("img/house.png")
ImgBomb = pygame.image.load("img/bomb.png")
ImgRedFlag = pygame.image.load("img/redflag.png")
ImgYellowFlag = pygame.image.load("img/Yellowflag.png")
ImgWhiteFlag = pygame.image.load("img/Whiteflag.png")
ImgOrangeFlag = pygame.image.load("img/Orangeflag.png")
ImgGreenflag = pygame.image.load("img/Greenflag.png")
ImgRunner = pygame.transform.scale(ImgRunner, (SizeCasilla, SizeCasilla))
ImgHouse = pygame.transform.scale(ImgHouse, (SizeCasilla, SizeCasilla))
ImgBomb = pygame.transform.scale(ImgBomb, (SizeCasilla, SizeCasilla))
ImgRedFlag = pygame.transform.scale(ImgRedFlag, (SizeCasilla, SizeCasilla))
ImgYellowFlag = pygame.transform.scale(ImgYellowFlag, (SizeCasilla, SizeCasilla))
ImgWhiteFlag = pygame.transform.scale(ImgWhiteFlag, (SizeCasilla, SizeCasilla))
ImgOrangeFlag = pygame.transform.scale(ImgOrangeFlag, (SizeCasilla, SizeCasilla))
ImgGreenflag = pygame.transform.scale(ImgGreenflag, (SizeCasilla, SizeCasilla))

#Objects
Objects = {
            1 : ImgRunner,
            2 : ImgHouse,
            3 : ImgBomb,
            4 : ImgGreenflag,
            5 : ImgWhiteFlag,
            6 : ImgYellowFlag,
            7 : ImgOrangeFlag,
            9 : ImgRedFlag
}

SetDifficulty(Difficulty)

while True:
    Ventana.fill(Background)

    #Dibujar Lineas del Tablero en X
    i = InitPlane + SizeCasilla
    while i < Size[0]:
        pygame.draw.line(Ventana, LineColor, (i, 0), (i, Size[1]), 1)
        i += SizeCasilla

    #Dibujar Lineas del Tablero en Y
    i = SizeCasilla
    while i < Size[1]:
        pygame.draw.line(Ventana, LineColor, (0, i), (Size[0], i), 1)
        i += SizeCasilla

    #Colocar Panel de Configuración
    pygame.draw.rect(Ventana, PanelColor, (0, 0, InitPlane, (NY * SizeCasilla)))

    for x in range(NX - 1):
        for y in range(NY - 1):
            if Matriz[x][y] != 0:
                #print(Objects[Matriz[x][y]])
                DrawImg(x, y, Objects[Matriz[x][y]])

    for evento in pygame.event.get():
        if evento.type == QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()
