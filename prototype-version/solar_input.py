# coding:utf-8
# license: GPLv3

import yaml


def read_data_from_file(input_filename):
    """Cчитывает данные о космических объектах из файла, создаёт сами объекты
    input_filename — имя входного файла
    """

    data = None
    with open(input_filename, 'r') as file:
        data = yaml.load(file)

    # чтение данных из файла

    return data


def write_data_to_file(output_filename, objects):
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
