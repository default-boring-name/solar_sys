import pygame as pg
from solar_obj import Objects


class COLORS:
    TRANSPARENT = (255, 255, 255, 0),
    BLACK = (0, 0, 0),
    WHITE = (255, 255, 255),
    GREY = (200, 200, 200),
    RED = (255, 0, 0),
    GREEN = (0, 255, 0),
    BLUE = (0, 0, 255),
    YELLOW = (255, 255, 0),
    CYAN = (0, 255, 255),
    MAGENTA = (255, 0, 255)
    ALL = [
        TRANSPARENT,
        BLACK,
        WHITE,
        GREY,
        RED,
        GREEN,
        BLUE,
        YELLOW,
        CYAN,
        MAGENTA
    ]


class Screen:
    '''
    Класс экрана, на котором будет отрисовываться
    некоторая сцена
    '''

    def __init__(self, size, bg_color=COLORS.TRANSPARENT):
        '''
        Функция для инициализации экрана
        :param size: словарь вида {"w", "h"}, размеры экрана
        :param bg_color: цвет из COLORS, цвет заднего фона экрана
                         (заливка), по умолчания он прозрачный
        '''

        self.size = dict(size)
        self.bg_color = bg_color
        self.surf = pg.Surface((self.size["w"], self.size["h"]),
                               pg.SRCALPHA)
        self.to_draw_list = []

    def update(self):
        '''
        Функция, которая перерисовывате экран
        (делает заливку bg_color и поочереди отрисовывает
        все обЪекты, содержащиеся в списке для отрисовки)
        '''

        self.surf.fill(self.bg_color)
        for obj in self.to_draw_list:
            obj.draw()

    def add_obj(self, obj):
        '''
        Функция, добавляющая переданный объект в список
        для отрисовки, если его там еще не было
        :param obj: обЪект, который нужно добавить в
                    список для отрисовки (обязательно должен
                    иметь метод draw() для отрисовки и метод
                    set_screen примающий объект Screen)
        '''

        if obj not in self.to_draw_list:
            self.to_draw_list.append(obj)

    def remove_obj(self, obj):
        '''
        Функция, исключающая переданный объект из списка
        для отрисовки (если он там был)
        :param obj: объект, который будет исключен из
                    списка для отрисовки
        '''

        if obj in self.to_draw_list:
            self.to_draw_list.remove(obj)

    def get_surface(self):
        '''
        Функция, возвращающая основную поверхность для рисования
        '''

        return self.surf


class MainScreen(Screen):
    '''
    Класс главного экрана приложения
    '''

    def __init__(self, size, bg_color=COLORS.WHITE):
        '''
        Функция для инициализации главного экрана приложения
        :param size: словарь вида {"w", "h"}, размеры экрана
        :param bg_color: цвет из COLORS, цвет заднего фона экрана
                         (заливка), по умолчания он белый
        '''

        super().__init__(size, bg_color)
        self.surf = pg.display.set_mode((self.size["w"],
                                         self.size["h"]))

    def update(self):
        '''
        Функция, которая перерисовывате экран
        (делает заливку bg_color и поочереди отрисовывает
        все обЪекты, содержащиеся в списке для отрисовки)
        '''

        super().update()

        pg.display.update()


class SubScreen(Screen):
    '''
    Класс подэкрана для отображения на главном экране сразу
    нескольких сцен
    '''

    def __init__(self, pos, size, bg_color=COLORS.TRANSPARENT):
        '''
        Функция для инициализации подэкрана приложения
        :param pos: словарь {x, y} с позицией левого верхнего
                    угла подэкрана
        :param size: словарь вида {"w", "h"}, размеры подэкрана
        :param bg_color: цвет из COLORS, цвет заднего фона подэкрана
                         (заливка), по умолчания он прозрачный
        '''
        self.pos = dict(pos)
        super().__init__(size, bg_color)
        self.screen = None

    def move(self, pos):
        '''
        Функция предвигающая подэкран в указанные координаты
        :param pos: словарь {x, y} с координатами точки, в
                    которую необходимо переместить левый верхний
                    угл подэкрана
        '''
        self.pos = dict(pos)

    def set_screen(self, screen):
        '''
        Функция, устанавливающая связь с экраном для
        отрисовки
        :param screen: объект Screen, с которым
                              нужно установить связь
        '''
        self.screen = screen

    def draw(self):
        '''
        Функция рисующая подэкран на предустановленном экране
        '''
        Screen.update(self)
        pg.draw.rect(self.surf, COLORS.BLACK,
                     self.surf.get_rect(), 2)
        self.screen.get_surface().blit(self.surf,
                                       (self.pos["x"], self.pos["y"]))


class Wrapper(SubScreen):
    def __init__(self, model, bg_color=COLORS.TRANSPARENT):
        self.model = model
        super.__init__(self, find_pos(self), find_size(self), bg_color)

    def draw(self):
        for mod in self.model:
            pic = Picture(mod)
            pic.draw(self.surf)

    def find_size(self):
        size = {}
        size['w'] = find_max(self)['xmax'] - find_max(self)['xmin']
        size['h'] = find_max(self)['ymax'] - find_max(self)['ymin']
        return size

    def find_pos(self):
        pos = {}
        pos['x'] = find_max(self)['xmin']
        pos['y'] = find_max(self)['ymin']

    def find_max(self):
        if self.model:
            xmax = self.model[0].x
            xmin = self.model[0].x
            ymin = self.model[0].y
            ymax = self.model[0].y
        for obj in model:
            if obj.x > xmax:
                xmax.obj.x
            if obj.x < xmin:
                xmin = obj.x
            if obj.y > ymax:
                ymax = obj.y
            if obj.y < ymin:
                ymin = obj.y
        max_min = {}
        max_min['xmin'] = xmin
        max_min['xmax'] = xmax
        max_min['ymin'] = ymin
        max_min['ymax'] = ymax


class Picture:
    def __init__(self, obj):
        self.obj = obj

    def draw(self, surf):
        pg.draw.circle(surf, self.obj.color,
                       (self.obj.x, self.obj.y), self.obj.r)


if __name__ == "__main__":
    print("This module is not for direct call!!!")
