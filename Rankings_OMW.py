# Rankings_OMW.py
import datetime
import os
import config

ARQUIVO_RANKING = "ranking.txt"
lista_top_10 = []

def formatar_tempo(segundos):
    minutos = int(segundos) // 60
    seg = int(segundos) % 60
    return f"{minutos:02d}:{seg:02d}"

def salvar_ranking(nome, tempo_segundos):
    # Se a jornada NÃO for completa, para a função aqui mesmo e não grava nada
    if not config.jornada_completa:
        return 

    data_atual = datetime.date.today().strftime("%d/%m/%Y")
    
    with open(ARQUIVO_RANKING, "a", encoding="utf-8") as f:
        f.write(f"{nome},{int(tempo_segundos)},{data_atual}\n")

def carregar_ranking():
    global lista_top_10
    
    if not os.path.exists(ARQUIVO_RANKING):
        lista_top_10 = []
        return
    
    pontuacoes = []
    with open(ARQUIVO_RANKING, "r", encoding="utf-8") as f:
        for linha in f:
            linha = linha.strip()
            if linha:
                partes = linha.split(",")
                if len(partes) == 3:
                    nome, tempo_str, data = partes
                    pontuacoes.append((nome.strip(), int(tempo_str.strip()), data.strip()))
    
    # Ordena do menor tempo para o maior
    pontuacoes.sort(key=lambda x: x[1], reverse=False)
    lista_top_10 = pontuacoes[:10]

def rodar_ranking(janela, teclado):
    
    carregar_ranking()

    janela.set_background_color((0, 0, 0))
    
    # Título centralizado
    janela.draw_text("=== TOP 10 MELHORES TEMPOS ===", janela.width/2 - 210, 30, size=26, color=(255, 255, 0))
    
    y_pos = 90  
    
    if not lista_top_10:
        janela.draw_text("Nenhum recorde registrado ainda!", janela.width/2 - 180, 200, size=20, color=(255, 255, 255))
    else:
        for i, jogador in enumerate(lista_top_10):
            nome, tempo_segundos, data = jogador
            tempo_formatado = formatar_tempo(tempo_segundos)
            
            texto = f"{i+1}º  {nome.upper():<12} -  {tempo_formatado}  ({data})"
            janela.draw_text(texto, janela.width/2 - 200, y_pos, size=20, color=(255, 255, 255))
            y_pos += 40
            
    janela.draw_text("Pressione ESC para voltar ao Menu", janela.width/2 - 160, 540, size=16, color=(150, 150, 150))
    
    if teclado.key_pressed("esc"):
        return "menu"
        
    return "ranking"