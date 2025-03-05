import pygame

class Entity:
    def __init__(self, x, y):
        self.image = pygame.image.load("exemples/assets/chevalier.png") 
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = 5 
        self.gravity = 1  # Intensité de la gravité
        self.velocity_y = 0  # Vitesse verticale
        self.on_ground = False  # Vérification si le joueur est au sol

    def apply_gravity(self, obstacles):
        self.velocity_y += self.gravity
        new_rect = self.rect.copy()
        new_rect.y += self.velocity_y

        for obstacle in obstacles:
            if new_rect.colliderect(obstacle.rect):
                if self.velocity_y > 0:  # Si on tombe
                    self.rect.bottom = obstacle.rect.top
                    self.velocity_y = 0
                    self.on_ground = True
                elif self.velocity_y < 0:  # Si on monte
                    self.rect.top = obstacle.rect.bottom
                    self.velocity_y = 0
                return
        
        self.on_ground = False
        self.rect.y += self.velocity_y

    def jump(self):
        if self.on_ground:
            self.velocity_y = -15  # Force du saut
            self.on_ground = False

    def move(self, keys, obstacles):
        new_rect = self.rect.copy()
        
        if keys[pygame.K_LEFT]:
            new_rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            new_rect.x += self.speed
        if keys[pygame.K_SPACE]:  # Sauter
            self.jump()
        
        if not any(new_rect.colliderect(obstacle.rect) for obstacle in obstacles):
            self.rect.x = new_rect.x

        self.apply_gravity(obstacles)

# Fonction pour afficher l'arrière-plan et gérer le jeu
def Background(longueur, largeur, image, name):
    pygame.init()

    fond = pygame.image.load(image)
    fond = pygame.transform.scale(fond, (longueur, largeur))

    pygame.display.set_caption(name)
    screen = pygame.display.set_mode((longueur, largeur))

    player = Entity(200, 200)
    ground = Entity(0, 600)  # Sol pour que le joueur puisse marcher
    ground.image = pygame.Surface((longueur,50 ))  # Création d'un sol simple
    ground.image.fill((0, 255, 0))  # Coloration du sol
    ground.rect = ground.image.get_rect(topleft=(0, 1000))

    run = True
    clock = pygame.time.Clock()

    while run:
        screen.blit(fond, (0, 0))
        screen.blit(player.image, player.rect.topleft)
        screen.blit(ground.image, ground.rect.topleft)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()
        player.move(keys, [ground])

        clock.tick(60)

    pygame.quit()

Background(1920, 1080, "exemples/assets/header.jpg", "Scène1")
