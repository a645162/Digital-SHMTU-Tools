import os.path
from datetime import datetime

from selenium.webdriver.common.by import By

from Utils import path

url_ecard = r"https://ecard.shmtu.edu.cn/epay/"


def parse_elem_tbody(elem_tbody):
    re = []

    elem_trs = elem_tbody.find_elements(By.XPATH, "./*")
    for tr in elem_trs:
        elem_tds = tr.find_elements(By.XPATH, "./*")

        if len(elem_tds) != 7:
            print("程序出错！elem_tds长度不为7！")
            continue

        # 创建时间
        str_date_time = elem_tds[0].text.strip()
        str_date = str_date_time[:str_date_time.find("\n")].strip()
        str_time = str_date_time[str_date_time.find("\n") + 1:].strip()
        str_time = str_time[:2] + ":" + str_time[2:4] + ":" + str_time[4:]

        # 名称+交易号
        str_name_num = elem_tds[1].text.strip()
        # 名称
        str_name = str_name_num[:str_name_num.find("交易号")].strip()

        # 交易号
        str_num = str_name_num[str_name_num.find("交易号") + 4:].strip()

        # 对方
        str_target = elem_tds[2].text.strip()

        # 金额
        str_money = elem_tds[3].text.strip()

        # 付款方式
        str_pay_type = elem_tds[4].text.strip()

        # 状态
        str_status = "交易成功"
        try:
            elem_tds[5].find_element(By.CLASS_NAME, "label-success")
        except:
            str_status = "fail"
            print(str_status)
            print("状态部分的HTML代码！")
            print(elem_tds[5].get_attribute('innerHTML'))

        current_data = [
            str_date,
            str_time,
            str_name,
            str_num,
            str_target,
            str_money,
            str_pay_type,
            str_status
        ]
        re.append(current_data)
        # print(current_data)

    return re


def get_bill(driver, save_path):
    driver.get(url_ecard)
    driver.get(r"https://ecard.shmtu.edu.cn/epay/consume/query?pageNo=1&tabNo=1")

    list_consumption = []

    elem_tab_content = driver.find_element(By.CLASS_NAME, "tab-content")
    elem_page = (
        elem_tab_content.find_element(
            By.XPATH,
            '//*[@id="aazone.zone_show_box_1"]/div/table/tbody/tr/td[1]'
        )
    )
    page_text = elem_page.text.strip()[2:-1]
    total_page = int(page_text[page_text.find("/") + 1:])
    print("页面加载成功！")
    print("总页数：", total_page)
    print("正在处理第1页！")

    elem_tbody = (
        elem_tab_content.find_element(
            By.XPATH,
            '//*[@id="aazone.zone_show_box_1"]/table/tbody'
        )
    )
    list_consumption.extend(parse_elem_tbody(elem_tbody))

    print("第1页处理完毕！\n继续处理后续页面！")
    for i in range(2, total_page + 1):
        print("正在处理第", i, "页")
        driver.get(
            r"https://ecard.shmtu.edu.cn/epay/consume/query?pageNo={}&tabNo=1"
            .format(i)
        )
        elem_tab_content = driver.find_element(By.CLASS_NAME, "tab-content")
        elem_tbody = (
            elem_tab_content.find_element(
                By.XPATH,
                '//*[@id="aazone.zone_show_box_1"]/table/tbody'
            )
        )
        list_consumption.extend(parse_elem_tbody(elem_tbody))

    print("所有页面处理完毕！")
    print("总共有{}条记录".format(len(list_consumption)))

    now = datetime.now()
    date_time = now.strftime("%Y-%m-%d_%H-%M-%S")

    file_name = "consumption_{}.csv".format(date_time)
    file_path = os.path.join(save_path, file_name)
    print("准备写出到文件：", file_path)
    path.create_dir_if_not_exist(save_path)
    csv_file = \
        open(file_path, 'w', newline='', encoding='utf-8')

    import csv

    column = [
        "date", "time", "name", "num",
        "target", "money", "pay_type", "status"
    ]
    writer = csv.writer(csv_file)
    writer.writerow(column)
    for data in list_consumption:
        writer.writerow(data)
    csv_file.close()
    print("文件写出完毕！")
