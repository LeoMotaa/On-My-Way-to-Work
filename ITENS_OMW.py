# ITENS_OMW.py
from pplay.sprite import *
import random
import config
import MAPA_OMW
import math  
import AUDIO_OMW 

def gerar_itens():
    config.lista_cafes = []
    config.lista_relogios = []

    # Puxa a lista de coordenadas limpas das fases
    possiveis_posicoes = MAPA_OMW.puxar_dados_itens()
    
    if len(possiveis_posicoes) >= 5:
        posicoes_sorteadas = random.sample(possiveis_posicoes, 5)
        
        # Cria os 2 Cafés
        for i in range(2):
            pos = posicoes_sorteadas.pop()
            cafe = Sprite("assets/coffee.png") 
            cafe.set_position(pos[0], pos[1])
            config.lista_cafes.append(cafe)
            
        # Cria os 3 Relógios
        for i in range(3):
            pos = posicoes_sorteadas.pop()
            relogio = Sprite("assets/relogio.png") 
            relogio.set_position(pos[0], pos[1])
            config.lista_relogios.append(relogio)

def atualizar_e_desenhar_itens(jogador, delta):
    if not hasattr(config, 'tempo_animacao'):
        config.tempo_animacao = 0.0
    config.tempo_animacao += delta

    # Efeito Juice: Oscilação sutil de 8 pixels para cima e para baixo
    deslocamento_y = math.sin(config.tempo_animacao * 4) * 8

    # Pegamos as novas configurações do Super Ímã (com valores padrão de segurança)
    raio_ima = getattr(config, "DISTANCIA_ATRACAO_IMA", 300)
    velocidade_atracao = getattr(config, "VELOCIDADE_ATRACAO_ITEM", 400)

    # --- GERENCIAR CAFÉS ---
    for cafe in config.lista_cafes[:]:
        
        #  SKILL: ÍMÃ DE ACHADOS
        if "ima" in config.skills_adquiridas:
            centro_jogador_x = jogador.x + jogador.width / 2
            centro_jogador_y = jogador.y + jogador.height / 2
            centro_cafe_x = cafe.x + cafe.width / 2
            centro_cafe_y = cafe.y + cafe.height / 2
            
            dx = centro_jogador_x - centro_cafe_x
            dy = centro_jogador_y - centro_cafe_y
            distancia = math.hypot(dx, dy) # Otimização matemática
            
            # Puxa o item utilizando o novo raio consideravelmente maior
            if 0 < distancia <= raio_ima:
                cafe.x += (dx / distancia) * velocidade_atracao * delta
                cafe.y += (dy / distancia) * velocidade_atracao * delta

        if jogador.collided(cafe):
            config.cafe_ativo = True
            config.fator_tempo_mundo = 0.85
            AUDIO_OMW.tocar_sfx("coleta_item")
            config.lista_cafes.remove(cafe)
            continue
            
        X_na_tela = cafe.x - config.camera_x
        if 0 <= X_na_tela <= config.LARGURA:
            pos_real_x = cafe.x
            pos_real_y = cafe.y
            
            cafe.x = X_na_tela
            cafe.y = pos_real_y + deslocamento_y
            cafe.draw()
            
            cafe.x = pos_real_x
            cafe.y = pos_real_y

    # --- GERENCIAR RELÓGIOS ---
    for relogio in config.lista_relogios[:]:
        
        # SKILL: ÍMÃ DE ACHADOS (Atração Física do Relógio)
        if "ima" in config.skills_adquiridas:
            centro_jogador_x = jogador.x + jogador.width / 2
            centro_jogador_y = jogador.y + jogador.height / 2
            centro_relogio_x = relogio.x + relogio.width / 2
            centro_relogio_y = relogio.y + relogio.height / 2
            
            dx = centro_jogador_x - centro_relogio_x
            dy = centro_jogador_y - centro_relogio_y
            distancia = math.hypot(dx, dy)
            
            # Puxa o item utilizando o novo raio consideravelmente maior
            if 0 < distancia <= raio_ima:
                relogio.x += (dx / distancia) * velocidade_atracao * delta
                relogio.y += (dy / distancia) * velocidade_atracao * delta

        if jogador.collided(relogio):
            if config.relogios_coletados < 3:
                config.relogios_coletados += 1
                
            AUDIO_OMW.tocar_sfx("coleta_item")
            config.lista_relogios.remove(relogio)
            continue
            
        X_na_tela = relogio.x - config.camera_x
        if 0 <= X_na_tela <= config.LARGURA:
            pos_real_x = relogio.x
            pos_real_y = relogio.y
            
            relogio.x = X_na_tela
            relogio.y = pos_real_y + deslocamento_y
            relogio.draw()
            
            relogio.x = pos_real_x
            relogio.y = pos_real_y