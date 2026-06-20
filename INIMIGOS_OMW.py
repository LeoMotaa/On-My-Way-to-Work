# INIMIGOS_OMW.py
from pplay.sprite import *
import config
import random
import pygame
import AUDIO_OMW

def gerar_inimigos():
    config.lista_inimigos = []
    
    import MAPA_OMW
    rotas = MAPA_OMW.puxar_dados_inimigos()
    
    tipos_pedestres = ["velho", "homem", "mulher"]

    # Desempacota as 6 variáveis vindo da fase
    for x_ini, y_base, x_min, x_max, tipo, velocidade in rotas:
        
        if tipo == "terrestre":
            sub_tipo = random.choice(tipos_pedestres)
            caminho_inicial = f"assets/pedestres/{sub_tipo}/esquerda/{sub_tipo}1_esq.png"
            inimigo = Sprite(caminho_inicial)
            
            inimigo.tipo = "terrestre"
            inimigo.sub_tipo = sub_tipo
            inimigo.direcao = "esquerda"
            inimigo.velocidade = velocidade
            inimigo.y_base = y_base
            
            inimigo.hitbox_w = 32
            inimigo.hitbox_h = inimigo.height
            inimigo.hitbox_x = 0
            inimigo.hitbox_y = 0
            
            inimigo.x_real = x_ini
            inimigo.x_min = x_min
            inimigo.x_max = x_max
            inimigo.frame_atual = 1
            inimigo.cronometro_animacao = 0.0
            
            inimigo.set_position(x_ini, y_base - inimigo.height)
            config.lista_inimigos.append(inimigo)

def atualizar_e_desenhar_inimigos(hitbox_player, dt):
    colidiu = False
    
    if not hasattr(atualizar_e_desenhar_inimigos, "cache_sprites"):
        atualizar_e_desenhar_inimigos.cache_sprites = {}
        
    cache = atualizar_e_desenhar_inimigos.cache_sprites

    for inimigo in config.lista_inimigos:
        vel_ajustada = inimigo.velocidade * config.fator_tempo_mundo
        
        if inimigo.direcao == "esquerda":
            inimigo.x_real -= vel_ajustada * dt
            if inimigo.x_real <= inimigo.x_min:
                inimigo.direcao = "direita"
        else:
            inimigo.x_real += vel_ajustada * dt
            if inimigo.x_real >= inimigo.x_max:
                inimigo.direcao = "esquerda"

        inimigo.cronometro_animacao += dt
        if inimigo.cronometro_animacao >= 0.18:
            inimigo.frame_atual = 2 if inimigo.frame_atual == 1 else 1
            inimigo.cronometro_animacao = 0.0
        
        sufixo = "dir" if inimigo.direcao == "direita" else "esq"
        pasta_dir = "direita" if inimigo.direcao == "direita" else "esquerda"
        caminho_img = f"assets/pedestres/{inimigo.sub_tipo}/{pasta_dir}/{inimigo.sub_tipo}{inimigo.frame_atual}_{sufixo}.png"
        
        if caminho_img not in cache:
            try: cache[caminho_img] = pygame.image.load(caminho_img).convert_alpha()
            except: cache[caminho_img] = None
            
        img = cache[caminho_img] if 'caminho_img' not in locals() else cache[caminho_img]
        if img:
            inimigo.image = img
            inimigo.width = img.get_width()
            inimigo.height = img.get_height()

        x_tela = inimigo.x_real - config.camera_x
        inimigo.x = x_tela  
        inimigo.y = inimigo.y_base - inimigo.height
        
        if -inimigo.width <= x_tela <= config.LARGURA:
            inimigo.draw()

            hitbox_npc_x = inimigo.x_real + (inimigo.width - 32) / 2
            hitbox_npc_y = inimigo.y_base - inimigo.height
            hitbox_npc_w = 32
            hitbox_npc_h = inimigo.height
            
            if (hitbox_player.x < hitbox_npc_x + hitbox_npc_w and
                hitbox_player.x + hitbox_player.width > hitbox_npc_x and
                hitbox_player.y < hitbox_npc_y + hitbox_npc_h and
                hitbox_player.y + hitbox_player.height > hitbox_npc_y):
                
                base_pe_player = hitbox_player.y + hitbox_player.height
                topo_cabeca_inimigo = hitbox_npc_y
                area_cabeca = topo_cabeca_inimigo + 25
                
                # Jogador pulou na cabeça do inimigo (Eliminação)
                if getattr(config, "vel_y", 0) > 0 and base_pe_player <= area_cabeca:
                    
                    # SONOPLASTIA: Toca o som de eliminação do inimigo
                    AUDIO_OMW.tocar_sfx("eliminar_inimigo")
                    
                    config.lista_inimigos.remove(inimigo)
                    config.vel_y = -250 
                    break  
                else:
                    colidiu = True

    return colidiu