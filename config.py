# config.py

# Estado do jogo
tela = "menu"
fase_selecionada = 1
pode_clicar = True

# Configurações da Janela
LARGURA = 1366
ALTURA = 768

# Cores
COR_FUNDO_JOGO = (30, 30, 30)

# --- FÍSICA E JOGADOR ---
VELOCIDADE_JOGADOR = 210  # Pixels por segundo andando de lado
FORCA_PULO = -666       # Força para cima (negativa no eixo Y do Pygame)
GRAVIDADE = 1260         # Aceleração puxando para baixo

# Estados dinâmicos do jogador (começam em zero)
vel_x = 0                
vel_y = 0
no_chao = False          # Diz se o personagem está pisando em uma plataforma

# Lista que guardará os sprites de plataformas/blocos da fase atual
blocos_fase = []

camera_x = 0


tempo_fase_atual = 0.0    
tempo_total_jogo = 0.0    

# Controle do Café (Efeito Bullet Time: -15% de velocidade no mundo e cronômetro)
cafe_ativo = False
fator_tempo_mundo = 1.0   # Multiplicador que afeta o relógio e inimigos (padrão: 1.0)

# Controle do Relógio (Stack de até 3 itens: cada um tira 5% do tempo final)
relogios_coletados = 0

# Listas de sprites para o gerenciador de itens
lista_cafes = []
lista_relogios = []

# --- INIMIGOS / OBSTÁCULOS ---
VELOCIDADE_INIMIGO = 120  # Pixels por segundo

# Lista que guardará os sprites e direções dos inimigos na fase
lista_inimigos = []

# --- HISTÓRICO DE TEMPOS ---
tempo_fase1 = 0.0
tempo_fase2 = 0.0
tempo_fase3 = 0.0

# Objeto que representará a linha de chegada na gameplay
linha_chegada = None

tempo_animacao = 0.0

# --- CONTROLE DE ANIMACAO POR ARQUIVOS SEPARADOS ---
frame_corrida_atual = 1
cronometro_animacao = 0.0

lista_pombos = []
lista_bostas = []
reducao_velocidade = False  # Indica se o player está sob efeito do debuff
tempo_reducao = 0.0         # Cronômetro de quanto tempo dura a lentidão

proxima_fase = 1
pool_skills = ["laxante", "maleta", "energetico", "pulo_duplo", "ima"]
skills_adquiridas = []
cards_sprites = []

BUFF_ENERGETICO = 1.25 

DISTANCIA_ATRACAO_IMA = 300  # Raio em pixels onde o ímã começa a puxar os itens
VELOCIDADE_ATRACAO_ITEM = 400  # Velocidade com que o item voa até o player

jornada_completa = True