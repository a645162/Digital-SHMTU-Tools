import os
import json

current_py_path = os.path.dirname(os.path.abspath(__file__))


def read_json(file_name):
    f = \
        open(
            os.path.join(current_py_path, file_name),
            'r',
            encoding="utf-8"
        )
    content = f.read()
    a = json.loads(content)
    f.close()
    return a


def read_field():
    j = read_json("field.json")
    return j


def read_schedule():
    j = read_json("schedule.json")
    return j


def read_type():
    j = read_json("type.json")
    return j


def read_position():
    j = read_json("position.json")
    return j


if __name__ == '__main__':
    print(read_field())
    print(read_schedule())
    print(read_type())
    print(read_position())
