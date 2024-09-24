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
    def __init__(self, id, name):
        self.id = id
        self.name = name
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

    def insert(self, node, id, name):
        if not node:
            return TreeNode(id, name)

        if id < node.id:
            node.left = self.insert(node.left, id, name)
        elif id > node.id:
            node.right = self.insert(node.right, id, name)
        else:
            return node  # Si el ID ya existe, no lo insertamos

        # Actualizar la altura del ancestro
        node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))

        # Obtener el balance del ancestro
        balance = self.get_balance(node)

        # Balancear el nodo si está desbalanceado
        if balance > 1 and id < node.left.id:
            return self.rotate_right(node)
        if balance < -1 and id > node.right.id:
            return self.rotate_left(node)
        if balance > 1 and id > node.left.id:
            node.left = self.rotate_left(node.left)
            return self.rotate_right(node)
        if balance < -1 and id < node.right.id:
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
    right_x = x + branch_length * math.cos(math.radians(angle + 30))
    right_y = y + branch_length * math.sin(math.radians(angle + 30))

    # Dibuja las líneas entre los nodos (las ramas)
    if node.left:
        pygame.draw.line(screen, BLACK, (x, y), (left_x, left_y), 2)
        draw_tree(screen, node.left, left_x, left_y, angle + 30, depth + 1, max_depth, length)

    if node.right:
        pygame.draw.line(screen, BLACK, (x, y), (right_x, right_y), 2)
        draw_tree(screen, node.right, right_x, right_y, angle + 30, depth + 1, max_depth, length)

    # Dibuja el nodo como un círculo
    pygame.draw.circle(screen, BLUE, (int(x), int(y)), 20)
    text = font.render(f"{node.id}: {node.name}", True, WHITE)
    screen.blit(text, (int(x) - 30, int(y) - 10))  # Muestra el ID y el nombre

# Crear y llenar el árbol AVL
avl_tree = AVLTree()
root = None

# Variables para el control del árbol y la inserción de nuevos números
max_depth = 5
input_id = ""    # Para capturar el ID
input_name = ""  # Para capturar el nombre
inserting_id = True  # Indica si estamos en el campo de ID o de nombre

# Bucle principal del programa
running = True
while running:
    # Rellena la pantalla de blanco
    screen.fill(WHITE)

    # Dibujar el árbol centrado en la pantalla, con la raíz arriba
    if root:
        draw_tree(screen, root, width // 2, 50, 0, 0, max_depth)

    # Mostrar la entrada del ID y del nombre
    input_text_id = font.render(f"Insertar ID: {input_id}", True, BLACK)
    input_text_name = font.render(f"Insertar Nombre: {input_name}", True, BLACK)
    screen.blit(input_text_id, (10, height - 60))
    screen.blit(input_text_name, (10, height - 30))

    # Actualiza la pantalla
    pygame.display.flip()

    # Manejo de eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Captura el input del teclado para insertar un nuevo ID y nombre
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                # Borra el último carácter de la entrada activa
                if inserting_id and len(input_id) > 0:
                    input_id = input_id[:-1]  # Borra del ID
                elif not inserting_id and len(input_name) > 0:
                    input_name = input_name[:-1]  # Borra del nombre
            elif event.key == pygame.K_RETURN:
                if inserting_id:
                    # Cambiar al campo de nombre
                    inserting_id = False
                else:
                    # Verificar que el ID no esté vacío y que el nombre tenga al menos un carácter
                    if input_id.isdigit() and len(input_name) > 0:
                        # Inserta el ID y nombre en el árbol AVL
                        root = avl_tree.insert(root, int(input_id), input_name)  # Actualiza la raíz aquí
                        input_id = ""    # Limpia el input del ID después de la inserción
                        input_name = ""  # Limpia el input del nombre después de la inserción
                        inserting_id = True  # Volver al campo de ID
            elif event.unicode.isalnum() or event.unicode in [' ', '_']:  # Permitir letras, números, espacios y guiones bajos
                # Agregar caracteres al campo correspondiente
                if inserting_id:
                    input_id += event.unicode  # Agrega el carácter al ID
                else:
                    input_name += event.unicode  # Agrega el carácter al nombre

# Salir de pygame
pygame.quit()
