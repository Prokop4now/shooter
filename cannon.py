import random as rnd
import math
import pygame

from my_colors import *

FPS = 30
GRAVITY_ACCELERATION = 9.8  # Ускорение свободного падения для снаряда.
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600


class Cannon:
    max_velocity = 10

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.shell_num = None  # TODO: оставшееся на данный момент количество снарядов
        self.direction = math.pi / 4
        self.color = "WHITE"
        self.r = 20
        self.length_gun = 50

    def aim(self, x, y):
        if x > self.x:
            self.direction = math.atan((y - self.y) / (x - self.x))
        if x < self.x:
            self.direction = math.atan((y - self.y) / (x - self.x)) + math.pi

        if x == self.x and y < self.y:
            self.direction = -math.pi / 2
        if x == self.x and y > self.y:
            self.direction = math.pi / 2

        """
        Меняет направление direction так, чтобы он из точки
         (self.x, self.y) указывал в точку (x, y).
        :param x: координата x, в которую целимся
        :param y: координата y, в которую целимся
        :return: None
        """
        # TODO
        # return self.direction

    def fire(self, dt):
        """
        Создаёт объект снаряда (если ещё не потрачены все снаряды)
        летящий в направлении угла direction
        со скоростью, зависящей от длительности клика мышки
        :param dt:  длительность клика мышки, мс
        :return: экземпляр снаряда типа Shell
        """


    def draw(self):
        pygame.draw.circle(screen, self.color,
                           (int(round(self.x)), int(round(self.y))), self.r)

        pygame.draw.line(screen, self.color, [self.x, self.y], [self.x + self.length_gun * math.cos(self.direction),
                                                                self.y + self.length_gun * math.sin(self.direction)],
                         width=7)

    def cannon_move(self, motion):
        if motion == 'LEFT':
            self.x -= 4

        elif motion == 'RIGHT':
            self.x += 4

        elif motion == 'UP':
            self.y -= 4

        elif motion == 'DOWN':
            self.y += 4

        elif motion == 'LEFT_UP':
            self.y -= 3
            self.x -= 3

        elif motion == 'RIGHT_UP':
            self.x += 3
            self.y -= 3

        elif motion == 'LEFT_DOWN':
            self.x -= 3
            self.y += 3

        elif motion == 'RIGHT_DOWN':
            self.x += 4
            self.y += 4




class Shell(Cannon):
    standard_radius = 3

    def __init__(self, x, y, x1, y1):
        #if x1 > x:
        super().__init__(x1, y1)
        self.direction = math.atan((y - y1) / (x - x1))  # угол направления полета пули

        # if x1 < x:
        #     self.direction = (math.atan((y - y1) / (x - y1)) + math.pi)  # угол направления полета пули
        # if x1 == self.x:
        #     self.direction = math.pi / 2
        self.x = x + math.cos(self.direction)
        self.y = y + math.sin(self.direction)

        #     if x2 > x:
        #         self.x, self.y = x + 50 * math.sin(math.atan((y - y2) / (x - x2))), y + 50 * math.cos(math.atan((y - y2) / (x - x2)))
        #     if x2 < x:
        #         self.x, self.y = x + 50 * math.sin(math.pi-math.atan(y - y2) / (x - x2)), y + 50 * math.cos(
        #             math.atan(math.pi-(y - y2) / (x - x2)))

        self.Vx, self.Vy = 10, 10
        self.r = Shell.standard_radius
        self.color = 'black'

    def move(self, dt):
        """
        Сдвигает снаряд исходя из его кинематических характеристик
        и длины кванта времени dt
        в новое положение, а также меняет его скорость.
        :param dt:
        :return:
        """
        # ax, ay = 0, GRAVITY_ACCELERATION
        self.x += self.Vx * math.cos(self.direction)  # + ax * (dt ** 2) / 2
        self.y += self.Vy * math.sin(self.direction)  # + ay * (dt ** 2) / 2
        # self.Vx += ax * dt
        # self.Vy += ay * dt
        # TODO: Уничтожать (в статус deleted) снаряд, когда он касается земли.

    def draw(self):
        pygame.draw.circle(screen, self.color,
                           (int(round(self.x)), int(round(self.y))), self.r)

    def detect_collision(self, other):
        """
        Проверяет факт соприкосновения снаряда и объекта other
        :param other: объект, который должен иметь поля x, y, r
        :return: логическое значение типа bool
        """
        length = ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5
        return length <= self.r + other.r


class Target:
    standard_radius = 15

    def __init__(self, x, y, Vx, Vy):
        self.x, self.y = x, y
        self.Vx, self.Vy = Vx, Vy
        self.r = Target.standard_radius
        self.color = COLORS[rnd.randint(0, len(COLORS) - 1)]

    def move(self, dt):
        """
        Сдвигает шарик-мишень исходя из его кинематических характеристик
        и длины кванта времени dt
        в новое положение, а также меняет его скорость.
        :param dt:
            :return:
        """
        ax, ay = 0, GRAVITY_ACCELERATION
        self.x += self.Vx * dt
        self.y += self.Vy * dt
        self.Vx += ax * dt
        self.Vy += ay * dt
        # TODO: Шарики-мишени должны отражаться от стенок

    def draw(self):
        pygame.draw.circle(screen, self.color,
                           (int(round(self.x)), int(round(self.y))), self.r)

    def collide(self, other):
        """
        Расчёт абсолютно упругого соударения
        :param other:
        :return:
        """
        pass  # TODO


class Bomb:
    pass


def generate_random_targets(number: int):
    targets = []
    for i in range(number):
        x = rnd.randint(0, SCREEN_HEIGHT)
        y = rnd.randint(0, SCREEN_HEIGHT)
        Vx = rnd.randint(-30, +30)
        Vy = rnd.randint(-30, +30)
        target = Target(x, y, Vx, Vy)
        targets.append(target)
    return targets


def game_main_loop():
    global direct
    queue = []
    mv = 0  # направление движения пушки пр нажатии клавиш движения
    targets = generate_random_targets(10)
    clock = pygame.time.Clock()
    finished = False
    gun = Cannon(300, 300)

    while not finished:
        dt = clock.tick(FPS) / 1000
        print(dt)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
            elif event.type == pygame.MOUSEMOTION:
                x, y = pygame.mouse.get_pos()
                gun.aim(x, y)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                print('Click!')
                queue.append(Shell(gun.x, gun.y, x, y))

            keys = pygame.key.get_pressed()
            if keys[pygame.K_a] and keys[pygame.K_w]:
                mv = 'LEFT_UP'
            elif keys[pygame.K_d] and keys[pygame.K_w]:
                mv = 'RIGHT_UP'
            elif keys[pygame.K_a] and keys[pygame.K_s]:
                mv = 'LEFT_DOWN'
            elif keys[pygame.K_d] and keys[pygame.K_s]:
                mv = 'RIGHT_DOWN'
            elif keys[pygame.K_a]:
                mv = 'LEFT'
            elif keys[pygame.K_w]:
                mv = 'UP'
            elif keys[pygame.K_s]:
                mv = 'DOWN'
            elif keys[pygame.K_d]:
                mv = 'RIGHT'

            else:
                mv = 0

        gun.cannon_move(mv)
        gun.draw()

        for bullets in queue:
            bullets.draw()

            bullets.move(3)

        pygame.display.update()
        screen.fill('GRAY')

        for target in targets:
            target.move(dt)

        for target in targets:
            target.draw()

    pygame.quit()


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.update()

    game_main_loop()
