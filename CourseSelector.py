# coding=utf-8
"""
Author0 = K
Author1 = Eric Chan
CreateTime = 2016.7.2
"""

import urllib
import urllib2
import cookielib
import time
import re
import sys
from multiprocessing import Pool


def login(username, password, pro_id):
    # 初始化一个CookieJar来处理Cookie的信息
    cookie = cookielib.CookieJar()
    # 建一个新的opener来使用我们的CookieJar
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
    header = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Connection': 'keep-alive',
        'Host': 'jxgl.gdufs.edu.cn',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/47.0.2526.106 Safari/537.36'
    }
    data = {
        'USERNAME': username,
        'PASSWORD': password
    }
    post_data = urllib.urlencode(data)

    req = urllib2.Request(url='http://jxgl.gdufs.edu.cn/jsxsd/', headers=header)
    result = opener.open(req)
    print time.strftime("%Y-%m-%d %H:%M:%S"), '进程%i---->  选课系统主页' % pro_id
    html = result.read()
    print time.strftime("%Y-%m-%d %H:%M:%S"), '进程%i---->  准备登陆' % pro_id
    html = opener.open("http://jxgl.gdufs.edu.cn/jsxsd/xk/LoginToXkLdap", data=post_data).read()  # 登陆
    print time.strftime("%Y-%m-%d %H:%M:%S"), '进程%i---->  登陆成功' % pro_id

    # 选课的网址 每年更新 需手动修改
    html = opener.open(
        "http://jxgl.gdufs.edu.cn/jsxsd/xsxk/xsxk_index?jx0502zbid=5EBAB7201F344576A0FF03EA7F833ED2").read()  # 选课系统

    # 选修的课程的url 需手动修改
    url_list = ["http://jxgl.gdufs.edu.cn/jsxsd/xsxkkc/ggxxkxkOper?jx0404id=201620172011063&xkzy=&trjf=",
                "http://jxgl.gdufs.edu.cn/jsxsd/xsxkkc/ggxxkxkOper?jx0404id=201620172010785&xkzy=&trjf=",
                "http://jxgl.gdufs.edu.cn/jsxsd/xsxkkc/ggxxkxkOper?jx0404id=201620172010833&xkzy=&trjf=",
                "http://jxgl.gdufs.edu.cn/jsxsd/xsxkkc/ggxxkxkOper?jx0404id=201620172010828&xkzy=&trjf="
                ]
    try_num = 0
    course_num = url_list.__len__()
    while True:
        if course_num == 0:
            break
        time.sleep(0.025)
        try:
            index = try_num % course_num
            html = opener.open(url_list[index]).read()
            try_num += 1
        except:
            continue
        if 'loginUrl' in html:
            return 0
        pattern = '"message":"(.*?)"'
        if '"message"' in html:
            sys.stdout.write(
                '\r进程%i---->第%i次尝试  ' % (pro_id, try_num) + time.strftime("%Y-%m-%d %H:%M:%S") + "  " + re.search(
                    pattern, html).group(1))
            sys.stdout.flush()
        else:
            sys.stdout.write('\r' + time.strftime("%Y-%m-%d %H:%M:%S") + "     " + html)
            sys.stdout.flush()
        if "此课程已选" in html or "最多只能选" in html:
            print "选课成功！"
            url_list.pop(index)
            course_num = url_list.__len__()


if __name__ == '__main__':
    pool_num = 8  # 进程数 根据电脑配置自行修改
    p = Pool(processes=pool_num)
    for i in range(pool_num):
        p.apply_async(login, ['学号', '密码', i])
    p.close()
    p.join()
