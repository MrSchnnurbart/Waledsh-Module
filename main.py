import pygame

class Entity:
    def __init__(self, x, y):
        self.image = pygame.image.load("exemples/assets/chevalier.png") 
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = 5 

    def move(self, keys, obstacles):
        """Gère les déplacements du joueur en fonction des touches pressées et des collisions"""
        new_rect = self.rect.copy()

        if keys[pygame.K_LEFT]:
            new_rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            new_rect.x += self.speed
        if keys[pygame.K_UP]:
            new_rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            new_rect.y += self.speed

        if not any(new_rect.colliderect(obstacle.rect) for obstacle in obstacles):
            self.rect = new_rect

# Fonction pour afficher l'arrière-plan et gérer le jeu
def Background(longueur, largeur, image, name):
    pygame.init()

    # Charger et redimensionner l'image de fond
    fond = pygame.image.load(image)
    fond = pygame.transform.scale(fond, (longueur, largeur))

    pygame.display.set_caption(name)
    screen = pygame.display.set_mode((longueur, largeur))

    # Création du personnage jouable
    player = Entity(200, 200)  # Position de départ
    obstacle = Entity(500, 500)  # Position de l'obstacle

    run = True
    clock = pygame.time.Clock()

    while run:
        screen.blit(fond, (0, 0))  # Dessiner l'arrière-plan
        screen.blit(player.image, player.rect.topleft)  # Dessiner le joueur
        screen.blit(obstacle.image, obstacle.rect.topleft)  # Dessiner l'obstacle

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # Gestion des mouvements du joueur avec détection des collisions
        keys = pygame.key.get_pressed()
        player.move(keys, [obstacle])  # Vérifie si le joueur entre en collision avec l'obstacle

        clock.tick(60)  # Limite le jeu à 60 FPS

    pygame.quit()

# Lancer la fenêtre de jeu
Background(1920, 1080, "exemples/assets/header.jpg", "Scène1")