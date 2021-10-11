#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import time
import urllib3
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from concurrent.futures import ThreadPoolExecutor

urllib3.disable_warnings()


def recheck(url, username, password):
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # 启用headless模式，不显示浏览器界面
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_experimental_option('excludeSwitches', ['enable-automation',
                                                               'enable-logging'])  # 去除“chrome正受到自动测试软件的控制”提示,去除chromedriver的日志打印
    chrome_options.add_argument('--ignore-certificate-errors')  # 消除“不是私密连接”错误
    browser = webdriver.Chrome(options=chrome_options)
    browser.get(url)
    user_tag = browser.find_element_by_name("pma_username")
    pass_tag = browser.find_element_by_name("pma_password")
    user_tag.send_keys(username)
    pass_tag.send_keys(password)
    browser.find_element_by_id("input_go").click()
    time.sleep(2)  # 等待网页加载完
    try:
        username_tag = browser.find_element_by_name("pma_username")
        print(url + "\t" + username + "\t" + password + "失败")
    except:
        with open("success.txt", "a", encoding='utf-8') as f1:
            f1.write(url + "  |  " + username + "  |  " + password + "\n")
        print(url + "\t" + username + "\t" + password + "成功")
        return True
    finally:
        browser.quit()


pool = ThreadPoolExecutor(max_workers=1)  # 设置线程池大小

if __name__ == '__main__':
    for line in open("recheck.txt"):
        url, username, password = line.strip().split("  |  ")
        pool.submit(recheck, url, username, password)
