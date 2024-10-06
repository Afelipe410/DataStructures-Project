import pygame
import math
import sys
import pygame_gui
from datetime import timedelta

# Inicializa pygame
pygame.init()

# Definir los colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (183, 249, 0)

# Crear la ventana
width, height = 800, 700
screen = pygame.display.set_mode((width, height))
dragging = False  # Indica si se está arrastrando el mouse
zoom = 1.0  # Nivel de zoom inicial
offset_x, offset_y = 0, 0
pygame.display.set_caption("Árbol AVL en Pygame")

# Inicializa la fuente para el texto
pygame.font.init()
font_size = int(14 * zoom)
font = pygame.font.SysFont('Arial', font_size)


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


class PriceSearchPopup:
    def __init__(self, manager, window_surface, avl_tree, root):
        self.manager = manager
        self.window_surface = window_surface
        self.avl_tree = avl_tree
        self.root = root
        self.is_active = True
        self.focused_entry = None

        # Crear la ventana con un botón de cierre
        self.popup_window = pygame_gui.elements.UIWindow(
            pygame.Rect(50, 50, 500, 300),
            self.manager,
            window_display_title="Búsqueda por Precio",
            object_id="#price_search_window",
            resizable=False
        )
        self.min_price_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(10, 10, 100, 30),
            text="Precio Mínimo:",
            manager=self.manager,
            container=self.popup_window
        )
        self.min_price_entry = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect(120, 10, 100, 30),
            manager=self.manager,
            container=self.popup_window
        )

        self.max_price_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(10, 50, 100, 30),
            text="Precio Máximo:",
            manager=self.manager,
            container=self.popup_window
        )

        self.max_price_entry = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect(120, 50, 100, 30),
            manager=self.manager,
            container=self.popup_window
        )

        self.search_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(10, 90, 100, 30),
            text="Buscar",
            manager=self.manager,
            container=self.popup_window
        )

        self.results_textbox = pygame_gui.elements.UITextBox(
            relative_rect=pygame.Rect(10, 130, 480, 160),
            html_text="Los resultados se mostrarán aquí.",
            manager=self.manager,
            container=self.popup_window
        )

    def handle_event(self, event):
        if event.type == pygame_gui.UI_WINDOW_CLOSE:
            if event.ui_element == self.popup_window:
                self.cleanup()
                return True

        elif event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.search_button:
                self.perform_search()

        elif event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED:
            if event.ui_element in [self.min_price_entry, self.max_price_entry]:
                self.focused_entry = event.ui_element

        return False

    def cleanup(self):
        """Limpia los recursos de la ventana"""
        self.is_active = False
        self.popup_window.kill()
        self.min_price_entry = None
        self.max_price_entry = None
        self.search_button = None
        self.results_textbox = None

    def perform_search(self):
        try:
            min_price = float(self.min_price_entry.get_text())
            max_price = float(self.max_price_entry.get_text())

            if min_price > max_price:
                min_price, max_price = max_price, min_price

            search_results = []
            self.avl_tree.search_by_price_range(self.root, min_price, max_price, search_results)

            if search_results:
                result_text = "<br>".join([
                    f"ID: {r.value}, Nombre: {r.name}, Precio: {r.price}, Cantidad: {r.quantity}, Categoría: {r.category}"
                    for r in search_results
                ])
            else:
                result_text = "No se encontraron resultados."

            self.results_textbox.html_text = result_text
            self.results_textbox.rebuild()
        except ValueError:
            self.results_textbox.html_text = "Por favor, ingrese valores numéricos válidos para los precios."
            self.results_textbox.rebuild()


class IdSearchPopup:
    def __init__(self, manager, window_surface, avl_tree, root):
        self.manager = manager
        self.window_surface = window_surface
        self.avl_tree = avl_tree
        self.root = root

        self.popup_window = pygame_gui.elements.UIWindow(
            pygame.Rect(50, 50, 500, 200),
            self.manager,
            window_display_title="Búsqueda por ID",
            object_id="#id_search_window"
        )

        self.id_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(10, 10, 100, 30),
            text="ID del Producto:",
            manager=self.manager,
            container=self.popup_window
        )

        self.id_entry = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect(120, 10, 100, 30),
            manager=self.manager,
            container=self.popup_window
        )

        self.search_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(10, 50, 100, 30),
            text="Buscar",
            manager=self.manager,
            container=self.popup_window
        )

        self.results_textbox = pygame_gui.elements.UITextBox(
            relative_rect=pygame.Rect(10, 90, 480, 100),
            html_text="Los resultados se mostrarán aquí.",
            manager=self.manager,
            container=self.popup_window
        )

    def handle_event(self, event):
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.search_button:
                self.perform_search()

    def perform_search(self):
        try:
            id_to_search = int(self.id_entry.get_text())
            result = self.avl_tree.search_by_id(self.root, id_to_search)

            if result:
                result_text = f"ID: {result.value}, Nombre: {result.name}, Precio: {result.price}, Cantidad: {result.quantity}, Categoría: {result.category}"
            else:
                result_text = "No se encontró ningún producto con ese ID."

            self.results_textbox.html_text = result_text
            self.results_textbox.rebuild()
        except ValueError:
            self.results_textbox.html_text = "Por favor, ingrese un ID válido (número entero)."
            self.results_textbox.rebuild()


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

    def search_by_id(self, node, id):
        if node is None:
            return None
        if id == node.value:
            return node
        if id < node.value:
            return self.search_by_id(node.left, id)
        return self.search_by_id(node.right, id)

    def search_by_price_range(self, node, min_price, max_price, results):
        if node is None:
            return
        if min_price <= node.price <= max_price:
            results.append(node)
        if node.price > min_price:
            self.search_by_price_range(node.left, min_price, max_price, results)
        if node.price < max_price:
            self.search_by_price_range(node.right, min_price, max_price, results)


# Función para dibujar el árbol
CATEGORY_COLORS = {
    'Lácteos': (249, 243, 122),
    'Bebidas': (144, 238, 144),
    'Carnes': (255, 182, 193),
    'Aseo': (165, 209, 229),
    'Frutas': (255, 160, 122),
    'Verduras': (152, 251, 152),
    'Snacks': (255, 218, 185),
    'Cereales': (222, 184, 135),
    'Panadería': (255, 222, 173),
    'Congelados': (166, 156, 232)
}

zoom = 1
offset_x = 0
offset_y = 0
mouse_x = 0
mouse_y = 0


# Modificar la función draw_tree para usar los colores por categoría
def draw_tree(screen, node, x, y, angle, depth, max_depth, length=300):
    if node is None or depth > max_depth:
        return

    # Ajustar la longitud de las ramas para cada nivel
    branch_length = (length / (depth + 1)) * zoom  # Aplicar zoom

    # Calcular las posiciones de los hijos en diagonal
    left_x = x - branch_length * math.cos(math.radians(angle + 30))
    left_y = y + branch_length * math.sin(math.radians(angle + 30))
    right_x = x + branch_length * math.cos(math.radians(angle + 30))
    right_y = y + branch_length * math.sin(math.radians(angle + 30))

    # Dibuja las líneas entre los nodos (las ramas)
    if node.left:
        line_thickness = max(1, int(2 * zoom))
        # Escalar las posiciones de los nodos para que coincidan con el zoom
        pygame.draw.line(screen, BLACK,
                         (int(x * zoom + offset_x), int(y * zoom + offset_y)),
                         (int(left_x * zoom + offset_x), int(left_y * zoom + offset_y)),
                         line_thickness)
        draw_tree(screen, node.left, left_x, left_y, angle + 30, depth + 1, max_depth, length)

    if node.right:
        line_thickness = max(1, int(2 * zoom))
        pygame.draw.line(screen, BLACK,
                         (int(x * zoom + offset_x), int(y * zoom + offset_y)),
                         (int(right_x * zoom + offset_x), int(right_y * zoom + offset_y)),
                         line_thickness)
        draw_tree(screen, node.right, right_x, right_y, angle + 30, depth + 1, max_depth, length)
    # Obtener el color basado en la categoría
    node_color = CATEGORY_COLORS.get(node.category, BLUE)  # Si la categoría no existe, usa el color por defecto

    # Dibuja el nodo como un círculo con el color de la categoría
    pygame.draw.circle(screen, node_color, (int(x * zoom + offset_x), int(y * zoom + offset_y)), int(50 * zoom))
    pygame.draw.circle(screen, BLACK, (int(x * zoom + offset_x), int(y * zoom + offset_y)), int(50 * zoom), 2)

    # Mostrar la información dentro del nodo
    product_name = font.render(f"{node.name}", True, BLACK)
    product_details = font.render(f"Cant: {node.quantity} $: {node.price}", True, BLACK)
    product_category = font.render(f"Catg: {node.category}", True, BLACK)

    # Colocar los textos dentro del nodo
    text_offset_x = 40 * zoom
    screen.blit(product_name, (int(x * zoom + offset_x) - text_offset_x, int(y * zoom + offset_y) - 30 * zoom))
    screen.blit(product_details, (int(x * zoom + offset_x) - text_offset_x, int(y * zoom + offset_y) - 10 * zoom))
    screen.blit(product_category, (int(x * zoom + offset_x) - text_offset_x, int(y * zoom + offset_y) + 10 * zoom))


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
GRAY = (200, 200, 200)
DARK_GRAY = (150, 150, 150)
SCROLL_BAR_COLOR = (100, 100, 100)
SCROLL_THUMB_COLOR = (80, 80, 80)

# Lista de categorías disponibles (agregué más para demostrar el scroll)
CATEGORIES = ['Lácteos', 'Bebidas', 'Carnes', 'Aseo', 'Frutas', 'Verduras',
              'Snacks', 'Cereales', 'Panadería', 'Congelados']


class ScrollBar:
    def __init__(self, x, y, w, h, total_items, visible_items):
        self.rect = pygame.Rect(x, y, w, h)
        self.thumb_rect = pygame.Rect(x, y, w, 30)  # 30 es el alto inicial del thumb
        self.total_items = total_items
        self.visible_items = visible_items
        self.scroll_pos = 0
        self.dragging = False
        self.calculate_thumb_size()

    def calculate_thumb_size(self):
        # Calcula el tamaño del thumb basado en la proporción de items visibles
        if self.total_items > self.visible_items:
            thumb_height = max(20, (self.visible_items / self.total_items) * self.rect.height)
            self.thumb_rect.height = thumb_height

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.thumb_rect.collidepoint(event.pos):
                self.dragging = True
                return True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            _, rel_y = event.rel
            self.thumb_rect.y = max(self.rect.y,
                                    min(self.rect.bottom - self.thumb_rect.height,
                                        self.thumb_rect.y + rel_y))
            # Calcular la posición del scroll basado en la posición del thumb
            scroll_range = self.total_items - self.visible_items
            if scroll_range > 0:
                self.scroll_pos = ((self.thumb_rect.y - self.rect.y) /
                                   (self.rect.height - self.thumb_rect.height) * scroll_range)
            return True
        return False

    def draw(self, surface):
        pygame.draw.rect(surface, SCROLL_BAR_COLOR, self.rect)
        pygame.draw.rect(surface, SCROLL_THUMB_COLOR, self.thumb_rect)


class DropdownMenu:
    def __init__(self, x, y, w, h, options):
        self.rect = pygame.Rect(x, y, w, h)
        self.options = options
        self.active = False
        self.selected = None
        self.visible_items = 3  # Número de items visibles a la vez
        self.option_height = h

        # Crear los rectángulos para las opciones visibles
        self.option_rects = []
        for i in range(self.visible_items):
            self.option_rects.append(pygame.Rect(x, y + (i + 1) * h, w - 15, h))  # -15 para dar espacio a la barra

        # Crear la barra de desplazamiento
        self.scrollbar = ScrollBar(x + w - 15, y + h, 15,
                                   self.visible_items * h,
                                   len(options), self.visible_items)

    def draw(self, surface):
        # Dibujar el botón principal
        pygame.draw.rect(surface, GRAY, self.rect)
        text = font.render(self.selected if self.selected else "Seleccionar categoría", True, BLACK)
        surface.blit(text, (self.rect.x + 5, self.rect.y + 5))

        # Si está activo, mostrar las opciones y la barra de desplazamiento
        if self.active:
            start_idx = int(self.scrollbar.scroll_pos)

            # Dibujar el fondo del área desplegable
            dropdown_rect = pygame.Rect(self.rect.x, self.rect.y + self.rect.height,
                                        self.rect.width, self.visible_items * self.option_height)
            pygame.draw.rect(surface, DARK_GRAY, dropdown_rect)

            # Dibujar las opciones visibles
            for i in range(self.visible_items):
                option_idx = start_idx + i
                if option_idx < len(self.options):
                    pygame.draw.rect(surface, DARK_GRAY, self.option_rects[i])
                    text = font.render(self.options[option_idx], True, BLACK)
                    surface.blit(text, (self.option_rects[i].x + 5, self.option_rects[i].y + 5))

            # Dibujar la barra de desplazamiento
            self.scrollbar.draw(surface)

    def handle_event(self, event):
        if self.active:
            # Manejar eventos de la barra de desplazamiento
            if self.scrollbar.handle_event(event):
                return False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
                return False
            elif self.active:
                # Calcular qué opción fue clickeada
                for i, rect in enumerate(self.option_rects):
                    if rect.collidepoint(event.pos):
                        option_idx = int(self.scrollbar.scroll_pos) + i
                        if option_idx < len(self.options):
                            self.selected = self.options[option_idx]
                            self.active = False
                            return True

        # Manejar el scroll con la rueda del mouse
        elif event.type == pygame.MOUSEWHEEL and self.active:
            self.scrollbar.scroll_pos = max(0, min(len(self.options) - self.visible_items,
                                                   self.scrollbar.scroll_pos - event.y))
            self.scrollbar.thumb_rect.y = (self.scrollbar.rect.y +
                                           (self.scrollbar.scroll_pos / (len(self.options) - self.visible_items)) *
                                           (self.scrollbar.rect.height - self.scrollbar.thumb_rect.height))

        return False


def draw_color_legend(screen, x, y):
    legend_title = font.render("Categorías:", True, BLACK)
    screen.blit(legend_title, (x, y))

    y_offset = 20
    for category, color in CATEGORY_COLORS.items():
        # Dibujar un pequeño rectángulo con el color de la categoría
        pygame.draw.rect(screen, color, (x, y + y_offset, 20, 20))
        pygame.draw.rect(screen, BLACK, (x, y + y_offset, 20, 20), 1)

        # Dibujar el nombre de la categoría
        category_text = font.render(category, True, BLACK)
        screen.blit(category_text, (x + 30, y + y_offset))

        y_offset += 25


# Crear el menú desplegable con la nueva implementación
dropdown = DropdownMenu(200, height - 90, 150, 25, CATEGORIES)
show_legend = False

# Modificar el bucle principal del programa:
running = True
manager = pygame_gui.UIManager((width, height))
price_search_popup = None
id_search_popup = None
searching_by_id = False
searching_by_price = False
id_to_search = ""
search_results = []

clock = pygame.time.Clock()

while running:
    timedelta = clock.tick(60) / 1000.0

    screen.fill(WHITE)

    # Dibujar el árbol
    if root:
        draw_tree(screen, root, (width // 2 - offset_x) / zoom, (50 - offset_y) / zoom, 0, 0, max_depth)

    # Crear el botón "Buscar precio" encima del botón "Categorías"
    button_rect = pygame.Rect(width - 150, height - 260, 140, 40)
    pygame.draw.rect(screen, (100, 100, 100), button_rect)
    advanced_search_text = font.render("Buscar por criterios", True, WHITE)
    screen.blit(advanced_search_text, (width - 140, height - 250))

    # Crear botones para búsquedas
    price_search_button = pygame.Rect(width - 150, height - 210, 140, 40)
    pygame.draw.rect(screen, (100, 100, 100), price_search_button)
    price_search_text = font.render("Buscar por Precio", True, WHITE)
    screen.blit(price_search_text, (width - 140, height - 200))

    id_search_button = pygame.Rect(width - 150, height - 160, 140, 40)
    pygame.draw.rect(screen, (100, 100, 100), id_search_button)
    id_search_text = font.render("Buscar por ID", True, WHITE)
    screen.blit(id_search_text, (width - 140, height - 150))

    # Crear el botón "Buscar por Categoría"
    button_rect = pygame.Rect(width - 150, height - 110, 140, 40)
    pygame.draw.rect(screen, (100, 100, 100), button_rect)
    category_search_text = font.render("Buscar por Categoría", True, WHITE)
    screen.blit(category_search_text, (width - 140, height - 100))

    # Crear el botón "Categorías"
    button_rect = pygame.Rect(width - 150, height - 60, 140, 38)
    pygame.draw.rect(screen, (100, 100, 100), button_rect)
    categories_text = font.render("Categorías", True, WHITE)
    screen.blit(categories_text, (width - 140, height - 50))

    # Mostrar la leyenda de categorías en la esquina superior derecha
    if show_legend:
        draw_color_legend(screen, width - 200, 20)  # Cambié la posición a la parte superior derecha

    # Dibujar instrucciones de inserción de productos
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
        dropdown.draw(screen)

    manager.update(timedelta)
    manager.draw_ui(screen)

    pygame.display.flip()

    # Manejo de eventos
    for event in pygame.event.get():
        manager.process_events(event)
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if id_search_button.collidepoint(event.pos):
                searching_by_id = True
                searching_by_price = False
                id_to_search = ""
                search_results = []
            elif price_search_button.collidepoint(event.pos):
                if price_search_popup is None or not price_search_popup.is_active:
                    price_search_popup = PriceSearchPopup(manager, screen, avl_tree, root)
            elif id_search_button.collidepoint(event.pos):
                if id_search_popup is None:
                    id_search_popup = IdSearchPopup(manager, screen, avl_tree, root)
            elif button_rect.collidepoint(event.pos):
                show_legend = not show_legend

        if price_search_popup and price_search_popup.is_active:
            if price_search_popup.handle_event(event):
                price_search_popup = None
        if id_search_popup:
            id_search_popup.handle_event(event)
        elif event.type == pygame.KEYDOWN:
            if not (price_search_popup and price_search_popup.is_active):
                if searching_by_id:
                    if event.key == pygame.K_RETURN:
                        if id_to_search.isdigit():
                            result = avl_tree.search_by_id(root, int(id_to_search))
                            if result:
                                search_results = [result]
                            else:
                                search_results = []
                        searching_by_id = False
                    elif event.key == pygame.K_BACKSPACE:
                        id_to_search = id_to_search[:-1]
                    else:
                        id_to_search += event.unicode
                else:
                    if event.key == pygame.K_BACKSPACE:
                        if step == 0:
                            input_value = input_value[:-1]
                        elif step == 1:
                            input_name = input_name[:-1]
                        elif step == 2:
                            input_quantity = input_quantity[:-1]
                        elif step == 3:
                            input_price = input_price[:-1]
                    elif event.key == pygame.K_RETURN:
                        if step == 0 and input_value.isdigit():
                            step = 1
                        elif step == 1 and input_name:
                            step = 2
                        elif step == 2 and input_quantity.isdigit():
                            step = 3
                        elif step == 3 and input_price.replace(".", "", 1).isdigit():
                            step = 4
                        elif step == 4 and dropdown.selected:
                            # Insertar el nodo
                            root = avl_tree.insert(root, int(input_value), input_name, int(input_quantity),
                                                   float(input_price), dropdown.selected)

                            # Limpiar las entradas
                            input_value = ""
                            input_name = ""
                            input_quantity = ""
                            input_price = ""
                            dropdown.selected = None
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
            dropdown.handle_event(event)

        # Manejo de desplazamiento
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:  # Rueda hacia arriba
                zoom *= 1.1
            elif event.button == 5:  # Rueda hacia abajo
                zoom /= 1.1

        manager.update(timedelta)
        # ... resto del código de dibujo ...
        manager.draw_ui(screen)

pygame.quit()

