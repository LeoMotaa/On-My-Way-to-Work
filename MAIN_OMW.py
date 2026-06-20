# MAIN_OMW.py

import os
import sys

pasta_lib = os.path.abspath(os.path.join(os.path.dirname(__file__), "lib"))
if pasta_lib not in sys.path:
    sys.path.insert(0, pasta_lib)

from pplay.window import *
from pplay.keyboard import *
from pplay.mouse import *
from lib.config import *
import pygame 

# Importação da arquitetura modular do jogo
from lib.MENU_OMW import*
from lib.Sel_Fases_OMW import*
from lib.GAMEPLAY_OMW import*
from lib.SELECAO_SKILLS_OMW import*
from lib.AUDIO_OMW import*
from lib.TELAS_FINAIS_OMW import*
from lib.Rankings_OMW import*

# 1. INICIALIZAÇÃO
janela = Window(config.LARGURA, config.ALTURA)
janela.set_title("Oh My Word! - On My Way")

inicializar_menu()
inicializar_jogo() 
inicializar_fases()

teclado = Keyboard()
mouse = Mouse()
mouse_pressionado_anterior = False


tela_anterior = "menu"

# 2. LOOP PRINCIPAL DO JOGO
while True:
    atualizar_musica()
    delta = janela.delta_time()
    if delta > 0.1: delta = 0.1

    # Esconde o mouse também na tela de desistencia já que ela usa apenas o teclado (S/N)
    if config.tela in ["jogo", "vitoria", "gameover", "desistencia"]:
        pygame.mouse.set_visible(False)
    else:
        pygame.mouse.set_visible(True)

    mouse_pressionado_atual = mouse.is_button_pressed(1)
    clicou = mouse_pressionado_atual and not mouse_pressionado_anterior
    mouse_pressionado_anterior = mouse_pressionado_atual

    if not mouse_pressionado_atual:
        config.pode_clicar = True


    if config.tela == "jogo" and tela_anterior in ["menu", "fases", "selecao_skills"]:
        inicializar_jogo()

    tela_anterior = config.tela

    if config.tela == "menu":
        rodar_menu(janela, clicou)

    elif config.tela == "fases":
        rodar_selecao_fases(janela, clicou)

    elif config.tela == "ranking": 
        config.tela = Rankings_OMW.rodar_ranking(janela, teclado)

    elif config.tela == "jogo":
        # Se pressionar ESC jogando, muda o estado e congela a gameplay
        if teclado.key_pressed("esc"):
            config.tela = "desistencia"
        else:
            resultado = rodar_gameplay(janela, teclado, delta)
            
            if resultado == "selecao_skills":
                inicializar_selecao()
                config.tela = "selecao_skills"
            elif resultado == "vitoria":
                config.tela = "vitoria"
            elif resultado == "gameover": 
                config.tela = "gameover"
            elif resultado:
                config.tela = resultado

    elif config.tela == "selecao_skills":
        rodar_selecao_skills(janela, clicou)

    #TELA NA MÁQUINA DE ESTADOS:
    elif config.tela == "desistencia":
        config.tela = rodar_desistencia(janela, teclado)

    elif config.tela == "vitoria":
        config.tela = rodar_vitoria(janela, teclado)

    elif config.tela == "gameover":
        config.tela = rodar_gameover(janela, teclado)

    janela.update()

