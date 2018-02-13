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

def IsValidPos(x, y):
    return Matriz[x][y] != 3 and Matriz[x][y] != 8

pygame.init()

#Tamaño de las Casillas
SizeCasilla = 30

#Numero de Casillas X, Y
NX, NY = 35, 20

#Inicio de Tablero
InitPlane = SizeCasilla * 6

#Variables
StartGame = 1
RunnerPos = LastPos = (0, 0)
NewPos = (0, 0)
HousePos = (NX - 1, NY - 1)
Difficulty = 50
NumberBombs = 0
TimeDelay = 250

#Linea Bresenham Inicial
LineBresenham = list(bresenham(RunnerPos[0], RunnerPos[1], HousePos[0], HousePos[1]))

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
Visitados = [[0 for x in range(NY)] for y in range(NX)]
Matriz[HousePos[0]][HousePos[1]] = 2

#Imagenes
print("Cargando ImgGreenflag")
ImgGreenflag = pygame.image.load("img/Greenflag.png")
print("Cargando Runner")
ImgRunner = pygame.image.load("img/run.png")
print("Cargando ImgHouse")
ImgHouse = pygame.image.load("img/house.png")
print("Cargando ImgBomb")
ImgBomb = pygame.image.load("img/bomb.png")
print("Cargando ImgRedFlag")
ImgRedFlag = pygame.image.load("img/redflag.png")
print("Cargando ImgYellowFlag")
ImgYellowFlag = pygame.image.load("img/Yellowflag.png")
print("Cargando ImgWhiteFlag")
ImgWhiteFlag = pygame.image.load("img/Whiteflag.png")
print("Cargando ImgOrangeFlag")
ImgOrangeFlag = pygame.image.load("img/Orangeflag.png")

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
            8 : ImgRedFlag
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

    for x in range(NX):
        for y in range(NY):
            if Matriz[x][y] != 0:
                DrawImg(x, y, Objects[Matriz[x][y]])

    if StartGame == 1:
        NewPos = LineBresenham.pop(0)

        if len(LineBresenham) == 0:
            StartGame = 0
        TimeDelay = 500
        if not IsValidPos(NewPos[0], NewPos[1]):
            # print("Posicion Invalida")
            # print(NewPos)

            #Matriz Posiciones Validas
            ValidPos = [1, 1, 1],[1, 0, 1],[1, 1, 1]
            ValidPos[(NewPos[0] - RunnerPos[0]) + 1][(NewPos[1] - RunnerPos[1]) + 1] = 0

            #Contador de Posiciones Invalidas
            UnvalidCounter = 2
            Valid = 0
            while not Valid:
                # print("\n\nMatriz Validos")
                # for i in ValidPos:
                #     print(i)
                #
                # TimeDelay = 10000

                RandomPos = (randint(-1, 1), randint(-1, 1))
                print(RunnerPos[0] + RandomPos[0])
                print(RunnerPos[1] + RandomPos[1])
                NewPos = (RunnerPos[0] + RandomPos[0], RunnerPos[1] + RandomPos[1])

                # print("RandomPos: ")
                # print(RandomPos)
                # print("NewPos: ")
                # print(NewPos)

                #Regresar Posición Anterior y Colocar Banderin
                if RandomPos == LastPos and UnvalidCounter == 8:
                    # print("Regresar Posicion Anterior")
                    Matriz[NewPos[0]][NewPos[1]] = 8
                    NewPos = LastPos
                    Valid = 1

                #Invalidar Fuera de Rangos
                elif NewPos[0] < 0 or NewPos[0] >= NX or NewPos[1] < 0 or NewPos[1] >= NY :
                    if ValidPos[RandomPos[0] + 1][RandomPos[1] + 1] == 1:
                        # print("Posicion Fuera de Rango")
                        ValidPos[RandomPos[0] + 1][RandomPos[1] + 1] = 0
                        UnvalidCounter += 1

                #Invalidar Casilla Invalidas por Objeto
                elif ValidPos[RandomPos[0] + 1][RandomPos[1] + 1] == 1 and not IsValidPos(NewPos[0], NewPos[1]):
                    # print("Objeto en Posicion")
                    ValidPos[RandomPos[0]][RandomPos[1]] == 0
                    UnvalidCounter += 1

                elif ValidPos[RandomPos[0] + 1][RandomPos[1] + 1] == 1 and IsValidPos(NewPos[0], NewPos[1]):
                    # print("Posicion Valida, Nueva Linea")
                    LineBresenham = list(bresenham(NewPos[0], NewPos[1], HousePos[0], HousePos[1]))
                    Valid = 1

                #Game Over
                if UnvalidCounter == 9:
                    print("Game Over")
                    print("\n\nMatriz Validos")
                    for i in ValidPos:
                        print(i)

                    print("UnvalidCounter: " + str(UnvalidCounter))

                    NewPos = RunnerPos
                    Valid = 1
                    StartGame = 0


        LastPos = RunnerPos
        RunnerPos = NewPos
        Visitados[RunnerPos[0]][RunnerPos[1]] += 1

        if Visitados[LastPos[0]][LastPos[1]] > 3 and Visitados[LastPos[0]][LastPos[1]] < 9:
            Matriz[LastPos[0]][LastPos[1]] = Visitados[LastPos[0]][LastPos[1]]
            # print("Banderin " + str(Matriz[RunnerPos[0]][RunnerPos[1]]))
        else:
            Matriz[LastPos[0]][LastPos[1]] = 0

        Matriz[RunnerPos[0]][RunnerPos[1]] = 1

    for evento in pygame.event.get():
        if evento.type == QUIT:
            pygame.quit()
            sys.exit()

    # for i in range(10):
    #     print("\n")
    #
    # for i in Matriz:
    #     print(i)
    pygame.display.update()
    pygame.time.delay(TimeDelay)
