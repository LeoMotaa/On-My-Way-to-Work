# BACKGROUND_OMW.py
import pygame
import config

# Dicionário de cache para carregar as imagens apenas UMA vez na memória
cache_backgrounds = {}

def inicializar_backgrounds():
    """Carrega as imagens de fundo uma única vez para evitar lentidão."""
    global cache_backgrounds
    try:
        # 1. Carrega o céu (compartilhado entre as fases)
        cache_backgrounds["ceu"] = pygame.image.load("assets/backgrounds/ceu_bg.png").convert_alpha()
        
        # 2. Carrega os cenários correspondentes a cada fase (Camada 3)
        cache_backgrounds[1] = pygame.image.load("assets/backgrounds/centralpark_bg.png").convert_alpha()
        cache_backgrounds[2] = pygame.image.load("assets/backgrounds/timessquare_bg.png").convert_alpha()
        cache_backgrounds[3] = pygame.image.load("assets/backgrounds/empirestate_bg.png").convert_alpha()
    except Exception as e:
        print(f"[AVISO] Erro ao carregar imagens de fundo: {e}")
        print("Criando fundos coloridos temporários para o jogo não travar...")
        
        # Fallbacks de segurança caso dê erro no caminho do arquivo
        for fase, cor in {1: (34, 139, 34), 2: (128, 128, 128), 3: (75, 0, 130)}.items():
            surf = pygame.Surface((config.LARGURA, config.ALTURA))
            surf.fill(cor)
            cache_backgrounds[fase] = surf

def desenhar_background(janela):
    
    # Garante que as imagens estejam carregadas no dicionário
    if not cache_backgrounds:
        inicializar_backgrounds()
        
    tela_pygame = janela.screen
        
    # --- CAMADA 1: O CÉU (Estático / Horizonte)
    imagem_ceu = cache_backgrounds.get("ceu")
    if imagem_ceu:
        tela_pygame.blit(imagem_ceu, (0, 0))
    else:
        janela.set_background_color((135, 206, 235))
    
    
    # --- CAMADA 3: PRÉDIOS DA FASE (Parallax)
    fase_atual = config.fase_selecionada
    imagem_fundo = cache_backgrounds.get(fase_atual)
    
    if imagem_fundo:
        largura_bg = imagem_fundo.get_width()
        
        # FATOR PARALAXE: 0.35 (Se move a 35% da velocidade da câmera)
        fator_paralaxe = 0.35
        
        # O operador % faz a mágica do loop infinito
        x_ajustado = -int(config.camera_x * fator_paralaxe) % largura_bg
        
        

        offsets_y = {
            1: 83,   # Fase 1: Central Park
            2: 23,   # Fase 2: Empire State
            3: 95   # Fase 3: Times Square
        }
        
        # Calcula a posição base
        y_pos = (config.ALTURA - imagem_fundo.get_height()) + offsets_y.get(fase_atual, 0)
        
        x_atual = x_ajustado - largura_bg
        
        # ...e continuamos carimbando o fundo até passar da largura da tela!
        while x_atual < config.LARGURA:
            tela_pygame.blit(imagem_fundo, (x_atual, y_pos))
            x_atual += largura_bg