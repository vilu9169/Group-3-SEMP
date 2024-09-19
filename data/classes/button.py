import pygame as pg

"""Class ActionButton is a reactive button that does an action when the mouse clicks on an ActionButton object.  """
class ActionButton():

    def __init__(self, position, width, height, color, action = None):

        self.mouse_hover = False  
        self.position = position
        self.width = width
        self.height = height
        self.color = color
        self.action = action

        #Normal size of button
        self.normal_rect = pg.Rect( 
            self.position[0],
            self.position[1],
            self.width,
            self.height
        )
        #Size that the button transforms to on mouse hover. Position is adjusted so that the button expands from the middle.
        self.highlighted_rect = pg.Rect( 
            self.position[0] -(width*0.1),
            self.position[1] - (height*0.1),
            self.width * 1.2,
            self.height *1.2
        )

        self.rects = [self.normal_rect,
                      self.highlighted_rect]

    #Updates whether the button is being hovered by the mouse or not. If the mouse clicks the function will return what action to perform
    def update(self, mouse_pos, mouse_clicked):
        if self.normal_rect.collidepoint(mouse_pos):
            self.mouse_hover = True
            if mouse_clicked:
                return self.action
        else:
            self.mouse_hover = False

    #draws the normal button if the mouse is not hovering, otherwise it draws the highlighted button
    def draw(self, screen):
        if self.mouse_hover:
            pg.draw.rect(screen, self.color, self.rects[1], 0, 25)
        else:
            pg.draw.rect(screen, self.color, self.rects[0], 0, 25)
            