import pygame
import numpy as np
import heapq
import math


pygame.init()

# 1 = parede e 0 = caminho livre
Matriz_labirinto = [
    [0, 1, 1, 1, 0, 0, 0, 1, 1, 1],
    [0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
    [0, 1, 0, 1, 1, 1, 0, 1, 1, 1],
    [0, 0, 0, 0, 1, 0, 0, 1, 0, 0],
    [1, 0, 1, 1, 0, 1, 0, 1, 0, 1],
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
    [0, 1, 1, 1, 1, 0, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 1, 0, 1, 1, 1, 1, 0, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]
labirinto = np.array(Matriz_labirinto)

entrada = (0, 0)
saida = (9, 9)

direcoes = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Movimentos: cima, baixo, esquerda, direita

def vizinhos(labirinto, coordenada_atual):
    x, y = coordenada_atual
    vizinhos_permitidos = []
    for movimento in direcoes:
        aux_x = x + movimento[0]
        aux_y = y + movimento[1]
        # Checando se o vizinho é válido -> coordenadas dentro do labirinto e caminho livre
        if 0 <= aux_x < labirinto.shape[0] and 0 <= aux_y < labirinto.shape[1] and labirinto[aux_x, aux_y] == 0:
            vizinhos_permitidos.append((aux_x, aux_y))
    return vizinhos_permitidos

# Distância Euclidiana entre dois pontos (P1 e P2)
def distancia_euclidiana(P1, P2):
    x1, y1 = P1
    x2, y2 = P2
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

# Distância de Manhattan entre dois pontos (P1 e P2)
def distancia_manhattan(P1, P2):
    x1, y1 = P1
    x2, y2 = P2
    return abs(x2 - x1) + abs(y2 - y1)

def dijkstra(labirinto, entrada, saida):
    distancias = np.full(labirinto.shape, np.inf)
    distancias[entrada] = 0
    Min_heap = [(0, entrada)] 
    caminho = {}

    while Min_heap:
        dist_atual, coord_atual = heapq.heappop(Min_heap)

        if coord_atual == saida:
            break 

        for vizinho in vizinhos(labirinto, coord_atual):
            nova_dist = dist_atual + distancia_euclidiana(coord_atual, vizinho)

            if nova_dist < distancias[vizinho]:
                distancias[vizinho] = nova_dist
                heapq.heappush(Min_heap, (nova_dist, vizinho))
                caminho[vizinho] = coord_atual

    return caminho, distancias

# Cores
COR_LIVRE = (200, 200, 200)   # Cinza claro
COR_OBSTACULO = (0, 0, 0)     # Preto
COR_CAMINHO = (0, 0, 200)     # Vermelho
COR_INICIO = (0, 255, 0)      # Verde
COR_FIM = (255, 0, 0)         # Vermelho

# Dimensões do mapa
LARGURA = 500
ALTURA_LABIRINTO = 500
ALTURA_DISTANCIAS = 100
TAMANHO_CELULA = 50

fonte = pygame.font.SysFont(None, 20)


#Mostrar o labirinto 
def desenhar_mapa(labirinto, entrada, saida):
    for i in range(labirinto.shape[0]):
        for j in range(labirinto.shape[1]):
            cor = COR_LIVRE if labirinto[i, j] == 0 else COR_OBSTACULO
            pygame.draw.rect(screen, cor, (j * TAMANHO_CELULA, i * TAMANHO_CELULA, TAMANHO_CELULA, TAMANHO_CELULA))
    pygame.draw.rect(screen, COR_INICIO, (entrada[1] * TAMANHO_CELULA, entrada[0] * TAMANHO_CELULA, TAMANHO_CELULA, TAMANHO_CELULA))
    pygame.draw.rect(screen, COR_FIM, (saida[1] * TAMANHO_CELULA, saida[0] * TAMANHO_CELULA, TAMANHO_CELULA, TAMANHO_CELULA))

def desenhar_path(caminho=[]):
    for coordenada in caminho:
        pygame.draw.rect(screen, COR_CAMINHO, (coordenada[1] * TAMANHO_CELULA, coordenada[0] * TAMANHO_CELULA, TAMANHO_CELULA, TAMANHO_CELULA))

def desenhar_linha(entrada, saida):
    entrada_pixel = (entrada[1] * TAMANHO_CELULA, entrada[0] * TAMANHO_CELULA)  
    saida_pixel = (saida[1] * TAMANHO_CELULA + TAMANHO_CELULA - 1, saida[0] * TAMANHO_CELULA + TAMANHO_CELULA - 1)  
    pygame.draw.line(screen, (255, 0, 0), entrada_pixel, saida_pixel, 3)  # Linha vermelha


def mostrar_distancias(distancia_real, distancia_linha_reta, distancia_manhattan_reta):
    texto_real = fonte.render(f"Distância do Caminho: {distancia_real:.2f}", True, (0, 0, 0))
    texto_linha = fonte.render(f"Distância em Linha Reta (Euclidiana): {distancia_linha_reta:.2f}", True, (0, 0, 0))
    texto_manhattan = fonte.render(f"Distância em Linha Reta (Manhattan): {distancia_manhattan_reta:.2f}", True, (0, 0, 0))
    screen.blit(texto_real, (10, ALTURA_LABIRINTO + 20))
    screen.blit(texto_linha, (10, ALTURA_LABIRINTO + 50))
    screen.blit(texto_manhattan, (10, ALTURA_LABIRINTO + 80))


ALTURA_TOTAL = ALTURA_LABIRINTO + ALTURA_DISTANCIAS
screen = pygame.display.set_mode((LARGURA, ALTURA_TOTAL))
pygame.display.set_caption('Dijkstra - Pygame')

caminho, distancias = dijkstra(labirinto, entrada, saida)

# Refaz o caminho mais curto da saída para a entrada
caminho_curto = []
atual = saida
while atual != entrada:
    caminho_curto.append(atual)
    atual = caminho.get(atual, entrada)
caminho_curto.append(entrada)
caminho_curto.reverse()

# Calculando distâncias
distancia_dijkstra = distancias[saida]  
distancia_linha_reta = distancia_euclidiana(entrada, saida)
distancia_manhattan_reta = distancia_manhattan(entrada, saida)

# Estado de controle das exibições: 0 = somente início e fim, 1 = caminho, 2 = linha reta + distâncias
estado = 0
rodando = True
while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE:
                estado = (estado + 1) % 3 

    screen.fill((255, 255, 255))

    desenhar_mapa(labirinto, entrada, saida)

    if estado == 1:
        desenhar_path(caminho_curto)  
    elif estado == 2:
        desenhar_path(caminho_curto)
        desenhar_linha(entrada, saida) 
        mostrar_distancias(distancia_dijkstra, distancia_linha_reta, distancia_manhattan_reta)  

    pygame.display.update()

pygame.quit()
