import pygame

class DropDown():

    def __init__(self, color_menu, color_option, x, y, w, h, font, main, options, game):
        self.color_menu = color_menu
        self.color_option = color_option
        self.rect = pygame.Rect(x, y, w, h)
        self.w = w
        self.h = h
        self.y = y
        self.x = x
        self.font = font
        self.main = main
        self.orig = main
        self.options = options
        self.draw_menu = False
        self.menu_active = False
        self.active_option = -1
        self.game = game
        self.menu_open = False

    def draw(self, surf, drops = []):
        self.rect[1] = self.y
        for dropdown in drops:
            if dropdown.menu_open:
                self.rect[1] += len(dropdown.options) * (dropdown.rect[3]+2)
        pygame.draw.rect(surf, self.color_menu[self.menu_active], self.rect, 0, border_radius=12)
        surf.blit(self.game.emoji, pygame.Rect(self.rect[0]+self.w-15, self.rect[1]+(self.h/2)-6, self.rect[2], self.rect[3]))
        msg = self.font.render(self.main, 1, (0, 0, 0))
        surf.blit(msg, msg.get_rect(center = self.rect.center))

        if self.orig == "Normal":
            pos111 = msg.get_rect(center = self.rect.center)
            pos111[0] += self.w
            surf.blit(self.font.render(" In development (don't use)", 1, (0, 0, 0)), pos111)
        if self.draw_menu:
            for i, text in enumerate(self.options):
                rect = self.rect.copy()
                rect.y += (i+1) * (self.rect.height+2)
                pygame.draw.rect(surf, self.color_option[1 if i == self.active_option else 0], rect, 0,  border_radius=12)
                msg = self.font.render(text, 1, (0, 0, 0))
                surf.blit(msg, msg.get_rect(center = rect.center))

    def update(self, event, resolution):
        if self.game.fullScreen:
            mpos = (pygame.mouse.get_pos()[0]/(self.game.monitor_size[0]/320), pygame.mouse.get_pos()[1]/(self.game.monitor_size[1]/240))
        else:
            mpos = (pygame.mouse.get_pos()[0]/(resolution[0]/320), pygame.mouse.get_pos()[1]/(resolution[1]/240))
        self.menu_active = self.rect.collidepoint(mpos)
        
        self.active_option = -1
        for i in range(len(self.options)):
            rect = self.rect.copy()
            rect.y += (i+1) * self.rect.height
            if rect.collidepoint(mpos):
                self.active_option = i
                break

        if not self.menu_active and self.active_option == -1:
            self.draw_menu = False
            self.menu_open = False

        # print(event_list)
        
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.menu_active:
                self.menu_open= not self.menu_open
                self.draw_menu = not self.draw_menu
            elif self.draw_menu and self.active_option >= 0:
                self.draw_menu = False
                return self.active_option
        return -1