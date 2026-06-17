import pygame
import os
import sys
import random

pygame.init()

#Pantalla
ANCHO = 1000
ALTO = 700
VENTANA = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Crazy Snack Rush TEC")
RELOJ = pygame.time.Clock()

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
GRIS = (100, 100, 100)
VERDE = (50, 205, 50)
AZUL = (30, 144, 255)
ROJO = (220, 20, 60)
AMARILLO = (255, 215, 0)
OSCURO_PANEL = (25, 25, 25)

# Estados del Juego
ESTADO_INICIO = "inicio"
ESTADO_JUEGO = "juego"
ESTADO_GANASTE = "ganaste"
ESTADO_PERDISTE = "perdiste"
estado_actual = ESTADO_INICIO

nivel_actual = 1

# Cantidad de pedidos necesarios para completar cada nivel
OBJETIVOS_NIVEL = {
    1: 6,
    2: 10,
    3: 12
}

# CARGA DE IMÁGENE
def cargar_img(carpeta, archivo, escala=None):
    ruta = os.path.join(carpeta, archivo)
    try:
        img = pygame.image.load(ruta).convert_alpha()
        if escala:
            img = pygame.transform.scale(img, escala)
        return img
    except FileNotFoundError:
        base, ext = os.path.splitext(archivo)
        alt_ext = ".jpg" if ext.lower() == ".png" else ".png"
        ruta_alt = os.path.join(carpeta, base + alt_ext)
        try:
            img = pygame.image.load(ruta_alt).convert_alpha()
            if escala:
                img = pygame.transform.scale(img, escala)
            return img
        except FileNotFoundError:
            print(f" Alerta: No se encontró {ruta}. Usando textura temporal.")
            superficie = pygame.Surface(escala if escala else (64, 64))
            superficie.fill((255, 0, 255))
            return superficie

#Personajes
img_chefs = [
    cargar_img("Personajes", "águila.png", (64, 64)),
    cargar_img("Personajes", "loro.png", (64, 64)),
    cargar_img("Personajes", "chica.png", (64, 64)),
    cargar_img("Personajes", "caja.png", (64, 64))
]

# Alimentos
img_tomate = cargar_img("Alimentos", "tomate.png", (40, 40))
img_lechuga = cargar_img("Alimentos", "lechuga.png", (40, 40))
img_hojas = cargar_img("Alimentos", "hojas.png", (40, 40))
img_carne_cruda = cargar_img("Alimentos", "carnecruda.png", (40, 40))
img_carne_cocida = cargar_img("Alimentos", "carnecocinada.png", (40, 40))
img_ensalada = cargar_img("Alimentos", "ensalada.png", (45, 45))
img_cafe = cargar_img("Alimentos", "Café.png", (40, 40))
img_tomatepicado = cargar_img("Alimentos", "tomatepicado.png", (40, 40))
img_pan = cargar_img("Alimentos", "pan.png", (40, 40))
img_panpicado = cargar_img("Alimentos", "panpicado.png", (40, 40))
img_pancito = cargar_img("Alimentos", "pancito.png", (45, 45))
img_papas = cargar_img("Alimentos", "papas.png", (40, 40))
img_papasfritas = cargar_img("Alimentos", "papasfritas.png", (45, 45))
img_pastacruda = cargar_img("Alimentos", "pastacruda.png", (40, 40))
img_pasta = cargar_img("Alimentos", "pasta.png", (45, 45))
img_sopa = cargar_img("Alimentos", "sopa.png", (45, 45))

#Instrumentos y Extras
img_horno_mueble = cargar_img("Instrumentos", "horno.png", (70, 70))
img_coffeemaker = cargar_img("Instrumentos", "coffemaker.png", (60, 70))
img_basurero = cargar_img("Instrumentos", "basurero.png", (70, 80)) 
img_olla = cargar_img("Instrumentos", "olla.png", (70, 70))
img_lavabo = cargar_img("Instrumentos", "lavabo.png", (70, 70))
img_plato = cargar_img("Instrumentos", "plato.png", (70, 70))
img_cuchillo = cargar_img("Instrumentos", "cuchillo.png", (70, 70))
img_fuego = cargar_img("Extras", "fuego.png", (60, 60))


img_bolsa_entrega = cargar_img("Extras", "bolsa.png", (100, 100))


img_escenarios = {
    1: cargar_img("Escenarios", "Escenario 1.png", (ANCHO, ALTO)),
    2: cargar_img("Escenarios", "Escenario 2.png", (ANCHO, ALTO)),
    3: cargar_img("Escenarios", "Escenario 3.png", (ANCHO, ALTO))
}


class MuebleObstaculo:
    def __init__(self, x, y, ancho, alto, tipo_estacion="muro", id_estacion=0):
        self.rect = pygame.Rect(x, y, ancho, alto)
        self.tipo_estacion = tipo_estacion
        self.id_estacion = id_estacion 

class Chef:
    def __init__(self, nombre, imagen, x, y):
        self.nombre = nombre
        self.imagen = imagen
        self.rect = pygame.Rect(x, y, 40, 40)
        self.velocidad = 5
        self.item = None 

    def mover(self, dx, dy, obstaculos):
        self.rect.x += dx
        for obj in obstaculos:
            if self.rect.colliderect(obj.rect):
                if dx > 0: self.rect.right = obj.rect.left
                if dx < 0: self.rect.left = obj.rect.right
        
        self.rect.y += dy
        for obj in obstaculos:
            if self.rect.colliderect(obj.rect):
                if dy > 0: self.rect.bottom = obj.rect.top
                if dy < 0: self.rect.top = obj.rect.bottom

    def dibujar(self, ventana):
        ventana.blit(self.imagen, (self.rect.x - 12, self.rect.y - 12))
        if self.item == "tomate": ventana.blit(img_tomate, (self.rect.x, self.rect.y - 35))
        elif self.item == "lechuga": ventana.blit(img_lechuga, (self.rect.x, self.rect.y - 35))
        elif self.item == "tomate_picado": ventana.blit(img_tomatepicado, (self.rect.x, self.rect.y - 35))
        elif self.item == "hojas": ventana.blit(img_hojas, (self.rect.x, self.rect.y - 35))
        elif self.item == "carne": ventana.blit(img_carne_cruda, (self.rect.x, self.rect.y - 35))
        elif self.item == "carne_cocida": ventana.blit(img_carne_cocida, (self.rect.x, self.rect.y - 35))
        elif self.item == "ensalada": ventana.blit(img_ensalada, (self.rect.x - 2, self.rect.y - 35))
        elif self.item == "cafe": ventana.blit(img_cafe, (self.rect.x, self.rect.y - 35))
        elif self.item == "pan": ventana.blit(img_pan, (self.rect.x, self.rect.y - 35))
        elif self.item in ["pan_1_corte", "pan_rebanado"]: ventana.blit(img_panpicado, (self.rect.x, self.rect.y - 35))
        elif self.item == "papas": ventana.blit(img_papas, (self.rect.x, self.rect.y - 35))
        elif self.item == "papas_picadas": ventana.blit(img_papasfritas, (self.rect.x, self.rect.y - 35))
        elif self.item == "pastacruda": ventana.blit(img_pastacruda, (self.rect.x, self.rect.y - 35))
        elif self.item == "pancito": ventana.blit(img_pancito, (self.rect.x, self.rect.y - 35))
        elif self.item == "sopa": ventana.blit(img_sopa, (self.rect.x, self.rect.y - 35))
        elif self.item == "papasfritas": ventana.blit(img_papasfritas, (self.rect.x, self.rect.y - 35))
        elif self.item == "pasta": ventana.blit(img_pasta, (self.rect.x, self.rect.y - 35))
        elif self.item == "olla_vacia": ventana.blit(img_olla, (self.rect.x - 15, self.rect.y - 40))


muebles_por_nivel = {
    1: [
        MuebleObstaculo(0, 0, 1000, 140, "muro"),
        MuebleObstaculo(0, 0, 140, 700, "muro"),
        MuebleObstaculo(860, 0, 140, 700, "muro"),
        MuebleObstaculo(0, 580, 1000, 120, "muro"),
        MuebleObstaculo(160, 140, 90, 70, "despensa_carne"), 
        MuebleObstaculo(260, 140, 70, 70, "horno", id_estacion=1), 
        MuebleObstaculo(335, 140, 70, 70, "horno", id_estacion=2), 
        MuebleObstaculo(430, 140, 60, 70, "coffeemaker", id_estacion=1), 
        MuebleObstaculo(540, 140, 60, 70, "coffeemaker", id_estacion=2), 
        MuebleObstaculo(670, 160, 100, 100, "entrega"), 
        MuebleObstaculo(260, 500, 70, 80, "basurero")
    ],
    2: [
        MuebleObstaculo(0, 0, 1000, 110, "muro"),
        MuebleObstaculo(0, 0, 110, 700, "muro"),
        MuebleObstaculo(890, 0, 110, 700, "muro"),
        MuebleObstaculo(0, 600, 1000, 100, "muro"),
        MuebleObstaculo(110, 140, 120, 70, "despensa_lechuga"),
        MuebleObstaculo(110, 240, 120, 70, "despensa_tomate"),
        MuebleObstaculo(110, 340, 120, 70, "despensa_carne"), 
        MuebleObstaculo(240, 110, 70, 70, "cuchillo"),
        MuebleObstaculo(330, 110, 70, 70, "lavabo"),
        MuebleObstaculo(420, 110, 70, 70, "olla_recogida"),
        MuebleObstaculo(510, 110, 60, 70, "coffeemaker", id_estacion=1), 
        MuebleObstaculo(600, 110, 70, 70, "plato"),
        MuebleObstaculo(130, 450, 100, 100, "entrega"), 
        MuebleObstaculo(330, 520, 70, 80, "basurero"),
        MuebleObstaculo(420, 520, 70, 70, "horno", id_estacion=1), 
        MuebleObstaculo(495, 520, 70, 70, "horno", id_estacion=2)
    ],
    3: [
        MuebleObstaculo(0, 0, 1000, 100, "muro"),
        MuebleObstaculo(0, 0, 150, 700, "muro"),
        MuebleObstaculo(840, 0, 160, 700, "muro"),
        MuebleObstaculo(0, 620, 1000, 80, "muro"),
        MuebleObstaculo(150, 130, 90, 65, "despensa_carne"),
        MuebleObstaculo(150, 205, 90, 65, "despensa_lechuga"),
        MuebleObstaculo(150, 280, 90, 65, "despensa_tomate"), 
        MuebleObstaculo(150, 355, 90, 65, "despensa_pan"), 
        MuebleObstaculo(150, 430, 90, 65, "despensa_papas"), 
        MuebleObstaculo(150, 505, 90, 65, "despensa_pasta"), 
        MuebleObstaculo(270, 100, 70, 70, "cuchillo"),
        MuebleObstaculo(370, 100, 70, 70, "lavabo"),
        MuebleObstaculo(470, 100, 70, 70, "olla_recogida"),
        MuebleObstaculo(550, 100, 70, 70, "horno", id_estacion=1), 
        MuebleObstaculo(625, 100, 70, 70, "horno", id_estacion=2), 
        MuebleObstaculo(705, 100, 60, 70, "coffeemaker", id_estacion=1), 
        MuebleObstaculo(720, 180, 100, 100, "entrega"), 
        MuebleObstaculo(420, 340, 200, 70, "plato"), 
        MuebleObstaculo(480, 520, 70, 80, "basurero")
    ]
}

chefs = [
    Chef("Chef1", img_chefs[0], 450, 380),
    Chef("Chef2", img_chefs[1], 520, 380),
    Chef("Chef3", img_chefs[2], 450, 440),
    Chef("Chef4", img_chefs[3], 520, 440)
]

indice_j1 = 0
indice_j2 = 2


ingredientes_en_plato = {
    "tomate_picado": False, 
    "hojas": False, 
    "carne_cocida": False,
    "pan_rebanado": False,
    "tomate_pancito": False,
    "hojas_pancito": False
}


olla_interna = {
    "en_escenario": True, 
    "x": 420, "y": 110,    
    "ingredientes": [], 
    "tiene_agua": False,
    "estado_coccion": "crudo", 
    "tiempo_coccion": 0,
    "tipo_receta": None    
}


estado_hornos = {
    1: {"item": None, "tiempo": 0, "fuego": False, "olla": None},
    2: {"item": None, "tiempo": 0, "fuego": False, "olla": None}
}

TIEMPO_OK_COCCION = 10 * 60   
TIEMPO_QUEMADO_CARNE = 20 * 60 


estado_cafeteras = {
    1: {"estado": "vacio", "tiempo": 0},
    2: {"estado": "vacio", "tiempo": 0}
}
TIEMPO_OK_CAFE = 10 * 60

TIEMPO_INICIAL_NIVEL = 180 * 60 
tiempo_restante_marcos = TIEMPO_INICIAL_NIVEL
pedidos_completados = 0
puntuacion_total = 0


RECETAS_POR_NIVEL = {
    1: ["Café Solo", "Carne Cocinada"],
    2: ["Café Solo", "Carne Cocinada", "Ensalada Mixta", "Sopa de Tomate"],
    3: ["Café Solo", "Carne Cocinada", "Ensalada Mixta", "Sopa de Tomate", "Papas Fritas", "Pancito", "Pasta Fiel"]
}

RECETAS_INFO = {
    "Café Solo": img_cafe,
    "Carne Cocinada": img_carne_cocida,
    "Ensalada Mixta": img_ensalada,
    "Sopa de Tomate": img_sopa,
    "Papas Fritas": img_papasfritas,
    "Pancito": img_pancito,
    "Pasta Fiel": img_pasta
}

cola_pedidos = []

def generar_nuevo_pedido():
    pool = RECETAS_POR_NIVEL[nivel_actual]
    nombre = random.choice(pool)
    return {"nombre": nombre, "tiempo_creacion": tiempo_restante_marcos}

for _ in range(3):
    cola_pedidos.append(generar_nuevo_pedido())

# Fuentes
fuente_titulos = pygame.font.SysFont("Arial", 40, bold=True)
fuente_UI = pygame.font.SysFont("Arial", 18, bold=True)
fuente_reloj = pygame.font.SysFont("Consolas", 24, bold=True)
fuente_controles = pygame.font.SysFont("Consolas", 13, bold=True)

# Función Truco Tecla Z
def forzar_siguiente_nivel():
    global nivel_actual, pedidos_completados, tiempo_restante_marcos, olla_interna, estado_hornos, cola_pedidos, estado_actual, ingredientes_en_plato
    if nivel_actual < 3:
        nivel_actual += 1
        pedidos_completados = 0
        tiempo_restante_marcos = TIEMPO_INICIAL_NIVEL
        olla_interna = {"en_escenario": True, "x": 420, "y": 110, "ingredientes": [], "tiene_agua": False, "estado_coccion": "crudo", "tiempo_coccion": 0, "tipo_receta": None}
        for h in estado_hornos:
            estado_hornos[h] = {"item": None, "tiempo": 0, "fuego": False, "olla": None}
        ingredientes_en_plato = {k: False for k in ingredientes_en_plato}
        cola_pedidos.clear()
        for _ in range(3):
            cola_pedidos.append(generar_nuevo_pedido())
        for c in chefs: 
            c.rect.x, c.rect.y = 450, 380
    else:
        estado_actual = ESTADO_GANASTE


def interactuar(chef, obstaculos):
    global ingredientes_en_plato, nivel_actual, estado_actual, estado_hornos
    global pedidos_completados, tiempo_restante_marcos, estado_cafeteras, puntuacion_total, olla_interna
    
    rango_accion = chef.rect.inflate(45, 45) 
    
    for obj in obstaculos:
        if rango_accion.colliderect(obj.rect):
            
            if obj.tipo_estacion == "basurero" and chef.item is not None:
                chef.item = None
                return

            if chef.item is None:
                if obj.tipo_estacion == "despensa_tomate": chef.item = "tomate"; return
                elif obj.tipo_estacion == "despensa_lechuga": chef.item = "lechuga"; return
                elif obj.tipo_estacion == "despensa_carne": chef.item = "carne"; return
                elif obj.tipo_estacion == "despensa_pan": chef.item = "pan"; return
                elif obj.tipo_estacion == "despensa_papas": chef.item = "papas"; return
                elif obj.tipo_estacion == "despensa_pasta": chef.item = "pastacruda"; return

            if obj.tipo_estacion == "cuchillo" and chef.item is not None:
                if chef.item == "tomate": chef.item = "tomate_picado"
                elif chef.item == "lechuga": chef.item = "hojas"
                elif chef.item == "papas": chef.item = "papas_picadas"
                elif chef.item == "pan": chef.item = "pan_1_corte"
                elif chef.item == "pan_1_corte": chef.item = "pan_rebanado"
                return
            
            if obj.tipo_estacion == "lavabo":
                if chef.item == "olla_vacia" and not olla_interna["tiene_agua"]:
                    olla_interna["tiene_agua"] = True
                    return

            if obj.tipo_estacion == "olla_recogida" and olla_interna["en_escenario"]:
                if chef.item == "tomate_picado" and "tomate_picado" not in olla_interna["ingredientes"]:
                    olla_interna["ingredientes"].append("tomate_picado")
                    chef.item = None; return
                elif chef.item == "papas_picadas" and "papas_picadas" not in olla_interna["ingredientes"]:
                    olla_interna["ingredientes"].append("papas_picadas")
                    chef.item = None; return
                elif chef.item == "pastacruda" and "pastacruda" not in olla_interna["ingredientes"]:
                    olla_interna["ingredientes"].append("pastacruda")
                    chef.item = None; return
                fuego_en_cocina = estado_hornos[1]["fuego"] or estado_hornos[2]["fuego"]
                if chef.item is None and not fuego_en_cocina: 
                    chef.item = "olla_vacia"
                    olla_interna["en_escenario"] = False
                    return
            
            if obj.tipo_estacion == "olla_recogida" and chef.item == "olla_vacia" and not olla_interna["en_escenario"]:
                chef.item = None
                olla_interna["en_escenario"] = True
                olla_interna["x"], olla_interna["y"] = obj.rect.x, obj.rect.y
                return

            if obj.tipo_estacion == "horno":
                id_h = obj.id_estacion
                
                if estado_hornos[id_h]["fuego"]:
                    estado_hornos[id_h]["fuego"] = False
                    estado_hornos[id_h]["item"] = None
                    estado_hornos[id_h]["tiempo"] = 0
                    estado_hornos[id_h]["olla"] = None
                    olla_interna = {"en_escenario": True, "x": 420, "y": 110, "ingredientes": [], "tiene_agua": False, "estado_coccion": "crudo", "tiempo_coccion": 0, "tipo_receta": None}
                    return

                if chef.item == "carne" and estado_hornos[id_h]["item"] is None and olla_interna["tipo_receta"] is None:
                    estado_hornos[id_h]["item"] = "carne"
                    estado_hornos[id_h]["tiempo"] = 0
                    chef.item = None
                    return
                elif chef.item is None and estado_hornos[id_h]["item"] == "carne" and estado_hornos[id_h]["tiempo"] >= TIEMPO_OK_COCCION:
                    chef.item = "carne_cocida"
                    estado_hornos[id_h]["item"] = None
                    estado_hornos[id_h]["tiempo"] = 0
                    return
                
                if chef.item == "olla_vacia" and estado_hornos[id_h]["item"] is None and olla_interna["tiene_agua"]:
                    if "tomate_picado" in olla_interna["ingredientes"]: olla_interna["tipo_receta"] = "sopa"
                    elif "papas_picadas" in olla_interna["ingredientes"]: olla_interna["tipo_receta"] = "papas"
                    elif "pastacruda" in olla_interna["ingredientes"]: olla_interna["tipo_receta"] = "pasta"
                    
                    if olla_interna["tipo_receta"] is not None:
                        estado_hornos[id_h]["item"] = "olla"
                        estado_hornos[id_h]["olla"] = dict(olla_interna)
                        chef.item = None
                    return
                elif chef.item is None and estado_hornos[id_h]["item"] == "olla" and estado_hornos[id_h]["olla"]["estado_coccion"] == "cocinado":
                    chef.item = "olla_vacia"
                    olla_interna["tipo_receta"] = estado_hornos[id_h]["olla"]["tipo_receta"]
                    olla_interna["estado_coccion"] = "cocinado"
                    estado_hornos[id_h]["item"] = None
                    estado_hornos[id_h]["olla"] = None
                    return

            if obj.tipo_estacion == "coffeemaker":
                id_c = obj.id_estacion
                if chef.item is None and estado_cafeteras[id_c]["estado"] == "vacio":
                    estado_cafeteras[id_c]["estado"] = "preparando"
                    estado_cafeteras[id_c]["tiempo"] = 0
                elif chef.item is None and estado_cafeteras[id_c]["estado"] == "listo":
                    chef.item = "cafe"
                    estado_cafeteras[id_c]["estado"] = "vacio"
                return
            
            if obj.tipo_estacion == "plato":
                if chef.item == "olla_vacia" and olla_interna["estado_coccion"] == "cocinado":
                    if olla_interna["tipo_receta"] == "sopa": chef.item = "sopa"
                    elif olla_interna["tipo_receta"] == "papas": chef.item = "papasfritas"
                    elif olla_interna["tipo_receta"] == "pasta": chef.item = "pasta"
                    olla_interna = {"en_escenario": True, "x": 420, "y": 110, "ingredientes": [], "tiene_agua": False, "estado_coccion": "crudo", "tiempo_coccion": 0, "tipo_receta": None}
                    return

                # LÓGICA DEL PLATO CORREGIDA
                if chef.item == "tomate_picado":
                    if ingredientes_en_plato["pan_rebanado"]:
                        if not ingredientes_en_plato["tomate_pancito"]:
                            ingredientes_en_plato["tomate_pancito"] = True
                            chef.item = None; return
                    else:
                        if not ingredientes_en_plato["tomate_picado"]:
                            ingredientes_en_plato["tomate_picado"] = True
                            chef.item = None; return
                            
                if chef.item == "hojas":
                    if ingredientes_en_plato["pan_rebanado"]:
                        if not ingredientes_en_plato["hojas_pancito"]:
                            ingredientes_en_plato["hojas_pancito"] = True
                            chef.item = None; return
                    else:
                        if not ingredientes_en_plato["hojas"]:
                            ingredientes_en_plato["hojas"] = True
                            chef.item = None; return
                
                if chef.item == "pan_rebanado" and not ingredientes_en_plato["pan_rebanado"]:
                    if ingredientes_en_plato["tomate_picado"] or ingredientes_en_plato["hojas"]:
                        ingredientes_en_plato["tomate_picado"] = False
                        ingredientes_en_plato["hojas"] = False
                    ingredientes_en_plato["pan_rebanado"] = True
                    chef.item = None; return
                    
                if chef.item == "carne_cocida" and ingredientes_en_plato["pan_rebanado"] and not ingredientes_en_plato["carne_cocida"]:
                    ingredientes_en_plato["carne_cocida"] = True
                    chef.item = None; return

                if chef.item is None:
                    if ingredientes_en_plato["tomate_picado"] and ingredientes_en_plato["hojas"] and not ingredientes_en_plato["pan_rebanado"]:
                        chef.item = "ensalada"
                        ingredientes_en_plato = {k: False for k in ingredientes_en_plato}
                        return
                    if ingredientes_en_plato["pan_rebanado"] and ingredientes_en_plato["tomate_pancito"] and ingredientes_en_plato["hojas_pancito"] and ingredientes_en_plato["carne_cocida"]:
                        chef.item = "pancito"
                        ingredientes_en_plato = {k: False for k in ingredientes_en_plato}
                        return

            if obj.tipo_estacion == "entrega" and chef.item is not None:
                for idx, pedido in enumerate(cola_pedidos[:3]):
                    entrega_valida = False
                    if chef.item == "ensalada" and pedido["nombre"] == "Ensalada Mixta": entrega_valida = True
                    elif chef.item == "carne_cocida" and pedido["nombre"] == "Carne Cocinada": entrega_valida = True
                    elif chef.item == "cafe" and pedido["nombre"] == "Café Solo": entrega_valida = True
                    elif chef.item == "sopa" and pedido["nombre"] == "Sopa de Tomate": entrega_valida = True
                    elif chef.item == "papasfritas" and pedido["nombre"] == "Papas Fritas": entrega_valida = True
                    elif chef.item == "pancito" and pedido["nombre"] == "Pancito": entrega_valida = True
                    elif chef.item == "pasta" and pedido["nombre"] == "Pasta Fiel": entrega_valida = True

                    if entrega_valida:
                        chef.item = None
                        pedidos_completados += 1
                        puntuacion_total += 25  
                        
                        if (pedido["tiempo_creacion"] - tiempo_restante_marcos) <= 25 * 60:
                            puntuacion_total += 15
                        
                        cola_pedidos.pop(idx) 
                        cola_pedidos.append(generar_nuevo_pedido()) 
                        
                        if pedidos_completados >= OBJETIVOS_NIVEL[nivel_actual]:
                            forzar_siguiente_nivel()
                        return


ejecutando = True

while ejecutando:
    RELOJ.tick(60)
    obstaculos_actuales = muebles_por_nivel[nivel_actual]

    if estado_actual == ESTADO_JUEGO:
        if tiempo_restante_marcos > 0:
            tiempo_restante_marcos -= 1
        else:
            estado_actual = ESTADO_PERDISTE

        for h in [1, 2]:
            if estado_hornos[h]["item"] == "carne" and not estado_hornos[h]["fuego"]:
                estado_hornos[h]["tiempo"] += 1
                if estado_hornos[h]["tiempo"] >= TIEMPO_QUEMADO_CARNE:
                    estado_hornos[h]["fuego"] = True  
                    
            elif estado_hornos[h]["item"] == "olla" and not estado_hornos[h]["fuego"]:
                estado_hornos[h]["olla"]["tiempo_coccion"] += 1
                
                tiempo_meta = 10 * 60 
                if estado_hornos[h]["olla"]["tipo_receta"] == "sopa": tiempo_meta = 25 * 60
                elif estado_hornos[h]["olla"]["tipo_receta"] == "papas": tiempo_meta = 20 * 60
                elif estado_hornos[h]["olla"]["tipo_receta"] == "pasta": tiempo_meta = 30 * 60
                
                if estado_hornos[h]["olla"]["tiempo_coccion"] >= tiempo_meta:
                    estado_hornos[h]["olla"]["estado_coccion"] = "cocinado"
                
                if estado_hornos[h]["olla"]["tiempo_coccion"] >= (tiempo_meta + 2400):
                    estado_hornos[h]["fuego"] = True

        for id_c in [1, 2]:
            if id_c in estado_cafeteras and estado_cafeteras[id_c]["estado"] == "preparando":
                estado_cafeteras[id_c]["tiempo"] += 1
                if estado_cafeteras[id_c]["tiempo"] >= TIEMPO_OK_CAFE:
                    estado_cafeteras[id_c]["estado"] = "listo"

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
            
        if evento.type == pygame.KEYDOWN:
            if estado_actual == ESTADO_INICIO and evento.key == pygame.K_RETURN:
                estado_actual = ESTADO_JUEGO
                puntuacion_total = 0
                cola_pedidos.clear()
                for _ in range(3): cola_pedidos.append(generar_nuevo_pedido())
            elif estado_actual in [ESTADO_GANASTE, ESTADO_PERDISTE] and evento.key == pygame.K_RETURN:
                nivel_actual = 1
                pedidos_completados = 0
                puntuacion_total = 0
                tiempo_restante_marcos = TIEMPO_INICIAL_NIVEL
                estado_actual = ESTADO_INICIO
                ingredientes_en_plato = {k: False for k in ingredientes_en_plato}
                for h in estado_hornos:
                    estado_hornos[h] = {"item": None, "tiempo": 0, "fuego": False, "olla": None}
                olla_interna = {"en_escenario": True, "x": 420, "y": 110, "ingredientes": [], "tiene_agua": False, "estado_coccion": "crudo", "tiempo_coccion": 0, "tipo_receta": None}

            if estado_actual == ESTADO_JUEGO:
                if evento.key == pygame.K_TAB:
                    indice_j1 = 1 if indice_j1 == 0 else 0
                if evento.key == pygame.K_RSHIFT:
                    indice_j2 = 3 if indice_j2 == 2 else 2
                
              
                if evento.key == pygame.K_z:
                    forzar_siguiente_nivel()

                if evento.key == pygame.K_e:
                    interactuar(chefs[indice_j1], obstaculos_actuales)
                if evento.key == pygame.K_SPACE:
                    interactuar(chefs[indice_j2], obstaculos_actuales)

    if estado_actual == ESTADO_JUEGO:
        teclas = pygame.key.get_pressed()
        j1 = chefs[indice_j1]
        j2 = chefs[indice_j2]
        
        dx1, dy1 = 0, 0
        if teclas[pygame.K_w]: dy1 = -j1.velocidad
        if teclas[pygame.K_s]: dy1 = j1.velocidad
        if teclas[pygame.K_a]: dx1 = -j1.velocidad
        if teclas[pygame.K_d]: dx1 = j1.velocidad
        j1.mover(dx1, dy1, obstaculos_actuales)
        
        dx2, dy2 = 0, 0
        if teclas[pygame.K_UP]: dy2 = -j2.velocidad
        if teclas[pygame.K_DOWN]: dy2 = j2.velocidad
        if teclas[pygame.K_LEFT]: dx2 = -j2.velocidad
        if teclas[pygame.K_RIGHT]: dx2 = j2.velocidad
        j2.mover(dx2, dy2, obstaculos_actuales)

    VENTANA.fill(NEGRO)

    if estado_actual == ESTADO_INICIO:
        txt_titulo = fuente_titulos.render("Crazy Snack Rush - TEC Edition", True, VERDE)
        txt_sub = fuente_UI.render("Presione ENTER para arrancar la cocina", True, BLANCO)
        VENTANA.blit(txt_titulo, (ANCHO // 2 - txt_titulo.get_width() // 2, 250))
        VENTANA.blit(txt_sub, (ANCHO // 2 - txt_sub.get_width() // 2, 350))
        
    elif estado_actual == ESTADO_JUEGO:
        VENTANA.blit(img_escenarios[nivel_actual], (0, 0))
        
        for obj in obstaculos_actuales:
            if obj.tipo_estacion == "despensa_tomate": VENTANA.blit(img_tomate, (obj.rect.x + 15, obj.rect.y + 15))
            elif obj.tipo_estacion == "despensa_lechuga": VENTANA.blit(img_lechuga, (obj.rect.x + 15, obj.rect.y + 15))
            elif obj.tipo_estacion == "despensa_carne": VENTANA.blit(img_carne_cruda, (obj.rect.x + 15, obj.rect.y + 15))
            elif obj.tipo_estacion == "despensa_pan": VENTANA.blit(img_pan, (obj.rect.x + 15, obj.rect.y + 15))
            elif obj.tipo_estacion == "despensa_papas": VENTANA.blit(img_papas, (obj.rect.x + 15, obj.rect.y + 15))
            elif obj.tipo_estacion == "despensa_pasta": VENTANA.blit(img_pastacruda, (obj.rect.x + 15, obj.rect.y + 15))
            elif obj.tipo_estacion == "basurero": VENTANA.blit(img_basurero, (obj.rect.x, obj.rect.y))
            elif obj.tipo_estacion == "lavabo": VENTANA.blit(img_lavabo, (obj.rect.x, obj.rect.y))
            elif obj.tipo_estacion == "cuchillo": VENTANA.blit(img_cuchillo, (obj.rect.x, obj.rect.y))
            elif obj.tipo_estacion == "plato": VENTANA.blit(img_plato, (obj.rect.x, obj.rect.y))
            elif obj.tipo_estacion == "entrega": VENTANA.blit(img_bolsa_entrega, (obj.rect.x, obj.rect.y))

            en_algun_horno = estado_hornos[1]["item"] == "olla" or estado_hornos[2]["item"] == "olla"
            if obj.tipo_estacion == "olla_recogida" and olla_interna["en_escenario"] and not en_algun_horno:
                VENTANA.blit(img_olla, (obj.rect.x, obj.rect.y))
                
            elif obj.tipo_estacion == "horno":
                id_h = obj.id_estacion
                VENTANA.blit(img_horno_mueble, (obj.rect.x, obj.rect.y))
                
                if estado_hornos[id_h]["fuego"]:
                    VENTANA.blit(img_fuego, (obj.rect.x + 5, obj.rect.y - 35))
                else:
                    if estado_hornos[id_h]["item"] == "carne":
                        barra = int((estado_hornos[id_h]["tiempo"] / TIEMPO_OK_COCCION) * 40) if estado_hornos[id_h]["tiempo"] < TIEMPO_OK_COCCION else 40
                        pygame.draw.rect(VENTANA, ROJO, (obj.rect.x + 15, obj.rect.y - 12, 40, 6))
                        pygame.draw.rect(VENTANA, AZUL, (obj.rect.x + 15, obj.rect.y - 12, min(barra, 40), 6))
                    elif estado_hornos[id_h]["item"] == "olla":
                        VENTANA.blit(img_olla, (obj.rect.x, obj.rect.y - 15))
                        if estado_hornos[id_h]["olla"]["estado_coccion"] == "cocinado":
                            pygame.draw.rect(VENTANA, VERDE, (obj.rect.x + 15, obj.rect.y - 25, 40, 6))
                        else:
                            pygame.draw.rect(VENTANA, AMARILLO, (obj.rect.x + 15, obj.rect.y - 25, 40, 6))

            elif obj.tipo_estacion == "coffeemaker":
                id_c = obj.id_estacion if obj.id_estacion in estado_cafeteras else 1
                VENTANA.blit(img_coffeemaker, (obj.rect.x, obj.rect.y))
                if estado_cafeteras[id_c]["estado"] == "preparando":
                    largo_barra = int((estado_cafeteras[id_c]["tiempo"] / TIEMPO_OK_CAFE) * 40)
                    pygame.draw.rect(VENTANA, ROJO, (obj.rect.x + 10, obj.rect.y - 12, 40, 6))
                    pygame.draw.rect(VENTANA, AZUL, (obj.rect.x + 10, obj.rect.y - 12, largo_barra, 6))
                elif estado_cafeteras[id_c]["estado"] == "listo":
                    VENTANA.blit(img_cafe, (obj.rect.centerx - 20, obj.rect.y - 35))

        for i, chef in enumerate(chefs):
            chef.dibujar(VENTANA)
            if i == indice_j1 or i == indice_j2:
                pygame.draw.circle(VENTANA, VERDE, (chef.rect.centerx, chef.rect.top - 45), 5)
        
        for idx, ped in enumerate(cola_pedidos[:3]): 
            y_offset = 15 + (idx * 95)
            x_pos = 845  
            color_carta = (40, 40, 45) if idx > 0 else (60, 55, 30)
            pygame.draw.rect(VENTANA, color_carta, (x_pos, y_offset, 140, 80), border_radius=6)
            
            txt_p = fuente_controles.render(ped["nombre"], True, BLANCO)
            VENTANA.blit(txt_p, (x_pos + 8, y_offset + 10))
            if ped["nombre"] in RECETAS_INFO:
                VENTANA.blit(RECETAS_INFO[ped["nombre"]], (x_pos + 85, y_offset + 30))

        segundos_totales = tiempo_restante_marcos // 60
        str_tiempo = f"{segundos_totales // 60:02d}:{segundos_totales % 60:02d}"
        
        pygame.draw.rect(VENTANA, OSCURO_PANEL, (15, 15, 210, 110), border_radius=8)
        txt_lvl = fuente_UI.render(f"Nivel {nivel_actual}/3", True, BLANCO)
        txt_cnt = fuente_UI.render(f"Pedidos: {pedidos_completados}/{OBJETIVOS_NIVEL[nivel_actual]}", True, AMARILLO)
        txt_pts = fuente_UI.render(f"PUNTOS: {puntuacion_total}", True, VERDE)
        txt_clk = fuente_reloj.render(str_tiempo, True, BLANCO)
        
        VENTANA.blit(txt_lvl, (25, 20))
        VENTANA.blit(txt_cnt, (25, 42))
        VENTANA.blit(txt_pts, (25, 64))
        VENTANA.blit(txt_clk, (25, 90))
        
        pygame.draw.rect(VENTANA, OSCURO_PANEL, (0, 620, ANCHO, 80))
        txt_j1 = fuente_controles.render("JUGADOR 1: W,A,S,D | Acción [ E ]  |  JUGADOR 2: Flechas | Acción [ ESPACIO ]", True, BLANCO)
        
        VENTANA.blit(txt_j1, (20, 640))
        
    elif estado_actual == ESTADO_GANASTE:
        txt_ganaste = fuente_titulos.render("¡FIESTA TOTAL EN EL TEC!", True, VERDE)
        txt_pts_fin = fuente_UI.render(f"Puntuación Magistral Obtenida: {puntuacion_total} Puntos", True, AMARILLO)
        VENTANA.blit(txt_ganaste, (ANCHO // 2 - txt_ganaste.get_width() // 2, 280))
        VENTANA.blit(txt_pts_fin, (ANCHO // 2 - txt_pts_fin.get_width() // 2, 350))
        
    elif estado_actual == ESTADO_PERDISTE:
        txt_perdiste = fuente_titulos.render("¡COCINA COLAPSADA!", True, ROJO)
        txt_pts_fin = fuente_UI.render(f"Puntuación Final: {puntuacion_total} Puntos. Presione ENTER.", True, BLANCO)
        VENTANA.blit(txt_perdiste, (ANCHO // 2 - txt_perdiste.get_width() // 2, 280))
        VENTANA.blit(txt_pts_fin, (ANCHO // 2 - txt_pts_fin.get_width() // 2, 350))

    pygame.display.update()

pygame.quit()
sys.exit()