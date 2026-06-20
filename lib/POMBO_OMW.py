# POMBO_OMW.py
from pplay.sprite import *
import config
import pygame
import math
import random
import AUDIO_OMW

def gerar_pombos(largura_mapa):
    config.lista_pombos = []
    config.lista_bostas = [] 
    
    if config.fase_selecionada == 1:
        passo = 700
    elif config.fase_selecionada == 2:
        passo = 500
    else:
        passo = 380 
    
    for x_centro in range(400, largura_mapa - 400, passo):
        pombo = Sprite("assets/pombo/direita/voo1_dir.png")
        
        pombo.x_centro = x_centro
        pombo.y_centro = random.randint(50, 90)     
        pombo.raio_x = random.randint(220, 280)      
        pombo.raio_y = random.randint(12, 18)         
        pombo.theta = random.uniform(0, 2 * math.pi)
        
        if config.fase_selecionada == 1:
            pombo.vel_angular = random.uniform(1.1, 1.5)
        elif config.fase_selecionada == 2:
            pombo.vel_angular = random.uniform(1.4, 1.7)
        else:
            pombo.vel_angular = random.uniform(1.6, 1.9)
        
        pombo.x_real = pombo.x_centro + pombo.raio_x * math.cos(pombo.theta)
        pombo.y_real = pombo.y_centro + pombo.raio_y * math.sin(pombo.theta)
        
        pombo.frame_atual = 1
        pombo.direcao_animacao = 1  
        pombo.cronometro_animacao = 0.0
        pombo.direcao_voo = "direita"
        
        pombo.cronometro_ataque = 0.0
        
        if config.fase_selecionada == 1:
            pombo.intervalo_ataque = random.uniform(2.5, 4.5)
        elif config.fase_selecionada == 2:
            pombo.intervalo_ataque = random.uniform(1.8, 3.2)
        else:
            pombo.intervalo_ataque = random.uniform(1.2, 2.2)
        
        #  SKILL: Laxante
        if "laxante" in getattr(config, "skills_adquiridas", []):
            pombo.intervalo_ataque *= 0.7
        
        config.lista_pombos.append(pombo)

def atualizar_e_desenhar_pombos(hitbox_player, dt):
    if not hasattr(atualizar_e_desenhar_pombos, "cache_pombos"):
        atualizar_e_desenhar_pombos.cache_pombos = {}
    cache = atualizar_e_desenhar_pombos.cache_pombos

    fator_tempo = config.fator_tempo_mundo

    # 1. PROCESSAMENTO DOS POMBOS & DISPAROS
    for pombo in config.lista_pombos:
        pombo.theta += pombo.vel_angular * fator_tempo * dt
        pombo.theta = pombo.theta % (2 * math.pi)
        
        x_antigo = pombo.x_real
        pombo.x_real = pombo.x_centro + pombo.raio_x * math.cos(pombo.theta)
        pombo.y_real = pombo.y_centro + pombo.raio_y * math.sin(pombo.theta)
        
        pombo.direcao_voo = "direita" if pombo.x_real > x_antigo else "esquerda"

        pombo.cronometro_animacao += dt
        limite_batimento = 0.11 / (1.0 + (config.fase_selecionada * 0.1))
        if pombo.cronometro_animacao >= limite_batimento:  
            pombo.cronometro_animacao = 0.0
            pombo.frame_atual += pombo.direcao_animacao
            if pombo.frame_atual == 3: pombo.direcao_animacao = -1
            elif pombo.frame_atual == 1: pombo.direcao_animacao = 1

        sufixo = "dir" if pombo.direcao_voo == "direita" else "esq"
        pasta = "direita" if pombo.direcao_voo == "direita" else "esquerda"
        caminho_img = f"assets/pombo/{pasta}/voo{pombo.frame_atual}_{sufixo}.png"
        
        if caminho_img not in cache:
            try: cache[caminho_img] = pygame.image.load(caminho_img).convert_alpha()
            except: cache[caminho_img] = None
        img = cache[caminho_img]
        if img:
            pombo.image = img
            pombo.width = img.get_width()
            pombo.height = img.get_height()

        pombo.x = pombo.x_real - config.camera_x
        pombo.y = pombo.y_real  

        if -pombo.width <= pombo.x <= config.LARGURA:
            pombo.draw()
            
            pombo.cronometro_ataque += dt
            if pombo.cronometro_ataque >= pombo.intervalo_ataque:
                pombo.cronometro_ataque = 0.0
                
                if config.fase_selecionada == 1:
                    pombo.intervalo_ataque = random.uniform(2.5, 4.5)
                    chance_disparo = 0.30 
                elif config.fase_selecionada == 2:
                    pombo.intervalo_ataque = random.uniform(1.8, 3.2)
                    chance_disparo = 0.45 
                else:
                    pombo.intervalo_ataque = random.uniform(1.2, 2.2)
                    chance_disparo = 0.55 
                
                # SKILL: Laxante
                if "laxante" in getattr(config, "skills_adquiridas", []):
                    pombo.intervalo_ataque *= 0.7
                    chance_disparo = min(1.0, chance_disparo * 1.5)
                
                if random.random() <= chance_disparo:
                    bosta = Sprite("assets/pombo/bosta.png")
                    bosta.x_real = pombo.x_real + (pombo.width / 2)
                    bosta.y_real = pombo.y_real + pombo.height
                    bosta.vel_y = 0.0
                    config.lista_bostas.append(bosta)

    # 2. PROCESSAMENTO DOS PROJÉTEIS (BOSTAS)
    y_chao = config.ALTURA - 100
    
    for bosta in config.lista_bostas[:]:
        bosta.vel_y += config.GRAVIDADE * fator_tempo * dt
        bosta.y_real += bosta.vel_y * dt
        
        bosta.x = bosta.x_real - config.camera_x
        bosta.y = bosta.y_real

        if -bosta.width <= bosta.x <= config.LARGURA:
            bosta.draw()

            # Colisão com o Player
            if (bosta.x_real < hitbox_player.x + hitbox_player.width and
                bosta.x_real + bosta.width > hitbox_player.x and
                bosta.y_real < hitbox_player.y + hitbox_player.height and
                bosta.y_real + bosta.height > hitbox_player.y):
                
                # SKILL: Maleta
                if "maleta" in config.skills_adquiridas and getattr(config, "defendendo_maleta", False):
                    # O projétil é destruído e o debuff NÃO afeta o jogador
                    config.lista_bostas.remove(bosta)
                    
                    AUDIO_OMW.tocar_sfx("colisao_bosta")
                    continue
                
                # Caso contrário, toma o debuff padrão de lentidão
                config.reducao_velocidade = True
                config.tempo_reducao = 4.0
                AUDIO_OMW.tocar_sfx("colisao_bosta")
                config.lista_bostas.remove(bosta)
                continue

        if bosta.y_real >= y_chao or bosta.y > config.ALTURA:
            config.lista_bostas.remove(bosta)

    # 3. GERENCIADOR DO TEMPO DE DEBUFF
    if config.reducao_velocidade:
        config.tempo_reducao -= dt
        
        if config.tempo_reducao <= 0:
            config.reducao_velocidade = False
        else:
            if "icon_lento" not in cache:
                try: cache["icon_lento"] = Sprite("assets/pombo/debuff_lento.png")
                except: cache["icon_lento"] = None
            
            icone = cache["icon_lento"]
            if icone:
                player_x_tela = hitbox_player.x - config.camera_x
                player_y_tela = hitbox_player.y
                
                icone.x = player_x_tela + (hitbox_player.width - icone.width) / 2
                icone.y = player_y_tela - icone.height - 8
                icone.draw()