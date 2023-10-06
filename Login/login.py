import time

from selenium.webdriver.common.by import By

url_portal = r"https://portal.shmtu.edu.cn/"


def login(driver, user_id="", user_pwd=""):
    driver.get(url_portal)

    elem_id = driver.find_element(By.CSS_SELECTOR, "#username")
    # elem_id = driver.find_element(By.ID, "username")
    elem_id.send_keys(user_id)
    elem_pwd = driver.find_element(By.ID, "password")
    elem_pwd.send_keys(user_pwd)

    while driver.current_url.find('https://portal.shmtu.edu.cn/node') == -1:
        # 没有成功跳转，那就等待1秒后继续检测
        time.sleep(1)
