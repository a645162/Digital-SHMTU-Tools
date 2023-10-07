import os
import json

current_py_path = os.path.dirname(os.path.abspath(__file__))

csv_column = [
    "date", "time", "name", "num",
    "target", "money", "pay_type", "status"
]


def save_json(data, path):
    json_str = (
        json.dumps(
            data,
            indent=2,
            separators=(',', ': ')
        )
    )
    with open(path, 'w', encoding="utf-8") as f:
        f.write(json_str)


if __name__ == '__main__':
    field_dict = {}
    for i in range(len(csv_column)):
        field_dict[csv_column[i]] = i

    save_json(
        field_dict,
        os.path.join(current_py_path, "field.json")
    )
