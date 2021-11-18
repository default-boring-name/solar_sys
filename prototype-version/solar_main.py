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

    # События менеджера пользовательско интерфейса

    UPDATELABEL = pg.event.custom_type()

    '''
    Событие данного типа должно иметь
    атрибут target - название надписи, которую
    нужно обновить, и атрибут text - новая текст
    надписи
    '''

    button = gui.elements.ui_button.UIButton
    file_dialog = gui.windows.ui_file_dialog.UIFileDialog
    horiz_slider = gui.elements.ui_horizontal_slider.UIHorizontalSlider
    label = gui.elements.ui_label.UILabel

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
        self.stopwatch.change_flow(0.1)

        load_button_params = {
                              "relative_rect": pg.Rect(20, 20, 100, 50),
                              "text": "Load model",
                              "manager": self.gui_manager
                             }
        load_button = UIManager.button(**load_button_params)

        pause_button_params = {
                               "relative_rect": pg.Rect(120, 20, 100, 50),
                               "text": "Pause",
                               "manager": self.gui_manager
                              }
        pause_button = UIManager.button(**pause_button_params)

        play_button_params = {
                               "relative_rect": pg.Rect(220, 20, 100, 50),
                               "text": "Play",
                               "manager": self.gui_manager
                              }
        play_button = UIManager.button(**play_button_params)

        speed_slider_params = {
                               "relative_rect": pg.Rect(20, 70, 200, 25),
                               "manager": self.gui_manager,
                               "start_value": 0,
                               "value_range": (-6, 12)
                              }
        speed_slider = UIManager.horiz_slider(**speed_slider_params)

        timer_label_params = {
                              "relative_rect": pg.Rect(0, 20, 200, 50),
                              "manager": self.gui_manager,
                              "text": "Model time: 0y 0m",
                              "anchors": {
                                          "left": "right",
                                          "right": "right",
                                          "top": "top",
                                          "bottom": "top"
                                         }
                             }
        timer_label_params["relative_rect"].topright = (-20, 20)

        timer_label = UIManager.label(**timer_label_params)

        self.ui_pool = {
                        "load button": load_button,
                        "pause button": pause_button,
                        "play button": play_button,
                        "speed slider": {
                                         "slider": speed_slider,
                                         "last value": 0
                                        },
                        "timer label": timer_label
                       }

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
                self.button_handling(event)

            elif event.user_type == gui.UI_HORIZONTAL_SLIDER_MOVED:
                self.slider_handling(event)

            elif event.user_type == gui.UI_FILE_DIALOG_PATH_PICKED:
                self.file_dialog_handling(event)

        elif event.type == UIManager.UPDATELABEL:
            if event.target in self.ui_pool.keys():
                self.ui_pool[event.target].set_text(event.text)

    def button_handling(self, event):
        '''
        Функция, обрабатывающая события, связанные с кнопками
        :param event: полученное событие, на которое пользовательский
                      интерфейс должен прореагировать
        '''
        if event.user_type == gui.UI_BUTTON_PRESSED:
            if event.ui_element is self.ui_pool["load button"]:
                win_params = {
                              "rect": pg.Rect(20, 20, 500, 400),
                              "manager": self.gui_manager,
                              "window_title": "Choose the model"
                             }
                file_dialog = UIManager.file_dialog(**win_params)
                self.ui_pool.update({"file dialog": file_dialog})

            elif event.ui_element is self.ui_pool["pause button"]:
                pause_event = pg.event.Event(ModelManager.TOGGLE,
                                             {"mode": False})
                pg.event.post(pause_event)

            elif event.ui_element is self.ui_pool["play button"]:
                play_event = pg.event.Event(ModelManager.TOGGLE,
                                            {"mode": True})
                pg.event.post(play_event)

    def slider_handling(self, event):
        '''
        Функция, обрабатывающая события, связанные со слайдерами
        :param event: полученное событие, на которое пользовательский
                      интерфейс должен прореагировать
        '''
        if event.user_type == gui.UI_HORIZONTAL_SLIDER_MOVED:
            if event.ui_element == self.ui_pool["speed slider"]["slider"]:
                value = event.ui_element.get_current_value()

                if value != self.ui_pool["speed slider"]["last value"]:
                    self.ui_pool["speed slider"]["last value"] = value

                    scale = 10 ** (value / 10)
                    scale_event = pg.event.Event(ModelManager.CHANGEFLOW,
                                                 {"scale": scale})
                    pg.event.post(scale_event)

    def file_dialog_handling(self, event):
        '''
        Функция, обрабатывающая события, связанные со окном выбора файла
        :param event: полученное событие, на которое пользовательский
                      интерфейс должен прореагировать
        '''

        if event.user_type == gui.UI_FILE_DIALOG_PATH_PICKED:
            if "file dialog" in self.ui_pool:
                if event.ui_element is self.ui_pool["file dialog"]:
                    load_event = pg.event.Event(ModelManager.LOAD,
                                                {"file": event.text})
                    pg.event.post(load_event)
                    self.ui_pool.pop("file dialog")

                    self.ui_pool["speed slider"]["slider"].set_current_value(0)
                    self.ui_pool["speed slider"]["last value"] = 0

                    self.ui_pool["timer label"].set_text("Model time: 0y 0m")

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
    атрибут scale - новая скорость течения времени
    в модели относительно дефолтной скорости течения времени в модели
    (загружается из файла)
    '''

    TOGGLE = pg.event.custom_type()

    '''
    Событие данного типа должно иметь
    атрибут mode (boolean value) - режим, в который
    нужно переключить модель
    '''

    def __init__(self, pos, size):
        '''
        Функция инициализирующая менеджер модели
        :param size: словарь вида {"w", "h"}, размеры окна
        '''
        self.size = dict(size)
        self.pos = dict(pos)
        self.model = None
        self.visual = None
        self.screen = None
        self.stopwatch = None
        self.default_speed = 1

    def call(self, event):
        '''
        Функция, описывающая реакцию менеджера модели на
        полученное событие
        :param event: полученное событие, на которое пользовательский
                      интерфейс должен прореагировать
        '''

        if event.type == ModelManager.LOAD:
            if self.model is not None:
                remove_event = pg.event.Event(VisualManager.REMOVEOBJ,
                                              {"target": self.visual})
                pg.event.post(remove_event)

            data = s_input.read_data_from_file(event.file)
            self.model = s_model.Model()
            self.model.load(data["Objects"])

            self.stopwatch = TimeManager.Stopwatch()
            self.stopwatch.play()
            self.stopwatch.change_flow(data["Time scale"])
            self.default_speed = data["Time scale"]

            max_distance = 2.1 * self.model.get_max_distance()
            scale = min(self.size.values()) / max_distance
            print(max_distance)

            self.visual = s_vis.ModelVisual(scale, self.model,
                                            self.pos, self.size)
            self.visual.set_screen(self.screen)
            add_event = pg.event.Event(VisualManager.ADDOBJ,
                                       {"target": self.visual})
            pg.event.post(add_event)

        elif event.type == ModelManager.CHANGEFLOW:
            if self.stopwatch is not None:
                self.stopwatch.change_flow(event.scale * self.default_speed)

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

                time = int(self.stopwatch.get_time())
                years = time // (365 * 24 * 60 * 60)
                months = time % (365 * 24 * 60 * 60) // (30 * 24 * 60 * 60)

                time_str = f"Model time: {years}y {months}m"
                label_update_event = pg.event.Event(UIManager.UPDATELABEL,
                                                    {"target": "timer label",
                                                     "text": time_str})
                pg.event.post(label_update_event)

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

    model_pos = {"x": WIN_SIZE["w"] * 0.05,
                 "y": WIN_SIZE["h"] * 0.15}
    model_size = {"w": WIN_SIZE["w"] * 0.9,
                  "h": WIN_SIZE["h"] * 0.80}

    model_manager = ModelManager(model_pos, model_size)
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
