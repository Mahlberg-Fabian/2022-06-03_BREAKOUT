from pygame.constants import (
    KEYDOWN, K_LEFT
)
import pygame               # imports
import random
import time
import os


pygame.init()

class Settings(pygame.sprite.Sprite):
    sw = 800                    # Fenstergröße
    sh = 800
    fps = 60

    bg = pygame.image.load('images/background.jpg')        # Hintergrund
    win = pygame.display.set_mode((sw, sh)) 
    pygame.display.set_caption("Breakout")           
 
    brickHitSound = pygame.mixer.Sound("bullet.wav")
    bounceSound = pygame.mixer.Sound("hitGameSound.wav")
    failSound = pygame.mixer.Sound("fail.mp3")
    siegSound = pygame.mixer.Sound("sieg.mp3")
    backgroundmusik = pygame.mixer.Sound("background.mp3")
    backgroundmusik.play()
    bounceSound.set_volume(.1)
    backgroundmusik.set_volume(0.075)


    clock = pygame.time.Clock()

    gameover = False


class Globals:
    points = 0          # Punktevariable auf 0 gesetzt
    soundlaenge = 1


class Paddle(pygame.sprite.Sprite):                                   # Spieler
    def __init__(self, x, y, w, h, color):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.color = color
        self.xx = self.x + self.w
        self.yy = self.y + self.h

    def draw(self, win):
        pygame.draw.rect(win, self.color, [self.x, self.y, self.w, self.h])


class Ball(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, color):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.color = color
        self.xv = random.choice([2, 3, 4, -2, -3, -4])          # Ball Geschwindigkeit
        self.yv = random.randint(3, 4)
        self.xx = self.x + self.w
        self.yy = self.y + self.h

    def draw(self, win):
        pygame.draw.rect(win, self.color, [self.x, self.y, self.w, self.h])


    def move(self):
        self.x += self.xv
        self.y += self.yv

class Brick(pygame.sprite.Sprite):                 # Balken oben
    def __init__(self, x, y, w, h, color):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.color = color
        self.visible = True
        self.xx = self.x + self.w
        self.yy = self.y + self.h

        self.ranNum = random.randint(0, 10)
        if self.ranNum < 3:
            self.pregnant = True
        else:
            self.pregnant = False



    def draw(self, win):
        pygame.draw.rect(win, self.color, [self.x, self.y, self.w, self.h])


bricks = []
def init():
    global bricks
    bricks = []
    for i in range(6):
        for j in range(10):
            bricks.append(Brick(10 + j * 79, 50 + i * 35, 70, 25, (120, 205, 250)))      # Abstand der Balken


def redrawGameWindow():    # Game wird geblittet
    Settings.win.blit(Settings.bg, (0,0))
    player.draw(Settings.win)
    for ball in balls:
        ball.draw(Settings.win)
    for b in bricks:
        b.draw(Settings.win)

    font = pygame.font.SysFont('ComicSans', 50)
    
    if Settings.gameover:
        if len(bricks) == 0:    # wenn keine Balken mehr übrig sind
            resText = font.render("Du hast GEWONNEN! sehr gut!", 1, (124,252,0))
        else:
            resText = font.render("VERLOREN", 1, 	(255,0,0))
        Settings.win.blit(resText, ((Settings.sw//2 - resText.get_width()//2), Settings.sh//2 - resText.get_height()//2))
        playAgainText = font.render("Drück LEERTASTE zum neustarten", 1, (255, 165, 0))
        Settings.win.blit(playAgainText, ((Settings.sw//2 - playAgainText.get_width()//2),Settings.sh//2 + 30))
#        text = font.render(Globals.points, True, (0, 255, 0))
#        textRect = text.get_rect()
        
        



    pygame.display.update()


player = Paddle(Settings.sw/2 - 50, Settings.sh - 100, 140, 20, (0, 255, 100))
ball = Ball(Settings.sw/2 - 10, Settings.sh - 400, 20, 20, (255, 255, 255))
balls = [ball]


init()
run = True
while run:
    Settings.clock.tick(150)
    if not Settings.gameover:
        for ball in balls:
            ball.move()

        if pygame.mouse.get_pos()[0] - player.w//2 < 0:
            player.x = 0
        elif pygame.mouse.get_pos()[0] + player.w//2 > Settings.sw:     # Balken kann nicht aus
            player.x = Settings.sw - player.w                           # dem Bildschirmrand
        else:
            player.x = pygame.mouse.get_pos()[0] - player.w //2
        
        


        for ball in balls:
            if (ball.x >= player.x and ball.x <= player.x + player.w) or (ball.x + ball.w >= player.x and ball.x + ball.w <= player.x + player.w):
                if ball.y + ball.h >= player.y and ball.y + ball.h <= player.y + player.h:            # Kollisionsprüfung mit Balken
                    ball.yv *= -1
                    ball.y = player.y - ball.h - 1     # fix -> Ball stuck in Ecke
                    Settings.bounceSound.play()
                    Globals.points += 1
                  # self.font_bigsize.render(f"Score: {Globals.points}", True, (0, 136, 255))
                  # self.screen.blit(text, (0, 10))
                  # pygame.display.flip()


            if ball.x + ball.w >= Settings.sw:
                Settings.bounceSound.play()
                ball.xv *= -1
            if ball.x < 0:
                Settings.bounceSound.play()                    # Kollisionsprüfung mit Spielseiten
                ball.xv *= -1
            if ball.y <= 0:
                Settings.bounceSound.play()
                ball.yv *= -1

            if ball.y > Settings.sh:
                balls.pop(balls.index(ball))
            



        for brick in bricks:
            for ball in balls:
                if (ball.x >= brick.x and ball.x <= brick.x + brick.w) or ball.x + ball.w >= brick.x and ball.x + ball.w <= brick.x + brick.w:
                    if (ball.y >= brick.y and ball.y <= brick.y + brick.h) or ball.y + ball.h <= brick.y + brick.h:
                        brick.visible = False                                                     # Kollision mit Balken
                        if brick.pregnant:
                            balls.append(Ball(brick.x, brick.y, 20, 20, (255, 255, 255)))
                        #  bricks.pop(bricks.index(brick))
                        ball.yv *= -1
                        Settings.brickHitSound.play()
                        break


        for brick in bricks:
            if brick.visible == False:
                bricks.pop(bricks.index(brick))
        




        if len(balls) == 0:
            Settings.gameover = True
            Settings.failSound.play()      
        
        



    keys = pygame.key.get_pressed()
    if len(bricks) == 0:
        won = True
        Settings.gameover = True
        Settings.siegSound.play()
        pygame.time.Clock.tick(100)
        #pygame.mixer.siegSound.play(0)
            #Settings.siegSound + 1
        

    if Settings.gameover:
        if keys[pygame.K_SPACE]:
            Settings.gameover = False
            won = False
            ball = Ball(Settings.sw/2 - 10, Settings.sh - 400, 20, 20, (255, 255, 255))
            if len(balls) == 0:       # Wenn Liste von Bällen leer ist, dann neuen Ball appenden
                balls.append(ball)

            bricks.clear()
            for i in range(6):
                for j in range(10):
                    bricks.append(Brick(10 + j * 79, 50 + i * 35, 70, 25, (120, 205, 250)))



    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

            

    redrawGameWindow()


pygame.quit()

if __name__ == '__main__':
    os.environ['SDL_VIDEO_WINDOW_POS'] = "450, 40"



# Quellen
# background:  https://www.pexels.com/de-de/foto/gradient-multicolor-hintergrund-mit-farbverlauf-7130558/
# Video:       https://www.youtube.com/watch?v=DLptMaCxllI

# Sound Effekte:
# Failsound: https://www.youtube.com/watch?v=hckIjL7z5z4
# Siegsound: https://www.youtube.com/watch?v=y4AxbbbUKRo


