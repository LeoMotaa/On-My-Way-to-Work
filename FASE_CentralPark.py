# FASE_CentralPark.py
import random
from pplay.sprite import *
import config

def carregar():
    largura_bloco = 36 
    altura_chao = config.ALTURA - 100
    comprimento_mapa = 180 
    
    # O chão agora é gerado por completo, sem buracos fantasmas
    for i in range(0, comprimento_mapa): 
        bloco = Sprite("assets/bloco_teste.png")
        bloco.width = 36
        bloco.height = 36
        bloco.set_position(i * largura_bloco, altura_chao)
        bloco.tem_colisao = True # Atributo padrão de colisão ativada
        config.blocos_fase.append(bloco)



def obter_dados_objetos():
    automoveis = []
    onibus = []
    hidrantes = []
    bueiros = []

    x = 500  
    fim_mapa = (180 * 36) - 1000  

    while x < fim_mapa:
        dado = random.random()
        
        if dado < 0.12:  # 12% de chance de Carros
            tipo_carro = "carro" if random.random() < 0.7 else "taxi"
            automoveis.append((x, tipo_carro))
            x += random.randint(400, 650)  # Bom respiro entre um carro e outro
            
        elif dado < 0.18:  # 6% de chance de Ônibus
            onibus.append(x)
            x += random.randint(600, 900) 
            
        elif dado < 0.26:  # 8% de Hidrantes
            hidrantes.append(x)
            x += random.randint(250, 400)
            
        elif dado < 0.29:  # 3% de Bueiros
            bueiros.append(x)
            x += random.randint(600, 900)
            
        else:
            x += random.randint(80, 150) # Passos mais largos para avançar o mapa vazio

    return automoveis, onibus, hidrantes, bueiros

def obter_posicoes_itens():
    altura_itens = config.ALTURA - 220 
    posicoes_aleatorias = []
    for x_base in range(400, 6300, 300):
        if random.random() < 0.8:
            x_final = x_base + random.randint(-50, 50)
            posicoes_aleatorias.append((x_final, altura_itens))
    return posicoes_aleatorias

def obter_rotas_inimigos():
    rotas = []
    y_chao = config.ALTURA - 100
    
    for x_base in range(600, 6300, 600):
        tipo = random.choice(["terrestre", "voador"])
        raio_patrulha = random.randint(80, 150)
        x_min = x_base - raio_patrulha
        x_max = x_base + raio_patrulha
        velocidade = random.randint(120, 160)
        
        rotas.append((x_base, y_chao, x_min, x_max, tipo, velocidade))
    return rotas

def obter_comprimento_mapa():
    return 180 * 36