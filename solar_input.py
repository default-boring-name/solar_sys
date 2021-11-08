# coding:utf-8
# license: GPLv3

import yaml
from solar_obj import Objects

def read_space_objects_data_from_file(input_filename):
    """Cчитывает данные о космических объектах из файла, создаёт сами объекты
    input_filename — имя входного файла
    """

    objects = []
    with open(input_filename, 'r') as file:
        data = yaml.load(file)['Objects']
    #чтение данных из файла
    
    for base in data:
        x = base ['x']
        y= base ['y']
        v_x = base['v_x']
        v_y=base['v_y']
        r=base['r']
        m=base['m']
        color=base['color']
        objects.append(Objects(x,y,v_x,v_y,color,r,m))
    #образование массива объектов
    return objects




def write_space_objects_data_to_file(output_filename, space_objects):
    """Сохраняет данные о космических объектах в файл.

    Строки должны иметь следующий формат:

    Star <радиус в пикселах> <цвет> <масса> <x> <y> <Vx> <Vy>

    Planet <радиус в пикселах> <цвет> <масса> <x> <y> <Vx> <Vy>

    Параметры:

    **output_filename** — имя входного файла

    **space_objects** — список объектов планет и звёзд
    """
    with open(output_filename, 'w') as out_file:
        for obj in space_objects:
            print(out_file, "%s %d %s %f" % ('1', 2, '3', 4.5))
            # FIXME!


#if __name__ == "__main__":
    #print("This module is not for direct call!")
