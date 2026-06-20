# MAIN_OMW.py
from pplay.window import *
from pplay.keyboard import *
from pplay.mouse import *
import config
import pygame 

# Importação da arquitetura modular do jogo
import MENU_OMW
import Sel_Fases_OMW
import GAMEPLAY_OMW
import SELECAO_SKILLS_OMW
import AUDIO_OMW
import TELAS_FINAIS_OMW 
import Rankings_OMW 

# 1. INICIALIZAÇÃO
janela = Window(config.LARGURA, config.ALTURA)
janela.set_title("Oh My Word! - On My Way")

MENU_OMW.inicializar_menu()
GAMEPLAY_OMW.inicializar_jogo() 
Sel_Fases_OMW.inicializar_fases()

teclado = Keyboard()
mouse = Mouse()
mouse_pressionado_anterior = False


tela_anterior = "menu"

# 2. LOOP PRINCIPAL DO JOGO
while True:
    AUDIO_OMW.atualizar_musica()
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

     
    if config.tela == "jogo" and tela_anterior in ["menu", "fases"]:
        GAMEPLAY_OMW.inicializar_jogo()

    tela_anterior = config.tela

    if config.tela == "menu":
        MENU_OMW.rodar_menu(janela, clicou)

    elif config.tela == "fases":
        Sel_Fases_OMW.rodar_selecao_fases(janela, clicou)

    elif config.tela == "ranking": 
        config.tela = Rankings_OMW.rodar_ranking(janela, teclado)

    elif config.tela == "jogo":
        # Se pressionar ESC jogando, muda o estado e congela a gameplay
        if teclado.key_pressed("esc"):
            config.tela = "desistencia"
        else:
            resultado = GAMEPLAY_OMW.rodar_gameplay(janela, teclado, delta)
            
            if resultado == "selecao_skills":
                SELECAO_SKILLS_OMW.inicializar_selecao()
                config.tela = "selecao_skills"
            elif resultado == "vitoria":
                config.tela = "vitoria"
            elif resultado == "gameover": 
                config.tela = "gameover"
            elif resultado:
                config.tela = resultado

    elif config.tela == "selecao_skills":
        SELECAO_SKILLS_OMW.rodar_selecao_skills(janela, clicou)

    #TELA NA MÁQUINA DE ESTADOS:
    elif config.tela == "desistencia":
        config.tela = TELAS_FINAIS_OMW.rodar_desistencia(janela, teclado)

    elif config.tela == "vitoria":
        config.tela = TELAS_FINAIS_OMW.rodar_vitoria(janela, teclado)

    elif config.tela == "gameover":
        config.tela = TELAS_FINAIS_OMW.rodar_gameover(janela, teclado)

    janela.update()

