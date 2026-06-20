# AUDIO_OMW.py
import pygame
import config
import random  # Importado para podermos sortear entre as duas buzinas!

# Inicializa o mixer de áudio do Pygame
pygame.mixer.init()

# --- PLAYLIST DE MÚSICAS ---
PLAYLIST = {
    "menu": "assets/audio/lobby_salsa.mp3",
    "ranking": "assets/audio/lobby_salsa.mp3",
    "fases": "assets/audio/lobby_salsa.mp3",
    "fase_1": "assets/audio/central_park_jazz.mp3",
    "fase_2": "assets/audio/times_square_funk.mp3",
    "fase_3_a": "assets/audio/empire_state_swing_1.mp3",
    "fase_3_b": "assets/audio/empire_state_swing_2.mp3",
    "gameover": "assets/audio/gameover_melancolico.mp3",
    "vitoria": "assets/audio/vitoria_fanfarra.mp3"
}

# --- CAMINHOS DOS EFEITOS SONOROS (SFX) ---
SFX_PATHS = {
    "buzina_1": "assets/audio/sfx_buzina1.mp3",
    "buzina_2": "assets/audio/sfx_buzina2.mp3",
    "eliminar_inimigo": "assets/audio/sfx_eliminar.mp3",
    "colisao_bosta": "assets/audio/sfx_bosta.mp3",
    "coleta_item": "assets/audio/sfx_item.mp3"
}

# Dicionário de cache para guardar os áudios carregados na memória
sfx_carregados = {}

musica_atual = None

# Variáveis de controle da Fase 3
fase3_faixa_ativa = "fase_3_a"
fase3_em_transicao = False
fase3_timestamp_estado = 0

def atualizar_musica():
    global musica_atual, fase3_faixa_ativa, fase3_em_transicao, fase3_timestamp_estado
    
    tempo_atual_ms = pygame.time.get_ticks()
    no_jogo = (config.tela == "jogo")
    na_fase_3 = (no_jogo and config.fase_selecionada == 3)
    
    if not na_fase_3:
        fase3_faixa_ativa = "fase_3_a"
        fase3_em_transicao = False
        fase3_timestamp_estado = tempo_atual_ms
        
    if na_fase_3:
        tempo_passado = (tempo_atual_ms - fase3_timestamp_estado) / 1000.0
        
        if fase3_em_transicao:
            if tempo_passado >= 3.0:
                fase3_em_transicao = False
                fase3_faixa_ativa = "fase_3_b" if fase3_faixa_ativa == "fase_3_a" else "fase_3_a"
                fase3_timestamp_estado = tempo_atual_ms
                musica_atual = None
            else:
                musica_atual = "silencio"
                return
        else:
            if tempo_passado >= 30.0:
                fase3_em_transicao = True
                fase3_timestamp_estado = tempo_atual_ms
                pygame.mixer.music.fadeout(500)
                musica_atual = "silencio"
                return

    if config.tela in ["menu", "ranking", "fases"]:
        faixa_obrigatoria = PLAYLIST["menu"]
    elif config.tela == "jogo":
        if config.fase_selecionada == 1:
            faixa_obrigatoria = PLAYLIST["fase_1"]
        elif config.fase_selecionada == 2:
            faixa_obrigatoria = PLAYLIST["fase_2"]
        elif config.fase_selecionada == 3:
            faixa_obrigatoria = PLAYLIST[fase3_faixa_ativa]
    elif config.tela in ["vitoria", "gameover"]:
        faixa_obrigatoria = PLAYLIST[config.tela]
    else:
        faixa_obrigatoria = None

    if faixa_obrigatoria and faixa_obrigatoria != musica_atual:
        try:
            pygame.mixer.music.fadeout(400)
            pygame.mixer.music.load(faixa_obrigatoria)
            pygame.mixer.music.play(-1)
            pygame.mixer.music.set_volume(0.4)
            musica_atual = faixa_obrigatoria
        except pygame.error:
            print(f"Erro: Música não encontrada: {faixa_obrigatoria}")
            musica_atual = faixa_obrigatoria

# --- SISTEMA DE DISPARO DE SFX ---
def tocar_sfx(nome_sfx):
    """Carrega dinamicamente o som (se não estiver no cache) e o reproduz instantaneamente."""
    global sfx_carregados
    
    # Se o som ainda não foi carregado na memória, tenta carregar
    if nome_sfx not in sfx_carregados:
        if nome_sfx in SFX_PATHS:
            try:
                # Carrega o arquivo usando o construtor Sound do Pygame
                som = pygame.mixer.Sound(SFX_PATHS[nome_sfx])
                som.set_volume(0.6) # Volume dos efeitos em 60% (um pouco mais alto que a música)
                sfx_carregados[nome_sfx] = som
            except pygame.error:
                print(f"Aviso: Arquivo de som para '{nome_sfx}' não encontrado em {SFX_PATHS[nome_sfx]}")
                sfx_carregados[nome_sfx] = None
        else:
            print(f"Erro: SFX com o nome '{nome_sfx}' não existe no dicionário de caminhos.")
            return

    # Se o som foi carregado com sucesso, toca ele
    if sfx_carregados[nome_sfx] is not None:
        sfx_carregados[nome_sfx].play()

def tocar_buzina_aleatoria():
    """Sorteia e toca uma das duas buzinas de carro disponíveis."""
    buzina_escolhida = random.choice(["buzina_1", "buzina_2"])
    tocar_sfx(buzina_escolhida)