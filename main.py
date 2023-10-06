import os
import time
import configparser
import json

from selenium.webdriver.common.by import By

from selenium import webdriver

from selenium.webdriver.chrome.service import Service as ChromeService
# import webdriver-manager
from webdriver_manager.chrome import ChromeDriverManager

from Login.login import login
from BillExport import bill
from Utils import path

# 获取当前目录
current_path = os.path.dirname(os.path.abspath(__file__))
workdir_path = os.path.join(current_path, "workdir")
path.create_dir_if_not_exist(workdir_path)

if __name__ == "__main__":
    option = webdriver.ChromeOptions()
    # option.add_argument('headless')

    driver = \
        webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()),
            options=option
        )

    # 读取配置文件
    config = configparser.ConfigParser()
    config.read(r"../shmtu_num_pwd.numpwd")

    # 读取账号密码
    user_id = config["User"]["id"]
    user_pwd = config["User"]["pwd"]
    print(user_id, user_pwd)

    # 执行登录相关流程
    login(
        driver=driver,
        user_id=user_id,
        user_pwd=user_pwd
    )

    bills_dir_path = os.path.join(workdir_path, "bills")
    path.create_dir_if_not_exist(bills_dir_path)
    # 获取账单
    bill.get_bill(
        driver=driver,
        save_path=bills_dir_path
    )
