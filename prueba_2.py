import pygame
import os

pygame.init()

# -----------------------------
# CONFIGURACIÓN
# -----------------------------
ANCHO = 1000
ALTO = 700

VENTANA = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Crazy Snack Rush TEC")

RELOJ = pygame.time.Clock()

BLANCO = (255, 255, 255)
objetos = []


# -----------------------------
# CLASES
# -----------------------------


class Ingrediente:

    def __init__(self, nombre):
        self.nombre = nombre
        self.estado = "crudo"


class VegetalFruta(Ingrediente):

    def __init__(self, nombre):
        super().__init__(nombre)


class PanBase(Ingrediente):

    def __init__(self, nombre):
        super().__init__(nombre)


class Proteina(Ingrediente):

    def __init__(self, nombre):
        super().__init__(nombre)
        self.cocinada = False


class Receta:

    def __init__(self, ingredientes, puntos, tiempo):
        self.lista_ingredientes = ingredientes
        self.puntos_receta = puntos
        self.max_time_receta = tiempo

    def comparar_receta(self, otra):

        if len(self.lista_ingredientes) != len(otra.lista_ingredientes):
            return False

        for i in range(len(self.lista_ingredientes)):

            if self.lista_ingredientes[i].nombre != otra.lista_ingredientes[i].nombre:
                return False

        return True


class Estacion:

    def __init__(self, nombre, ingredientes):
        self.nombre = nombre
        self.ingredientes_aceptados = ingredientes


class Chef:

    def __init__(self, nombre, imagen, x, y):

        self.nombre = nombre
        self.puntos = 0

        self.imagen = imagen

        self.x = x
        self.y = y

        self.velocidad = 5

        self.ingrediente = None

    def mover(self, dx, dy):

        self.x += dx
        self.y += dy

    def dibujar(self, ventana):

        ventana.blit(self.imagen, (self.x, self.y))


class Cocina:

    def __init__(self):

        self.tiempo = 0
        self.chefs = []
        self.ordenes = []

    def generar_receta(self):

        pan = PanBase("Pan")
        carne = Proteina("Carne")
        lechuga = VegetalFruta("Lechuga")

        return Receta(
            [pan, carne, lechuga],
            100,
            60
        )


# -----------------------------
# IMÁGENES
# -----------------------------

CARPETA = "Personajes"

ARCHIVOS = [
    "águila.png",
    "loro.png",
    "chica.png",
    "caja.png"
]

imagenes = []

for archivo in ARCHIVOS:

    ruta = os.path.join(CARPETA, archivo)

    img = pygame.image.load(ruta).convert_alpha()
    img = pygame.transform.scale(img, (64, 64))

    imagenes.append(img)

# -----------------------------
# COCINA Y CHEFS
# -----------------------------

cocina = Cocina()

chef1 = Chef("Chef1", imagenes[0], 100, 100)
chef2 = Chef("Chef2", imagenes[1], 300, 100)
chef3 = Chef("Chef3", imagenes[2], 100, 400)
chef4 = Chef("Chef4", imagenes[3], 300, 400)

cocina.chefs.extend([chef1, chef2, chef3, chef4])

indice_jugador1 = 0      # Chef1 o Chef2
indice_jugador2 = 2      # Chef3 o Chef4

# -----------------------------
# BUCLE
# -----------------------------

ejecutando = True

while ejecutando:

    RELOJ.tick(60)

    for evento in pygame.event.get():

        if evento.type == pygame.QUIT:
            ejecutando = False

        if evento.type == pygame.KEYDOWN:

            # Cambia entre Chef1 y Chef2
            if evento.key == pygame.K_TAB:

                if indice_jugador1 == 0:
                    indice_jugador1 = 1
                else:
                    indice_jugador1 = 0

            # Cambia entre Chef3 y Chef4
            if evento.key == pygame.K_RSHIFT:

                if indice_jugador2 == 2:
                    indice_jugador2 = 3
                else:
                    indice_jugador2 = 2

    teclas = pygame.key.get_pressed()

    jugador1 = cocina.chefs[indice_jugador1]
    jugador2 = cocina.chefs[indice_jugador2]

    # WASD
    if teclas[pygame.K_w]:
        jugador1.mover(0, -jugador1.velocidad)

    if teclas[pygame.K_s]:
        jugador1.mover(0, jugador1.velocidad)

    if teclas[pygame.K_a]:
        jugador1.mover(-jugador1.velocidad, 0)

    if teclas[pygame.K_d]:
        jugador1.mover(jugador1.velocidad, 0)

    # Flechas
    if teclas[pygame.K_UP]:
        jugador2.mover(0, -jugador2.velocidad)

    if teclas[pygame.K_DOWN]:
        jugador2.mover(0, jugador2.velocidad)

    if teclas[pygame.K_LEFT]:
        jugador2.mover(-jugador2.velocidad, 0)

    if teclas[pygame.K_RIGHT]:
        jugador2.mover(jugador2.velocidad, 0)

    VENTANA.fill(BLANCO)

    for chef in cocina.chefs:
        chef.dibujar(VENTANA)

    pygame.display.update()

pygame.quit()