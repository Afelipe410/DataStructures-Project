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
font = pygame.font.SysFont('Arial', 14)


# Clase para representar un nodo del árbol
class TreeNode:
    def __init__(self, value, name, quantity, price, category):
        self.value = value
        self.name = name
        self.quantity = quantity
        self.price = price
        self.category = category
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

    def insert(self, node, value, name, quantity, price, category):
        if not node:
            return TreeNode(value, name, quantity, price, category)

        if value < node.value:
            node.left = self.insert(node.left, value, name, quantity, price, category)
        elif value > node.value:
            node.right = self.insert(node.right, value, name, quantity, price, category)
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
def draw_tree(screen, node, x, y, angle, depth, max_depth, length=300):
    if node is None or depth > max_depth:
        return

    # Ajustar la longitud de las ramas para cada nivel
    branch_length = length / (depth + 1)

    # Calcular las posiciones de los hijos en diagonal
    left_x = x - branch_length * math.cos(math.radians(angle + 30))
    left_y = y + branch_length * math.sin(math.radians(angle + 30))
    right_x = x + branch_length * math.cos(math.radians(angle + 30))
    right_y = y + branch_length * math.sin(math.radians(angle + 30))

    # Dibuja las líneas entre los nodos (las ramas)
    if node.left:
        pygame.draw.line(screen, BLACK, (x, y), (left_x, left_y), 2)
        draw_tree(screen, node.left, left_x, left_y, angle + 30, depth + 1, max_depth, length)

    if node.right:
        pygame.draw.line(screen, BLACK, (x, y), (right_x, right_y), 2)
        draw_tree(screen, node.right, right_x, right_y, angle + 30, depth + 1, max_depth, length)

    # Dibuja el nodo como un círculo más grande para contener todos los detalles
    pygame.draw.circle(screen, BLUE, (int(x), int(y)), 50)

    # Mostrar la información dentro del nodo
    product_name = font.render(f"{node.name}", True, WHITE)
    product_details = font.render(f"Cant: {node.quantity} $: {node.price}", True, WHITE)
    product_category = font.render(f"Catg: {node.category}", True, WHITE)

    # Colocar los textos dentro del nodo
    screen.blit(product_name, (int(x) - 40, int(y) - 30))
    screen.blit(product_details, (int(x) - 40, int(y) - 10))
    screen.blit(product_category, (int(x) - 40, int(y) + 10))


# Crear y llenar el árbol AVL
avl_tree = AVLTree()
root = None

# Variables para el control del árbol y la inserción de nuevos productos
max_depth = 5
input_value = ""  # Para capturar el ID del producto que el usuario desea insertar
input_name = ""
input_quantity = ""
input_price = ""
input_category = ""
step = 0  # Para controlar el paso de la inserción

# Bucle principal del programa
running = True
while running:
    # Rellena la pantalla de blanco
    screen.fill(WHITE)

    # Dibujar el árbol centrado en la pantalla, con la raíz arriba
    if root:
        draw_tree(screen, root, width // 2, 50, 0, 0, max_depth)

    # Mostrar las entradas de los datos del producto
    input_text = font.render(f"Paso {step + 1}:", True, BLACK)
    screen.blit(input_text, (10, height - 120))

    if step == 0:
        instruction = font.render("ID del producto:", True, BLACK)
        screen.blit(instruction, (10, height - 90))
        input_display = font.render(input_value, True, BLACK)
        screen.blit(input_display, (200, height - 90))
    elif step == 1:
        instruction = font.render("Nombre del producto:", True, BLACK)
        screen.blit(instruction, (10, height - 90))
        input_display = font.render(input_name, True, BLACK)
        screen.blit(input_display, (200, height - 90))
    elif step == 2:
        instruction = font.render("Cantidad:", True, BLACK)
        screen.blit(instruction, (10, height - 90))
        input_display = font.render(input_quantity, True, BLACK)
        screen.blit(input_display, (200, height - 90))
    elif step == 3:
        instruction = font.render("Precio:", True, BLACK)
        screen.blit(instruction, (10, height - 90))
        input_display = font.render(input_price, True, BLACK)
        screen.blit(input_display, (200, height - 90))
    elif step == 4:
        instruction = font.render("Categoría:", True, BLACK)
        screen.blit(instruction, (10, height - 90))
        input_display = font.render(input_category, True, BLACK)
        screen.blit(input_display, (200, height - 90))

    # Actualiza la pantalla
    pygame.display.flip()

    # Manejo de eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Captura el input del teclado para insertar un nuevo producto
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                if step == 0:
                    input_value = input_value[:-1]
                elif step == 1:
                    input_name = input_name[:-1]
                elif step == 2:
                    input_quantity = input_quantity[:-1]
                elif step == 3:
                    input_price = input_price[:-1]
                elif step == 4:
                    input_category = input_category[:-1]
            elif event.key == pygame.K_RETURN:
                if step == 0 and input_value.isdigit():
                    step = 1
                elif step == 1:
                    step = 2
                elif step == 2 and input_quantity.isdigit():
                    step = 3
                elif step == 3 and input_price.replace(".", "", 1).isdigit():
                    step = 4
                elif step == 4:
                    root = avl_tree.insert(root, int(input_value), input_name, int(input_quantity), float(input_price),
                                           input_category)
                    # Limpiar las entradas después de insertar el producto
                    input_value = ""
                    input_name = ""
                    input_quantity = ""
                    input_price = ""
                    input_category = ""
                    step = 0
            else:
                if step == 0:
                    input_value += event.unicode
                elif step == 1:
                    input_name += event.unicode
                elif step == 2:
                    input_quantity += event.unicode
                elif step == 3:
                    input_price += event.unicode
                elif step == 4:
                    input_category += event.unicode

# Salir de pygame
pygame.quit()
