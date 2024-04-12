import pygame_gui, pygame
from pygame_gui.windows import UIColourPickerDialog
pygame.init()
class Color:
    def __init__(self, p1, p2, p3, p4, window):
        self.x = p1
        self.y = p2
        self.w = p3
        self.h = p4
        self.colour_picker = None
        self.current_colour = pygame.Color(0,0,0)
        self.window = window
        self.clock = pygame.time.Clock()
        self.rect = pygame.Rect(p1, p2, p3, p4)
    
    def run(self, event, ui): # IT IS CREATING A NEW COLOR WINDOW EVERYTIME YOUPICK A COLOR! FIXX
        if event.type == pygame_gui.UI_COLOUR_PICKER_COLOUR_PICKED:
            self.current_colour = event.colour
            print('picked')
        if (event.type == pygame_gui.UI_WINDOW_CLOSE and event.ui_element == self.colour_picker):
                self.colour_picker = None
        if event.type == pygame.MOUSEBUTTONDOWN:
            mp = pygame.mouse.get_pos()
            if self.rect.collidepoint(mp):
                self.colour_picker = UIColourPickerDialog(pygame.Rect(160, 50, 420, 400), ui, window_title='Change Colour...', initial_colour=self.current_colour)
                print('open')
        pygame.draw.rect(self.window, (255,0,0), self.rect)

        self.update(ui)

    def update(self, ui):
        time_delta = self.clock.tick(60) / 1000.0
        ui.update(time_delta)
        ui.draw_ui(self.window)
        