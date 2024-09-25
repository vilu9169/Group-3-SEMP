import pygame as pg

def show_popup(screen, message):
    # Create a pop-up window
    pop_up_width = 400
    pop_up_height = 300
    pop_up_surface = pg.Surface((pop_up_width, pop_up_height))
    pop_up_surface.fill((200, 200, 200))  # Light gray background

    # Draw the text on the pop-up window
    font = pg.font.Font(None, 36)
    text_surface = font.render(message, True, (0, 0, 0))
    text_rect = text_surface.get_rect(center=(pop_up_width // 2, pop_up_height // 2))
    pop_up_surface.blit(text_surface, text_rect)

    # Display the pop-up window on the screen
    screen.blit(pop_up_surface, (200, 150))  # Position the pop-up window

    # Update the display
    pg.display.flip()

    # Handle events to close the pop-up window
    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()
            elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                running = False  # Close the pop-up window on mouse click