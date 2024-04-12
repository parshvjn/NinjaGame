import pygame, sys, random
from fireClass import FireManager
from hearts.heartClass import HeartSystem
from colorDialogClass import Color
import pygame_gui
from pygame_gui.elements import UIButton
from pygame_gui.windows import UIColourPickerDialog

WINDOW_HEIGHT = 1000
window = pygame.display.set_mode((1280,WINDOW_HEIGHT))
ui_manager = pygame_gui.UIManager(window.get_size())
firesurf = pygame.Surface((1280, WINDOW_HEIGHT))
clock = pygame.time.Clock()

fire = FireManager(100, 100, firesurf, False) # change the surface to one of the display surfaces you used in the game already, don't make another one
fire2 = FireManager(200, 200, firesurf)
hearts = HeartSystem(8,8, firesurf)
color = Color(100, 100, 300, 300, firesurf)
fireOn = False
running = True
while running:
    window.fill((0,0,0))
    firesurf.fill((0,0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            sys.exit()
        ui_manager.process_events(event)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                fireOn = True
            if event.key == pygame.K_UP:
                hearts.get_health()
            if event.key == pygame.K_DOWN:
                hearts.get_damage()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                fireOn = False

    color.run(event, ui_manager)
    if fireOn: fire.attack(True)
    else: fire.attack(False)
    fire2.attack(None)
    fire.update(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], 2)
    fire2.update(500, 500, 1)
    hearts.update()

    window.blit(pygame.transform.scale(firesurf, (1280, WINDOW_HEIGHT)), (0, 0))
    pygame.display.update()
    clock.tick(60)

pygame.quit()