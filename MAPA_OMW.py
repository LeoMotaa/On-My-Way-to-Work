# MAPA_OMW.py
from pplay.sprite import *
import config

# Importa os módulos específicos de cada fase
import FASE_CentralPark
import FASE_TimesSquare
import FASE_EmpireState

def carregar_mapa():
    # Limpa a lista de blocos antes de carregar a fase atual
    config.blocos_fase = []
    
    # 1. Cada arquivo carrega sua respectiva matriz de cenário
    if config.fase_selecionada == 1:
        FASE_CentralPark.carregar()
    elif config.fase_selecionada == 2:
        FASE_TimesSquare.carregar()
    elif config.fase_selecionada == 3:
        FASE_EmpireState.carregar()

    config.blocos_fase = [bloco for bloco in config.blocos_fase if bloco.y >= 150]

    
    ajustes_x = {
        1: 0,    # Ajuste fino horizontal para o Metrô (Fase 1)
        2: 0,    # Ajuste fino horizontal para o Metrô (Fase 2)
        3: 0   # Ajuste fino horizontal para o Prédio da Firma (Fase 3)
    }
    
    ajustes_y = {
        1: 15,    # Ajuste fino vertical para o Metrô (Fase 1)
        2: 15,    # Ajuste fino vertical para o Metrô (Fase 2)
        3: 25     # Ajuste fino vertical para o Prédio da Firma (Fase 3)
    }

    largura_total_fase = puxar_comprimento_mapa()
    fase_atual = config.fase_selecionada
    
    # Define o arquivo correto de acordo com a fase
    if fase_atual in [1, 2]:
        config.linha_chegada = Sprite("assets/backgrounds/metro.png")
    else:
        config.linha_chegada = Sprite("assets/backgrounds/entrada.png")
        
    
    pos_x = (largura_total_fase - config.linha_chegada.width - 250) + ajustes_x.get(fase_atual, 0)
    
    pos_y = (658 - config.linha_chegada.height) + ajustes_y.get(fase_atual, 0)
    
    # Aplica as coordenadas finais ajustadas ao Sprite
    config.linha_chegada.set_position(pos_x, pos_y)


def puxar_comprimento_mapa():
    
    if config.fase_selecionada == 1:
        return FASE_CentralPark.obter_comprimento_mapa()
    elif config.fase_selecionada == 2:
        return FASE_TimesSquare.obter_comprimento_mapa()
    else:
        return FASE_EmpireState.obter_comprimento_mapa()

def puxar_dados_itens():
    if config.fase_selecionada == 1:
        return FASE_CentralPark.obter_posicoes_itens()
    elif config.fase_selecionada == 2:
        return FASE_TimesSquare.obter_posicoes_itens()
    else:
        return FASE_EmpireState.obter_posicoes_itens()

def puxar_dados_inimigos():
    if config.fase_selecionada == 1:
        return FASE_CentralPark.obter_rotas_inimigos()
    elif config.fase_selecionada == 2:
        return FASE_TimesSquare.obter_rotas_inimigos()
    else:
        return FASE_EmpireState.obter_rotas_inimigos()

def puxar_dados_objetos():
    if config.fase_selecionada == 1:
        return FASE_CentralPark.obter_dados_objetos()
    elif config.fase_selecionada == 2:
        return FASE_TimesSquare.obter_dados_objetos()
    else:
        return FASE_EmpireState.obter_dados_objetos()