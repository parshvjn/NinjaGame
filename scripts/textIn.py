import pygame

class tInput:
    def __init__(self, c1, c2, x, y, w, h, surf, index, game, droph, fontSize):
        self.surf = surf
        self.nActive = c1
        self.yActive = c2
        self.inputR = pygame.Rect(x, y, w, h)
        self.inputR[1] += index*(droph+2)
        self.droph = droph
        self.color = self.nActive
        self.font = pygame.font.Font(None, fontSize)
        self.user_text = ""
        self.active = False
        self.game = game
        self.text_surface = self.font.render(self.user_text, True, (255,255,255))
    
    def draw(self):
        pygame.draw.rect(self.surf, self.color, self.inputR, 2, border_radius=12)

        self.text_surface = self.font.render(self.user_text, True, (255,255,255))
        self.surf.blit(self.text_surface, (self.inputR[0] + 5, self.inputR[1] + 5))
    
    def update(self, event, resolution, addItem = 0):
        if addItem != 0:
            self.inputR[1] += addItem*(self.droph+2)
        else:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mpos = (pygame.mouse.get_pos()[0]/(resolution[0]/320), pygame.mouse.get_pos()[1]/(resolution[1]/240))
                if self.inputR.collidepoint(mpos): self.active = True
                else: self.active = False
            if event.type == pygame.KEYDOWN:
                if self.active and event.unicode.isdigit() or self.active and event.key == pygame.K_BACKSPACE:
                    if event.key == pygame.K_BACKSPACE:
                        self.user_text = self.user_text[:-1]
                    elif len(self.user_text)<=3:
                        self.user_text += event.unicode
            if self.active: self.color = self.yActive
            else: self.color = self.nActive