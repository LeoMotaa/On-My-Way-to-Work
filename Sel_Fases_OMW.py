# Sel_Fases_OMW.py
from pplay.sprite import *
import config

fase1 = None
fase2 = None
fase3 = None

def inicializar_fases():
    global fase1, fase2, fase3
    
    fase1 = Sprite("assets/FASE1.png")
    fase2 = Sprite("assets/FASE2.png")
    fase3 = Sprite("assets/FASE3.png")

    centro_x = config.LARGURA / 2
    centro_y = config.ALTURA / 2

    fase1.set_position(centro_x - fase1.width/2, centro_y - 150)
    fase2.set_position(centro_x - fase2.width/2, centro_y - 30)
    fase3.set_position(centro_x - fase3.width/2, centro_y + 90)

def rodar_selecao_fases(janela, clicou):
    
    janela.set_background_color((0, 0, 0))
    
    centro_x = config.LARGURA / 2
    janela.draw_text("SELECIONE O SEU TRAJETO", centro_x - 250, 80, size=35, color=(255, 255, 255))
    
    fase1.draw()
    fase2.draw()
    fase3.draw()

    if clicou and config.pode_clicar:
        if janela.mouse.is_over_object(fase1):
            config.fase_selecionada = 1 
            config.tela = "menu"
            config.jornada_completa = True         
            config.pode_clicar = False
        elif janela.mouse.is_over_object(fase2):
            config.fase_selecionada = 2 
            config.tela = "menu"
            config.jornada_completa = False
            config.pode_clicar = False
        elif janela.mouse.is_over_object(fase3):
            config.fase_selecionada = 3  
            config.tela = "menu"
            config.jornada_completa = False       
            config.pode_clicar = False