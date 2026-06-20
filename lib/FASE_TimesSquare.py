# FASE_TimesSquare.py
import random
from pplay.sprite import *
import config

def carregar():
    largura_bloco = 36 
    altura_chao = config.ALTURA - 100
    comprimento_mapa = 250 
    
    # O chão agora é gerado por completo
    for i in range(0, comprimento_mapa): 
        bloco = Sprite("assets/bloco_teste.png")
        bloco.width = 36
        bloco.height = 36
        bloco.set_position(i * largura_bloco, altura_chao)
        bloco.tem_colisao = True
        config.blocos_fase.append(bloco)



def obter_dados_objetos():
    automoveis = []
    onibus = []
    hidrantes = []
    bueiros = []

    x = 500  
    fim_mapa = (250 * 36) - 1000 

    while x < fim_mapa:
        dado = random.random()
        
        if dado < 0.22:  # 22% de chance de Carros/Táxis
            tipo_carro = "taxi" if random.random() < 0.8 else "carro"
            automoveis.append((x, tipo_carro))
            x += random.randint(250, 450)  # Distância equilibrada
            
        elif dado < 0.30:  # 8% de chance de Ônibus
            onibus.append(x)
            x += random.randint(450, 700)
            
        elif dado < 0.40:  # 10% de Hidrantes
            hidrantes.append(x)
            x += random.randint(200, 350)
            
        elif dado < 0.44:  # 4% de Bueiros
            bueiros.append(x)
            x += random.randint(500, 750)
            
        else:
            x += random.randint(60, 120)

    return automoveis, onibus, hidrantes, bueiros

def obter_posicoes_itens():
    altura_itens = config.ALTURA - 220 
    posicoes_aleatorias = []
    for x_base in range(400, 8500, 270):
        if random.random() < 0.72: 
            x_final = x_base + random.randint(-40, 40)
            posicoes_aleatorias.append((x_final, altura_itens))
    return posicoes_aleatorias

def obter_rotas_inimigos():
    rotas = []
    y_chao = config.ALTURA - 100
    
    for x_base in range(600, 8500, 450):
        tipo = random.choice(["terrestre", "voador"])
        raio_patrulha = random.randint(90, 160)
        x_min = x_base - raio_patrulha
        x_max = x_base + raio_patrulha
        velocidade = random.randint(130, 170)
        
        rotas.append((x_base, y_chao, x_min, x_max, tipo, velocidade))
    return rotas

def obter_comprimento_mapa():
    return 250 * 36