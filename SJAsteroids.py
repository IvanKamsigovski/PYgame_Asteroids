import math
import pygame 
import random
from pygame.math import Vector2

pygame.init()
screenwidth= 800
screenheight = 600
screen = pygame.display.set_mode((800, 600))

def calculate_new_xy( old_xy, speed, direction):
        new_x = old_xy[0] + (speed*math.cos(direction))
        new_y = old_xy[1] + (speed*math.sin(direction))
        return new_x, new_y

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y ):
        super(Player, self).__init__()
        self.image = pygame.image.load('spaceship.png')
        pos = (x, y)
        self.x = x
        self.y = y
        screen.blit(self.image, (self.x,self.y))
        self.border = 5
        self.orginalImg = self.image
        self.rect = self.image.get_rect(center=pos)
        self.position = Vector2(pos)
        self.direction = Vector2(0,1)
        self.speed = 0
        self.angle_speed = 0
        self.angle = 0
        self.helth = 2
    
    def update(self,events):
        if self.angle_speed != 0:
            #Rotacija vektora smjera pa slike
            self.direction.rotate_ip(self.angle_speed)
            self.angle += self.angle_speed
            self.image = pygame.transform.rotate(self.orginalImg, -self.angle)
            self.rect = self.image.get_rect(center=self.rect.center)
        #Updatamo vektor i rect
        self.position -= self.direction *self.speed
        self.rect.center = self.position
        keys = pygame.key.get_pressed()

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.speed += 1
                elif event.key == pygame.K_DOWN:
                    self.speed -= 1
                elif event.key == pygame.K_LEFT:
                    self.angle_speed = -4
                elif event.key == pygame.K_RIGHT:
                    self.angle_speed = 4
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.angle_speed = 0
                elif event.key == pygame.K_RIGHT:
                    self.angle_speed = 0
        
        #Border
        if self.position.x  > screenwidth: 
            self.position.x = -50
        elif self.position.x < -50:
            self.position.x = screenwidth
        elif self.position.y > screenheight:
            self.position.y = 0
        elif self.position.y < 0:
            self.position.y = screenheight

        #Shooting
        if keys[pygame.K_SPACE]:
            if len(self.groups()[0]) < 3:
                self.groups()[0].add(Projectile(self.rect.center, self.direction.normalize()))

    def draw_heart(self,screen):
        self.heartImg = pygame.image.load('heart.png')
        if self.helth == 2:
            screen.blit(self.heartImg, (10,10))
            screen.blit(self.heartImg, (30,10))
            screen.blit(self.heartImg, (50,10))
        elif self.helth == 1:
            screen.blit(self.heartImg, (10,10))
            screen.blit(self.heartImg, (30,10))
        elif self.helth == 0:
            screen.blit(self.heartImg, (10,10))


class Asteroid(pygame.sprite.Sprite):
    def __init__(self, x,y):
        pygame.sprite.Sprite.__init__(self)
        pos = (x,y)
        self.asteroidImg = pygame.image.load('meteorite.png')
        self.rect = self.asteroidImg.get_rect(center=pos)
        self.angle = random.randint(0,360)
        self.speed = 3 
        self.direction = math.radians(random.randint(0,360))

    def update(self):
        self.angle -= 3 % 360
        self.image = pygame.transform.rotate(self.asteroidImg, self.angle*-1)

        posX, posY = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = (posX,posY)

        #Move asteroid
        self.rect.center = calculate_new_xy(self.rect.center, self.speed, self.direction)
        
        #Border
        if self.rect.x > screenwidth: 
            self.rect.x = -50
        elif self.rect.x < -50:
            self.rect.x = screenwidth
        elif self.rect.y > screenheight:
            self.rect.y = -50
        elif self.rect.y < -50:
            self.rect.y = screenheight

    def draw(self,screen):
        screen.blit(self.image, self.rect)


class Projectile(pygame.sprite.Sprite):
    def __init__(self, pos, direction):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((8, 8))
        self.image.fill((0, 0, 0))
        self.image.set_colorkey((255, 255, 255))
        pygame.draw.circle(self.image, (0,0,0), (4, 4), 6)
        self.pos = pos
        self.rect = self.image.get_rect(center=pos)
        self.direction = direction
        self.pos = pygame.Vector2(self.rect.center)
        self.speed = 10
        self.lifetime = 0.0 

    def update(self, events):
        self.pos -= self.direction * self.speed
        self.rect.center = self.pos
        self.lifetime += 1
        if self.lifetime > 70:
            self.kill()
        if not pygame.display.get_surface().get_rect().contains(self.rect):
            self.kill()
            
#Funkcije

#main 
def main():
    sprites = pygame.sprite.Group(Player(400, 410))
    player = Player(400, 410)
    playersprite = pygame.sprite.RenderPlain((player))
    #------------------------
    asteroids = pygame.sprite.Group()
    for x in range(5):
        asteroids.add(Asteroid(400 + x*30, 50))
    #------------------------
    clock = pygame.time.Clock()
    score = 0
    font = pygame.font.SysFont('comicsans', 30, True, True)
    dt = 0
    timer = 0
    done = False
    def redraw_window():
        screen.fill((255,255,255))
        text = font.render('Score: ' + str(score), 1, (0,0,0))
        player.draw_heart(screen)
        screen.blit(text, (380,10))
        playersprite.draw(screen)
        asteroids.draw(screen)
        pygame.display.update()


    while not done:
        events = pygame.event.get()
        timer += 0.5
        dt = clock.tick(60)
        for event in events:
            if event.type == pygame.QUIT:
                #done = True
                quit()

        #Asteroid --------------------   
        if timer % 20 == 0:
            asteroids.add(Asteroid(200 + 30,50))
        
        hit = pygame.sprite.spritecollide(player, asteroids, True)
        if hit:
            player.helth -= 1
            print('udaren')
            if player.helth < 0:
                end_menu(score)
                print('mrtav')
        #Asteroid

        #Collision za metak ----------------------------
        bullets = player.groups()[0]

        hitBullet = pygame.sprite.groupcollide(asteroids, bullets, True,True)
        if hitBullet:
            score += 10
        #---------------------------------

        playersprite.update(events)
        asteroids.update()
        redraw_window()

#Menu funkcije
def main_menu():
    title_font = pygame.font.SysFont('comicsans', 50)
    run = True
    while run:
        screen.fill((255,255,255))
        title_label = title_font.render("Press the mouse to begin...", 1, (0,0,0))
        screen.blit(title_label, (screenwidth/2 -title_label.get_width()/2, 250))

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                main()
    
    pygame.quit()

def end_menu(score):
    score_font = pygame.font.SysFont('comicsans', 50)
    endgame_font = pygame.font.SysFont('comicsans', 40)
    run = True
    while run:
        screen.fill((255,255,255))
        score_label = score_font.render("Score: " + str(score), 1, (0,0,0))
        endgame_label = endgame_font.render("You died press mouse to repeat...", 1, (0,0,0))
        screen.blit(score_label, (screenwidth/2 -score_label.get_width()/2, 100))
        screen.blit(endgame_label, (screenwidth/2 -endgame_label.get_width()/2, 250))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                main()
    
    pygame.quit()


main_menu()
