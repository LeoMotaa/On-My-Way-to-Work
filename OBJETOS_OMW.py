# OBJETOS_OMW.py
from pplay.sprite import *
import config
import MAPA_OMW

lista_automoveis = []
lista_onibus = []
lista_hidrantes = []
lista_bueiros = []

class HitboxCustom:
    """Caixa de colisão invisível para ajuste fino de quinas e tetos"""
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        
    def collided(self, obj):
        return (self.x + self.width > obj.x and self.x < obj.x + obj.width and
                self.y + self.height > obj.y and self.y < obj.y + obj.height)

def gerar_objetos():
    global lista_automoveis, lista_onibus, lista_hidrantes, lista_bueiros
    
    lista_automoveis = []
    lista_onibus = []
    lista_hidrantes = []
    lista_bueiros = []
    
    # Nível superior da calçada onde os objetos se apoiam
    Y_RUA = config.ALTURA - 100 

    dados_autos, dados_onibus, dados_hidrantes, dados_bueiros = MAPA_OMW.puxar_dados_objetos()

    # 1. Carro / Táxi -> Sprite Real: 255x90
    for x, tipo in dados_autos:
        caminho = "assets/objetos/carro_comum.png" if tipo == "carro" else "assets/objetos/carro_taxi.png"
        auto = Sprite(caminho)
        auto.width, auto.height = 255, 90
        auto.set_position(x, Y_RUA - auto.height)
        
        largura_hitbox = 90
        recuo_x = (auto.width - largura_hitbox) // 2  
        auto.hitbox_fisica = HitboxCustom(x + recuo_x, Y_RUA - auto.height, largura_hitbox, auto.height)
        lista_automoveis.append(auto)

    # 2. Ônibus -> Sprite Real: 600x241
    for x in dados_onibus:
        onibus = Sprite("assets/objetos/onibus.png")
        onibus.width, onibus.height = 600, 241
        onibus.set_position(x, Y_RUA - onibus.height)
        
        onibus.hitbox_capo = HitboxCustom(x, Y_RUA - 120, 90, 120)
        onibus.hitbox_teto = HitboxCustom(x + 90, Y_RUA - 241, 510, 241)
        lista_onibus.append(onibus)

    # 3. Hidrantes -> Sprite Real: 45x53
    for x in dados_hidrantes:
        hidrante = Sprite("assets/objetos/hidrante.png")
        hidrante.width, hidrante.height = 45, 53
        hidrante.set_position(x, Y_RUA - hidrante.height)
        lista_hidrantes.append(hidrante)

    # 4. Bueiros Abertos -> Sprite Real: 108x41
    for x in dados_bueiros:
        bueiro = Sprite("assets/objetos/bueiro_aberto.png")
        bueiro.width, bueiro.height = 108, 41
        bueiro.set_position(x, Y_RUA) 
        lista_bueiros.append(bueiro)

def atualizar_e_desenhar_objetos(hitbox_player, camera_x, dt):
    global lista_automoveis, lista_onibus, lista_hidrantes, lista_bueiros
    
    for bueiro in lista_bueiros: _desenhar_com_camera(bueiro, camera_x)
    for hidrante in lista_hidrantes: _desenhar_com_camera(hidrante, camera_x)
    for auto in lista_automoveis: _desenhar_com_camera(auto, camera_x)
    for onibus in lista_onibus: _desenhar_com_camera(onibus, camera_x)

def _desenhar_com_camera(sprite, camera_x):
    pos_real_x = sprite.x
    sprite.x = sprite.x - camera_x
    if -sprite.width <= sprite.x <= config.LARGURA:
        sprite.draw()
    sprite.x = pos_real_x