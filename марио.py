from pygame import *
width=1000
height=700
win = display.set_mode((width,height))
display.set_caption('Mario Brothers')
background = transform.scale(image.load("фон-игры-Марио.png"),(width, height))
clock=time.Clock()
FPS=60
game=True
finish = False
class GS(sprite.Sprite):
    def __init__(self, pl_image, pl_x, pl_y, sp_w, sp_h, speed):
        super().__init__()
        self.image=transform.scale(image.load(pl_image),(sp_w, sp_h))
        self.rect = self.image.get_rect()
        self.rect.x=pl_x
        self.rect.y=pl_y
        self.speed=speed
        self.isJump = False
        self.jumpCount = 10
        self.onground=False
        self.y_vel=0
        self.gravity=0.5
        
    def reset(self):
        win.blit(self.image, (self.rect.x, self.rect.y))
    def update(self, platforms):
        keys_press=key.get_pressed()
        if keys_press[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys_press[K_d] and self.rect.x < width - 80:
            self.rect.x += self.speed
        self.y_vel+=self.gravity
        self.rect.y += self.y_vel
        self.onground = False
        for p in platforms:
            if sprite.collide_rect(self, p) and self.y_vel > 0:
                self.onground=True
                self.rect.bottom = p.rect.top
                self.y_vel=0
                self.isJump = False
                self.jumpCount=10
        if keys_press[K_SPACE] and self.onground:
            self.y_vel=-15
            self.isJump=True

        


class Wall(sprite.Sprite):
    def __init__(self, color_1, wall_x, wall_y, wall_w, wall_h):
        super().__init__()
        self.color_1=color_1
        self.w=wall_w
        self.h=wall_h
        self.image=Surface((self.w, self.h))
        self.image.fill(color_1)
        self.rect = self.image.get_rect()
        self.rect.x = wall_x
        self.rect.y = wall_y
    def draw_wall(self):
        win.blit(self.image, (self.rect.x, self.rect.y))

pl=GS('mario1.png', 0, 530, 80, 80, 10)
w1=Wall((238,118,33), 275, 400, 200, 10)
w2=Wall((238,118,33), 450, 300, 250, 10)
w3=Wall((238,118,33), 150,500, 120, 10)
w4=Wall((238,118,33), 600, 400, 200, 10)
wall=[w1, w2, w3, w4]

floor=Wall((238,118,33), 0, height-95, width, 10)
wall.append(floor)
while game:
    for e in event.get():
        if e.type == QUIT:
            game=False
    if finish != True: 
        win.blit(background, (0, 0))
        for w in wall:
            w.draw_wall()
        if pl.rect.y-60 >= w.rect.y:
            pl.rect.y= w.rect.y
        pl.reset()
        clock.tick(FPS)
        pl.update(wall)
        display.update()
