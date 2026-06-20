# FISICA_OMW.py
import config
import OBJETOS_OMW
import AUDIO_OMW

def atualizar_movimento_hitbox_player(hitbox_player, teclado, dt):
    # --- GERENCIADOR DO COOLDOWN DA BUZINA ---
    if not hasattr(config, "cooldown_buzina"):
        config.cooldown_buzina = 0.0
    
    if config.cooldown_buzina > 0:
        config.cooldown_buzina -= dt  # Reduz o tempo a cada frame

    # --- INICIALIZAÇÃO DO RASTREADOR DE PULO DUPLO ---
    if not hasattr(atualizar_movimento_hitbox_player, "up_anterior"):
        atualizar_movimento_hitbox_player.up_anterior = False
    if not hasattr(config, "pulos_feitos"):
        config.pulos_feitos = 0

    # Captura se a tecla W acabou de ser pressionada
    up_atual = teclado.key_pressed("W")
    apertou_up = up_atual and not atualizar_movimento_hitbox_player.up_anterior
    atualizar_movimento_hitbox_player.up_anterior = up_atual

    # Se estiver no chão firme, o contador de pulos reseta imediatamente
    if getattr(config, "no_chao", False):
        config.pulos_feitos = 0

    # ---  SKILL: MALETA  ---
    config.defendendo_maleta = False
    
    # Regra: Só ativa se tiver a skill, estiver no chão firme e segurando 'S'
    if "maleta" in config.skills_adquiridas and getattr(config, "no_chao", False) and teclado.key_pressed("S"):
        config.defendendo_maleta = True

    # 1. Controles laterais OU Lógica de Knockback
    if getattr(config, "knockback_ativo", False):
        direcao_kb = -1 if config.direcao_player == "direita" else 1
        config.vel_x = direcao_kb * (config.VELOCIDADE_JOGADOR * 1.3)
        
    elif config.defendendo_maleta:
        #  RESTRIÇÃO DA MALETA
        config.vel_x = 0
        
    else:
        # ---  SKILL: ENERGÉTICO ---
        vel_corrida = config.VELOCIDADE_JOGADOR
        if "energetico" in config.skills_adquiridas:
            vel_corrida *= config.BUFF_ENERGETICO
            
        # --- DEBUFF DA BOSTA DE POMBO ---
        if getattr(config, "reducao_velocidade", False):
            vel_corrida *= 0.50  # Aplica o redutor de velocidade
            
        config.vel_x = 0
        if teclado.key_pressed("A"):
            config.vel_x = -vel_corrida
        if teclado.key_pressed("D"):
            config.vel_x = vel_corrida

    # 2. Aplica gravidade
    config.vel_y += config.GRAVICADE * dt if hasattr(config, 'GRAVICADE') else config.GRAVIDADE * dt


    blocos_validos = []
    for bloco in config.blocos_fase:
        sob_bueiro = False
        for bueiro in getattr(OBJETOS_OMW, "lista_bueiros", []):
            if bloco.x < (bueiro.x + bueiro.width) and (bloco.x + bloco.width) > bueiro.x:
                sob_bueiro = True
                break
        if not sob_bueiro:
            blocos_validos.append(bloco)

    # 1. Obstáculos Sólidos Totais (Bloqueiam absolutamente tudo)
    obstaculos_solidos = (
        blocos_validos 
        + OBJETOS_OMW.lista_hidrantes
    )

    # 2. Plataformas Unidirecionais (Atravessáveis por baixo/lados, sólidas por cima)
    plataformas_unidirecionais = []
    
    # Inclui o teto e o capô do Ônibus
    for onibus in OBJETOS_OMW.lista_onibus:
        plataformas_unidirecionais.append(onibus.hitbox_capo)
        plataformas_unidirecionais.append(onibus.hitbox_teto)
        
    # Inclui a hitbox dos carros e táxis como plataformas unidirecionais
    for auto in OBJETOS_OMW.lista_automoveis:
        hitbox_carro = getattr(auto, "hitbox_fisica", auto)
        plataformas_unidirecionais.append(hitbox_carro)

    # -----------------------------------------

    # 3. Movimento Horizontal e Colisões (Apenas com calçada e hidrantes)
    hitbox_player.x += config.vel_x * dt

    for bloco in obstaculos_solidos:
        if hitbox_player.collided(bloco):
            if config.vel_x > 0: 
                hitbox_player.x = bloco.x - hitbox_player.width
            elif config.vel_x < 0: 
                hitbox_player.x = bloco.x + bloco.width

    # 4. Movimento Vertical e Colisões
    hitbox_player.y += config.vel_y * dt
    config.no_chao = False

    # 4a. Colisão vertical com blocos sólidos normais (chão rígido)
    for bloco in obstaculos_solidos:
        if hitbox_player.collided(bloco):
            if config.vel_y > 0: 
                hitbox_player.y = bloco.y - hitbox_player.height
                config.vel_y = 0
                config.no_chao = True
            elif config.vel_y < 0: 
                hitbox_player.y = bloco.y + bloco.width
                config.vel_y = 0

    # 4b. Colisão vertical com as plataformas (Ônibus, Carros e Táxis)
    base_do_pe = hitbox_player.y + hitbox_player.height
    for plat in plataformas_unidirecionais:
        if hitbox_player.collided(plat):
            
            
            if config.cooldown_buzina <= 0:
                AUDIO_OMW.tocar_buzina_aleatoria()
                config.cooldown_buzina = 8.0  # Tranca o som por 8 segundos
            
            if config.vel_y > 0 and (base_do_pe - config.vel_y * dt) <= plat.y + 20:
                hitbox_player.y = plat.y - hitbox_player.height
                config.vel_y = 0
                config.no_chao = True

    # ---  SKILL: PULO DUPLO ---
    # RESTRIÇÃO: Não pode pular se estiver defendendo com a maleta
    if apertou_up and not getattr(config, "knockback_ativo", False) and not config.defendendo_maleta:
        if config.no_chao:
            # Primeiro pulo padrão (Chão firme via 'W')
            config.vel_y = config.FORCA_PULO
            config.no_chao = False
            config.pulos_feitos = 1
        elif "pulo_duplo" in config.skills_adquiridas and config.pulos_feitos < 2:
            # Segundo pulo executado no ar (Sola de Mola ativa!)
            config.vel_y = config.FORCA_PULO
            config.pulos_feitos = 2