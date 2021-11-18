# coding:utf-8
import copy

class Model:
	'''
	Класс физической модели
	'''

	def __init__(self):
		'''
		Функция, иницализирующая модель
		'''
		self.space_objs = []

	def load(self, objects):
		'''
		Функция, загружающая объекты из переданного массива
		:param objects: массив с объектами, которые будут добавлены в проект
		'''
		self.space_objs = objects

	def update(self, dt):
		'''
		Функция, обновляющая модель в соответствии с dt
		:param dt: изменение времени
		'''
		for obj in self.space_objs:
			obj.calculate_force(self.space_objs)

		for obj in self.space_objs:
			obj.move()

        def get_link(self):
            '''
            Функция, возращающая ссылку на реальный массив с
            космическим объектами
            '''

            return self.space_objs

	def dump(self):
		'''
		Функция, возвращающая последнее состояние модели
		'''

		return copy.deepcopy(self.space_objs)

	def get_max_distance:
		'''
		Функция, возвращающая максимальное расстояние между
		объектами
		'''

		distance = 0

		for obj_1 in self.space_objs:
			for obj_2 in self.space_objs:
				new_distance = ((obj_1.x - obj_2.x) ** 2 + (obj_1.y - obj_2.y) ** 2)
				distance = max(new_distance, distance)

		return distance
