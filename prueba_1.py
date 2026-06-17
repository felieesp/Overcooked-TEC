import pygame
import sys

# 1. Inicialización y Configuración
pygame.init()
pygame.font.init()

ANCHO, ALTO = 800, 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Mini-Cooked!")
reloj = pygame.time.Clock()
fuente = pygame.font.SysFont("Arial", 20)

# Colores (RGB)
NEGRO = (30, 30, 30)
BLANCO = (255, 255, 255)
AZUL_CHEF = (50, 150, 255)
ROJO_TOMATE = (255, 50, 50)
VERDE_LECHUGA = (50, 205, 50)
GRIS_MESA = (120, 120, 120)
MADERA = (139, 69, 19)

# 2. Configuración de Estaciones (Mesas)
# Cada estación es un Rectángulo: (X, Y, Ancho, Alto)
estaciones = {
    "tomate": pygame.Rect(100, 100, 100, 60),
    "lechuga": pygame.Rect(250, 100, 100, 60),
    "picar": pygame.Rect(450, 100, 100, 60),
    "plato": pygame.Rect(600, 100, 100, 60),
    "entrega": pygame.Rect(350, 500, 100, 60)
}

# 3. Estado del Chef
chef_rect = pygame.Rect(375, 300, 40, 40)
chef_velocidad = 5
item_en_mano = None # Puede ser: "Tomate", "Lechuga", "Tomate Picado", "Lechuga Picado", "Ensalada"

# 4. Estado de las Estaciones Especiales
progreso_picar = 0  # De 0 a 100%
item_en_picadora = None
items_en_plato = [] # Guardará los ingredientes picados listos
puntuacion = 0

# Función auxiliar para dibujar texto centrado en las mesas
def dibujar_texto(texto, color, x, y):
    superficie = fuente.render(texto, True, color)
    rect = superficie.get_rect(center=(x, y))
    pantalla.blit(superficie, rect)

# --- BUCLE PRINCIPAL ---
jugando = True
while jugando:
    reloj.tick(60)
    
    # GESTIÓN DE EVENTOS
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            jugando = False
            
        # Al pulsar una tecla
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE:
                # Verificar con qué estación colisiona el chef al pulsar espacio
                for nombre, rect_estacion in estaciones.items():
                    if chef_rect.colliderect(rect_estacion):
                        
                        # LOGICA DE AGARRAR INGREDIENTES
                        if nombre == "tomate" and item_en_mano is None:
                            item_en_mano = "Tomate"
                        elif nombre == "lechuga" and item_en_mano is None:
                            item_en_mano = "Lechuga"
                            
                        # LÓGICA DE LA MESA DE PICAR
                        elif nombre == "picar":
                            if item_en_mano in ["Tomate", "Lechuga"] and item_en_picadora is None:
                                item_en_picadora = item_en_mano
                                item_en_mano = None
                                progreso_picar = 0
                            elif item_en_picadora and progreso_picar < 100:
                                # Picas manteniendo pulsado o apretando espacio
                                progreso_picar += 20 
                                if progreso_picar >= 100:
                                    item_en_picadora = item_en_picadora + " Picado"
                            elif item_en_picadora and "Picado" in item_en_picadora and item_en_mano is None:
                                item_en_mano = item_en_picadora
                                item_en_picadora = None
                                progreso_picar = 0
                                
                        # LÓGICA DE LA MESA DEL PLATO
                        elif nombre == "plato":
                            if item_en_mano in ["Tomate Picado", "Lechuga Picado"]:
                                if item_en_mano not in items_en_plato:
                                    items_en_plato.append(item_en_mano)
                                    item_en_mano = None
                                    # Si ya tenemos ambos, se convierte en ensalada
                                    if "Tomate Picado" in items_en_plato and "Lechuga Picado" in items_en_plato:
                                        items_en_plato = []
                                        item_en_mano = "Ensalada"
                                        
                        # LÓGICA DE LA ENTREGA
                        elif nombre == "entrega":
                            if item_en_mano == "Ensalada":
                                puntuacion += 100
                                item_en_mano = None

    # LÓGICA DE MOVIMIENTO DEL CHEF
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_LEFT] and chef_rect.left > 0:
        chef_rect.x -= chef_velocidad
    if teclas[pygame.K_RIGHT] and chef_rect.right < ANCHO:
        chef_rect.x += chef_velocidad
    if teclas[pygame.K_UP] and chef_rect.top > 0:
        chef_rect.x -= 0 # Truco visual, se mueve en el eje Y
        chef_rect.y -= chef_velocidad
    if teclas[pygame.K_DOWN] and chef_rect.bottom < ALTO:
        chef_rect.y += chef_velocidad

    # --- RENDERIZADO / DIBUJO ---
    pantalla.fill(NEGRO)

    # Dibujar Estaciones
    for nombre, rect in estaciones.items():
        color = GRIS_MESA
        if nombre == "tomate": color = ROJO_TOMATE
        elif nombre == "lechuga": color = VERDE_LECHUGA
        elif nombre == "entrega": color = MADERA
        
        pygame.draw.rect(pantalla, color, rect)
        pygame.draw.rect(pantalla, BLANCO, rect, 2) # Borde
        dibujar_texto(nombre.upper(), BLANCO, rect.centerx, rect.centery - 10)

    # Mostrar estados especiales en las estaciones
    if item_en_picadora:
        dibujar_texto(f"{item_en_picadora} ({progreso_picar}%)", BLANCO, estaciones["picar"].centerx, estaciones["picar"].centery + 15)
    if items_en_plato:
        dibujar_texto(f"En plato: {len(items_en_plato)}/2", BLANCO, estaciones["plato"].centerx, estaciones["plato"].centery + 15)

    # Dibujar Chef
    pygame.draw.rect(pantalla, AZUL_CHEF, chef_rect)
    
    # Dibujar lo que el Chef lleva en las manos
    if item_en_mano:
        dibujar_texto(item_en_mano, (255, 255, 0), chef_rect.centerx, chef_rect.top - 15)

    # Interfaz de Usuario (UI)
    dibujar_texto(f"PUNTUACIÓN: {puntuacion}", BLANCO, 100, 40)
    dibujar_texto("RECETA: Ensalada (Tomate Picado + Lechuga Picado)", BLANCO, ANCHO // 2, 40)
    dibujar_texto("Controles: Flechas para moverte | Espacio para interactuar con las mesas", (180, 180, 180), ANCHO // 2, ALTO - 30)

    pygame.display.flip()

pygame.quit()
sys.exit()