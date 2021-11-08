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




def write_space_objects_data_to_file(output_filename, objects):
    """Сохраняет данные о космических объектах в файл
    Параметры:

    **output_filename** — имя выходного файла

    **objects** — список объектов планет и звёзд
    """
    array = [vars(obj) for obj in objects]
    data = {'objects': array}
    with open(output_filename, 'w') as out_file:
        yaml.dump(data, out_file)
        
        
if __name__ == "__main__":
    print("This module is not for direct call!")
