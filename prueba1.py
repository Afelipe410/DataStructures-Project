import pygame
import math
import sys

# Inicializa pygame
pygame.init()

# Definir los colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)

# Crear la ventana
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Árbol AVL en Pygame")

# Inicializa la fuente para el texto
pygame.font.init()
font = pygame.font.SysFont('Arial', 20)


# Clase para representar un nodo del árbol
class TreeNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.height = 1


# Clase para manejar un árbol AVL
class AVLTree:
    def get_height(self, node):
        if not node:
            return 0
        return node.height

    def get_balance(self, node):
        if not node:
            return 0
        return self.get_height(node.left) - self.get_height(node.right)

    def rotate_right(self, y):
        x = y.left
        T2 = x.right

        # Rotación
        x.right = y
        y.left = T2

        # Actualizar alturas
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        x.height = 1 + max(self.get_height(x.left), self.get_height(x.right))

        return x

    def rotate_left(self, x):
        y = x.right
        T2 = y.left

        # Rotación
        y.left = x
        x.right = T2

        # Actualizar alturas
        x.height = 1 + max(self.get_height(x.left), self.get_height(x.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))

        return y

    def insert(self, node, value):
        if not node:
            return TreeNode(value)

        if value < node.value:
            node.left = self.insert(node.left, value)
        elif value > node.value:
            node.right = self.insert(node.right, value)
        else:
            return node

        # Actualizar la altura del ancestro
        node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))

        # Obtener el balance del ancestro
        balance = self.get_balance(node)

        # Balancear el nodo si está desbalanceado
        if balance > 1 and value < node.left.value:
            return self.rotate_right(node)
        if balance < -1 and value > node.right.value:
            return self.rotate_left(node)
        if balance > 1 and value > node.left.value:
            node.left = self.rotate_left(node.left)
            return self.rotate_right(node)
        if balance < -1 and value < node.right.value:
            node.right = self.rotate_right(node.right)
            return self.rotate_left(node)

        return node


# Función para dibujar el árbol
def draw_tree(screen, node, x, y, angle, depth, max_depth, length=100):
    if node is None or depth > max_depth:
        return

    # Ajustar la longitud de las ramas para cada nivel
    branch_length = length / (depth + 1)

    # Calcular las posiciones de los hijos en diagonal
    left_x = x - branch_length * math.cos(math.radians(angle + 30))
    left_y = y + branch_length * math.sin(math.radians(angle + 30))
    right_x = x + branch_length * math.cos(math.radians(angle - 30))
    right_y = y + branch_length * math.sin(math.radians(angle - 30))

    # Dibuja las líneas entre los nodos (las ramas)
    if node.left:
        pygame.draw.line(screen, BLACK, (x, y), (left_x, left_y), 2)
        draw_tree(screen, node.left, left_x, left_y, angle + 30, depth + 1, max_depth, length)

    if node.right:
        pygame.draw.line(screen, BLACK, (x, y), (right_x, right_y), 2)
        draw_tree(screen, node.right, right_x, right_y, angle + 30, depth + 1, max_depth,
                  length)  # Cambié el ángulo aquí

    # Dibuja el nodo como un círculo
    pygame.draw.circle(screen, BLUE, (int(x), int(y)), 20)
    text = font.render(str(node.value), True, WHITE)
    screen.blit(text, (int(x) - 10, int(y) - 10))


# Crear y llenar el árbol AVL
avl_tree = AVLTree()
root = None

# Variables para el control del árbol y la inserción de nuevos números
max_depth = 5
input_value = ""  # Para capturar el número que el usuario desea insertar

# Bucle principal del programa
running = True
while running:
    # Rellena la pantalla de blanco
    screen.fill(WHITE)

    # Dibujar el árbol centrado en la pantalla, con la raíz arriba
    if root:
        draw_tree(screen, root, width // 2, 50, 0, 0, max_depth)

    # Mostrar la entrada del número
    input_text = font.render(f"Insertar número: {input_value}", True, BLACK)
    screen.blit(input_text, (10, height - 40))

    # Actualiza la pantalla
    pygame.display.flip()

    # Manejo de eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Captura el input del teclado para insertar un nuevo número
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                input_value = input_value[:-1]  # Borra el último carácter
            elif event.key == pygame.K_RETURN:
                if input_value.isdigit():
                    # Inserta el número en el árbol AVL
                    root = avl_tree.insert(root, int(input_value))
                    input_value = ""  # Limpia el input después de la inserción
            elif event.unicode.isdigit():
                input_value += event.unicode  # Agrega el número a la cadena de entrada

# Salir de pygame
pygame.quit()
