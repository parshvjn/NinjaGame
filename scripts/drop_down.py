import pygame
from scripts.textIn import tInput

class DropDown():

    def __init__(self, color_menu, color_option, x, y, w, h, font, main, options, game, textInputIndexList = []):
        self.color_menu = color_menu
        self.color_option = color_option
        self.rect = pygame.Rect(x, y, w, h)
        self.rectText = self.rect
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
        self.tInputs = []
        self.extraPadding = 0
        self.paddingRight = 0
        self.msgCenter = None
        if textInputIndexList != []:
            for item in textInputIndexList:
                self.tInputs.append(tInput((0,0,0), (255,255,255), item[1][0], item[1][1], item[1][2], item[1][3], self.game.display, item[0], self.game, self.h, item[1][3]))
                


    def draw(self, surf, drops = []):
        self.rect[1] = self.y
        for dropdown in drops:
            if dropdown.menu_open:
                self.rect[1] += len(dropdown.options) * (dropdown.rect[3]+2)+dropdown.extraPadding
        pygame.draw.rect(surf, self.color_menu[self.menu_active], self.rect, 0, border_radius=12)
        surf.blit(self.game.emoji, pygame.Rect(self.rect[0]+self.w-15, self.rect[1]+(self.h/2)-6, self.rect[2], self.rect[3]))
        msg = self.font.render(self.main, 1, (0, 0, 0))
        surf.blit(msg, msg.get_rect(center = self.rect.center))


        if self.orig == "Normal":
            pos111 = msg.get_rect(center = self.rect.center)
            pos111[0] += self.w
            surf.blit(self.font.render(" In development (don't use)", 1, (0, 0, 0)), pos111)
        if self.orig == "640x480":
            pos112 = msg.get_rect(center = self.rect.center)
            pos112[0] += self.w
            surf.blit(self.font.render("Click F for full screen", 1, (0, 0, 0)), pos112)

        if self.draw_menu:
            for i, text in enumerate(self.options):
                rect = self.rect.copy()
                rect.y += (i+1) * (self.rect.height+2)
                self.msgCenter = rect.copy()
                if text == "Custom":
                    self.paddingRight = 33
                    rect.h *= 2
                    rect.w += self.paddingRight
                    self.msgCenter.w += self.paddingRight
                    self.extraPadding = rect.h/2
                    self.msgCenter.h /= 2

                pygame.draw.rect(surf, self.color_option[1 if i == self.active_option else 0], rect, 0,  border_radius=12)
                msg = self.font.render(text, 1, (0, 0, 0))
                surf.blit(msg, msg.get_rect(center = self.msgCenter.center))
                if text == "Custom":
                    if len(self.options) != 6:
                        msg = self.font.render("x", 1, (0, 0, 0))
                        surf.blit(msg, (64, 65+(i*(self.h+2))))
                    else:
                        msg = self.font.render("MAX", 1, (255, 0, 0) if self.options[self.active_option]!="Custom" else "#475F77")
                        surf.blit(msg, (64, 65+(i*(self.h+2))))
                        pos113 = msg.get_rect(center = rect.center)
                        pos114 = msg.get_rect(center = rect.center)
                        pos113[0] += self.w
                        pos114[0] += self.w
                        pos114[1]+= self.game.font_size
                        surf.blit(self.font.render("Hover Over a size you made and", 1, (0, 0, 0)), pos113)
                        surf.blit(self.font.render(" click d to remove (not defualt ones)", 1, (0, 0, 0)), pos114)
            for input in self.tInputs:
                if len(self.options) != 6:
                    input.draw()

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
            if i == len(self.options)-1 and self.orig == "640x480": # not going in this, fix conditions
                rect[3] *= 2
                rect[2] += self.paddingRight
                if rect.collidepoint(mpos):
                    self.active_option = i
                    break
            else:
                if rect.collidepoint(mpos):
                    self.active_option = i
                    break

        if not self.menu_active and self.active_option == -1:
            self.draw_menu = False
            self.menu_open = False
            for input in self.tInputs:
                input.active = False
                input.user_text = ""

        
        if self.draw_menu:
            for input in self.tInputs:
                input.update(event,resolution)

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.menu_active:
                # print(self.options[self.active_option])
                self.menu_open= not self.menu_open
                self.draw_menu = not self.draw_menu
            elif self.draw_menu and self.active_option >= 0:
                if self.options[self.active_option] != 'Custom':
                    self.draw_menu = False
                    return self.active_option
        
        if event.type == pygame.KEYDOWN and event.key == 13:
                if self.options[self.active_option] == 'Custom':
                    sizes = []
                    duplicate = False
                    for input in self.tInputs:
                        sizes.append(input.user_text)
                        input.active = False
                        input.user_text = ""
                    for option in self.options:
                        if option == sizes[0] + "x" + sizes[1]:
                            duplicate = True
                        if sizes[0] == "" or sizes[1] == "":
                            duplicate = True
                    if not duplicate:
                        self.options.insert(-1, sizes[0] + "x" + sizes[1])
                        for input in self.tInputs:
                            input.update(None, None, 1)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_d:
            if self.orig == "640x480" and self.options[self.active_option] != 'Custom' and self.active_option not in [0, 1, 2]:
                self.options.pop(self.active_option)
                for input in self.tInputs:
                    input.update(None, None, -1)

        return -1