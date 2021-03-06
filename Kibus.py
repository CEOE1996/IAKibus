'''
Created By Carlos Orozco
Date: 2018-02-14
URL: https://github.com/CEOE1996
'''

﻿import pygame, sys
from pygame.locals import *
from bresenham import bresenham
from random import randint

pygame.init()

#Tamaño de las Casillas
SizeCasilla = 30

#Numero de Casillas X, Y
NX, NY = 35, 20

#Inicio de Tablero
InitPlane = SizeCasilla * 6

#Variables
StartGame = 0

SetRunner = 1
SettingRunner = 0
RunnerSet = 0

SetHouse = 0
SettingHouse = 0
HouseSet = 0

HousePos = NewPos = RunnerPos = LastPos = (0, 0)

Difficulty = 0
SettingDifficulty = 0

NumberBombs = 0

DifficultyBarIn = DifficultyBar = 230
DifficultyBarFin = 470

TimeDelay = 0

#Tamaño Ventana Incluyendo Panel de Configuración y Tablero
Size = (InitPlane + (SizeCasilla * NX), (NY * SizeCasilla))

#Colores
Background = (41, 128, 185)
LineColor = (0, 0, 0)
PanelColor = (255, 255, 255)
ButtonIC = (0, 51, 204)
ButtonAC = (26, 83, 255)
inactive = (150, 150, 150)
SlidebarColor = (200, 200, 200)

#Matriz de Posiciones
Matriz = [[0 for x in range(NY)] for y in range(NX)]
Visitados = [[0 for x in range(NY)] for y in range(NX)]

#Imagenes
ImgRunner = pygame.image.load("img/run3.png")
ImgHouse = pygame.image.load("img/house.png")
ImgBomb = pygame.image.load("img/bomb.png")
ImgRedFlag = pygame.image.load("img/redflag.png")
ImgYellowFlag = pygame.image.load("img/Yellowflag.png")
ImgWhiteFlag = pygame.image.load("img/Whiteflag.png")
ImgOrangeFlag = pygame.image.load("img/Orangeflag.png")
ImgGreenflag = pygame.image.load("img/Greenflag.png")
ImgPlay = pygame.image.load("img/play.png")

ImgRunner = pygame.transform.scale(ImgRunner, (SizeCasilla, SizeCasilla))
ImgHouse = pygame.transform.scale(ImgHouse, (SizeCasilla, SizeCasilla))
ImgBomb = pygame.transform.scale(ImgBomb, (SizeCasilla, SizeCasilla))
ImgRedFlag = pygame.transform.scale(ImgRedFlag, (SizeCasilla, SizeCasilla))
ImgYellowFlag = pygame.transform.scale(ImgYellowFlag, (SizeCasilla, SizeCasilla))
ImgWhiteFlag = pygame.transform.scale(ImgWhiteFlag, (SizeCasilla, SizeCasilla))
ImgOrangeFlag = pygame.transform.scale(ImgOrangeFlag, (SizeCasilla, SizeCasilla))
ImgGreenflag = pygame.transform.scale(ImgGreenflag, (SizeCasilla, SizeCasilla))
ImgPlay = pygame.transform.scale(ImgPlay, (SizeCasilla, SizeCasilla))


#Declaración de Ventana
Ventana = pygame.display.set_mode(Size)
pygame.display.set_caption("Kibus")
pygame.display.set_icon(ImgRunner)

#Objects
Objects = {
            1 : ImgRunner,
            2 : ImgHouse,
            3 : ImgBomb,
            4 : ImgGreenflag,
            5 : ImgWhiteFlag,
            6 : ImgYellowFlag,
            7 : ImgOrangeFlag,
            8 : ImgRedFlag
}

#Functions
def SetDifficulty(Dif, m):
    NumberBombs = 0
    if Dif != Difficulty:
        for i in range(NX):
            for j in range(NY):
                if m[i][j] == 3:
                    m[i][j] = 0

        while NumberBombs < int(((NX * NY) * Dif / 100)):
            BX, BY = randint(0, NX - 1), randint(0, NY - 1)
            if m[BX][BY] == 0:
                m[BX][BY] = 3
                NumberBombs+= 1
        return Dif, m
    return Difficulty, m

def DrawImg(x, y, img):
    DX = InitPlane + (x * SizeCasilla)
    DY = y * SizeCasilla
    Ventana.blit(img, (DX, DY))

def IsValidPos(x, y):
    return Matriz[x][y] != 3 and Matriz[x][y] != 8

def button(x, y, w, h, ac, ic, active, image, ban):
    mouse = pygame.mouse.get_pos()
    pressed = pygame.mouse.get_pressed()
    if not active:
        pygame.draw.rect(Ventana, inactive, (x, y, w, h))

    elif x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(Ventana, ac, (x, y, w, h))
        if pressed[0] == 1 and active:
            return not active, not ban
    else:
        pygame.draw.rect(Ventana, ic, (x, y, w, h))
    Ventana.blit(image, (x + SizeCasilla, y + SizeCasilla))
    return active, ban

def SlideBarButton(x, y, w, h, ac, ic, active, m):
    ny = y - (h / 2)
    mouse = pygame.mouse.get_pos()
    pressed = pygame.mouse.get_pressed()
    d = Difficulty
    if not active:
        pygame.draw.rect(Ventana, inactive, (x, ny, w, h))
    elif x+w > mouse[0] > x and ny+h > mouse[1] > ny:
        pygame.draw.rect(Ventana, ac, (x, ny, w, h))
        if pressed[0] == 1 and active:
            if DifficultyBarFin > mouse[1] > DifficultyBarIn:
                DiffPercentage = round(((mouse[1] - DifficultyBarIn) * 80) / (DifficultyBarFin - DifficultyBarIn))
                if DiffPercentage % 10 == 0:
                    d, m = SetDifficulty(DiffPercentage, m)
                return mouse[1], d, m
    else:
        pygame.draw.rect(Ventana, ic, (x, ny, w, h))
    return y, d, m

def IsSettingObject(Setting, ban, image):
    #print(Setting)
    if Setting:
        mouse = pygame.mouse.get_pos()
        pressed = pygame.mouse.get_pressed()
        if mouse[0] > InitPlane:
            Ventana.blit(image, (mouse[0] - (SizeCasilla / 2), mouse[1] - (SizeCasilla / 2)))
            if pressed[0] == 1:
                return not Setting, 1, int((mouse[0] - InitPlane) / SizeCasilla), int((mouse[1]) / SizeCasilla)
    return Setting, 0, -1, -1

#Inicia Juego
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

    #Colocar Botones
    SetRunner, SettingRunner = button(45, 10, 90, 90, ButtonAC, ButtonIC, SetRunner, ImgRunner, SettingRunner)
    SetHouse, SettingHouse = button(45, 110, 90, 90, ButtonAC, ButtonIC, SetHouse, ImgHouse, SettingHouse)
    SettingDifficulty, StartGame = button(45, 500, 90, 90, ButtonAC, ButtonIC, SettingDifficulty, ImgPlay, StartGame)

    #Colocar Corredor
    SettingRunner, RunnerSet, x, y = IsSettingObject(SettingRunner, SetHouse, ImgRunner)
    if RunnerSet and not SettingRunner:
        RunnerPos = (x, y)
        Matriz[x][y] = 1
        SetHouse = 1

    #Colocar Casa
    SettingHouse, HouseSet, x, y = IsSettingObject(SettingHouse, 0, ImgHouse)
    if HouseSet and not SettingHouse:
        HousePos = (x, y)
        Matriz[x][y] = 2
        LineBresenham = list(bresenham(RunnerPos[0], RunnerPos[1], HousePos[0], HousePos[1]))
        SettingDifficulty = 1

    #Slidebar Dificultad
    pygame.draw.line(Ventana, SlidebarColor, (90, DifficultyBarIn), (90, DifficultyBarFin), 2)
    l = DifficultyBarIn
    for i in range(7):
        l += 30
        pygame.draw.line(Ventana, SlidebarColor, (80, l), (100, l), 2)

    #Configurar Dificultad
    DifficultyBar, Difficulty, Matriz = SlideBarButton(75, DifficultyBar, 30, 12, ButtonAC, ButtonIC, SettingDifficulty, Matriz)

    #Colocar Objetos de Matriz
    for x in range(NX):
        for y in range(NY):
            if Matriz[x][y] != 0:
                DrawImg(x, y, Objects[Matriz[x][y]])

    if StartGame == 1:
        TimeDelay = 250

        NewPos = LineBresenham.pop(0)

        if len(LineBresenham) == 0:
            StartGame = 0

        if not IsValidPos(NewPos[0], NewPos[1]):
            #Matriz Posiciones Validas
            ValidPos = [1, 1, 1],[1, 0, 1],[1, 1, 1]
            ValidPos[(NewPos[0] - RunnerPos[0]) + 1][(NewPos[1] - RunnerPos[1]) + 1] = 0

            #Contador de Posiciones Invalidas
            UnvalidCounter = 2
            Valid = 0
            while not Valid:
                #Generar Posición Aleatoria
                RandomPos = (randint(-1, 1), randint(-1, 1))
                NewPos = (RunnerPos[0] + RandomPos[0], RunnerPos[1] + RandomPos[1])

                #Regresar Posición Anterior y Colocar Banderin
                if NewPos == LastPos and UnvalidCounter == 8:
                    Visitados[RunnerPos[0]][RunnerPos[1]] = 10
                    Matriz[RunnerPos[0]][RunnerPos[1]] = 8
                    NewPos = LastPos
                    LineBresenham = list(bresenham(NewPos[0], NewPos[1], HousePos[0], HousePos[1]))
                    Valid = 1

                #Invalidar Fuera de Rangos
                elif NewPos[0] < 0 or NewPos[0] >= NX or NewPos[1] < 0 or NewPos[1] >= NY :
                    if ValidPos[RandomPos[0] + 1][RandomPos[1] + 1] == 1:
                        ValidPos[RandomPos[0] + 1][RandomPos[1] + 1] = 0
                        UnvalidCounter += 1

                elif ValidPos[RandomPos[0] + 1][RandomPos[1] + 1] == 1 and NewPos != LastPos:
                    #Nueva Posición, Trazar Linea Bresenham
                    if IsValidPos(NewPos[0], NewPos[1]):
                        LineBresenham = list(bresenham(NewPos[0], NewPos[1], HousePos[0], HousePos[1]))
                        Valid = 1
                    #Invalidar Casilla Invalidas por Objeto
                    else:
                        ValidPos[RandomPos[0] + 1][RandomPos[1] + 1] = 0
                        UnvalidCounter += 1

                #Game Over
                if UnvalidCounter == 9:
                    NewPos = RunnerPos
                    Valid = 1
                    StartGame = 0

        #Asignar Nuevas Posiciones
        LastPos = RunnerPos
        RunnerPos = NewPos
        Visitados[RunnerPos[0]][RunnerPos[1]] += 1

        #Dibujar Banderines o Limpiar Casilla
        if Visitados[LastPos[0]][LastPos[1]] > 3:
            if Visitados[LastPos[0]][LastPos[1]] < 9:
                Matriz[LastPos[0]][LastPos[1]] = Visitados[LastPos[0]][LastPos[1]]
            else:
                Matriz[LastPos[0]][LastPos[1]] = 8
        else:
            Matriz[LastPos[0]][LastPos[1]] = 0

        Matriz[RunnerPos[0]][RunnerPos[1]] = 1

    for evento in pygame.event.get():
        print(evento)
        if evento.type == QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()
    pygame.time.delay(TimeDelay)
