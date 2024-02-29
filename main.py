import pygame
import pickle
import time
import math


class Arena:
    def __init__(self):
        self.width = 1500
        self.height = 750
        self.block = 75
        self.__display = self.__create()
        img = pygame.image.load("assets/arena/background.png").convert()
        self.background = pygame.transform.scale(img, (1500, 750))
        self.colour = "green"

    def __create(self):
        pygame.init()
        win = pygame.display.set_mode((self.width, self.height))
        return win

    def get_display(self):
        return self.__display


    def run(self):
        self.__display.blit(self.background, (0, 0))


class Player:
    def __init__(self, arena: Arena):
        self.display = arena.get_display()
        self.colour = "green"
        self.x = 750
        self.y = 375
        self.y_vel = 0
        self.x_vel = 0
        self.ready = True
        self.dashing = False
        self.charge = 100
        self.cost = 20
        self.recharge = 1
        self.x_dash = 0
        self.y_dash = 0
        self.DASH = 50
        self.FRICTION = 1.1

    def __move(self):
        vel = 10
        key = pygame.key.get_pressed()
        if key[pygame.K_UP] or key[pygame.K_w]:
            self.y_vel = vel + self.y_dash
        if key[pygame.K_DOWN] or key[pygame.K_s]:
            self.y_vel = -vel + self.y_dash
        if key[pygame.K_RIGHT] or key[pygame.K_d]:
            self.x_vel = vel + self.x_dash
        if key[pygame.K_LEFT] or key[pygame.K_a]:
            self.x_vel = -vel + self.x_dash
        if self.x_vel or self.y_vel:
            unit = math.sqrt(self.x_vel**2 + self.y_vel**2)
            if self.y_vel:
                self.y -= self.y_vel**2/unit * (math.ceil(self.y_vel)//math.ceil(math.fabs(self.y_vel)))
            if self.x_vel:
                self.x += self.x_vel**2/unit * (math.ceil(self.x_vel)//math.ceil(math.fabs(self.x_vel)))
            self.y_vel /= self.FRICTION
            self.x_vel /= self.FRICTION

    def __dash(self):
        magnitude = math.sqrt(self.x_vel**2 + self.y_vel**2)
        try:
            x_unit = self.x_vel/magnitude
            y_unit = self.y_vel/magnitude
        except ZeroDivisionError:
            x_unit, y_unit = 0, 0

        print((pygame.key.get_pressed()[pygame.K_SPACE]) or "")

        if math.fabs(self.x_dash) < 0.1:
            self.x_dash = 0
        if math.fabs(self.y_dash) < 0.1:
            self.y_dash = 0

        if pygame.key.get_pressed()[pygame.K_SPACE] and self.ready:
            self.colour = "red"
            self.x_dash = x_unit * self.DASH
            self.y_dash = y_unit * self.DASH
            self.charge -= self.cost
            self.ready = False
        if not pygame.key.get_pressed()[pygame.K_SPACE]:
            self.ready = True
            self.colour = "green"
        if self.charge < 100:
            self.charge += self.recharge
        self.x_dash /= self.FRICTION
        self.y_dash /= self.FRICTION

    def __draw(self):
        pygame.draw.circle(self.display, self.colour, (self.x, self.y), 20)

    def run(self):

        self.__move()
        self.__dash()
        self.__draw()


class Enemy:
    def __init__(self, arena: Arena):
        self.display = arena.get_display()
        self.x = 200
        self.y = 200

    def __draw(self):
        pygame.draw.circle(self.display, "red", (self.x, self.y), 10)

    def run(self):
        self.__draw()


class Generator:
    def __init__(self, limit, arena: Arena):
        self.limit = limit
        self.arena = arena
        self.enemies = []

    def __generate(self):
        if len(self.enemies) < self.limit:
            enemy = Enemy(self.arena)
            self.enemies.append(enemy)

    def run(self):
        self.__generate()
        for enemy in self.enemies:
            enemy.run()


def runtime(func):
    def wrapper():
        start = time.time()
        func()
        end = time.time()
        print(f"Runtime: {end-start:.2f} seconds")
    return wrapper


@runtime
def run():
    arena = Arena()
    player = Player(arena)
    generator = Generator(1, arena)
    clock = pygame.time.Clock()

    running = True
    while running:
        clock.tick(60)
        ##
        arena.run()
        player.run()
        generator.run()
        ##
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                running = False


if __name__ == "__main__":
    run()
