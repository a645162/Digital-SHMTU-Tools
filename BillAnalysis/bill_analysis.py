import os
import csv
import time
import datetime

import Debug.debug_path
from Database.Bill import ReadDatabase, SaveJson
from Database.Bill import canteen_config, bath_config, output_config
from Utils import path

field_dict = dict(ReadDatabase.read_field())
type_dict = dict(ReadDatabase.read_type())
position_dict = dict(ReadDatabase.read_position())
schedule_dict_list = list(ReadDatabase.read_schedule())

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
            "str_date": record[0].strip(),
            "str_time": record[1].strip(),
            "name": record[2].strip(),
            "num": record[3].strip(),
            "target": record[4].strip(),
            "str_money": record[5].strip(),
            "pay_type": record[6].strip(),
            "status": record[7].strip(),
            "datetime": date_time_data,
            "money": float(record[5].strip())
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


def handle_canteen():
    # 对食堂问题做进一步分类
    new_canteen_list = []
    for canteen_record in classify_dict["canteen"]:
        new_canteen_record = dict(canteen_record).copy()

        # 食堂分类
        text = canteen_record[position_dict["field"]]
        keywords_dict = dict(position_dict["keywords"])
        found = False
        for keyword in keywords_dict.keys():
            if text.find(keyword) != -1:
                new_canteen_record["position"] = keywords_dict[keyword]["position"]
                new_canteen_record["room"] = keywords_dict[keyword]["room"]
                found = True
                break
        if not found:
            new_canteen_record["position"] = "未知"
            new_canteen_record["room"] = "未知"
            print(text, "未知位置，请在github反馈给开发者！")

        # 早中晚分类
        found = False
        for schedule_dict in schedule_dict_list:
            valid_date_dict = dict(schedule_dict["valid_date"])
            if canteen_config.date_is_in_range(
                    new_canteen_record["str_date"],
                    valid_date_dict["start_date"],
                    valid_date_dict["end_date"]
            ):
                timetable_dict = dict(schedule_dict["timetable"])
                for timetable_key in timetable_dict.keys():
                    current_timetable = dict(timetable_dict[timetable_key])
                    if canteen_config.time_is_in_range(
                            new_canteen_record["str_time"],
                            current_timetable["start_time"],
                            current_timetable["end_time"]
                    ):
                        new_canteen_record["timetable"] = current_timetable["name"]
                        found = True
                        break
                if found:
                    break

        new_canteen_list.append(new_canteen_record)
        classify_dict["canteen"] = new_canteen_list

    print("食堂处理完毕！")


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


def output_classify_to_csv(save_dir, time_str):
    print("=" * 50)

    print("开始输出！")
    save_time_dir = os.path.join(save_dir, time_str)

    not_output = []

    for key in classify_dict.keys():
        if key in not_output:
            continue
        print("-" * 50)
        print("输出分类 {} :".format(key))
        file_name = "classify_{}_{}.csv".format(key, time_str)
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


def output_canteen(save_dir, time_str):
    print("-" * 50)
    save_time_dir = os.path.join(save_dir, time_str)
    print("输出分类 食堂消费清单")
    file_name = "canteen_{}.csv".format(time_str)
    file_path = os.path.join(save_time_dir, file_name)
    path.create_dir_if_not_exist(save_time_dir)
    print("准备写出到文件：", file_path)
    csv_file = \
        open(file_path, 'w', newline='', encoding=output_config.encodings)

    writer = csv.writer(csv_file)
    writer.writerow(
        [
            "日期",
            "时间",
            "地点",
            "食堂名",
            "价格",
            "用餐时段"
        ]
    )
    total_money = 0
    for classify_data in classify_dict["canteen"]:
        if classify_data is not None:
            data = [
                classify_data["str_date"],
                classify_data["str_time"],
                classify_data["position"],
                classify_data["room"],
                classify_data["str_money"],
                classify_data["timetable"]
            ]
            total_money += classify_data["money"]
            writer.writerow(data)
    csv_file.close()
    print("食堂消费总金额为{}".format(round(total_money, 2)))


if __name__ == '__main__':
    csv_path = ""

    if (csv_path) == 0:
        csv_path = Debug.debug_path.csv_path

    analysis_csv(csv_path)
    print(field_dict)

    # 合并相邻的洗浴记录
    handle_bath()

    handle_canteen()

    now = datetime.datetime.now()
    date_time = now.strftime("%Y-%m-%d_%H-%M-%S")
    print("当前时间 ", date_time)
    # 输出每一个分类到csv文件
    output_classify_to_csv(
        save_dir=Debug.debug_path.classify_dir_path,
        time_str=date_time
    )

    output_canteen(
        save_dir=Debug.debug_path.classify_dir_path,
        time_str=date_time
    )
