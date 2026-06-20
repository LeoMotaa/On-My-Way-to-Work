# SELECAO_SKILLS_OMW.py
from pplay.sprite import *
import random
import config
import GAMEPLAY_OMW

def inicializar_selecao():
    
    config.cards_sprites = []

def rodar_selecao_skills(janela, clicou):
    
    janela.set_background_color((20, 24, 35)) 

    # 1. GERAÇÃO E CENTRALIZAÇÃO DAS CARTAS
    if not hasattr(config, "cards_sprites") or len(config.cards_sprites) == 0:
        config.cards_sprites = []
        temp_cards = []
        
        # Sorteia dinamicamente 3 opções
        qtd_para_sortear = min(3, len(config.pool_skills))
        config.skills_para_escolha = random.sample(config.pool_skills, qtd_para_sortear)
        
        
        for skill_nome in config.skills_para_escolha:
            card = Sprite(f"assets/skills/{skill_nome}.png")
            card.id_skill = skill_nome  # Guarda a ID da skill no próprio objeto
            temp_cards.append(card)
            
        if temp_cards:
            w_card = temp_cards[0].width
            h_card = temp_cards[0].height
            espacamento = 50
            
            # Calcula a largura total ocupada pelo bloco de cartas para centralizar na tela
            total_w = (len(temp_cards) * w_card) + ((len(temp_cards) - 1) * espacamento)
            inicio_x = (config.LARGURA - total_w) / 2
            
            
            for idx, card in enumerate(temp_cards):
                card.x = inicio_x + idx * (w_card + espacamento)
                card.y = (config.ALTURA - h_card) / 2
                config.cards_sprites.append(card)

    # 2. RENDERIZAÇÃO E DETECÇÃO DE CLIQUES
    for card in config.cards_sprites:
        card.draw()
        
        
        if janela.mouse.is_over_object(card) and clicou and getattr(config, "pode_clicar", True):
            config.pode_clicar = False  # Evita cliques duplicados indesejados
            
            # Salva o poder escolhido permanentemente na build da partida
            config.skills_adquiridas.append(card.id_skill)
            
            
            if card.id_skill in config.pool_skills:
                config.pool_skills.remove(card.id_skill)
            
            
            config.cards_sprites = []
            
            
            GAMEPLAY_OMW.inicializar_jogo()
            
            
            config.tela = "jogo"
            break