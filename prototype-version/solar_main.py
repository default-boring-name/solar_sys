import pygame as pg
import thorpy

FPS = 30
WIN_SIZE = {"w": 1000, "h": 900}

pg.init()


class ManageObj:
    '''
    Абстрактный класс, предоставляющий общий
    функционал для объектов, за котором может
    следить EventManager
    '''

    def __init__(self):
        '''
        Функция инициализирующая объект
        '''
        self.manager = None

    def idle(self):
        '''
        Функция, описывающая дефолтное поведение объекта
        '''
        pass

    def call(self, event):
        '''
        Функция, описывающая реакцию менеджера времени на полученное событие
        :param event: полученное событие, на которое пуля
                      должна прореагировать
        '''
        pass

    def set_manager(self, event_manager):
        '''
        Функция, устанавливающая связь с обработчиком
        событий
        :param event_manager: объект EventManager, с которым
                              нужно установить связь
        '''

        self.manager = event_manager
        add_event = pg.event.Event(EventManager.ADDOBJ,
                                   {"target": self})
        pg.event.post(add_event)


class TimeManager(ManageObj):
    '''
    Класс менеджера времени
    '''

    def __init__(self, fps):
        '''
        Функция инициализирующая менеджера времени
        '''
        self.fps = fps
        self.total_time = 0
        self.clock = pg.time.Clock()

        super().__init__()

    def idle(self):
        '''
        Функция, описывающая дефолтное поведение менеджера времени
        (отсчет времени, проверка таймеров и т.д.)
        '''
        self.clock.tick(self.fps)
        self.total_time += self.clock.get_time() / 1000

    def get_time(self):
        '''
        Функция, возвращающая время в секундах,
        прошедшее со старта программы
        '''
        return self.total_time


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
        self.timer = TimeManager(FPS)

        self.timer.set_manager(self)

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

    def get_time(self):
        '''
        Функция, возвращающая время в секундах,
        прошедшее со старта программы
        '''
        return self.timer.get_time()


def main():
    manager = EventManager()

    while manager.run():
        pass


if __name__ == "__main__":
    main()
