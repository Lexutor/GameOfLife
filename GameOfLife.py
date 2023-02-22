import pygame
import numpy as np
import time

pygame.init()

width, height = 1000, 1000 # Tamaño de la pantalla
screen = pygame.display.set_mode((height, width)) # Creación de la pantalla

gameBackground = 25, 25, 25 # Color de fondo
screen.fill(gameBackground) # Aplicación del color de fondo

nxC, nyC = 50, 50 # Cantidad de celdas en los dos ejes (X, Y)

# Dimensiones de las celdas
dimCellWidth = width / nxC
dimCellHeight = height / nyC

# Estado de las celdas, vivas (1) o muertas (0)
gameState = np.zeros((nxC, nyC))

# Control de ejecución del juego
pauseExcecuted = False

# Bucle de ejecución
while True:

    newGameState = np.copy(gameState) # Se crea una copia del estado actual del juego

    screen.fill(gameBackground)
    time.sleep(0.1) # Pequeña pausa entre iteraciones

    # Se registran los eventos del teclado y mouse
    ev = pygame.event.get()

    for event in ev:
        if event.type == pygame.KEYDOWN:
            pauseExcecuted = not pauseExcecuted
        
        mouseClick = pygame.mouse.get_pressed()

        if sum(mouseClick) > 0:
            posX, posY = pygame.mouse.get_pos()
            celX, celY = int(np.floor(posX / dimCellWidth)), int(np.floor(posY / dimCellHeight))
            newGameState[celX, celY] = not mouseClick[2]

    for y in range(0, nxC):
        for x in range(0, nyC):

            if not pauseExcecuted:
                # Calculando el número de vecinos cercanos
                n_neigh = gameState[(x - 1) % nxC, (y - 1) % nyC] + \
                        gameState[(x) % nxC, (y - 1) % nyC] + \
                        gameState[(x + 1) % nxC, (y - 1) % nyC] + \
                        gameState[(x - 1) % nxC, (y) % nyC] + \
                        gameState[(x + 1) % nxC, (y) % nyC] + \
                        gameState[(x - 1) % nxC, (y + 1) % nyC] + \
                        gameState[(x) % nxC, (y + 1) % nyC] + \
                        gameState[(x + 1) % nxC, (y + 1) % nyC]
                
                # Regla #1: una célula muerta con exactamente 3 vecinas vivas, "revive".
                if gameState[x, y] == 0 and n_neigh == 3:
                    newGameState[x, y] = 1

                # Regla #2: una célula viva con menos de 2 o más de 3 vecinas vivas, "muere".
                elif gameState[x, y] == 1 and (n_neigh < 2 or n_neigh > 3):
                    newGameState[x, y] = 0
                
            # Creación de cada celda que se va a dibujar
            poly = [((x) * dimCellWidth, y * dimCellHeight),
                    ((x + 1) * dimCellWidth, y * dimCellHeight),
                    ((x + 1) * dimCellWidth, (y + 1) * dimCellHeight),
                    ((x) * dimCellWidth, (y + 1) * dimCellHeight)]

            # Se dibuja la celda por cada par de X e Y
            if newGameState[x, y] == 0:
                pygame.draw.polygon(screen, (128, 128, 128), poly, 1)
            else:
                pygame.draw.polygon(screen, (255, 255, 255), poly, 0)
        
    # Se actualiza el estado del juego
    gameState = np.copy(newGameState)
    
    # Se muestra el juego en la pantalla
    pygame.display.flip()