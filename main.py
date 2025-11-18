import pygame
from pygame.locals import *
import random as r
pygame.init()
 
clock = pygame.time.Clock()
font = pygame.font.SysFont('Bauhaus 93' , 40)
colour = (255, 165, 0)
def draw_text(text , font , text_colour , x , y):
    img = font.render(text , True , text_colour)
    screen.blit(img,(x,y))

def reset():
    score = 0 
    paravai.rect.x = 120
    paravai.rect.y = int(Height/2)
    paravai.gravity = 0
    
    pipe_group.empty()
    return score

class Bird(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0
        for i in range(1,4):
            img = pygame.image.load(f'bird{i}.png')
            self.images.append(img)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
        self.gravity = 0
        self.pressed = 0

    def update(self):
        keys = pygame.key.get_pressed()   

        # fly up
        
        if keys[pygame.K_SPACE] and self.pressed == 0:
            self.pressed = 1
            self.gravity = -9

        if not keys[pygame.K_SPACE]:
            self.pressed = 0

        #gravity
        if flying == 1:
            self.gravity+=0.5
            if self.gravity>9:
                self.gravity = 9
            self.rect.y += int(self.gravity)
            if self.rect.bottom >=490:
                self.rect.bottom = 490
        
        #animation
        if gameover == 0:
            self.counter += 1
            cooldown = 6
            if self.counter > cooldown:
                self.counter = 0
                self.index += 1
                if(self.index >= len(self.images)):
                        self.index = 0
            self.image = self.images[self.index]
            
            #rotation
            
            self.image = pygame.transform.rotate(self.images[self.index] , self.gravity * -2)
        else:
            self.image = pygame.transform.rotate(self.images[self.index] , -80)


class Pipe(pygame.sprite.Sprite):
    def __init__(self,x,y,pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('pipe.png')
        self.rect = self.image.get_rect()
        #position 1 for top and -1 for bottom
        if pos == 1:
            self.image = pygame.transform.flip(self.image , False , True)
            self.rect.bottomleft = [x, y - int(pipe_gap / 2)]
        if pos == -1:
            self.rect.topleft = [x, y + int(pipe_gap / 2)]
    def update(self):
        if(gameover == 0):
            self.rect.x -= move_speed
        if self.rect.right < 0:
            self.kill()


class Button():
    def __init__(self,x,y,image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
    
    def draw(self):
        action  = False
        if pygame.key.get_pressed()[pygame.K_RETURN] or pygame.key.get_pressed()[pygame.K_SPACE]:
            action = True
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                action = True

        screen.blit(self.image, (self.rect.x,self.rect.y))
        return action
    
#variables

scoreflag = False
score = 0
pass_pipe = False 
FPS = 60
flying = 0
gameover = 0
Width = 800
Height = 600
ground_pos = 0 
move_speed = 3
pipe_gap = 150
time_gap = 1500
last_pipe = pygame.time.get_ticks() - time_gap
#special
fh = open("highscore.txt" , "r")
highscore = int(fh.read())
fh.close()

#apply
fend = pygame.image.load('end.jpg')
end = pygame.transform.scale(fend , (300,200))
bg = pygame.image.load('BG.png')
ground = pygame.image.load('Ground.png')
button_img = pygame.image.load('restart.png')
screen = pygame.display.set_mode((Width , Height))
pygame.display.set_caption('Vaaga guys')

#characters group

bird_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()

paravai = Bird(120 , int(Height/2))
bird_group.add(paravai)
button = Button((Width // 2)-10, 400 , button_img)

#runner

run = True
while run:
    clock.tick(FPS)

    screen.blit(bg,(0,0))
    bird_group.draw(screen)
    bird_group.update()
    pipe_group.draw(screen)
    screen.blit(ground,(ground_pos,490))
    screen.blit(ground , (ground_pos + Width , 490))
    if ground_pos <= -Width:
        ground_pos = 0
    
    
    #score

    if len(pipe_group) > 0:
        if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left\
        and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right\
        and pass_pipe == False:
            pass_pipe = True
        if pass_pipe == True:
            if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
                score+=1
                pass_pipe = False
    
    draw_text("SCORE: "+str(score) , font , colour , 200 , 30)
    draw_text("MAX: "+str(highscore) , font , colour, 450 ,30)

    #gameover

    if pygame.sprite.groupcollide(bird_group,pipe_group , False,False) or paravai.rect.top <= 0:
        gameover = 1
    if paravai.rect.bottom >= 490:
        gameover = 1
        flying = 0
    if gameover ==0 and flying ==0:
        draw_text("PRESS SPACE TO START" , font , (225,225,225), 185 ,500)
    if gameover == 0 and flying == 1:
        time_now = pygame.time.get_ticks()
        if time_now - last_pipe > time_gap:
            pipe_height = r.randint(-180,60)
            pipe_btm = Pipe(Width,int(Height/2) +pipe_height, -1)
            pipe_top = Pipe(Width,int(Height/2) +pipe_height, 1)
            pipe_group.add(pipe_btm)
            pipe_group.add(pipe_top)
            last_pipe = time_now
        ground_pos -= move_speed
        pipe_group.update()
    if score>highscore:
        highscore = score
        scoreflag=True
    if gameover==1:
        screen.blit(end,((Width/2) - 150,(Height/2) -185))

        if scoreflag:
            fh = open("highscore.txt","w")
            fh.write(str(highscore))
            fh.close()

        if button.draw() == True :
            gameover = 0
            score = reset()


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if  event.key == pygame.K_SPACE and flying == 0 and gameover == 0:
                flying = 1

    pygame.display.update()
pygame.quit()
