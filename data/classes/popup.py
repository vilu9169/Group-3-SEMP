import pygame as pg

def show_popup(screen, message):
    #Create a pop-up window
    pop_up_width = 600
    pop_up_height = 500
    pop_up_surface = pg.Surface((pop_up_width, pop_up_height))
    pop_up_surface.fill((255, 255, 255))

    pop_up_x = 100
    pop_up_y = 50

    # Draw the text on the pop-up window
    font = pg.font.Font(None, 24)
    words = message.split(' ')
    lines = []
    current_line = ""
    for word in words:
        if '\n' in word:
            parts = word.split('\n')
            for part in parts[:-1]:
                test_line = current_line + part
                lines.append(test_line)
                current_line = ""
            current_line = parts[-1] + " "
        else:
            test_line = current_line + word + " "
            if font.size(test_line)[0] < pop_up_width - 40: 
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word + " "
    lines.append(current_line)

    # Calculate the total height of the text
    line_height = font.size("Tg")[1]
    total_text_height = line_height * len(lines)

    # Initial scroll position
    scroll_y = 0

    #Define exit button
    exit_button_rect = pg.Rect(pop_up_width - 30, 10, 20, 20)

    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()
            elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                mouse_x, mouse_y = event.pos
                if pop_up_x <= mouse_x <= pop_up_x + pop_up_width and pop_up_y <= mouse_y <= pop_up_y + pop_up_height:
                    if exit_button_rect.collidepoint(mouse_x - pop_up_x, mouse_y - pop_up_y):
                        running = False  # Close the pop-up window on exit button click
            elif event.type == pg.MOUSEWHEEL:
                scroll_y += event.y * 10  # Adjust scroll speed
                scroll_y = max(min(scroll_y, 0), pop_up_height - total_text_height - 40)  # 40 for padding


        # Clear the pop-up surface
        pop_up_surface.fill((255, 255, 255))

        # Draw the text lines
        y = 20 + scroll_y
        for line in lines:
            text_surface = font.render(line, True, (0, 0, 0))
            pop_up_surface.blit(text_surface, (20, y))
            y += line_height

        # Draw the exit button
        pg.draw.rect(pop_up_surface, (255, 0, 0), exit_button_rect)  # Red exit button
        exit_font = pg.font.Font(None, 24)
        exit_text = exit_font.render('X', True, (255, 255, 255))
        pop_up_surface.blit(exit_text, (pop_up_width - 28, 10))

        #Display the pop-up window on the screen
        screen.blit(pop_up_surface, (100, 50))
        pg.display.flip()