#!/usr/bin/python3.4
# Setup Python ----------------------------------------------- #
import pygame, sys, random
import scripts.cloth as cloth

# Setup pygame/window ---------------------------------------- #
mainClock = pygame.time.Clock()
from pygame.locals import *
pygame.init()
pygame.display.set_caption('cloth?')
screen = pygame.display.set_mode((500, 500),0,32)

rag_data = cloth.load_rags('data/rags')

my_cloth = cloth.ClothObj(rag_data['vine'])
my_cloth1 = cloth.ClothObj(rag_data['vine'])

render_mode = 0

# Loop ------------------------------------------------------- #
while True:

    # Background --------------------------------------------- #
    screen.fill((0,0,0))

    # Cloth -------------------------------------------------- #

    # move

    my_cloth.move_grounded([100, 100])

    # process
    my_cloth.update()
    my_cloth.update_sticks()
    my_cloth1.move_grounded([100, 200])

    # process
    my_cloth1.update(random.randint(1,3)/100)
    my_cloth1.update_sticks()


    # render
    if render_mode:
        my_cloth.render_polygon(screen, (255, 255, 255))
        my_cloth1.render_polygon(screen, (255, 255, 255))
    else:
        my_cloth.render_sticks(screen)
        my_cloth1.render_sticks(screen)

    # Buttons ------------------------------------------------ #
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()

            if event.key == K_r:
                if render_mode:
                    render_mode = 0
                else:
                    render_mode = 1

    # Update ------------------------------------------------- #
    pygame.display.update()
    mainClock.tick(60)
