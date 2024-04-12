import pygame
class Slider:
    def __init__(self, x, y, w, h, min, max, fontSize, window, text, fColor, boxColor, circleColor):
        self.x, self.y, self.w, self.h = x, y, w, h
        self.min, self.max = min, max
        self.val = self.min
        self.valx = self.x
        self.font = pygame.font.Font("../data/fonts/Retro Gaming.ttf", fontSize)
        self.window = window
        self.text = text
        self.fx, self.fy = self.x, self.y - fontSize - 5
        self.fColor = fColor
        self.cursorC, self.boxC = circleColor, boxColor

    def set_val(self, val):
        self.val = val
        self.valx = self.x + self.w*(self.val/(self.max-self.min))

    def update(self, mx, my, mp):
        if mp:
            if pygame.Rect(self.x, self.y, self.w, self.h).collidepoint((mx, my)):
                   self.val = ((mx - self.x)/self.w)*(self.max-self.min)+self.min
                   self.valx = mx

        pygame.draw.rect(window, self.boxC, (self.x+self.h/2, self.y, self.w-self.h, self.h), 0)
        pygame.draw.circle(window, self.boxC, (self.x+self.h/2, self.y+self.h/2), self.h/2)
        pygame.draw.circle(window, self.boxC, (self.x+self.w-self.h/2, self.y+self.h/2), self.h/2)
        pygame.draw.circle(window, self.cursorC, (self.valx, self.y+self.h/2), self.h/2)

        self.window.blit(self.font.render(f"{self.text}: {round(self.val, 0)}", False, self.fColor), (self.fx, self.fy))

pygame.init()
sliders = []
window = pygame.display.set_mode((800,800))
sliders.append(Slider(100, 200, 400, 15, 0, 100000, 40, window, "Nums", (255,0,0), (0,255,0), (255,255,255)))
sliders[0].set_val(2.9)

# sliders[1].set_val(3)
# sliders[2].set_val(1.25)
# sliders[3].set_val(1.0)
# sliders[4].set_val(0)
running = True
while running:
    window.fill((0,0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            running = False
    
    mx, my = pygame.mouse.get_pos()
    mp = pygame.mouse.get_pressed()[0]

    for slider in sliders:
        slider.update(mx, my, mp)
    
    pygame.display.update()