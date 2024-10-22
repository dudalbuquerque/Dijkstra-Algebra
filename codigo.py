import pygame
import numpy as np
import heapq
import math


#inicialização 
pygame.init()

#cores 
CINZA = (200,200,200) 
PRETO = (0, 0, 0,) 
AZUL = (0, 0, 200)
VERDE = (0, 255, 0) 
VERMELHO = (255, 0, 0) 

#dimensões do mapa
LARGURA = 500
ALTURA_LABIRINTO = 500
ALTURA_DISTANCIA = 100
TAMANHO_CELULA = 50

entrada = (0, 0)
saida = (9, 9)

direcoes = [(-1,0), (1,0), (0,-1), (0,1)]

matriz = [
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
Labirinto = np.array(matriz) #a lista de lista(matriz) em uma array NumPy

def distancia_manhattan(ponto1, ponto2):
    x1, y1 = ponto1
    x2, y2 = ponto2
    return abs(x1-x2)+abs(y1-y2)

def distancia_euclidiana(ponto1, ponto2):
    x1, y1 = ponto1
    x2, y2 = ponto2
    return math.sqrt((x2-x1)**2 + (y2-y1)**2)

def movimentos(Labirinto, posicao_atual):
    x, y = posicao_atual
    movimentos_permitidos = []
    for direcao in direcoes:
        aux_x = x+direcao[0]
        aux_y = y+direcao[1]
        # Checando se o movimento é válido => coordenadas dentro do labirinto e caminho livre
        if 0 <= aux_x < Labirinto.shape[0] and 0 <= aux_y < Labirinto.shape[1] and Labirinto[aux_x, aux_y] == 0:
            movimentos_permitidos.append((aux_x, aux_y))
    return movimentos_permitidos

def dijkstra(Labirinto, entrada, saida):
    distancias = np.full(Labirinto.shape, np.inf) # um matriz igual a ao labirinto porém preenchida com o valor np.inf(infinito)
    distancias[entrada] = 0 
    min_heap = [(0, entrada)]
    caminho = {}

    parar = False
    while not parar:
        distancia_atual, coordenada_atual = heapq.heappop(min_heap) 

        if coordenada_atual == saida:
            parar = True 
        for movimento in movimentos(Labirinto, coordenada_atual):
            distancia_nova = distancia_atual + distancia_euclidiana(coordenada_atual, movimento)        
            if distancia_nova < distancias[movimento]:
                distancias[movimento] = distancia_nova
                heapq.heappush(min_heap, (distancia_nova, movimento))
                caminho[movimento] = coordenada_atual
    return caminho, distancias
    
# DESENHANDO
def desenhar_mapa(Labirinto, entrada, saida):
    for i in range(Labirinto.shape[0]):
        for j in range(Labirinto.shape[1]):
            if Labirinto[i, j] == 0:
                cor = CINZA
            else:
                cor = PRETO
            pygame.draw.rect(screen, cor, (j*TAMANHO_CELULA, i*TAMANHO_CELULA, TAMANHO_CELULA, TAMANHO_CELULA))
    pygame.draw.rect(screen, VERDE, (entrada[1] * TAMANHO_CELULA, entrada[0] * TAMANHO_CELULA, TAMANHO_CELULA, TAMANHO_CELULA))
    pygame.draw.rect(screen, VERMELHO, (saida[1] * TAMANHO_CELULA, saida[0] * TAMANHO_CELULA, TAMANHO_CELULA, TAMANHO_CELULA))

def desenhar_caminho(caminho=[]):
    for coordenada in caminho:
        pygame.draw.rect(screen, AZUL, (coordenada[1] * TAMANHO_CELULA, coordenada[0] * TAMANHO_CELULA, TAMANHO_CELULA, TAMANHO_CELULA))

def desenhar_linha(entrada, saida):
    inicio_linha = (entrada[1] * TAMANHO_CELULA, entrada[0] * TAMANHO_CELULA)  
    fim_linha = (saida[1] * TAMANHO_CELULA + TAMANHO_CELULA - 1, saida[0] * TAMANHO_CELULA + TAMANHO_CELULA - 1)
    pygame.draw.line(screen, (255, 0, 0), inicio_linha, fim_linha, 3) 

#fonte da letra
fonte = pygame.font.SysFont(None, 20)
def mostrar_distancias(distancia_dijkstra_, distancia_linha_, distancia_manhattan_):
    texto_dijk = fonte.render(f'Distância do Menor Caminho: {distancia_dijkstra_:.2f}', True, (50,50,50))
    texto_linha = fonte.render(f'Distância Euclidicana: {distancia_linha_:.2f}', True, (50,50,50))
    texto_manhattan = fonte.render(f'Distância Euclidicana: {distancia_manhattan_:.2f}', True, (50,50,50))
    screen.blit(texto_dijk, (10, ALTURA_LABIRINTO + 20))
    screen.blit(texto_linha, (10, ALTURA_LABIRINTO + 50))
    screen.blit(texto_manhattan, (10, ALTURA_LABIRINTO + 80))

ALTURA_TOTAL = ALTURA_LABIRINTO + ALTURA_DISTANCIA
screen = pygame.display.set_mode((LARGURA, ALTURA_TOTAL))
pygame.display.set_caption('Dijkstra - Pygame')

caminho, distancias = dijkstra(Labirinto, entrada, saida)

menor_caminho = []
atual = saida
while atual != entrada:
    menor_caminho.append(atual)
    atual = caminho.get(atual, entrada)
menor_caminho.append(entrada)
menor_caminho.reverse()

# Calculando as distâncias
distancia_dijkstra = distancias[saida]  
distancia_linha_ = distancia_euclidiana(entrada, saida)
distancia_manhattan_ = distancia_manhattan(entrada, saida)

# controle das exibições: 0 = somente início e fim, 1 = caminho, 2 = linha reta + distâncias
estado = 0
rodando = True
while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE:
                estado = (estado + 1) % 3 
    screen.fill((255, 255, 255)) #fundo branco

    desenhar_mapa(Labirinto, entrada, saida)
    if estado == 1:
        desenhar_caminho(menor_caminho)  
    elif estado == 2:
        desenhar_caminho(menor_caminho)
        desenhar_linha(entrada, saida) 
        mostrar_distancias(distancia_dijkstra, distancia_linha_, distancia_manhattan_)  

    pygame.display.update()
pygame.quit()
