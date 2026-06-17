import pygame
import os
import sys

pygame.init()

# -----------------------------
# CONFIGURACIÓN DE PANTALLA
# -----------------------------
ANCHO = 1000
ALTO = 700
VENTANA = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Crazy Snack Rush TEC")
RELOJ = pygame.time.Clock()

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
GRIS = (200, 200, 200)
VERDE = (50, 205, 50)
AZUL = (30, 144, 255)

# Estados del Juego
ESTADO_INICIO = "inicio"
ESTADO_JUEGO = "juego"
ESTADO_GANASTE = "ganaste"
estado_actual = ESTADO_INICIO

nivel_actual = 1

# -----------------------------
# CARGA DE IMÁGENES (SISTEMA SEGURO)
# -----------------------------
def cargar_img(carpeta, archivo, escala=None):
    ruta = os.path.join(carpeta, archivo)
    try:
        # Intentar cargar con el nombre exacto dado
        img = pygame.image.load(ruta).convert_alpha()
        if escala:
            img = pygame.transform.scale(img, escala)
        return img
    except FileNotFoundError:
        # Si falla, intentamos alternar entre .png y .jpg por si acaso
        base, ext = os.path.splitext(archivo)
        alt_ext = ".jpg" if ext.lower() == ".png" else ".png"
        ruta_alt = os.path.join(carpeta, base + alt_ext)
        try:
            img = pygame.image.load(ruta_alt).convert_alpha()
            if escala:
                img = pygame.transform.scale(img, escala)
            return img
        except FileNotFoundError:
            # Si no encuentra nada, crea un cuadro de color para que el juego NO se caiga
            print(f"⚠️ Alerta: No se encontró {ruta}. Usando textura temporal.")
            superficie = pygame.Surface(escala if escala else (64, 64))
            superficie.fill((255, 0, 255)) # Rosado fosforescente de error
            return superficie

# Cargar Personajes
img_chefs = [
    cargar_img("Personajes", "águila.png", (64, 64)),
    cargar_img("Personajes", "loro.png", (64, 64)),
    cargar_img("Personajes", "chica.png", (64, 64)),
    cargar_img("Personajes", "caja.png", (64, 64))
]

# Cargar Alimentos
img_tomate = cargar_img("Alimentos", "tomate.png", (40, 40))
img_lechuga = cargar_img("Alimentos", "lechuga.png", (40, 40))
img_hojas = cargar_img("Alimentos", "hojas.png", (40, 40))
img_plato = cargar_img("Alimentos", "ensalada.png", (45, 45)) # Usamos ensalada como plato/resultado

# Cargar Escenarios (Mapas de fondo)
img_escenarios = {
    1: cargar_img("Escenarios", "Escenario 1.png", (ANCHO, ALTO)),
    2: cargar_img("Escenarios", "Escenario 2.png", (ANCHO, ALTO)),
    3: cargar_img("Escenarios", "Escenario 3.png", (ANCHO, ALTO))
}

# -----------------------------
# CLASES LOGICAS
# -----------------------------
class ObjetoCocina:
    def __init__(self, nombre, x, y, ancho, alto, tipo_estacion):
        self.rect = pygame.Rect(x, y, ancho, alto)
        self.nombre = nombre
        self.tipo_estacion = tipo_estacion # "despensa_tomate", "despensa_lechuga", "cuchillo", "plato", "entrega"

class Chef:
    def __init__(self, nombre, imagen, x, y):
        self.nombre = nombre
        self.imagen = imagen
        self.rect = pygame.Rect(x, y, 50, 50)
        self.velocidad = 5
        self.item = None # Qué tiene en las manos: None, "tomate", "lechuga", "tomate_picado", "hojas", "plato_vacio", "ensalada"

    def mover(self, dx, dy, obstaculos):
        # Movimiento en X con colisión
        self.rect.x += dx
        for obj in obstaculos:
            if self.rect.colliderect(obj.rect):
                if dx > 0: self.rect.right = obj.rect.left
                if dx < 0: self.rect.left = obj.rect.right
        
        # Movimiento en Y con colisión
        self.rect.y += dy
        for obj in obstaculos:
            if self.rect.colliderect(obj.rect):
                if dy > 0: self.rect.bottom = obj.rect.top
                if dy < 0: self.rect.top = obj.rect.bottom

        # Límites de pantalla
        if self.rect.left < 0: self.rect.left = 0
        if self.rect.right > ANCHO: self.rect.right = ANCHO
        if self.rect.top < 0: self.rect.top = 0
        if self.rect.bottom > ALTO: self.rect.bottom = ALTO

    def dibujar(self, ventana):
        ventana.blit(self.imagen, (self.rect.x - 7, self.rect.y - 7))
        # Dibujar el ítem que carga sobre su cabeza
        if self.item == "tomate": ventana.blit(img_tomate, (self.rect.x + 5, self.rect.y - 35))
        elif self.item == "lechuga": ventana.blit(img_lechuga, (self.rect.x + 5, self.rect.y - 35))
        elif self.item == "tomate_picado": ventana.blit(img_tomate, (self.rect.x + 5, self.rect.y - 35)) # Puedes cambiar a versión picada
        elif self.item == "hojas": ventana.blit(img_hojas, (self.rect.x + 5, self.rect.y - 35))
        elif self.item == "ensalada": ventana.blit(img_plato, (self.rect.x + 2, self.rect.y - 35))

# -----------------------------
# CONFIGURACIÓN DE ESTACIONES (Zonas interactivas por Escenario)
# Mapeado aproximado basado en la estructura de tus imágenes
# -----------------------------
estaciones_por_nivel = {
    1: [
        ObjetoCocina("Despensa Tomate", 40, 200, 120, 150, "despensa_tomate"),
        ObjetoCocina("Despensa Lechuga", 40, 200, 120, 150, "despensa_lechuga"),
        ObjetoCocina("Mesa Cuchillo", 290, 190, 70, 70, "cuchillo"),
        ObjetoCocina("Mesa Plato", 570, 190, 70, 70, "plato"),
        ObjetoCocina("Zona Entrega", 790, 190, 80, 90, "entrega")
    ],
    2: [
        ObjetoCocina("Despensa Tomate", 80, 220, 110, 140, "despensa_tomate"),
        ObjetoCocina("Despensa Lechuga", 80, 220, 110, 140, "despensa_lechuga"),
        ObjetoCocina("Mesa Cuchillo", 570, 110, 70, 70, "cuchillo"),
        ObjetoCocina("Mesa Plato", 270, 110, 70, 70, "plato"),
        ObjetoCocina("Zona Entrega", 740, 110, 80, 90, "entrega")
    ],
    3: [
        ObjetoCocina("Despensa Tomate", 160, 370, 110, 170, "despensa_tomate"),
        ObjetoCocina("Despensa Lechuga", 160, 370, 110, 170, "despensa_lechuga"),
        ObjetoCocina("Mesa Cuchillo", 570, 100, 70, 70, "cuchillo"),
        ObjetoCocina("Mesa Plato", 370, 320, 70, 70, "plato"),
        ObjetoCocina("Zona Entrega", 720, 100, 80, 90, "entrega")
    ]
}

# Inicializar chefs
chefs = [
    Chef("Chef1", img_chefs[0], 200, 400),
    Chef("Chef2", img_chefs[1], 300, 400),
    Chef("Chef3", img_chefs[2], 500, 400),
    Chef("Chef4", img_chefs[3], 600, 400)
]

indice_j1 = 0
indice_j2 = 2

# Estado de la mesa de preparación (Plato)
ingredientes_en_plato = {"tomate_picado": False, "hojas": False}

# Fuentes
fuente_titulos = pygame.font.SysFont("Arial", 50, bold=True)
fuente_UI = pygame.font.SysFont("Arial", 24, bold=True)

# -----------------------------
# ACCIONES DE INTERACCIÓN
# -----------------------------
def interactuar(chef, estaciones):
    global ingredientes_en_plato, nivel_actual, estado_actual
    
    # Crear un rango de interacción un poco más grande que el cuerpo del chef
    rango_interaccion = chef.rect.inflate(25, 25)
    
    for est in estaciones:
        if rango_interaccion.colliderect(est.rect):
            
            # 1. Sacar de la Despensa
            if est.tipo_estacion == "despensa_tomate" and chef.item is None:
                chef.item = "tomate"
                return
            elif est.tipo_estacion == "despensa_lechuga" and chef.item is None:
                chef.item = "lechuga"
                return
            
            # 2. Usar la mesa de picar (Cuchillo)
            elif est.tipo_estacion == "cuchillo":
                if chef.item == "tomate":
                    chef.item = "tomate_picado"
                    return
                elif chef.item == "lechuga":
                    chef.item = "hojas"
                    return
            
            # 3. Colocar en la mesa del Plato
            elif est.tipo_estacion == "plato":
                if chef.item == "tomate_picado" and not ingredientes_en_plato["tomate_picado"]:
                    ingredientes_en_plato["tomate_picado"] = True
                    chef.item = None
                elif chef.item == "hojas" and not ingredientes_en_plato["hojas"]:
                    ingredientes_en_plato["hojas"] = True
                    chef.item = None
                elif chef.item is None and ingredientes_en_plato["tomate_picado"] and ingredientes_en_plato["hojas"]:
                    # Si la ensalada está completa, el chef recoge el plato listo
                    chef.item = "ensalada"
                    ingredientes_en_plato["tomate_picado"] = False
                    ingredientes_en_plato["hojas"] = False
                return
            
            # 4. Entregar la Receta
            elif est.tipo_estacion == "entrega" and chef.item == "ensalada":
                chef.item = None
                print(f"¡Nivel {nivel_actual} Completado con Éxito!")
                if nivel_actual < 3:
                    nivel_actual += 1
                else:
                    estado_actual = ESTADO_GANASTE
                return

# -----------------------------
# BUCLE PRINCIPAL
# -----------------------------
ejecutando = True

while ejecutando:
    RELOJ.tick(60)
    estaciones_actuales = estaciones_por_nivel[nivel_actual]

    # --- CONTROL DE EVENTOS ---
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
            
        if evento.type == pygame.KEYDOWN:
            # Controles en Pantalla de Inicio / Fin
            if estado_actual == ESTADO_INICIO and evento.key == pygame.K_RETURN:
                estado_actual = ESTADO_JUEGO
            elif estado_actual == ESTADO_GANASTE and evento.key == pygame.K_RETURN:
                nivel_actual = 1
                estado_actual = ESTADO_INICIO
                
            # Cambios de personajes en juego
            if estado_actual == ESTADO_JUEGO:
                if evento.key == pygame.K_TAB:
                    indice_j1 = 1 if indice_j1 == 0 else 0
                if evento.key == pygame.K_RSHIFT:
                    indice_j2 = 3 if indice_j2 == 2 else 2
                
                # Botones de Acción para interactuar
                if evento.key == pygame.K_e: # J1 interactúa con E
                    interactuar(chefs[indice_j1], estaciones_actuales)
                if evento.key == pygame.K_SPACE: # J2 interactúa con ESPACIO
                    interactuar(chefs[indice_j2], estaciones_actuales)

    # --- LÓGICA DE JUEGO ---
    if estado_actual == ESTADO_JUEGO:
        teclas = pygame.key.get_pressed()
        j1 = chefs[indice_j1]
        j2 = chefs[indice_j2]
        
        # Movimiento J1 (WASD)
        dx1, dy1 = 0, 0
        if teclas[pygame.K_w]: dy1 = -j1.velocidad
        if teclas[pygame.K_s]: dy1 = j1.velocidad
        if teclas[pygame.K_a]: dx1 = -j1.velocidad
        if teclas[pygame.K_d]: dx1 = j1.velocidad
        j1.mover(dx1, dy1, estaciones_actuales)
        
        # Movimiento J2 (Flechas)
        dx2, dy2 = 0, 0
        if teclas[pygame.K_UP]: dy2 = -j2.velocidad
        if teclas[pygame.K_DOWN]: dy2 = j2.velocidad
        if teclas[pygame.K_LEFT]: dx2 = -j2.velocidad
        if teclas[pygame.K_RIGHT]: dx2 = j2.velocidad
        j2.mover(dx2, dy2, estaciones_actuales)

    # --- RENDERIZADO / DIBUJO ---
    VENTANA.fill(NEGRO)

    if estado_actual == ESTADO_INICIO:
        # Pantalla de Bienvenida
        txt_titulo = fuente_titulos.render("CRAZY SNACK RUSH - TEC", True, VERDE)
        txt_sub = fuente_UI.render("Presiona ENTER para comenzar a cocinar", True, BLANCO)
        VENTANA.blit(txt_titulo, (ANCHO // 2 - txt_titulo.get_width() // 2, 250))
        VENTANA.blit(txt_sub, (ANCHO // 2 - txt_sub.get_width() // 2, 350))
        
    elif estado_actual == ESTADO_JUEGO:
        # Dibujar el Fondo del Escenario Actual
        VENTANA.blit(img_escenarios[nivel_actual], (0, 0))
        
        # Opcional: Dibujar cajas de colisión transparentes/líneas para guiarte en el desarrollo
        # for est in estaciones_actuales:
        #     pygame.draw.rect(VENTANA, (255, 0, 0), est.rect, 2)
        
        # Dibujar Chefs activos e inactivos
        for chef in chefs:
            chef.dibujar(VENTANA)
            
        # UI superior informativa
        txt_lvl = fuente_UI.render(f"ESCENARIO / NIVEL: {nivel_actual}", True, NEGRO)
        txt_receta = fuente_UI.render("RECETA ACTIVA: Ensalada (Tomate + Lechuga)", True, AZUL)
        VENTANA.blit(txt_lvl, (20, 20))
        VENTANA.blit(txt_receta, (20, 50))
        
    elif estado_actual == ESTADO_GANASTE:
        # Pantalla Final
        txt_ganaste = fuente_titulos.render("¡FELICIDADES, TE GRADUASTE DE CHEF TEC!", True, VERDE)
        txt_reiniciar = fuente_UI.render("Presiona ENTER para volver al menú", True, BLANCO)
        VENTANA.blit(txt_ganaste, (ANCHO // 2 - txt_ganaste.get_width() // 2, 250))
        VENTANA.blit(txt_reiniciar, (ANCHO // 2 - txt_reiniciar.get_width() // 2, 350))

    pygame.display.update()

pygame.quit()
sys.exit()