# coding:utf-8
import math


class Objects:
    grav_constant = 6.67408e-11

    def __init__(self, x, y, v_x, v_y, color, r, m):
        '''
        инициализация класса объектов солнечной системы
        x - координата x
        y - координата y
        v_x - горизонтальная скорость
        v_y - вертикальная скорость
        color - цвет
        r - радиус
        m - масса
        '''
        self.x = x
        self.y = y
        self.v_x = v_x
        self.v_y = v_y
        self.color = color
        self.r = r
        self.m = m
        self.a_x = 0
        self.a_y = 0

    def calculate_force(self, objects):
        '''
        вычисление силы, действующей на объект
        objects - массив объектов, с которыми взаимодействует объект
        '''
        self.a_x = 0
        self.a_y = 0
        for obj in objects:
            if obj != self:
                l = ((self.x - obj.x) ** 2 + (self.y - obj.y) ** 2) ** 0.5

                # проверка слишком близкого сближения
                if l < (self.r + obj.r):
                    alpha = math.atan2((self.y - obj.y), (self.x - obj.x))
                    sin = math.sin(alpha)
                    cos = math.cos(alpha)
                    vpself = self.v_y * sin + self.v_x * cos
                    vpobj = obj.v_y * sin + obj.v_x * cos
                    # вычисление составляющей скорости, параллельной линии,
                    # соединяющей центры шаров
                    if vpself * vpobj < 0:
                        # изменение сокоростей при сближении
                        vparself = -self.v_y * cos + self.v_x * sin
                        vparobj = -obj.v_y * cos + obj.v_x * sin
                        vpself *= -1
                        vpobj *= -1
                        self.v_x = vparself * sin + vpself * cos
                        self.v_y = - vparself * cos + vpself * sin
                        obj.v_x = vparobj * sin + vpobj * cos
                        obj.v_y = - vparobj * cos + vpobj * sin

                else:
                    # непосредственное вычисление силы,
                    # если объекты не слишком близко
                    F = Objects.grav_constant * self.m * obj.m / l ** 2
                    F_x = -F * (self.x - obj.x) / l
                    F_y = -F * (self.y - obj.y) / l
                    self.a_y += F_y / self.m
                    self.a_x += F_x / self.m

    def move(self, dt):
        '''
        передвижение тела за определенное время
        dt - время, за которое рассматривается изменение
        '''
        self.v_x += self.a_x * dt
        self.v_y += self.a_y * dt
        self.x += self.v_x * dt
        self.y += self.v_y * dt
