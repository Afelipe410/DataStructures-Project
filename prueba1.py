import pygame
import math

# Inicializa pygame
pygame.init()

# Definir los colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)

# Crear la ventana
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Árbol Binario en Pygame")


# Clase para representar un nodo del árbol
class TreeNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


# Función para dibujar el árbol
def draw_tree(screen, node, x, y, angle, depth, max_depth, length=80):
    if node is None or depth > max_depth:
        return

    # Calcula las posiciones de los hijos
    branch_length = length / (depth + 1)  # Reduce el largo de las ramas a medida que baja en el árbol
    left_x = x + branch_length * math.cos(math.radians(angle - 30))
    left_y = y + branch_length * math.sin(math.radians(angle - 30))
    right_x = x + branch_length * math.cos(math.radians(angle + 30))
    right_y = y + branch_length * math.sin(math.radians(angle + 30))

    # Dibuja las líneas entre los nodos (las ramas)
    if node.left:
        pygame.draw.line(screen, BLACK, (x, y), (left_x, left_y), 2)
        draw_tree(screen, node.left, left_x, left_y, angle - 30, depth + 1, max_depth)

    if node.right:
        pygame.draw.line(screen, BLACK, (x, y), (right_x, right_y), 2)
        draw_tree(screen, node.right, right_x, right_y, angle + 30, depth + 1, max_depth)

    # Dibuja el nodo como un círculo
    pygame.draw.circle(screen, BLUE, (int(x), int(y)), 20)
    font = pygame.font.SysFont('Arial', 20)
    text = font.render(str(node.value), True, WHITE)
    screen.blit(text, (int(x) - 10, int(y) - 10))


# Función para crear un árbol binario de ejemplo
def create_example_tree():
    root = TreeNode(1)
    root.left = TreeNode(2)
    root.right = TreeNode(3)
    root.left.left = TreeNode(4)
    root.left.right = TreeNode(5)
    root.right.left = TreeNode(6)
    root.right.right = TreeNode(7)
    return root


# Variables para el control del árbol
root = create_example_tree()
max_depth = 3

# Bucle principal del programa
running = True
while running:
    # Rellena la pantalla de blanco
    screen.fill(WHITE)

    # Dibujar el árbol
    draw_tree(screen, root, width // 2, 100, -90, 0, max_depth)

    # Actualiza la pantalla
    pygame.display.flip()

    # Manejo de eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

# Salir de pygame
pygame.quit()
