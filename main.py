# Projeto snake game de Felipe de Negredo, Deborah Heinig e Luísa R Foppa
# -----------------------------------------------------------------------------

import pygame
import pygame_menu
import random
import os
from pygame.locals import *
from pygame_menu.font import FONT_FRANCHISE, FONT_MUNRO
from pygame_menu.locals import ALIGN_CENTER
from pygame_menu.themes import *
from pygame_menu.widgets import MENUBAR_STYLE_UNDERLINE_TITLE
from typing import Tuple, Any, Optional, List

Vermelho = pygame.Color(165, 0, 21)
Verde = pygame.Color(29, 207, 78)
Azul = pygame.Color(74, 181, 230)
Amarelo = pygame.Color(250, 189, 6)
Roxo = pygame.Color(182, 42, 237)
Rosa = pygame.Color(237, 1, 171)
Bege = pygame.Color(237, 212, 176)
branco = pygame.Color(255, 255, 255)

CORES = ['Verde']

clock: Optional['pygame.time.Clock'] = None
main_menu: Optional['pygame_menu.Menu'] = None
surface: Optional['pygame.Surface'] = None

# definição para o movimento da cobra
CIMA = 0
DIREITA = 1
BAIXO = 2
ESQUERDA = 3

nome = ''


def menu(window):
    tela = window
    pygame.display.set_caption('Jogo da Cobra')

    #botão de jogar
    def jogar(color: List):

        def on_grid_random():
            x = random.randint(0, 59)
            y = random.randint(0, 59)
            return (x * 10), (y * 10)

        def colisao(c1, c2):
            return c1[0] == c2[0] and c1[1] == c2[1]

        # a cobra é uma lista de segmentos, cada segmento é uma tupla (x, y)
        cobra = [(200, 200), (210, 200), (220, 200)]
        # cor da cobra (RGB)

        cobra_skin = pygame.Surface((10, 10))

        if CORES[0] == 'Verde':
            cobra_skin.fill(Verde)
        if CORES[0] == 'Azul':
            cobra_skin.fill(Azul)
        if CORES[0] == 'Vermelho':
            cobra_skin.fill(Vermelho)
        if CORES[0] == 'Amarelo':
            cobra_skin.fill(Amarelo)
        if CORES[0] == 'Roxo':
            cobra_skin.fill(Roxo)
        if CORES[0] == 'Rosa':
            cobra_skin.fill(Rosa)
        if CORES[0] == 'Bege':
            cobra_skin.fill(Bege)

        minha_direcao= ESQUERDA

        apple_pos = on_grid_random()
        apple = pygame.Surface((10, 10))
        apple.fill((255, 0, 0))

        # limitar fps
        clock = pygame.time.Clock()

        font = pygame.font.Font(FONT_MUNRO, 18)
        score = 0

        game_over = False

        # enquanto game_over for falso
        while not game_over:
            clockvar = 10
            clock.tick(clockvar + score)

            # pegar todos os eventos de mudança (entradas)
            for event in pygame.event.get():
                # botão de fechar
                if event.type == QUIT:
                    pygame.quit()
                # se uma tecla for pressionada
                if event.type == KEYDOWN:
                    if event.key == K_UP and minha_direcao != BAIXO:
                        minha_direcao = CIMA
                    if event.key == K_DOWN and minha_direcao != CIMA:
                        minha_direcao = BAIXO
                    if event.key == K_LEFT and minha_direcao != DIREITA:
                        minha_direcao = ESQUERDA
                    if event.key == K_RIGHT and minha_direcao != ESQUERDA:
                        minha_direcao = DIREITA

            if colisao(cobra[0], apple_pos):
                apple_pos = on_grid_random()
                cobra.append((0, 0))
                score = score + 1

            # verificar se a cobra passou da janela
            if cobra[0][0] == 600 or cobra[0][1] == 600 or cobra[0][0] < 0 or cobra[0][1] < 0:
                game_over = True
                break

            # verificar se a cobra bateu nela mesma
            for i in range(1, len(cobra) -1):
                if cobra[0][0] == cobra[i][0] and cobra[0][1] == cobra[i][1]:
                    game_over = True
                    break

            if game_over:
                break

            for i in range(len(cobra) - 1, 0, -1):
                cobra[i] = (cobra[i-1][0], cobra[i-1][1])

            # faz a cobra se mover
            if minha_direcao == CIMA:
                cobra[0] = (cobra[0][0], cobra[0][1] - 10)
            if minha_direcao == BAIXO:
                cobra[0] = (cobra[0][0], cobra[0][1] + 10)
            if minha_direcao == DIREITA:
                cobra[0] = (cobra[0][0] + 10, cobra[0][1])
            if minha_direcao == ESQUERDA:
                cobra[0] = (cobra[0][0] - 10, cobra[0][1])

            # limpar tela para atualizar
            tela.fill((0, 0, 0))
            tela.blit(apple, apple_pos)

            for x in range(0, 600, 10): # Faz as linhas horizontais
                pygame.draw.line(tela, (40, 40, 40), (x, 0), (x, 600))
            for y in range(0, 600, 10):  # Faz as linhas verticas
                pygame.draw.line(tela, (40, 40, 40), (0, y), (600, y))

            # o True define que as bordas são suavizadas
            score_font = font.render('Score: %s' % score, True, (255, 255, 255))
            score_rect = score_font.get_rect()
            score_rect.topleft = (600 - 120, 10)
            tela.blit(score_font, score_rect)

            for pos in cobra:
                tela.blit(cobra_skin, pos)

            pygame.display.update()
        pass

        def salvar_score(nome, score):
            try:
                # Abre o arquivo
                # o a significa que ele é aberto para ser escrito no final do arquivo
                high_score_arquivo = open("high_score.txt", "a")
                high_score_arquivo.write(str(nome + " - " + score))
                high_score_arquivo.write(" || ")
                high_score_arquivo.close()
            except IOError:
                # Se não for possível salvar
                print("Não foi possível salvar a pontuação")
        pass

        if game_over:
            print('O score final foi: ', score)
            salvar_score(nome, str(score))

    pass

    def armazenanome(value):
        global nome
        nome = value
    pass

    def set_cor(valor: Tuple[Any, int], cor: str):
        selecao, indice = valor
        print(f'Cor Selecionada: "{selecao}" ({cor}) no índice {indice}')
        CORES[0] = cor
    pass

    def ScoreTexto():
        txt_highscore = open("high_score.txt", "r")
        textoarq = []
        for linha in txt_highscore:
            textoarq.append(linha)
        textoarq = ''.join(textoarq)

        go_score = True
        while go_score:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    go_score = False
                tela.fill(pygame.Color(18, 18, 18))
                fontText = pygame.font.SysFont('Arial', 35)
                Mostraessetexto = fontText.render(textoarq, True, pygame.Color(0, 255, 0))
                tela.blit(Mostraessetexto, (20, 50))
                if event.type == MOUSEBUTTONDOWN:
                    go_score = False
                pygame.display.update()

        txt_highscore.close()
    pass


    # saída no menu
    def sair():
       #pygame_menu.events.EXIT
       pygame.quit()
       pass

    # criação do tema

    fonte = pygame_menu.font.FONT_MUNRO
    otema_menu = Theme(background_color=(68, 68, 68, 68),  # dark background
                       title_background_color=(8, 122, 61),
                       title_bar_style=MENUBAR_STYLE_UNDERLINE_TITLE,
                       title_font=FONT_FRANCHISE,
                       title_font_size=100,
                       title_font_color=(82, 173, 102),
                       title_font_shadow=False,
                       widget_padding=5,
                       widget_font=fonte,
                       widget_font_size=50,
                       )

    menu = pygame_menu.Menu('Jogo da Cobra'.center(25), 600, 400, theme=otema_menu)

    otema_menu.title_bar_style = ALIGN_CENTER

    def validate_simple(data: Any):
        return True
    pass

    # botões

    #butao= False

    menu.add.text_input('Nome :', font_color='green', onchange=armazenanome, default="")  # nome pro placar
    menu.add.button('Jogar', jogar, CORES, font_color='green')
    menu.add.selector('Cor da cobra :', [('Verde', 'Verde'), ('Vermelho', 'Vermelho'), ('Azul', 'Azul'),
                            ('Amarelo', 'Amarelo'), ('Roxo', 'Roxo'), ('Rosa', 'Rosa'), ('Bege', 'Bege')
                            ], onchange=set_cor, selector_id='set_color', font_color='green')
    menu.add.button('Placar', ScoreTexto, font_color='green')  # placar a configurar ainda
    menu.add.button('Sair', sair, font_color='red')

    #if butao == True:
    #    ScoreTexto()

    menu.mainloop(tela)


def main():
    pygame.init()  # inicia o pygame
    janelamenu = pygame.display.set_mode((600, 600))  # janela que será o menu
    pygame.display.set_caption('Jogo da Cobra')
    menu(janelamenu)


main()

