import pygame as pg

from os.path import join

_ground_path = join("assets", "ground.png")
_cactus_path = join("assets", "cactus.png")


_trex_scale = (40, 40)
_bird_scale = (40, 40)
_cactus_scale = (30, 30)



class _Base(pg.sprite.Sprite):

    def __init__(self, image):
        pg.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()

    def set_position(self, x, y):

        # Change my rectangle

        self.rect.x = x
        self.rect.y = y

class Ground(_Base):

    def __init__(self):
        image = pg.image.load(_ground_path).convert_alpha()
        _Base.__init__(self, image)

class Trex(_Base):

    def __init__(self):
        self.__images = [pg.transform.scale(pg.image.load(join(
            "assets", "t-rex" + str(i) + ".png")).convert_alpha(), _trex_scale) for i in range(1, 6)]
        self.__index = 0
        self.is_alive = True
        self.is_jumping = False
        self.jump_height = 0
        self.did_score = False
        self.score = 0
        _Base.__init__(self, self.__images[self.__index])


    def animate(self):

        if self.__index == len(self.__images):
            self.__index = 0

        self.image = self.__images[self.__index]
        self.__index += 1


class Cactus(_Base):

    def __init__(self):
        image = pg.transform.scale(pg.image.load(_cactus_path).convert_alpha(), _cactus_scale)
        _Base.__init__(self, image)


class Bird(_Base):

    def __init__(self):
        self.images = self.__images = [pg.transform.scale(pg.image.load(join(
            "assets", "bird" + str(i) + ".png")).convert_alpha(), _bird_scale) for i in range(1, 3)]
        self.__index = 0
        self.__counter = 0
        _Base.__init__(self, self.images[self.__index])


    def animate(self):

        self.__counter += 1

        if self.__counter % 5 == 0: # Delay bird flap
            self.__counter = 0
            if self.__index == len(self.__images):
                self.__index = 0

            self.image = self.__images[self.__index]
            self.__index += 1

