import os
import csv
import time

from Database.Bill import ReadDatabase

csv_path = r"H:\Dev\github\Digital-SHMTU-Tools\workdir\bills\consumption_2023-10-06_16-36-19.csv"

field_dict = ReadDatabase.read_field()


# file_name = os.path.basename(csv_path)
# print(file_name)

def read_csv_data(path):
    list_consumption = []

    # 读取文件
    print("正在读取文件...")
    print(path)
    with open(path, encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            list_consumption.append(row)

    del (list_consumption[0])
    print("读取文件成功！")

    # print(list_consumption)
    return list_consumption


def analysis_csv(path):
    list_consumption = read_csv_data(path)

    consumption_classify = {
        "other": []
    }

    for record in list_consumption:
        if len(record) != 8:
            print("!!!错误:")
            print(record)
            print("长度不为7!")
            print("csv文件有问题！")
            continue

        timeArray = time.strptime(
            "{} {}".format(record[0], record[1]),
            "%Y.%m.%d %H:%M:%S"
        )

        # 转为其它显示格式
        other_style_time = time.strftime("%Y/%m/%d %H:%M:%S", timeArray)
        print(other_style_time)

        record_dict = {
            "str_date": record[0],
            "str_time": record[1],
            "name": record[2],
            "num": record[3],
            "target": record[4],
            "str_money": record[5],
            "pay_type": record[6],
            "status": record[7],
            "time": timeArray,
            "money": float(record[5])
        }
        print(record_dict)


if __name__ == '__main__':
    # analysis_csv(csv_path)
    print(field_dict)
