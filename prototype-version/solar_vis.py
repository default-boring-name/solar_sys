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
    ����� ������, �� ������� ����� ��������������
    ��������� �����
    '''

    def __init__(self, size, bg_color=COLORS.TRANSPARENT):
        '''
        ������� ��� ������������� ������
        :param size: ������� ���� {"w", "h"}, ������� ������
        :param bg_color: ���� �� COLORS, ���� ������� ���� ������
                         (�������), �� ��������� �� ����������
        '''

        self.size = dict(size)
        self.bg_color = bg_color
        self.surf = pg.Surface((self.size["w"], self.size["h"]),
                               pg.SRCALPHA)
        self.to_draw_list = []

    def update(self):
        '''
        �������, ������� �������������� �����
        (������ ������� bg_color � ��������� ������������
        ��� �������, ������������ � ������ ��� ���������)
        '''

        self.surf.fill(self.bg_color)
        for obj in self.to_draw_list:
            obj.draw()

    def add_obj(self, obj):
        '''
        �������, ����������� ���������� ������ � ������
        ��� ���������, ���� ��� ��� ��� �� ����
        :param obj: ������, ������� ����� �������� �
                    ������ ��� ��������� (����������� ������
                    ����� ����� draw() ��� ��������� � �����
                    set_screen ��������� ������ Screen)
        '''

        if obj not in self.to_draw_list:
            self.to_draw_list.append(obj)

    def remove_obj(self, obj):
        '''
        �������, ����������� ���������� ������ �� ������
        ��� ��������� (���� �� ��� ���)
        :param obj: ������, ������� ����� �������� ��
                    ������ ��� ���������
        '''

        if obj in self.to_draw_list:
            self.to_draw_list.remove(obj)

    def get_surface(self):
        '''
        �������, ������������ �������� ����������� ��� ���������
        '''

        return self.surf


class MainScreen(Screen):
    '''
    ����� �������� ������ ����������
    '''

    def __init__(self, size, bg_color=COLORS.WHITE):
        '''
        ������� ��� ������������� �������� ������ ����������
        :param size: ������� ���� {"w", "h"}, ������� ������
        :param bg_color: ���� �� COLORS, ���� ������� ���� ������
                         (�������), �� ��������� �� �����
        '''

        super().__init__(size, bg_color)
        self.surf = pg.display.set_mode((self.size["w"],
                                         self.size["h"]))

    def update(self):
        '''
        �������, ������� �������������� �����
        (������ ������� bg_color � ��������� ������������
        ��� �������, ������������ � ������ ��� ���������)
        '''

        super().update()

        pg.display.update()


class SubScreen(Screen):
    '''
    ����� ��������� ��� ����������� �� ������� ������ �����
    ���������� ����
    '''

    def __init__(self, pos, size, bg_color=COLORS.TRANSPARENT):
        '''
        ������� ��� ������������� ��������� ����������
        :param pos: ������� {x, y} � �������� ������ ��������
                    ���� ���������
        :param size: ������� ���� {"w", "h"}, ������� ���������
        :param bg_color: ���� �� COLORS, ���� ������� ���� ���������
                         (�������), �� ��������� �� ����������
        '''
        self.pos = dict(pos)
        super().__init__(size, bg_color)
        self.screen = None

    def move(self, pos):
        '''
        ������� ������������ �������� � ��������� ����������
        :param pos: ������� {x, y} � ������������ �����, �
                    ������� ���������� ����������� ����� �������
                    ��� ���������
        '''
        self.pos = dict(pos)

    def set_screen(self, screen):
        '''
        �������, ��������������� ����� � ������� ���
        ���������
        :param screen: ������ Screen, � �������
                              ����� ���������� �����
        '''
        self.screen = screen

    def draw(self):
        '''
        ������� �������� �������� �� ����������������� ������
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
