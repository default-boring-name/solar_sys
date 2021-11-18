# coding:utf-8
import pygame as pg
import solar_vis as s_vis
import solar_model as s_model
import solar_input as s_input
import pygame_gui as gui

FPS = 30
WIN_SIZE = {"w": 900, "h": 800}

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
        self.event_manager = None

    def idle(self):
        '''
        Функция, описывающая дефолтное поведение объекта
        '''
        pass

    def call(self, event):
        '''
        Функция, описывающая реакцию объекта на полученное событие
        :param event: полученное событие, на которое объект
                      должен прореагировать
        '''
        pass

    def set_manager(self, event_manager):
        '''
        Функция, устанавливающая связь с обработчиком
        событий
        :param event_manager: объект EventManager, с которым
                              нужно установить связь
        '''

        self.event_manager = event_manager
        add_event = pg.event.Event(EventManager.ADDOBJ,
                                   {"target": self})
        pg.event.post(add_event)


class TimeManager(ManageObj):
    '''
    Класс менеджера времени
    '''

    # События менеджера времени

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

    class Stopwatch:
        '''
        Класс секудомера
        '''

        def __init__(self, scale=1):
            '''
            Функция, иницализирующая секундомер
            :param scale: скорость течения времени секундомер относительно
                          реального времени, по умолчанию равна 1
            '''
            self.dt = 0
            self.running = False
            self.scale = scale
            self.current_time = 0
            add_event = pg.event.Event(TimeManager.ADDOBJ, {"target": self})
            pg.event.post(add_event)

        def update(self, dt):
            '''
            Функция, обновляющая значение времени секундомера
            :param dt: реальное кол-во прошедшего времени
            '''

            if self.running:
                self.current_time += self.scale * dt
                self.dt = self.scale * dt

        def get_time(self):
            '''
            Функция, возвращающая кол-во прошедшего времени с момента
            последнего перезапуска
            '''

            return self.current_time

        def get_tick(self):
            '''
            Функция, возвращающая последнее обновление времени
            '''

            return self.dt

        def play(self):
            '''
            Функция, активирующая секундомер
            '''

            self.running = True

        def pause(self):
            '''
            Функция, приостанавливающая секундомер
            '''

            self.running = False

        def restart(self, init_time=0):
            '''
            Функция перезапускающая секундомер
            :param init_time: начальное время секундомера, по умолчанию
                              равно 0
            '''

            self.current_time = init_time

        def change_flow(self, scale, addjust_time=False):
            '''
            Функция, изменяющая скорость течения времени секундомера
            относительно реального
            :param scale: новая относительная
            :param addjsut_time: флаг, показывающий надо ли подстроить
                                 уже прошедшее время под новое течение
                                 времени
            '''
            if addjust_time:
                self.current_time *= scale / self.scale
            self.scale = scale

    def __init__(self, fps):
        '''
        Функция инициализирующая менеджера времени
        '''
        self.fps = fps
        self.total_time = 0
        self.pool = []
        self.clock = pg.time.Clock()

        super().__init__()

    def idle(self):
        '''
        Функция, описывающая дефолтное поведение менеджера времени
        (отсчет времени, проверка таймеров и т.д.)
        '''
        dt = self.clock.tick(self.fps) / 1000
        self.total_time += dt

        for obj in self.pool:
            obj.update(dt)

    def call(self, event):
        '''
        Функция, описывающая реакцию объекта на полученное событие
        :param event: полученное событие, на которое объект
                      должен прореагировать
        '''
        if event.type == TimeManager.ADDOBJ:
            if event.target not in self.pool:
                self.pool.append(event.target)

        elif event.type == TimeManager.REMOVEOBJ:
            if event.target in self.pool:
                self.pool.remove(event.target)

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


class VisualManager(ManageObj):
    '''
    Класс менеджера отрисовки, выполняющий роль
    пройслойки между между модулем solar_vis.py и остальной программой.
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

    def __init__(self, win_size):
        '''
        Функция, инициализирующая менеджер отрисовки.
        :param win_size: словарь вида {"w", "h"}, размеры окна
        '''

        super().__init__()
        self.main_screen = s_vis.MainScreen(win_size)

    def idle(self):
        '''
        Функция, описывающая дефолтное поведение менеджера отрисовки
        '''

        self.main_screen.update()

    def call(self, event):
        '''
        Функция, описывающая реакцию менеджера отрисовки на полученное
        событие
        :param event: полученное событие, на которое менеджер отрисовки
                      должен прореагировать
        '''
        if event.type == VisualManager.ADDOBJ:
            self.main_screen.add_obj(event.target)

        elif event.type == VisualManager.REMOVEOBJ:
            self.main_screen.remove_obj(event.target)


class UIManager(ManageObj):
    '''
    Класс пользовательского интерфейса
    '''

    button = gui.elements.ui_button.UIButton
    file_dialog = gui.windows.ui_file_dialog.UIFileDialog

    def __init__(self, win_size):
        '''
        Функция, инициализирующая менеджер пользовательского
        интерфейса.
        :param win_size: словарь вида {"w", "h"}, размеры окна
        '''

        super().__init__()
        self.screen = None
        self.gui_manager = gui.UIManager((win_size["w"], win_size["h"]))
        self.stopwatch = TimeManager.Stopwatch()
        self.stopwatch.play()

        self.ui_pool = dict()

        load_button_params = {
                              "relative_rect": pg.Rect(20, 20, 100, 50),
                              "text": "Load model",
                              "manager": self.gui_manager
                             }
        load_button = UIManager.button(**load_button_params)
        self.ui_pool.update({"load button": load_button})

    def call(self, event):
        '''
        Функция, описывающая реакцию пользовательский интерфейс на
        полученное событие
        :param event: полученное событие, на которое пользовательский
                      интерфейс должен прореагировать
        '''
        self.gui_manager.process_events(event)
        self.gui_manager.update(self.stopwatch.get_tick())

        if event.type == pg.USEREVENT:
            if event.user_type == gui.UI_BUTTON_PRESSED:
                if event.ui_element is self.ui_pool["load button"]:
                    win_params = {
                                  "rect": pg.Rect(20, 20, 500, 400),
                                  "manager": self.gui_manager,
                                  "window_title": "Choose the model"
                                 }
                    file_dialog = UIManager.file_dialog(**win_params)
                    self.ui_pool.update({"file dialog": file_dialog})

            if event.user_type == gui.UI_FILE_DIALOG_PATH_PICKED:
                if "file dialog" in self.ui_pool:
                    if event.ui_element is self.ui_pool["file dialog"]:
                        load_event = pg.event.Event(ModelManager.LOAD,
                                                    {"file": event.text})
                        pg.event.post(load_event)
                        self.ui_pool.pop("file dialog")

    def draw(self):
        '''
        Функция, отрисовывающая пользовательский интерфейс
        '''
        self.gui_manager.draw_ui(self.screen.get_surface())

    def set_screen(self, screen):
        '''
        Функция, устанавливающая связь с холстом
        :param screen: объект solar_vis.Screen, с которым
                              нужно установить связь
        '''
        self.screen = screen

        add_event = pg.event.Event(VisualManager.ADDOBJ,
                                   {"target": self})
        pg.event.post(add_event)


class ModelManager(ManageObj):
    '''
    Класс менеджера модели, являющийся прослойкой между
    solar_model.py и остальной программой
    '''

    # События менеджера модели

    LOAD = pg.event.custom_type()

    '''
    Событие данного типа должно иметь
    атрибут file, содержащий путь к файлу,
    из которого нужно загрузить модель
    '''

    CHANGEFLOW = pg.event.custom_type()

    '''
    Событие данного типа должно иметь
    атрибут scale - новую скорость течения времени
    в модели
    '''

    TOGGLE = pg.event.custom_type()

    '''
    Событие данного типа должно иметь
    атрибут mode (boolean value) - режим, в который
    нужно переключить модель
    '''

    def __init__(self, win_size):
        '''
        Функция инициализирующая менеджер модели
        :param win_size: словарь вида {"w", "h"}, размеры окна
        '''
        self.win_size = dict(win_size)
        self.model = None
        self.visual = None
        self.screen = None
        self.stopwatch = None

    def call(self, event):
        '''
        Функция, описывающая реакцию менеджера модели на
        полученное событие
        :param event: полученное событие, на которое пользовательский
                      интерфейс должен прореагировать
        '''

        if event.type == ModelManager.LOAD:
            objects = s_input.read_space_objects_data_from_file(event.file)
            self.model = s_model.Model()
            self.model.load(objects)

            self.stopwatch = TimeManager.Stopwatch()
            self.stopwatch.play()
            self.stopwatch.change_flow(365 * 24 * 60 * 2)

            max_distance = 2 * self.model.get_max_distance()
            scale = min(self.win_size.values()) / max_distance
            pos = {"x": 0, "y": 0}

            self.visual = s_vis.ModelVisual(scale, self.model, pos,
                                            self.win_size)
            self.visual.set_screen(self.screen)
            add_event = pg.event.Event(VisualManager.ADDOBJ,
                                       {"target": self.visual})
            pg.event.post(add_event)

        elif event.type == ModelManager.CHANGEFLOW:
            if self.stopwatch is not None:
                self.stopwatch.change_flow(event.scale)

        elif event.type == ModelManager.TOGGLE:
            if self.stopwatch is not None:
                if event.mode:
                    self.stopwatch.play()
                else:
                    self.stopwatch.pause()

    def idle(self):
        '''
        Функция, описывающая дефолтное поведение менеджера модели
        '''

        if self.stopwatch is not None:
            if self.stopwatch.running:
                self.model.update(self.stopwatch.get_tick())

    def set_screen(self, screen):
        '''
        Функция, устанавливающая связь с холстом
        :param screen: объект solar_vis.Screen, с которым
                              нужно установить связь
        '''
        self.screen = screen


def main():
    event_manager = EventManager()
    visual_manager = VisualManager(WIN_SIZE)
    model_manager = ModelManager(WIN_SIZE)
    ui_manager = UIManager(WIN_SIZE)

    visual_manager.set_manager(event_manager)
    model_manager.set_manager(event_manager)
    ui_manager.set_manager(event_manager)

    ui_manager.set_screen(visual_manager.main_screen)
    model_manager.set_screen(visual_manager.main_screen)

    while event_manager.run():
        pass

    pg.quit()


if __name__ == "__main__":
    main()
