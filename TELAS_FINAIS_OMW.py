# TELAS_FINAIS_OMW.py
import config

def rodar_vitoria(janela, teclado):
    janela.set_background_color((0, 0, 0)) # Fundo preto clássico
    
    # Mensagem de Vitória
    janela.draw_text("VOCÊ VENCEU!", janela.width/2 - 140, janela.height/2 - 100, size=42, color=(0, 255, 0))
    
    # EXIBIÇÃO DO RANKING / TEMPO NA TELA
    if config.jornada_completa:
        # Mostra o tempo formatado com duas casas decimais
        texto_tempo = f"Tempo Final: {config.tempo_total_jogo:.2f}s (Salvo no Ranking!)"
        janela.draw_text(texto_tempo, janela.width/2 - 190, janela.height/2 - 20, size=18, color=(255, 215, 0)) # Dourado
    else:
        
        texto_aviso = "Tempo não registrado: Você usou a Seleção de Fases."
        janela.draw_text(texto_aviso, janela.width/2 - 240, janela.height/2 - 20, size=16, color=(255, 70, 70)) # Vermelho/Alerta

    
    janela.draw_text("Pressione ESC para voltar ao Menu", janela.width/2 - 170, janela.height/2 + 50, size=18, color=(255, 255, 255))
    
    if teclado.key_pressed("esc"):
        config.fase_selecionada = 1
        return "menu"
        
    return "vitoria"


def rodar_gameover(janela, teclado):
    janela.set_background_color((0, 0, 0))
    
    # Mensagem de Derrota
    janela.draw_text("VOCÊ PERDEU!", janela.width/2 - 140, janela.height/2 - 40, size=42, color=(255, 0, 0))
    janela.draw_text("Pressione ESC para voltar ao Menu", janela.width/2 - 170, janela.height/2 + 40, size=18, color=(255, 255, 255))
    
    if teclado.key_pressed("esc"):
        config.fase_selecionada = 1
        return "menu"
        
    return "gameover"


def rodar_desistencia(janela, teclado):
    
    janela.set_background_color((30, 30, 35))
    
    
    janela.draw_text("DESEJA DESISTIR DA PARTIDA?", janela.width/2 - 240, janela.height/2 - 60, size=28, color=(255, 255, 0))
    
    
    janela.draw_text("Pressione S para SIM (Voltar ao Menu)", janela.width/2 - 200, janela.height/2 + 10, size=18, color=(255, 100, 100))
    janela.draw_text("Pressione N para NÃO (Voltar ao Jogo)", janela.width/2 - 195, janela.height/2 + 50, size=18, color=(100, 255, 100))
    
    # AQUI ACONTECE O RESET TOTAL CASO DESISTA:
    if teclado.key_pressed("s"):
        config.fase_selecionada = 1
        config.tempo_total_jogo = 0.0
        config.tempo_fase_atual = 0.0
        config.skills_adquiridas = []
        config.pool_skills = ["laxante", "maleta", "energetico", "pulo_duplo", "ima"]
        return "menu"
        
    # Se pressionar N, volta para a partida exatamente de onde parou
    if teclado.key_pressed("n"):
        return "jogo"
        
    return "desistencia"