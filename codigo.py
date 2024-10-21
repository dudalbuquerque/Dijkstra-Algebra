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

direcoes = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Movimentos possíveis: cima, baixo, esquerda, direita

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
    
def distancia_Manhattan(P1, P2):
		x1, y1 = P1
    x2, y2 = P2
	    return abs(x1 - x2) - abs(y1 - y2)

def dijkstra(labirinto, entrada, saida):
    distancias = np.full(labirinto.shape, np.inf)
    distancias[entrada] = 0
    Min_heap = [(0, entrada)]  # Fila com (distância, nó)
    caminho = {}

    while Min_heap:
        dist_atual, coord_atual = heapq.heappop(Min_heap)

        if coord_atual == saida:
            break  # Encontrou o destino

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
COR_CAMINHO = (255, 0, 0)     # Vermelho
COR_INICIO = (0, 255, 0)      # Verde
COR_FIM = (0, 255, 0)         # Verde

# Dimensões do mapa
LARGURA = 500
ALTURA_LABIRINTO = 500
ALTURA_DISTANCIAS = 100
TAMANHO_CELULA = 50

# Fontes (diminuindo o tamanho da fonte para 20)
fonte = pygame.font.SysFont(None, 20)

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


# Nova função que desenha a linha do primeiro pixel da célula de entrada ao último pixel da célula de saída
def desenhar_linha(entrada, saida):
    entrada_pixel = (entrada[1] * TAMANHO_CELULA, entrada[0] * TAMANHO_CELULA)  # Canto superior esquerdo
    saida_pixel = (saida[1] * TAMANHO_CELULA + TAMANHO_CELULA - 1, saida[0] * TAMANHO_CELULA + TAMANHO_CELULA - 1)  # Canto inferior direito
    pygame.draw.line(screen, (0, 255, 255), entrada_pixel, saida_pixel, 3)


def mostrar_distancias(distancia_real, distancia_linha_reta):
    texto_real = fonte.render(f"Distância do Caminho: {distancia_real:.2f}", True, (0, 0, 0))
    texto_linha = fonte.render(f"Distância em Linha Reta: {distancia_linha_reta:.2f}", True, (0, 0, 0))
    screen.blit(texto_real, (10, ALTURA_LABIRINTO + 20))
    screen.blit(texto_linha, (10, ALTURA_LABIRINTO + 50))


# Ajuste a altura da tela para comportar o labirinto e as distâncias
ALTURA_TOTAL = ALTURA_LABIRINTO + ALTURA_DISTANCIAS
screen = pygame.display.set_mode((LARGURA, ALTURA_TOTAL))
pygame.display.set_caption('Dijkstra - Pygame')

# Usar Dijkstra com distância Euclidiana
caminho, distancias = dijkstra(labirinto, entrada, saida)

# Reconstruir o caminho mais curto da saída até a entrada
caminho_reconstruido = []
coord_atual = saida
while coord_atual != entrada:
    caminho_reconstruido.append(coord_atual)
    coord_atual = caminho.get(coord_atual, entrada)
caminho_reconstruido.append(entrada)
caminho_reconstruido.reverse()

# Distância total percorrida pelo caminho
distancia_real = sum(distancia_euclidiana(caminho_reconstruido[i], caminho_reconstruido[i+1]) for i in range(len(caminho_reconstruido)-1))

# Distância em linha reta (Euclidiana) entre o primeiro pixel da entrada e o último pixel da saída
distancia_linha_reta = distancia_euclidiana(
    (entrada[0] * TAMANHO_CELULA, entrada[1] * TAMANHO_CELULA),  # Primeiro pixel da entrada
    (saida[0] * TAMANHO_CELULA + TAMANHO_CELULA - 1, saida[1] * TAMANHO_CELULA + TAMANHO_CELULA - 1)  # Último pixel da saída
)

# Loop principal
running = True
mostrar_caminho = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                mostrar_caminho = not mostrar_caminho

    screen.fill((255, 255, 255))  # Limpa a tela
    desenhar_mapa(labirinto, entrada, saida)
    if mostrar_caminho:
        desenhar_path(caminho_reconstruido)
        desenhar_linha(entrada, saida)

        # Mostrar distâncias abaixo do labirinto
        mostrar_distancias(distancia_real, distancia_linha_reta)

    pygame.display.flip()

pygame.quit()
