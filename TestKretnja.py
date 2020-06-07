import math
import pygame 
import random
from pygame.math import Vector2

screenSize = 500
screen = pygame.display.set_mode((500, 500))

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
    
    def update(self,events,dt):
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
        if self.position.x  > screenSize: 
            self.position.x = -50
        elif self.position.x < -50:
            self.position.x = screenSize
        elif self.position.y > screenSize:
            self.position.y = 0
        elif self.position.y < 0:
            self.position.y = screenSize

        #Pucanje
        if keys[pygame.K_SPACE]:
            if len(self.groups()[0]) < 5:
                self.groups()[0].add(Projectile(self.rect.center, self.direction.normalize()))


class Asteroid(pygame.sprite.Sprite):
    def __init__(self, x,y):
        pygame.sprite.Sprite.__init__(self)
        pos = (x,y)
        self.asteroidImg = pygame.image.load('meteorite.png')
        self.rect = self.asteroidImg.get_rect(center=pos)
        self.angle = random.randint(0,360)
        self.speed = 3 #mozda koristit random vidit cemo
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
        if self.rect.x > screenSize: 
            self.rect.x = -50
        elif self.rect.x < -50:
            self.rect.x = screenSize
        elif self.rect.y > screenSize:
            self.rect.y = -50
        elif self.rect.y < -50:
            self.rect.y = screenSize

    def draw(self,screen):
        screen.blit(self.image, self.rect)

class Projectile(pygame.sprite.Sprite):
    def __init__(self, pos, direction):
        super().__init__()
        self.image = pygame.Surface((8, 8))
        self.image.fill((0, 0, 0))
        self.image.set_colorkey((0, 0, 0))
        pygame.draw.circle(self.image, (255,0,0), (4, 4), 4)
        self.pos = pos
        #self.image = pygame.image.load('circle.png')
        #screen.blit(self.image, pos)
        self.rect = self.image.get_rect(center=pos)
        self.direction = direction
        self.pos = pygame.Vector2(self.rect.center)
        self.speed = 10 

    def update(self, events,dt):
        self.pos -= self.direction * self.speed# vamo bilo dt mogli smo ga skroz izbacit vidit poslje
        self.rect.center = self.pos
        if not pygame.display.get_surface().get_rect().contains(self.rect):
            self.kill()

    def draw(self,screen):
         pygame.draw.circle(self.image, (255,0,0), (4, 4), 4)

#main klasa
def main():
    pygame.init()
    #------------------------------

    #------------------------------
    sprites = pygame.sprite.Group(Player(200, 410))
    player = Player(200, 410)
    playersprite = pygame.sprite.RenderPlain((player))
    #------------------------
    asteroids = pygame.sprite.Group()
    for x in range(5):
        asteroids.add(Asteroid(200 + x*30, 50))
    #------------------------
    clock = pygame.time.Clock()
    dt = 0
    timer = 0
    done = False
    def redraw_window():
        screen.fill((255,255,255))
        playersprite.draw(screen)
        asteroids.draw(screen)
        pygame.display.update()
        

    while not done:
        events = pygame.event.get()
        timer += 0.5
        dt = clock.tick(60)
        for event in events:
            if event.type == pygame.QUIT:
                done = True
        #Asteroid --------------------   
        if timer % 100 == 0:
            asteroids.add(Asteroid(200 + 30,50))
        
        #bullet_hit = pygame.sprite.spritecollide(sprites, asteroids, True)
        hit = pygame.sprite.spritecollide(player, asteroids, True)
        if hit:
            player.helth -= 1
            print('udaren')
            if player.helth < 0:
                print('mrtav')
        #Asteroid

        #sprites.update(dt)
        playersprite.update(events,dt)
        asteroids.update()
        redraw_window()
       # pygame.display.update()

if __name__ == '__main__':
    main()
    pygame.quit()