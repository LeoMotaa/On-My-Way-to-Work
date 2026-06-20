# MENU_OMW.py
from pplay.sprite import *
import config
import GAMEPLAY_OMW 

# Deixamos as variáveis globais do módulo vazias por enquanto
background = None
jogar = None
fases = None
ranking = None
sair = None

def inicializar_menu():
    global background, jogar, fases, ranking, sair
    
    # Só criamos os sprites aqui, depois que a janela já existe!
    background = Sprite("assets/BACKGROUND_MENU.png")
    background.set_position(0, 0)

    jogar = Sprite("assets/JOGAR.png")
    fases = Sprite("assets/FASES.png") 
    ranking = Sprite("assets/RANKINGS.png")
    sair = Sprite("assets/SAIR.png")

    centro_x = config.LARGURA / 2
    centro_y = config.ALTURA / 2
    espaco_x = 30
    linha1_y = centro_y - 50
    linha2_y = centro_y + 125

    jogar.set_position(centro_x - jogar.width - espaco_x, linha1_y)
    fases.set_position(centro_x + espaco_x, linha1_y)
    ranking.set_position(centro_x - ranking.width - espaco_x, linha2_y)
    sair.set_position(centro_x + espaco_x, linha2_y)

def rodar_menu(janela, clicou):
    global background, jogar, fases, ranking, sair
    
    background.draw() 
    jogar.draw()
    fases.draw()
    ranking.draw()
    sair.draw()

    if clicou and config.pode_clicar:

        if janela.mouse.is_over_object(jogar):
            
            if config.fase_selecionada == 1:
                config.jornada_completa = True
            
            # Zera os cronômetros para a nova tentativa
            config.tempo_total_jogo = 0.0
            config.tempo_fase_atual = 0.0
            
            # Limpa o inventário de poderes do jogador
            config.skills_adquiridas = []
            config.pool_skills = ["laxante", "maleta", "energetico", "pulo_duplo", "ima"]
            
            # Reconstrói o mapa baseado na fase ativa (seja ela 1, 2 ou 3!)
            GAMEPLAY_OMW.inicializar_jogo()
            
            # Altera o estado da máquina para iniciar o jogo
            config.tela = "jogo"
            config.pode_clicar = False
            
        elif janela.mouse.is_over_object(fases):
            config.tela = "fases"
            config.pode_clicar = False
            
        elif janela.mouse.is_over_object(ranking):
            config.tela = "ranking"
            config.pode_clicar = False
            
        elif janela.mouse.is_over_object(sair):
            janela.close()