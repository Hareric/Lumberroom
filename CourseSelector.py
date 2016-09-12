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
from multiprocessing import Process,Manager,Lock,Pool

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
    postdata = urllib.urlencode(data)

    req = urllib2.Request(url='http://jxgl.gdufs.edu.cn/jsxsd/', headers=header)
    result = opener.open(req)
    print time.strftime("%Y-%m-%d %H:%M:%S"), '进程%i---->  选课系统主页' % pro_id
    html = result.read()
    print time.strftime("%Y-%m-%d %H:%M:%S"), '进程%i---->  准备登陆' % pro_id
    html = opener.open("http://jxgl.gdufs.edu.cn/jsxsd/xk/LoginToXkLdap", data=postdata).read()  # 登陆
    print time.strftime("%Y-%m-%d %H:%M:%S"), '进程%i---->  登陆成功' % pro_id
    html = opener.open("http://jxgl.gdufs.edu.cn/jsxsd/xsxk/xklc_list?Ves632DSdyV=NEW_XSD_PYGL").read()  #
    print time.strftime("%Y-%m-%d %H:%M:%S"), '进程%i---->  选课中心' % pro_id
    html = opener.open(
        "http://jxgl.gdufs.edu.cn/jsxsd/xsxk/xsxk_index?jx0502zbid=7F1363248E0D41438D19DE2681AC1CAA").read()  # 选课系统
    if '未开放' in html:
        print "当前未开放选课，具体请查看学校选课通知！ "
        assert False
    while "不在选课时间" in html:
        time.sleep(20)
        html = opener.open(
            "http://jxgl.gdufs.edu.cn/jsxsd/xsxk/xsxk_index?jx0502zbid=7F1363248E0D41438D19DE2681AC1CAA").read()  # 选课系统
        print "Again!!!"
        if 'loginUrl' in html:
            return 0
    print time.strftime("%Y-%m-%d %H:%M:%S"), '  学生选课首页'
    html = opener.open("http://jxgl.gdufs.edu.cn/jsxsd/xsxkkc/comeInXxxk").read()
    print time.strftime("%Y-%m-%d %H:%M:%S"), '  院系选修课首页'
    url_list = ["http://jxgl.gdufs.edu.cn/jsxsd/xsxkkc/xxxkOper?jx0404id=201620171008818",  # 接口
                # "http://jxgl.gdufs.edu.cn/jsxsd/xsxkkc/xxxkOper?jx0404id=201620171008766", # 软件工程
                # "http://jxgl.gdufs.edu.cn/jsxsd/xsxkkc/xxxkOper?jx0404id=201620171008867", # 图像 龚永义
                # "http://jxgl.gdufs.edu.cn/jsxsd/xsxkkc/xxxkOper?jx0404id=201620171008822", #图像 吴
                "http://jxgl.gdufs.edu.cn/jsxsd/xsxkkc/xxxkOper?jx0404id=201620171008826",  # 互联网程序设计
                "http://jxgl.gdufs.edu.cn/jsxsd/xsxkkc/xxxkOper?jx0404id=201620171008763"]  # 组网

    try_num = 0
    course_num = url_list.__len__()
    while True:
        time.sleep(0.025)
        try:
            index = try_num % course_num
            html = opener.open(url_list[index]).read()
            try_num += 1
        except:
            print 'Time out'
            continue
        if 'loginUrl' in html:
            return 0
        pattern = '"message":"(.*?)"'
        if '"message":"选课' in html:
            sys.stdout.write(
                '\r进程%i---->第%i次尝试  ' % (pro_id, try_num) + time.strftime("%Y-%m-%d %H:%M:%S") + "  " + re.search(pattern, html).group(1))
            sys.stdout.flush()
        else:
            sys.stdout.write('\r' + time.strftime("%Y-%m-%d %H:%M:%S") + "     " + html)
            sys.stdout.flush()
        if "此课程已选" in html:
            print "选课成功！"
            url_list.pop(index)
            course_num = url_list.__len__()


if __name__ == '__main__':

    # while True:
    #     if login('2014###', '###') == 0:  # 输入帐号密码
    #         continue
    #     else:
    #         break
    p = Pool(processes=10)
    for i in range(10):
        p.apply_async(login, ['2014####', '####', i])
    p.close()
    p.join()
