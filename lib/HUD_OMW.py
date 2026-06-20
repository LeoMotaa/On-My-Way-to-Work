# HUD_OMW.py
import pygame
import config

def desenhar_hud(janela, delta):
    """Desenha uma barra de HUD com miniaturas grandes das skills ao lado do texto."""
    tela_pygame = janela.screen
    
    # 1. Dimensionamento do Painel
    ALTURA_HUD = 80
    Y_HUD = config.ALTURA - ALTURA_HUD  # Ex: 768 - 80 = 688
    
    # 2. Desenho do Painel Sólido
    COR_PAINEL = (40, 25, 15)       # Marrom escuro
    COR_BORDA = (90, 60, 38)        # Borda discreta
    COR_DIVISOR = (25, 15, 8)
    
    pygame.draw.rect(tela_pygame, COR_PAINEL, (0, Y_HUD, config.LARGURA, ALTURA_HUD))
    pygame.draw.line(tela_pygame, COR_BORDA, (0, Y_HUD), (config.LARGURA, Y_HUD), 4)
    pygame.draw.line(tela_pygame, COR_DIVISOR, (0, Y_HUD + 3), (config.LARGURA, Y_HUD + 3), 1)
    
    # 3. Cálculo do FPS
    fps = int(1 / delta) if delta > 0 else 0

    
    # --- COLUNA 1: STATUS DO JOGADOR (Esquerda) ---
    
    x_col1 = 30
    janela.draw_text("SAÚDE:", x_col1, Y_HUD + 12, size=14, color=(180, 180, 180), bold=True)
    janela.draw_text("♥ " * config.vidas, x=x_col1 + 65, y=Y_HUD + 6, size=24, color=(255, 40, 40), font_name="Arial")
    
    if config.reducao_velocidade:
        janela.draw_text(f"💩 LENTIDÃO ({config.tempo_reducao:.1f}s)", x_col1, Y_HUD + 42, size=14, color=(139, 69, 19), bold=True)
    else:
        janela.draw_text("Status: OK", x_col1, Y_HUD + 42, size=13, color=(130, 130, 130))
        
    janela.draw_text(f"FPS: {fps}", x_col1, Y_HUD + 62, size=11, color=(90, 90, 90))



    # NOVA CONFIGURAÇÃO: SKILLS ALINHADAS LADO A LADO (Centro-Esquerda)

    x_skills = 200  # Puxado um pouco para a esquerda para abrir mais ala
    
    # O texto "SKILLS:" agora fica centralizado na altura das cartas grandes
    janela.draw_text("SKILLS:", x_skills, Y_HUD + 32, size=13, color=(170, 170, 170), bold=True)
    
    if not hasattr(config, "cache_icones_hud"):
        config.cache_icones_hud = {}
        
    for idx, skill_nome in enumerate(config.skills_adquiridas):
        if skill_nome not in config.cache_icones_hud:
            try:
                img_original = pygame.image.load(f"assets/skills/{skill_nome}.png")
                img_mini = pygame.transform.scale(img_original, (50, 50))
                config.cache_icones_hud[skill_nome] = img_mini
            except Exception as e:
                continue
                
        icone_surface = config.cache_icones_hud[skill_nome]
        
        
        pos_x = x_skills + 65 + (idx * 56)
        
        pos_y = Y_HUD + 15 
        
        tela_pygame.blit(icone_surface, (pos_x, pos_y))



    # --- COLUNA 2: INVENTÁRIO E BUFFS (Movida para a Direita) ---

    x_col2 = 520  
    
    desconto_atual = config.relogios_coletados * 5
    janela.draw_text(f"Relógios: {config.relogios_coletados}/3 (-{desconto_atual}%)", x_col2, Y_HUD + 18, size=16, color=(255, 215, 0), bold=True)
    
    if config.cafe_ativo:
        janela.draw_text("☕ COFFEE TIME (Mundo -15%)", x_col2, Y_HUD + 46, size=14, color=(0, 255, 0), bold=True)
    else:
        janela.draw_text("☕ Café: Inativo", x_col2, Y_HUD + 46, size=14, color=(140, 140, 140))


    # --- COLUNA 3: CRONÔMETROS (Extrema Direita) ---
    x_col3 = config.LARGURA - 300
    janela.draw_text(f"Tempo Fase: {config.tempo_fase_atual:.2f}s", x_col3, Y_HUD + 12, size=18, color=(255, 255, 255), bold=True)
    
    tempo_acumulado_total = config.tempo_total_jogo + config.tempo_fase_atual
    janela.draw_text(f"Total: {tempo_acumulado_total:.2f}s", x_col3, Y_HUD + 40, size=14, color=(200, 200, 200))
    
    janela.draw_text(f"Fase: {config.fase_selecionada}/3", x_col3 + 180, Y_HUD + 40, size=13, color=(255, 255, 100), bold=True)