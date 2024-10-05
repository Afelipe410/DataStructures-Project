button_rect = pygame.Rect(width - 150, height - 240, 140, 40)
    pygame.draw.rect(screen, (100,100,100), button_rect)
    advanced_search_text = font.render("Buscar por criterios", True, WHITE)
    screen.blit(advanced_search_text, (width - 140, height - 230))    

    button_rect = pygame.Rect(width - 150, height - 190, 140, 40)
    pygame.draw.rect(screen, (100,100,100), button_rect)
    price_search_text = font.render("Buscar por Precio", True, WHITE)
    screen.blit(price_search_text, (width - 140, height - 180))

    # Crear el botón "Buscar por ID"
    button_rect = pygame.Rect(width - 150, height - 140, 140, 40)
    pygame.draw.rect(screen, (100,100,100), button_rect)
    id_search_text = font.render("Buscar por ID", True, WHITE)
    screen.blit(id_search_text, (width - 140, height - 130))

    # Crear el botón "Buscar por Categoría"
    button_rect = pygame.Rect(width - 150, height - 90, 140, 40)
    pygame.draw.rect(screen, (100,100,100), button_rect)
    category_search_text = font.render("Buscar por Categoría", True, WHITE)
    screen.blit(category_search_text, (width - 140, height - 80))

    # Crear el botón "Categorías"
    button_rect = pygame.Rect(width - 150, height - 40, 140, 38)
    pygame.draw.rect(screen, (100,100,100), button_rect)
    categories_text = font.render("Categorías", True, WHITE)
    screen.blit(categories_text, (width - 140, height - 30))

    # Mostrar la leyenda de categorías en la esquina superior derecha
    if show_legend:
        draw_color_legend(screen, width - 100, 20)  # Cambié la posición a la parte superior derecha

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
