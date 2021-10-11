# BruteForce-phpmyadmin

暴力破解phpMyAdmin密码
***

## 免责声明

依据中华人民共和国网络安全法第二十七条：任何个人和组织不得从事非法侵入他人网络、干扰他人网络正常功能、窃取网络数据等危害网络安全的活动；不得提供专门用于侵入网络、干扰网络正常功能及防护措施、窃取网络数据等危害网络安全活动的程序、工具；明知他人从事危害网络安全的活动的不得为其提供技术支持、广告推广、支付结算等帮助。

使用本工具则默认遵守网络安全法
***

## 使用方法

新建urls.txt，存放目标网址，一个url一行。
user.txt和password.txt分别存放用户名和密码字典

### 脚本一：`bf.py`

采用发送post请求，获取响应的方式，速度较快，但受phpMyAdmin版本不同影响，适用性较差，结果不准确。

>python3 bf.py

结果保存在recheck.txt中，建议使用`recheck_chrome.py`或者手动复查

### 脚本二：`bf_chrome.py`

采用模拟chrome浏览器输入账号密码点击登录，需要[下载](http://npm.taobao.org/mirrors/chromedriver/)对应版本的webdriver放入python根目录。速度较慢，结果相对准确。

>python3 bf_chrome.py

结果保存在success.txt中。
