# GAMEPLAY_OMW.py
from pplay.sprite import *
from pplay.window import *
from pplay.animation import *
import config
import FISICA_OMW 
import Rankings_OMW

# Importação dos módulos do jogo
import MAPA_OMW
import ITENS_OMW
import INIMIGOS_OMW
import OBJETOS_OMW
import POMBO_OMW
import BACKGROUND_OMW
import HUD_OMW

# Globais
jogador = None
hitbox_player = None

# Adicionado "defesa" ao dicionário para evitar KeyError
offsets_manuais = {
    "parado": 0, "corrida1": 0, "corrida2": 0, "corrida3": 0,
    "corrida4": 0, "corrida5": 0, "corrida6": 0, "salto1": 0, "salto2": 0,
    "defesa": 0
}

def inicializar_jogo():
    global jogador, hitbox_player

    # 1. Corpo Físico (O que colide com o mundo)
    hitbox_player = Sprite("assets/hitbox_invisivel.png") 
    hitbox_player.width = 78
    hitbox_player.height = 138
    hitbox_player.set_position(100, 520)
    
    # 2. Visual (Apenas a imagem que segue a hitbox)
    jogador = Sprite("assets/player/direita/parado_dir.png") 
    


    # Se voltou para a Fase 1 (por vitória ou reset), limpa o cronômetro acumulado
    if config.fase_selecionada == 1:
        config.tempo_total_jogo = 0.0

    config.direcao_player = "direita"
    config.estado_player = "parado"
    config.frame_corrida_atual = 1  
    config.cronometro_animacao = 0.0
    
    # SISTEMA DE VIDA E INTANGIBILIDADE
    config.vidas = 3
    config.invulneravel = False
    config.tempo_invulneravel = 0.0
    config.knockback_ativo = False
    config.tempo_knockback = 0.0
    config.visivel = True
    config.tempo_pisca = 0.0
    
    config.camera_x = 0
    config.tempo_fase_atual = 0.0 
    config.cafe_ativo = False
    config.fator_tempo_mundo = 1.0
    config.relogios_coletados = 0
    config.blocos_fase = []
    config.lista_cafes = []
    config.lista_inimigos = []
    config.lista_relogios = []
    
    MAPA_OMW.carregar_mapa()
    ITENS_OMW.gerar_itens()  
    INIMIGOS_OMW.gerar_inimigos()
    OBJETOS_OMW.gerar_objetos()
    largura_da_fase = MAPA_OMW.puxar_comprimento_mapa()
    POMBO_OMW.gerar_pombos(largura_da_fase)

def rodar_gameplay(janela, teclado, delta):
    global jogador, hitbox_player

    # --- Desenha as imagens de fundo em Parallax antes de todo o resto ---
    BACKGROUND_OMW.desenhar_background(janela)
    
    config.tempo_fase_atual += delta

    # --- 1. TIMERS DE DANOS E REAÇÕES ---
    if config.knockback_ativo:
        config.tempo_knockback -= delta
        if config.tempo_knockback <= 0:
            config.knockback_ativo = False

    if config.invulneravel:
        config.tempo_invulneravel -= delta
        
        # Efeito de piscar: Inverte a visibilidade a cada 0.07 segundos
        config.tempo_pisca += delta
        if config.tempo_pisca >= 0.07:
            config.visivel = not config.visivel
            config.tempo_pisca = 0.0
            
        if config.tempo_invulneravel <= 0:
            config.invulneravel = False
            config.visivel = True # Garante que volte a ser visível ao fim do tempo
    
    # --- 2. PROCESSAMENTO DA FÍSICA ---
    FISICA_OMW.atualizar_movimento_hitbox_player(hitbox_player, teclado, delta)
    
    # --- 3. ATUALIZAÇÃO DA CÂMERA ---
    if hitbox_player.x - config.camera_x > config.LARGURA / 2:
        config.camera_x = hitbox_player.x - config.LARGURA / 2
    if hitbox_player.x < config.camera_x:
        hitbox_player.x = config.camera_x

    # --- 4. DESENHO DO CENÁRIO (BLOCOS E LINHA DE CHEGADA) ---
    for bloco in config.blocos_fase:
        X_na_tela = bloco.x - config.camera_x
        if -bloco.width <= X_na_tela <= config.LARGURA:
            pos_real_x = bloco.x
            bloco.x = X_na_tela
            bloco.draw()
            bloco.x = pos_real_x
            
    X_linha_tela = config.linha_chegada.x - config.camera_x
    if -config.linha_chegada.width <= X_linha_tela <= config.LARGURA:
        pos_real_linha = config.linha_chegada.x
        config.linha_chegada.x = X_linha_tela
        config.linha_chegada.draw()
        config.linha_chegada.x = pos_real_linha
        
    # DESENHA OBJETOS URBANOS
    OBJETOS_OMW.atualizar_e_desenhar_objetos(hitbox_player, config.camera_x, delta)
        
    # --- 5. ITENS E PROCESSAMENTO DE DANOS DE INIMIGOS ---
    ITENS_OMW.atualizar_e_desenhar_itens(hitbox_player, delta) 
    
    if not config.invulneravel:
        colidiu_com_inimigo = INIMIGOS_OMW.atualizar_e_desenhar_inimigos(hitbox_player, delta)
        
        if colidiu_com_inimigo:
            config.vidas -= 1
            
            if config.vidas <= 0:
                # GAME OVER: Reseta para a primeira fase e reinicia os atributos
                config.fase_selecionada = 1 
                inicializar_jogo()
                return "gameover"  
            else:
                # Ativa o estado de invencibilidade pós-dano e empurrão
                config.invulneravel = True
                config.tempo_invulneravel = 2.0  
                config.knockback_ativo = True
                config.tempo_knockback = 0.25   
                config.visivel = False
                config.tempo_pisca = 0.0
                config.vel_y = -300 # Pequeno pulo de impacto
    else:
        # Se estiver invulnerável, apenas desenha os inimigos sem processar novos danos
        INIMIGOS_OMW.atualizar_e_desenhar_inimigos(hitbox_player, delta)

    POMBO_OMW.atualizar_e_desenhar_pombos(hitbox_player, delta)

    # --- 5.9 VITÓRIA COLETADA ---
    if hitbox_player.collided(config.linha_chegada):
        percentual_desconto = (config.relogios_coletados * 5) / 100.0
        tempo_com_desconto = config.tempo_fase_atual * (1.0 - percentual_desconto)
        
        # SE ESTIVER NA FASE 1 -> VAI PARA A FASE 2
        if config.fase_selecionada == 1:
            config.tempo_fase1 = tempo_com_desconto
            config.tempo_total_jogo += config.tempo_fase1
            config.fase_selecionada = 2
            return "selecao_skills"

        # SE ESTIVER NA FASE 2 -> VAI PARA A FASE 3 
        elif config.fase_selecionada == 2:
            config.tempo_fase2 = tempo_com_desconto
            config.tempo_total_jogo += config.tempo_fase2
            config.fase_selecionada = 3
            return "selecao_skills"

        # SE ESTIVER NA FASE 3 -> FIM DE JOGO / VITÓRIA FINAL
        elif config.fase_selecionada == 3:
            config.tempo_fase3 = tempo_com_desconto
            config.tempo_total_jogo += config.tempo_fase3
            
            # --- RECOMPENSA DA SKILL: LAXANTE ---
            if "laxante" in config.skills_adquiridas:
                config.tempo_total_jogo *= 0.80  # Reduz o tempo total em 20%
            
            # Salvamento Automático Silencioso
            tag_nome = getattr(config, "nome_jogador", "PLAYER")
            Rankings_OMW.salvar_ranking(tag_nome, config.tempo_total_jogo)
            
            
            # Agora o tempo sobrevive o suficiente para ser exibido na tela de vitória.
            
            config.fase_selecionada = 1
            return "vitoria"  # Avisa o MAIN_OMW que o jogo foi zerado!

# --- 5.10 MORTE POR QUEDA NO ABISMO ---
    if hitbox_player.y > 688:
        hitbox_player.set_position(100, 520) # Teletransporta de volta ao início
        config.camera_x = 0                  # Reseta o scroll da tela
        config.vel_y = 0                     # Zera o vetor de gravidade
        config.tempo_fase_atual += 5.0       # Penalidade de tempo
        return

    # --- 6. MÁQUINA DE ESTADOS DE ANIMAÇÃO ---
    if not config.knockback_ativo:
        # Mudado de setas para WASD (A/D)
        if teclado.key_pressed("D"): config.direcao_player = "direita"
        elif teclado.key_pressed("A"): config.direcao_player = "esquerda"

    sufixo = "dir" if config.direcao_player == "direita" else "esq"
    pasta = config.direcao_player
    arquivo_sprite = ""
    
    # Verificação de Prioridade 1: Está defendendo com a maleta?
    if getattr(config, "defendendo_maleta", False):
        arquivo_sprite = f"assets/player/{pasta}/defesa_{sufixo}.png"
        
    # Verificação de Prioridade 2: No ar? (Salto)
    elif hasattr(config, 'vel_y') and config.vel_y != 0:
        arquivo_sprite = f"assets/player/{pasta}/salto1_{sufixo}.png" if config.vel_y <= 0 else f"assets/player/{pasta}/salto2_{sufixo}.png"
        
    # Verificação de Prioridade 3: Correndo? (Movendo com A ou D)
    elif teclado.key_pressed("D") or teclado.key_pressed("A"):
        config.cronometro_animacao += delta
        if config.cronometro_animacao >= 0.08:
            config.frame_corrida_atual = (config.frame_corrida_atual % 6) + 1
            config.cronometro_animacao = 0.0
        arquivo_sprite = f"assets/player/{pasta}/corrida{config.frame_corrida_atual}_{sufixo}.png"
        
    # Padrão: Parado
    else:
        arquivo_sprite = f"assets/player/{pasta}/parado_{sufixo}.png"

    # --- 6.3 APLICAÇÃO DO VISUAL CENTRALIZADO ---
    if not hasattr(rodar_gameplay, "cache_imagens"): rodar_gameplay.cache_imagens = {}
    if arquivo_sprite not in rodar_gameplay.cache_imagens:
        try: rodar_gameplay.cache_imagens[arquivo_sprite] = pygame.image.load(arquivo_sprite).convert_alpha()
        except: rodar_gameplay.cache_imagens[arquivo_sprite] = None

    img_carregada = rodar_gameplay.cache_imagens[arquivo_sprite]
    
    if img_carregada:
        jogador.image = img_carregada
        jogador.width = img_carregada.get_width()
        jogador.height = img_carregada.get_height()
        
        H_WIDTH, H_HEIGHT = 78, 138
        centro_x = hitbox_player.x + (H_WIDTH / 2) - (jogador.width / 2)
        base_y = hitbox_player.y + H_HEIGHT - jogador.height
        
        # Pega a string do estado dinamicamente (ex: "defesa" ou "parado")
        nome_estado = arquivo_sprite.split('_')[0].split('/')[-1]
        # Remove números se for do tipo corrida1, corrida2...
        nome_estado = ''.join([i for i in nome_estado if not i.isdigit()])
        
        jogador.set_position(centro_x + offsets_manuais.get(nome_estado, 0), base_y)
    
    # --- 6.4 DESENHO CONDICIONAL ---
    if config.visivel:
        jogador.x -= config.camera_x
        jogador.draw()
        jogador.x += config.camera_x 
  
    # --- 7. INTERFACE DE USUÁRIO (HUD) DEDICADA ---
    HUD_OMW.desenhar_hud(janela, delta)
