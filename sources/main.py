import pygame

def Entity(player_longueur, player_largeur, player_image, obstacle_longueur, obstacle_largeur, obstacle_image, final_longueur, final_largeur, final_image):
    class Player:
        def __init__(self, x, y, screen_width, screen_height):
            self.image = pygame.image.load(player_image) 
            self.image = pygame.transform.scale(self.image, (player_longueur, player_largeur))
            self.rect = self.image.get_rect(topleft=(x, y))
            self.speed = 5
            self.gravity = 1
            self.velocity_y = 0
            self.on_ground = False
            self.screen_width = screen_width
            self.screen_height = screen_height

        def apply_gravity(self, obstacles, finals):
            self.velocity_y += self.gravity
            new_rect = self.rect.copy()
            new_rect.y += self.velocity_y

            for obstacle in obstacles:
                if new_rect.colliderect(obstacle.rect):
                    if self.velocity_y > 0:
                        self.rect.bottom = obstacle.rect.top
                        self.velocity_y = 0
                        self.on_ground = True
                    elif self.velocity_y < 0:
                        self.rect.top = obstacle.rect.bottom
                        self.velocity_y = 0
                    return

            for final in finals:
                if new_rect.colliderect(final.rect):
                    print("Vous avez gagné")
                    pygame.quit()
                    exit()

            self.on_ground = False
            self.rect.y += self.velocity_y

            if self.rect.bottom > self.screen_height:
                print("Vous êtes mort")
                pygame.quit()
                exit()

            if self.rect.top < 0:
                self.rect.top = 0
                self.velocity_y = 0

        def jump(self):
            if self.on_ground:
                self.velocity_y = -15
                self.on_ground = False

        def move(self, keys, obstacles, finals):
            new_rect = self.rect.copy()

            if keys[pygame.K_LEFT]:
                new_rect.x -= self.speed
            if keys[pygame.K_RIGHT]:
                new_rect.x += self.speed
            if keys[pygame.K_UP]:
                self.jump()

            if not any(new_rect.colliderect(obstacle.rect) for obstacle in obstacles):
                self.rect.x = new_rect.x

            if self.rect.left < 0:
                self.rect.left = 0
            if self.rect.right > self.screen_width:
                self.rect.right = self.screen_width

            self.apply_gravity(obstacles, finals)

    class Obstacle:
        def __init__(self, x, y):
            self.image = pygame.image.load(obstacle_image) 
            self.image = pygame.transform.scale(self.image, (obstacle_longueur, obstacle_largeur))
            self.rect = self.image.get_rect(topleft=(x, y))

    class Final:
        def __init__(self, x, y):
            self.image = pygame.image.load(final_image)
            self.image = pygame.transform.scale(self.image, (final_longueur, final_largeur))
            self.rect = self.image.get_rect(topleft=(x, y))

    return Player, Obstacle, Final

def Game(longueur, largeur, background_image, nom, num_players, player_positions, num_obstacles, obstacle_positions, num_finals, final_positions,
         player_longueur, player_largeur, player_image, 
         obstacle_longueur, obstacle_largeur, obstacle_image,
         final_longueur, final_largeur, final_image):
    pygame.init()
    
    if len(obstacle_positions) < num_obstacles:
        raise ValueError("Le nombre de positions fournies est inférieur au nombre d'obstacles spécifié.")
    if len(player_positions) < num_players:
        raise ValueError("Le nombre de positions fournies est inférieur au nombre de joueurs spécifié.")
    if len(final_positions) < num_finals:
        raise ValueError("Le nombre de positions fournies est inférieur au nombre de finales spécifié.")
    
    Player, Obstacle, Final = Entity(player_longueur, player_largeur, player_image, 
                                     obstacle_longueur, obstacle_largeur, obstacle_image,
                                     final_longueur, final_largeur, final_image)

    players = [Player(x, y, longueur, largeur) for x, y in player_positions[:num_players]]
    obstacles = [Obstacle(x, y) for x, y in obstacle_positions[:num_obstacles]]
    finals = [Final(x, y) for x, y in final_positions[:num_finals]]

    fond = pygame.image.load(background_image)
    fond = pygame.transform.scale(fond, (longueur, largeur))
    
    pygame.display.set_caption(nom)
    screen = pygame.display.set_mode((longueur, largeur))
    
    run = True
    clock = pygame.time.Clock()

    while run:
        screen.blit(fond, (0, 0))

        for player in players:
            screen.blit(player.image, player.rect.topleft)
        for obstacle in obstacles:
            screen.blit(obstacle.image, obstacle.rect.topleft)
        for final in finals:
            screen.blit(final.image, final.rect.topleft)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()
        for player in players:
            player.move(keys, obstacles, finals)

        clock.tick(60)
    
    pygame.quit()

Game(
    1920, 1080, "exemples/assets/sky.jpg", "Scène1", num_players=1, 
    player_positions=[(300, 200)],
    num_obstacles=3,
    obstacle_positions=[(300, 500), (700, 600), (1000, 700)],
    num_finals=1,
    final_positions=[(1050, 550)],
    player_longueur=100, player_largeur=100, player_image="exemples/assets/chevalier.png",
    obstacle_longueur=200, obstacle_largeur=100, obstacle_image="exemples/assets/grass.jpg",
    final_longueur=150, final_largeur=150, final_image="exemples/assets/porte.png"
)
