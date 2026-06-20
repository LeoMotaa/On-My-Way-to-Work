# FASE_EmpireState.py
import random
from pplay.sprite import *
import config

def carregar():
    largura_bloco = 36 
    altura_chao = config.ALTURA - 100
    comprimento_mapa = 320 
    
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

    fim_mapa = (320 * 36) - 1200

    while x < fim_mapa:
        dado = random.random()
        
        if dado < 0.32:  # 32% de chance de Carros
            tipo_carro = "carro" if random.random() < 0.5 else "taxi"
            automoveis.append((x, tipo_carro))
            x += random.randint(180, 320)  
            
        elif dado < 0.44:  # 12% de chance de Ônibus
            onibus.append(x)
            x += random.randint(350, 550)
            
        elif dado < 0.54:  # 10% de Hidrantes
            hidrantes.append(x)
            x += random.randint(150, 280)
            
        elif dado < 0.59:  # 5% de Bueiros
            bueiros.append(x)
            x += random.randint(400, 600)
            
        else:
            x += random.randint(40, 90)

    return automoveis, onibus, hidrantes, bueiros

def obter_posicoes_itens():
    altura_itens = config.ALTURA - 220 
    posicoes_aleatorias = []
    for x_base in range(400, 11300, 240):
        if random.random() < 0.65: 
            x_final = x_base + random.randint(-30, 30)
            posicoes_aleatorias.append((x_final, altura_itens))
    return posicoes_aleatorias

def obter_rotas_inimigos():
    rotas = []
    y_chao = config.ALTURA - 100
    
    for x_base in range(600, 11300, 350):
        tipo = random.choice(["terrestre", "voador"])
        raio_patrulha = random.randint(100, 180)
        x_min = x_base - raio_patrulha
        x_max = x_base + raio_patrulha
        velocidade = random.randint(140, 180)
        
        rotas.append((x_base, y_chao, x_min, x_max, tipo, velocidade))
    return rotas

def obter_comprimento_mapa():
    return 320 * 36