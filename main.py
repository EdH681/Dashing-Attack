import pygame
import pickle
import time
import math


class Arena:
    def __init__(self):
        self.width = 1500
        self.height = 750
        self.block = 75
        self.grid = get_grid()
        self.__display = self.__create()

    def __create(self):
        pygame.init()
        win = pygame.display.set_mode((self.width, self.height))
        return win

    def __draw(self):
        for r, row in enumerate(self.grid):
            for c, col in enumerate(row):
                if col == 1:
                    pygame.draw.rect(self.__display, "white", (c*75, r*75, self.block, self.block))

    def get_display(self):
        return self.__display

    def run(self):
        self.__draw()


class Player:
    def __init__(self, display):
        self.display = display
        self.x = 750
        self.y = 375
        self.y_vel = 0
        self.x_vel = 0
        self.FRICTION = 1.1

    def __move(self):
        vel = 10
        key = pygame.key.get_pressed()
        if key[pygame.K_UP]:
            self.y_vel = vel
        if key[pygame.K_DOWN]:
            self.y_vel = -vel
        if key[pygame.K_RIGHT]:
            self.x_vel = vel
        if key[pygame.K_LEFT]:
            self.x_vel = -vel
        if self.x_vel or self.y_vel:
            unit = math.sqrt(self.x_vel**2 + self.y_vel**2)
            if self.y_vel:
                self.y -= self.y_vel**2/unit * (math.ceil(self.y_vel)//math.ceil(math.fabs(self.y_vel)))
            if self.x_vel:
                self.x += self.x_vel**2/unit * (math.ceil(self.x_vel)//math.ceil(math.fabs(self.x_vel)))
            self.y_vel /= self.FRICTION
            self.x_vel /= self.FRICTION

    def __draw(self):
        pygame.draw.circle(self.display, "green", (self.x, self.y), 20)

    def run(self):
        self.__move()
        self.__draw()


def get_grid():
    with open("arena", "rb")as get:
        data = pickle.load(get)
    return data


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
    win = arena.get_display()
    player = Player(win)

    clock = pygame.time.Clock()

    running = True
    while running:
        clock.tick(60)
        win.fill("black")
        ##
        arena.run()
        player.run()
        ##
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                running = False


if __name__ == "__main__":
    run()
