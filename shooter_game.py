from pygame import *
import random
from time import sleep
win_width=700
win_height=510
window=display.set_mode((win_width,win_height))
display.set_caption("Shooter")
back=image.load('background-1_0.png')
back=transform.scale(back,(win_width,win_height))
clock=time.Clock()
FPS=60

class GameSprite(sprite.Sprite):
    def __init__(self, width,height,picture,x,y,speed):
        super().__init__()
        self.width = width
        self.height = height
        self.image= transform.scale(image.load(picture),(self.width,self.height)) 
        self.rect=self.image.get_rect() 
        self.rect.x=x
        self.rect.y=y
        self.speed=speed
    def reset(self):
        window.blit(self.image,(self.rect.x,self.rect.y))

class Hero(GameSprite):
    def __init__(self, width,height,picture,x,y,speed):
        super().__init__(width,height,picture,x,y,speed)
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x>0:
            self.rect.x-=self.speed
        elif keys[K_d] and self.rect.x+self.width<win_width:
            self.rect.x+=self.speed
    def fire(self):
        global bullets
        global ammo  
        bullet = Bullet(20,20,'bullet.png',self.rect.x+41,self.rect.y,6)
        bullets.add(bullet)
        
            


class Bullet(GameSprite):
    def __init__(self, width,height,picture,x,y,speed):
        super().__init__(width,height,picture,x,y,speed)
    def update(self):
        self.rect.y-=self.speed
        if self.rect.y<0:
            self.kill()
    
class UFO(GameSprite):
    def __init__(self, width,height,picture,x,y,speed):
        super().__init__(width,height,picture,x,y,speed)
    def update(self):
        global skipped,text_skipped
        self.rect.y += self.speed
        if self.rect.y > win_height:
            skipped+=1
            text_skipped=font24.render("SKIPPED:{0}".format(skipped),True,(255,255,255))
            self.rect.y = 0
            self.rect.x = random.randint(0,win_width-self.width)
Rocket = Hero(70,70,'shorgunner.png',325,440,4)
enemies = sprite.Group()
bullets = sprite.Group()

for i in range(7):
    Ufo = UFO(70,70,'plus_zombie.png',random.randint(10,650),30,1)
    enemies.add(Ufo)
killed = 0
skipped = 0
font.init()
font24=font.SysFont('Arial',24)
font23=font.SysFont('Arial',48)
text_killed= font24.render("Ubito:{0}".format(killed),True,(255,255,255))
text_skipped=font24.render("SKIPPED:{0}".format(skipped),True,(255,255,255))
text_lose= font23.render("YOU LOSE!",True,(255,0,0))
text_win= font23.render("YOU WIN!",True,(0,255,0))
game = "in process"
while True:
    if game == "in process":
        window.blit(back,(0,0))
        window.blit(text_killed,(10,20))
        window.blit(text_skipped,(10,50))
    
        enemies.draw(window)
        enemies.update()
        Rocket.reset()
        Rocket.update()
        bullets.draw(window)
        bullets.update()
        hits = sprite.groupcollide(bullets,enemies,True,True)
    
        for i in hits:
            killed+=1
            text_killed= font24.render("Ubito:{0}".format(killed),True,(255,255,255))
            Ufo = UFO(70,70,'plus_zombie.png',random.randint(0,650),30,1)
            enemies.add(Ufo)
        if sprite.spritecollideany(Rocket,enemies):
            quit()
        if killed >= 10:
            game="win"
        if skipped >= 10:
            game="fail"
    elif game == "win":
        window.blit(text_win,(260,250))
        display.update()
    elif game == "fail":
        window.blit(text_lose,(260,250))
        display.update()

    
    for i in event.get():
        if i.type==QUIT:
            quit()
        if i.type==KEYDOWN:
            if i.key==K_l and game == "in process":
                Rocket.fire()
            if i.key==K_SPACE and game != "in process":
                skipped=0
                killed=0
                text_killed= font24.render("Ubito:{0}".format(killed),True,(255,255,255))
                text_skipped=font24.render("SKIPPED:{0}".format(skipped),True,(255,255,255))
                enemies.empty()
                bullets.empty()
                Rocket.rect.x=325
                for i in range(7):
                    Ufo = UFO(70,70,'plus_zombie.png',random.randint(10,650),30,1)
                    enemies.add(Ufo)
                game = "in process"
    display.update()
    clock.tick(FPS)