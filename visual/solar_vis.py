# coding:utf-8
import pygame as pg


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
        Функция, предвигающая подэкран в указанные координаты
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
        Функция, рисующая подэкран на предустановленном экране
        '''
        super().update()
        pg.draw.rect(self.surf, COLORS.BLACK,
                     self.surf.get_rect(), 2)
        self.screen.get_surface().blit(self.surf,
                                       (self.pos["x"], self.pos["y"]))


class ModelVisual(SubScreen):
    '''
    класс Обертки модели
    '''

    def __init__(self, scale, model, pos, size, bg_color=COLORS.BLACK):
        '''
        инициализация обретки
         model - объект класса Model
         bg_color=COLORS.BLACK - цвет фона
         scale - масштаб
         pos - словарь {x, y} с позицией левого верхнего
                    угла экрана для отрисовки
         size - размер экрана для отрисовки
        '''
        self.model = model
        self.scale = scale
        self.offset = {"x": 0, "y": 0}
        self.zoom = 0
        super().__init__(pos, size, bg_color)

        for obj in self.model.get_link():
            new_sprite = Sprite(obj, scale)
            new_sprite.set_screen(self)
            self.add_obj(new_sprite)

    def move_camera(self, offset):
        '''
        Функция, смещающие камеру на указанные координаты
        :param offset: словарь {x, y} с координатами смещения
                       камеры
        '''

        self.offset = {
                       "x": self.offset["x"] + offset["x"],
                       "y": self.offset["y"] + offset["y"]
                      }
        for sprite in self.to_draw_list:
            sprite.add_offset(-self.offset["x"], -self.offset["y"])

    def zoom_camera(self, zoom):
        '''
        Функция, приближающая камеру на указанное кол-во процентов
        :param zoom: кол-во процентов, которое приблизится камера
                     (например, если zoom = 10, то все рассояния
                      увеличатся в 1.1 раз)
        '''

        self.zoom += zoom
        for sprite in self.to_draw_list:
            sprite.set_scale(self.scale * (1 + self.zoom / 100))

    def default_camera(self):
        '''
        Функция, возвращающая камеру в дефолтное состояние
        '''

        self.zoom = 0
        self.offset = {"x": 0, "y": 0}
        for sprite in self.to_draw_list:
            sprite.add_offset(-self.offset["x"], -self.offset["y"])
            sprite.set_scale(self.scale * (1 + self.zoom / 100))


class Sprite:
    '''
    класс изображения объекта
    '''

    def __init__(self, obj, scale):
        '''
        инициализация изображения
        obj - объект класса Objects
        scale - масштаб
        '''
        self.obj = obj
        self.scale = scale
        self.screen = None
        self.offset_x = 0
        self.offset_y = 0

    def draw(self):
        '''
        отрисовка изображения объекта
        surf - поверхность для отрисовки
        '''
        x = self.obj.x * self.scale + self.offset_x
        y = self.obj.y * self.scale + self.offset_y
        surf = self.screen.get_surface()
        pg.draw.circle(surf, self.obj.color, (int(x), int(y)),
                       int(self.obj.r))

    def set_screen(self, screen):
        '''
        Функция, устанавливающая связь с экраном для
        отрисовки
        :param screen: объект Screen, с которым
                              нужно установить связь
        '''
        self.screen = screen

    def add_offset(self, offset_x, offset_y):
        '''
        Функция, смещающая спрайт на указанные координаты
        :param offset_x: горизонтальная координата смещения спрайта
        :param offset_y: вертикальная координата смещения спрайта
        '''
        self.offset_x = offset_x
        self.offset_y = offset_y

    def set_scale(self, scale):
        '''
        Функция, устанавливающая новый маштаб
        :param scale: новый маштаб изображения
        '''
        self.scale = scale


if __name__ == "__main__":
    print("This module is not for direct call!!!")
