import pygame,sys

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((800,800))
font = pygame.font.Font(None, 32)
user_text = ''

inputR = pygame.Rect(200, 200, 140, 32)
color = pygame.Color('lightskyblue3')
color1 = pygame.Color('gray15')
currentColor = color1

active = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if inputR.collidepoint(event.pos): active = True
            else: active = False
        if event.type == pygame.KEYDOWN:
            if active:
                if event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]
                else:
                    user_text += event.unicode
    
    screen.fill((0,0,0))

    if active: currentColor = color
    else: currentColor = color1
    print(currentColor)

    pygame.draw.rect(screen, currentColor, inputR, 2)

    text_surface = font.render(user_text, True, (255,255,255))
    screen.blit(text_surface, (inputR.x + 5, inputR.y + 5))

    inputR.w = max(100, text_surface.get_width() + 10)

    pygame.display.update()

    clock.tick(60)