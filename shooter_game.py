#Создай собственный Шутер!

from pygame import *
from random import *
font.init()
font = font.Font(None, 70)

mixer.init()
window = display.set_mode((700, 500))
display.set_caption('Шутер')
background = transform.scale(image.load('galaxy.jpg'), (700, 500))
clock = time.Clock()
FPS = 60
aimmo = 20
cooldown = 3
class GameSprite(sprite.Sprite):
    skip = 0
    point = 0
    def __init__(self, paint, skale, speed, x, y,):
        super().__init__()
        self.image = transform.scale(image.load(paint), skale)
        self.rect = self.image.get_rect()
        self.speed = speed
        self.rect.x = x
        self.rect.y = y

    def otobrazi(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_d] and self.rect.x < 595:
            self.rect.x += self.speed
        if keys_pressed[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed

class Enemy(GameSprite):
    def __init__(self, paint, skale, speed, x, y):
        super().__init__(paint, skale, speed, x, y)
        self.count = 0

    def update(self):
        self.rect.y += self.speed
        #self.count += 1
        #if self.count >= self.speed:
        #   self.rect.y += self.speed * 3
        #   self.count = 0

        if self.rect.y > 500:
            self.rect.y = 0
            self.rect.x = randint(20, 620)
            self.speed = randint(1, 5)
            GameSprite.skip += 1


class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

class asteroidi(GameSprite):
    def update(self):
        self.rect.y += self.speed

        if self.rect.y < 0:
            self.kill() 

        if self.rect.y > 500:
            self.rect.y = 0
            self.rect.x = randint(20, 620)
            self.speed = randint(1, 10)

player = Player('rocket.png', (100, 100), 5, 300, 390)
win = font.render('YOU WIN!', True, (50, 205, 50))
lose = font.render('LOSE', True, (255, 0, 0))


monsters = sprite.Group()
bullets = sprite.Group()
asteroids = sprite.Group()
for i in range(5):
    monster = Enemy('ufo.png', (80, 80), randint(1, 5), randint(20, 620), randint(-100, 0))
    monsters.add(monster)

for i in range(3):
    asteroid = asteroidi('asteroid.png', (80, 80), randint(1,10), randint(20,620),0)
    asteroids.add(asteroid)

mixer.music.load('space.ogg')
mixer.music.play()
fire = mixer.Sound('fire.ogg')

game = True
finish = False
loose = False
wyn = False
reload = False

while game:
    keys_pressed = key.get_pressed()
    points = font.render(f'Счёт: {GameSprite.point}' , True, (50, 205, 50))
    skips = font.render(f'Пропущено: {GameSprite.skip}', True, (255, 0, 0))
    window.blit(background, (0, 0))
    window.blit(points, (20,30))
    window.blit(skips, (20,70))
    
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE and aimmo > 0:
                bullet = Bullet('bullet.png',(20,50), 6, player.rect.x + 45, player.rect.y )
                bullets.add(bullet)
                fire.play()
                aimmo -= 1
                podojdi = FPS * cooldown
    if aimmo <= 0:
        
        podojdi -= 1
        if podojdi <= 0:
            aimmo = 20



    if not finish:
        player.update()
        player.otobrazi()
    
        asteroids.draw(window)
        asteroids.update()

        monsters.update()
        monsters.draw(window) 

        bullets.draw(window)
        bullets.update()

        collides = sprite.groupcollide(bullets, monsters, True, True)
        for collide in collides:
            GameSprite.point += 1
            monster = Enemy('ufo.png', (80, 80), randint(1, 5), randint(20, 620), randint(-100, 0))
            monsters.add(monster)
        
        if sprite.spritecollide(player, monsters, False) or GameSprite.skip >= 3:
            finish = True
            loose = True
        if GameSprite.point >= 10:
            finish = True
            wyn = True        
        if sprite.spritecollide(player, asteroids, False):
            finish = True
            loose = True
        
        
    if loose:
        window.blit(lose, (275,210))
    if wyn:
        window.blit(win, (200,200))

    clock.tick(FPS)
    display.update()
