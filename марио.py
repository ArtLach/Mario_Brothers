from pygame import *

width = 1000
height = 700
win = display.set_mode((width, height))
display.set_caption('Mario Brothers')
background = transform.scale(image.load("фон-игры-Марио.png"), (width, height))
clock = time.Clock()
FPS = 60
game = True
finish = False

class GS(sprite.Sprite):
    def __init__(self, pl_image, pl_x, pl_y, sp_w, sp_h, speed):
        super().__init__()
        self.image = transform.scale(image.load(pl_image), (sp_w, sp_h))
        self.rect = self.image.get_rect()
        self.rect.x = pl_x
        self.rect.y = pl_y
        self.speed = speed
        self.isJump = False
        self.onground = False
        self.y_vel = 0
        self.gravity = 0.55
        self.prev_y = pl_y
        
    def reset(self):
        win.blit(self.image, (self.rect.x, self.rect.y))
    
    def update(self, platforms):
        self.prev_y = self.rect.y
        keys_press = key.get_pressed()
        if keys_press[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys_press[K_d] and self.rect.x < width - 80:
            self.rect.x += self.speed

        self.y_vel += self.gravity
        self.rect.y += self.y_vel
        self.onground = False
        for p in platforms:
            if sprite.collide_rect(self, p):
                if self.y_vel > 0 and self.rect.bottom > p.rect.top and self.prev_y + self.rect.height <= p.rect.top:
                    self.rect.bottom = p.rect.top
                    self.onground = True
                    self.y_vel = 0
                elif self.y_vel < 0 and self.rect.top < p.rect.bottom:
                    self.rect.top = p.rect.bottom
                    self.y_vel = 0
                elif self.rect.right > p.rect.left and self.rect.left < p.rect.left:
                    self.rect.right = p.rect.left
                elif self.rect.left < p.rect.right and self.rect.right > p.rect.right:
                    self.rect.left = p.rect.right
        
        if keys_press[K_SPACE] and self.onground:
            self.y_vel = -15

class Wall(sprite.Sprite):
    def __init__(self, wall_image, wall_x, wall_y, sp_w, sp_h):
        super().__init__()
        self.image = transform.scale(image.load(wall_image), (sp_w, sp_h))
        self.rect = self.image.get_rect()
        self.rect.x = wall_x
        self.rect.y = wall_y
    
    def draw_wall(self):
        win.blit(self.image, (self.rect.x, self.rect.y))


pl = GS('mario1.png', 0, height-170, 80, 80, 10)
floor = Wall('ground_block.png', 0, height-90, width, 700)
blocks = [
    Wall('блок.jpg', 200, height-260, 60, 60),
    Wall('блок.jpg', 260, height-260, 60, 60),
    Wall('блок.jpg', 320, height-260, 60, 60),
    Wall('блок.jpg', 430, height-340, 60, 60),
    Wall('блок.jpg', 490, height-340, 60, 60),
    Wall('блок.jpg', 550, height-340, 60, 60),
    Wall('блок.jpg', 700, height-150, 60, 60),
    Wall('блок.jpg', 700, height-210, 60, 60),
    Wall('блок.jpg', 700, height-270, 60, 60)
]

wall = [floor] + blocks
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
    
    if not finish: 
        win.blit(background, (0, 0))
        
        for w in wall:
            w.draw_wall()
        pl.reset()
        pl.update(wall)
        display.update()
        clock.tick(FPS)
