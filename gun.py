import math
from random import choice
from random import randint


import pygame


FPS = 30

RED = 0xFF0000
BLUE = 0x0000FF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = (0, 0, 0)
WHITE = 0xFFFFFF
GREY = 0x7D7D7D
GAME_COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

WIDTH = 800
HEIGHT = 600


class Ball:
    def __init__(self, screen: pygame.Surface, x, y):
        """ Конструктор класса ball

        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.screen = screen
        self.x = x
        self.y = y
        self.r = 10
        self.vx = 0
        self.vy = 0
        self.color = choice(GAME_COLORS)
        self.live = 30

    def move(self, WIDTH, HEIGHT):
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
        # FIXME
        #print(self.vx, self.vx)
        if self.x - self.r <= 0:
            self.vx = abs(self.vx)
        if self.x + self.r >= WIDTH:
            #print(1)
            self.vx = -abs(self.vx)
        if self.y - self.r + self.vy>= HEIGHT:
            #print(2)
            self.vy = - abs(self.vy)
        if self.y + self.r + self.vy <= 0:
            #print('smksmf')
            self.vy = abs(self.vy)
        self.vy = self.vy + 3
        self.x += self.vx
        self.y += self.vy

    def draw(self):
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )

    def hittest(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """

        # FIXME
        if (self.x - obj.x)**2 + (self.y - obj.y)**2 <= (self.r + obj.r)**2:
            return True
        else:
            return False


class Gun:
    def __init__(self, screen):
        self.screen = screen
        self.f2_power = 50
        self.f2_on = 0
        self.an = 1
        self.color = GREY
        self.x = 25
        self.y = 500
        self.bx = 0
        self.by = 0

    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls, bullet
        bullet += 1
        new_ball = Ball(self.screen, self.bx, self.by)
        new_ball.r += 5
        #self.an = math.atan2((event.pos[1]-new_ball.y), (event.pos[0]-new_ball.x))
        new_ball.vx = self.f2_power * math.cos(self.an)
        new_ball.vy =  self.f2_power * math.sin(self.an)
        balls.append(new_ball)
        self.f2_on = 0
        #self.f2_power = 10

    def targetting(self, event):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            self.an = math.atan((event.pos[1] - self.y - 13) / (event.pos[0] - self.x + 132//2))
        if self.f2_on:
            self.color = RED
        else:
            self.color = GREY

    def draw(self):
        self.l = 100
        self.nx = self.l * math.cos(self.an)
        self.ny = self.l * math.sin(self.an)
        self.bx = self.x + 132 // 2 + self.nx
        self.by = self.y + 33 + self.ny

        #FIXIT don't know how to do it
        pygame.draw.rect(self.screen, (96, 3, 3), (self.x, self.y, 132, 30))
        pygame.draw.circle(self.screen, BLACK, (self.x + 37//2, self.y + 30 + 37//2), 37//2)
        pygame.draw.circle(self.screen, BLACK, (self.x + 132 - 37 // 2, self.y + 30 + 37//2),  37 // 2)
        pygame.draw.circle(self.screen, GREY, (self.x + 132//2, self.y - 13), 40//2)
        pygame.draw.line(self.screen, GREY, [self.x + 132//2, self.y - 13], [self.bx, self.by], 23)

    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            self.color = RED
        else:
            self.color = GREY


class Target:
    def __init__(self, screen):
        self.screen = screen
        self.points = 0
        self.live = 1
    # FIXME: don't work!!! How to call this functions when object is created?
        self.new_target()

    def new_target(self):
        """ Инициализация новой цели. """
        self.x = randint(100, 750)
        self.y = randint(50, 350)
        self.r = randint(2, 50)
        self.color = RED
        self.live = 1

    def hit(self, points=1):
        """Попадание шарика в цель."""
        self.points += points

    def draw(self):
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )
class TextObject:
    def __init__(self, screen):
        self.screen = screen
        self.field = pygame.font.Font(None, 36)

    def GetText(self, scores):
        self.scores = scores
        self.text = 'Scores: ' + str(self.scores)
        self.ren = self.field.render(self.text, True, BLACK)
        self.screen.blit(self.ren, (0,0))

pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
bullet = 0
balls = []

clock = pygame.time.Clock()
gun = Gun(screen)
target = Target(screen)
text = TextObject(screen)
finished = False

while not finished:
    #print(balls)
    screen.fill(WHITE)
    gun.draw()
    target.draw()
    text.GetText(target.points)

    for b in balls:
        b.draw()
    pygame.display.update()

    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            gun.fire2_start(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            gun.fire2_end(event)
        elif event.type == pygame.MOUSEMOTION:
            gun.targetting(event)

    for b in balls:
        b.move(WIDTH, HEIGHT)
        if b.y > 1.3 * HEIGHT:
            balls.remove(b)
        #print(balls)
        #print(b.x, b.y)
        #print(b.hittest(target), target.live)
        if b.hittest(target) and target.live:
            target.live = 0
            target.hit()
            target.new_target()
            print(target.points)
    gun.power_up()

pygame.quit()
