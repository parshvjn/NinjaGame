import pygame
def palette_swap(surf, old_c, new_c, img):
    img_copy = pygame.Surface(img.get_size())
    img_copy.fill(new_c)
    # surf.set_colorkey(old_c)
    img_copy.blit(surf, (0, 0))
    return img_copy