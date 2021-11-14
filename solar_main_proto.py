import pygame as pg
import thorpy

FPS = 30
WIN_SIZE = (1000, 900)

pg.init()


class EventManager:
    '''
    Класс менеджра событий, который обрабатывает как
    pygame события, так и пользовательские события
    '''

    # События менеджера событий

    REMOVEOBJ = pg.event.custom_type()
    '''
    Событие данного типа должно иметь
    атрибут target, указывающий на объект,
    который нужно удалить
    '''

    ADDOBJ = pg.event.custom_type()
    '''
    Событие данного типа должно иметь
    атрибут target, указывающий на объект,
    который нужно добавить
    '''

    def __init__(self):
        '''
        Функция для инициализация объекта менеджера событий
        '''
        self.pool = []

    def add_obj(self, obj):
        '''
        Функция, которая добавляет переданный объект в
        список отслеживаемых объектов, если его там уже не было
        :param obj: обЪект, который нужно добавить в
                    список(объект должен иметь метод
                    idle(), описывающий дефолтное поведение
                    объекта, метод call(), принимающий
                    объект события
        '''
        if obj not in self.pool:
            self.pool.append(obj)
            obj.set_manager(self)
            return True
        return False

    def remove_obj(self, obj):
        '''
        Функция, исключающая переданный объект из списка
        отслеживаемых объектов (если он там был)
        :param obj: объект, который будет исключен из
                    списка отслеживаемых объектов
        '''
        if obj in self.pool:
            self.pool.remove(obj)
            return True
        return False

    def get_pool(self):
        '''
        Функция, возращающая список отслеживаемых объектов
        '''
        return self.pool

    def run(self):
        '''
        Функция, забирающая события из очереди событий pygame,
        обрабатывающая их, пересылающая часть событий в
        объекты из списка отслеживаемых объектов, вызывающая
        дефолтное поведение объектов из списка отслеживаемых
        объектов и возращающая флаг продолжения работы
        '''

        running = True
        for event in pg.event.get():

            if event.type == pg.QUIT:
                running = False

            elif event.type == EventManager.REMOVEOBJ:
                self.remove_obj(event.target)

            elif event.type == EventManager.ADDOBJ:
                self.add_obj(event.target)

            else:
                for obj in self.pool:
                    obj.call(event)

        for obj in self.pool:
            obj.idle()

        return running


def main():
    pass


if __name__ == "__main__":
    main()
