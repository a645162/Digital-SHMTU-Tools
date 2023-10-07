import os
import csv
import time
import datetime

import Debug.debug_path
from Database.Bill import ReadDatabase, SaveJson, bath_config, output_config
from Utils import path

field_dict = dict(ReadDatabase.read_field())
type_dict = dict(ReadDatabase.read_type())
position_dict = dict(ReadDatabase.read_position())
schedule_list = list(ReadDatabase.read_schedule())

classify_dict = {
    "other": []
}

bath_max_interval_seconds = bath_config.get_max_interval_seconds()

for key1 in type_dict.keys():
    classify_dict[key1] = []


# file_name = os.path.basename(csv_path)
# print(file_name)

def read_csv_data(path):
    list_consumption = []

    # 读取文件
    print("正在读取文件...")
    print(path)
    with open(path, encoding=output_config.encodings) as csv_file:
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
            print("长度不为8!")
            print("csv文件有问题！")
            continue

        date_time_data = (
            datetime.datetime.strptime(
                "{} {}".format(record[0], record[1]),
                "%Y.%m.%d %H:%M:%S"
            )
        )

        record_dict = {
            "str_date": record[0],
            "str_time": record[1],
            "name": record[2],
            "num": record[3],
            "target": record[4],
            "str_money": record[5],
            "pay_type": record[6],
            "status": record[7],
            "datetime": date_time_data,
            "money": float(record[5])
        }
        print(record_dict)

        found_type = False
        for key1 in type_dict.keys():
            keywords_dict = dict(type_dict[key1])
            found = False
            for field_str in keywords_dict.keys():
                keywords_list = list(keywords_dict[field_str])
                for keywords in keywords_list:
                    if str(record_dict[field_str]).find(keywords) != -1:
                        found = True
                        break
                if found:
                    break
            if found:
                classify_dict[key1].append(record_dict)
                found_type = True
                break
        if not found_type:
            classify_dict["other"].append(record_dict)
            # print(keywords_dict)


def handle_canteen(canteen_list, save_path):
    # 对食堂问题做进一步分类
    pass


def judge_bath_record(record1, record2):
    time1 = record1["datetime"]
    time2 = record2["datetime"]
    diff = time2 - time1
    return (
            diff.days == 0
            and
            diff.seconds <= bath_max_interval_seconds
    )


def combine_bath_record(record_list):
    record_list = list(record_list)
    record_list.sort(key=lambda x: x["datetime"])
    length = len(record_list)
    re_dict = record_list[0].copy()

    for i in range(1, length):
        re_dict["money"] += record_list[i]["money"]

    re_dict["money"] = round(float(re_dict["money"]), 2)

    re_dict["str_money"] = str(re_dict["money"])

    return re_dict


def handle_bath():
    # 主要是解决洗澡洗一半拔卡而不是按暂停键的问题

    length = len(classify_dict["bath"])

    new_bath_record_list = []

    i = length - 1
    while i >= 0:
        # record_dict_list = classify_dict["bath"][i]
        current_index = i - 1
        last_record = classify_dict["bath"][i]
        end_index = i
        while current_index >= 0:
            current_record = classify_dict["bath"][current_index]
            if judge_bath_record(last_record, current_record):
                end_index = current_index
            else:
                break
            last_record = current_record
            current_index -= 1

        if i == end_index:
            # 无需合并
            new_bath_record_list.append(classify_dict["bath"][i])
            i -= 1
        else:
            # 需要合并
            new_bath_record_list.append(
                combine_bath_record(classify_dict["bath"][end_index:i + 1])
            )
            i = end_index - 1

    # new_bath_record_list.reverse()
    classify_dict["bath_combine"] = new_bath_record_list
    print("bath处理完毕！")


def output_classify_to_csv(save_dir):
    print("=" * 50)
    now = datetime.datetime.now()
    date_time = now.strftime("%Y-%m-%d_%H-%M-%S")
    print("开始输出！")
    print("当前时间 ", date_time)
    save_time_dir = os.path.join(save_dir, date_time)

    for key in classify_dict.keys():
        print("-" * 50)
        print("输出分类 {} :".format(key))
        file_name = "classify_{}_{}.csv".format(key, date_time)
        file_path = os.path.join(save_time_dir, file_name)
        path.create_dir_if_not_exist(save_time_dir)
        print("准备写出到文件：", file_path)
        csv_file = \
            open(file_path, 'w', newline='', encoding=output_config.encodings)

        writer = csv.writer(csv_file)
        writer.writerow(SaveJson.csv_column)
        total_money = 0
        for classify_data in classify_dict[key]:
            if classify_data is not None:
                data = [
                    "{} {}".format(classify_data["str_date"], classify_data["str_time"]),
                    classify_data["str_time"],
                    classify_data["name"],
                    classify_data["num"],
                    classify_data["target"],
                    classify_data["str_money"],
                    classify_data["pay_type"],
                    classify_data["status"],
                ]
                total_money += classify_data["money"]
                writer.writerow(data)
        csv_file.close()
        print("{}类，总金额为{}".format(key, round(total_money, 2)))
    print("-" * 50)
    print("输出结束！")
    print("=" * 50)


if __name__ == '__main__':
    analysis_csv(Debug.debug_path.csv_path)
    print(field_dict)

    # 合并相邻的洗浴记录
    handle_bath()

    handle_canteen(
        classify_dict["canteen"],
        Debug.debug_path.classify_dir_path
    )

    # 输出每一个分类到csv文件
    output_classify_to_csv(
        save_dir=Debug.debug_path.classify_dir_path
    )
