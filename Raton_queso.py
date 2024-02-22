import tkinter as tk
import pygame
import threading
import time

# Pygame setup
pygame.init()
laberinto_size = 5
cell_size = 50
laberinto = [[0] * laberinto_size for _ in range(laberinto_size)]

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

def draw(screen, laberinto, raton_pos, queso_pos, ruta_actual=None, contador_caminos=0):
    screen.fill(WHITE)
    
    for i in range(laberinto_size):
        for j in range(laberinto_size):
            pygame.draw.rect(screen, BLACK, ((laberinto_size - 1 - j) * cell_size, i * cell_size, cell_size, cell_size), 1)

    pygame.draw.circle(screen, RED, (raton_pos[1] * cell_size + cell_size // 2, (laberinto_size - 1 - raton_pos[0]) * cell_size + cell_size // 2), cell_size // 3)
    pygame.draw.circle(screen, RED, (queso_pos[1] * cell_size + cell_size // 2, (laberinto_size - 1 - queso_pos[0]) * cell_size + cell_size // 2), cell_size // 3)
    
    if ruta_actual:
        for pos in ruta_actual:
            pygame.draw.rect(screen, RED, ((laberinto_size - 1 - pos[1]) * cell_size, pos[0] * cell_size, cell_size, cell_size))
    
    font = pygame.font.Font(None, 36)
    text = font.render(f"Caminos: {contador_caminos}", True, BLACK)
    screen.blit(text, (10, 10))

    pygame.display.flip()

def encontrar_rutas(fila, columna, ruta_actual):
    if fila == columna == 0:
        return [ruta_actual[:]]

    rutas = []
    if fila - 1 >= 0 and (fila - 1, columna) not in ruta_actual:
        ruta = ruta_actual + [(fila - 1, columna)]
        rutas.extend(encontrar_rutas(fila - 1, columna, ruta))

    if columna - 1 >= 0 and (fila, columna - 1) not in ruta_actual:
        ruta = ruta_actual + [(fila, columna - 1)]
        rutas.extend(encontrar_rutas(fila, columna - 1, ruta))

    return rutas

def pygame_thread():
    window_size = (laberinto_size * cell_size, laberinto_size * cell_size)
    screen = pygame.display.set_mode(window_size)
    pygame.display.set_caption("Laberinto del Ratón")

    raton_pos = (laberinto_size - 1, laberinto_size - 1)
    queso_pos = (0, 0)

    rutas_posibles = encontrar_rutas(laberinto_size - 1, laberinto_size - 1, [(laberinto_size - 1, laberinto_size - 1)])

    for index, ruta in enumerate(rutas_posibles):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        draw(screen, laberinto, raton_pos, queso_pos, ruta, contador_caminos=index + 1)
        pygame.time.delay(1000)

    pygame.quit()

# Tkinter setup
def encontrar_caminos(x, y, visitado, contador, camino_actual):
    if x == 0 and y == 4:
        contador[0] += 1
        cuadro[0][4].config(bg="green")
        resultado_label.config(text=f"Número de caminos encontrados: {contador[0]}")
        root.update()
        time.sleep(0)
        cuadro[0][4].config(bg="gray")
        root.update()
        return

    visitado[x][y] = True
    cuadro[x][y].config(bg="yellow")
    root.update()

    direcciones = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
    for dx, dy in direcciones:
        if (0 <= dx < 5 and 0 <= dy < 5 and not visitado[dx][dy] and
                not (dx == 2 and dy == 2)):
            time.sleep(0.0)
            visitado[dx][dy] = True
            camino_actual.append((dx, dy))
            encontrar_caminos(dx, dy, visitado, contador, camino_actual)
            camino_actual.pop()
            visitado[dx][dy] = False

    visitado[x][y] = False
    cuadro[x][y].config(bg="white")
    root.update()

def simular():
    contador = [0]
    visitado = [[False]*5 for _ in range(5)]
    camino_actual = [(4, 0)]
    encontrar_caminos(4, 0, visitado, contador, camino_actual)

root = tk.Tk()
root.title("Simulación de búsqueda de caminos")

cuadro_width = 10
cuadro_height = 5
cuadro = [[None]*5 for _ in range(5)]

for i in range(5):
    for j in range(5):
        cuadro[i][j] = tk.Label(root, text="-", width=cuadro_width, height=cuadro_height, relief="ridge", borderwidth=2)
        cuadro[i][j].grid(row=i, column=j)

cuadro[0][4].config(bg="gray", state="disabled")

simular_button = tk.Button(root, text="Simular", command=simular)
simular_button.grid(row=5, column=0, columnspan=5)

resultado_label = tk.Label(root, text="Número de caminos encontrados: 0")
resultado_label.grid(row=6, column=0, columnspan=5)

pygame_thread = threading.Thread(target=pygame_thread)
pygame_thread.start()

root.mainloop()