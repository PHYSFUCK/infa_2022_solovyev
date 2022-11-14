import pygame
from pygame.draw import *
from random import randint
pygame.init()

FPS = 60
width = 800
height = 600
screen = pygame.display.set_mode((width, height))

RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

class Ball:
    def __init__(self, screen):
        '''рисует новый шарик '''
        self.screen = screen
        self.x = randint(100, width-100)
        self.y = randint(100, height-100)
        self.r = randint(10, 70)
        self.color = COLORS[randint(0, 5)]
        self.max_speed = 5
        self.vx = randint(-self.max_speed, self.max_speed)
        self.vy = randint(-self.max_speed, self.max_speed)
        self.life_time = 180

    def draw_ball(self):
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.r)

    def move(self):
        self.x += self.vx
        self.y += self.vy
        if self.x - self.r + self.vx <= 0:
            self.vx = abs(self.vx)
        if self.x + self.r + self.vx >= width:
            #print(1)
            self.vx = -abs(self.vx)
        if self.y + self.r + self.vy >= height:
            #print(2)
            self.vy = - abs(self.vy)
        if self.y - self.r + self.vy <= 0:
            #print('smksmf')
            self.vy = abs(self.vy)

    def catch(self, event):
        mx = event.pos[0]
        my = event.pos[1]
        #print((mx - (self.x + self.vx))**2 + (my - (self.y + self.vy))**2, self.r**2)
        if (mx - (self.x + self.vx))**2 + (my - (self.y + self.vy))**2 <= self.r**2:
            return True
        else:
            return False

class TextObject:
    def __init__(self, screen):
        self.screen = screen
        self.field = pygame.font.Font(None, 36)

    def GetText(self, scores, x, y, text):
        self.scores = scores
        self.x = x
        self.y = y
        self.text = text + str(self.scores)
        self.ren = self.field.render(self.text, True, WHITE)
        self.screen.blit(self.ren, (self.x, self.y))

    def RecordResult(self, out, points, time):
        print('Хотите записать ваш результат?')
        print('Y - Да', 'N - Нет')
        if input() == 'Y':
            print('Введите ваше Имя')
            name = input()
            d = {}
            with open(out, 'r') as f:

                for line in f.readlines():
                    print(line)
                    if line.rstrip() != 'Leaderboard':
                        l = line.split()
                        d[l[0]] = int(l[2])
            #print(d)
            if name not in d:
                d[name] = points
            else:
                if points > d[name]:
                    d[name] = points
            s_d = sorted(d, key = lambda x: d[x])[::-1]
            #print(d)
            with open(out, 'w') as f:
                f.write('Leaderboard' + '\n')
                for p in s_d:
                    #print(p, type(p))
                    #print(d[p], type(d[p]))
                    #print(p + ' Score: ' + str(d[p]) + '\n')
                    f.write(p + ' Score: ' + str(d[p]) + '\n')


pygame.font.init()
clock = pygame.time.Clock()
finished = False
time = 0
balls = []
points = 0
text = TextObject(screen)
full_time = 0

while not finished:
    clock.tick(FPS)
    screen.fill('BLACK')
    full_time += 1
    time += 1
    text.GetText(points, 0, 0, 'Scores: ')
    if time == 60 or len(balls) == 0:
        ball = Ball(screen)
        balls.append(ball)
        time = 0
    for b in balls:
        if b.life_time > 0:
            b.draw_ball()
            b.life_time -= 1
        else:
            balls.remove(b)
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:

            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            #print(45)
            for b in balls:
                if b.catch(event):

                    points += 1
                    print(points)
                    balls.remove(b)
    for b in balls:
        b.move()


pygame.quit()
text.RecordResult('output.txt', points, full_time)