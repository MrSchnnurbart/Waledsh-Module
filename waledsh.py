import pygame
pygame.init

def window(longueur, largeur, background, name):
    run = True
    fond = pygame.image.load(background)
    fond = pygame.transform.scale(fond, (longueur, largeur))
    pygame.display.set_caption(name)
    screen = pygame.display.set_mode((longueur, largeur))
    while run:
        screen.blit(fond, (0, 0))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False