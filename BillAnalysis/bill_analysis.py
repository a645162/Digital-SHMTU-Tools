import os
import csv

path = r"H:\Dev\github\Digital-SHMTU-Tools\workdir\bills\consumption_2023-10-06_16-36-19.csv"
file_name = os.path.basename(path)
print(file_name)

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

print(list_consumption)
