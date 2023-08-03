# -*- coding: utf8 -*-
# python >=3.8

import json,time,random,re,sys,os
from urllib.parse import quote
import requests
from bs4 import BeautifulSoup

session = requests.session()

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    "Content-Type": "application/x-www-form-urlencoded",
    # "Cookie": "filemanager=4hnj0rgoq0jefm47b6jnipvhv0; Hm_lvt_bb30997862cf435b1de95fb082db233b=1690794103; PHPSESSID=9qblkug6kl753o62t4omrclm15; Dor_last_search=1690795404; Hm_lpvt_bb30997862cf435b1de95fb082db233b=1690873770",
    "Host": "www.payititi.com",
    "Origin": "https://www.payititi.com",
    "Referer": "https://www.payititi.com/member/login/?forward=https%3A%2F%2Fwww.payititi.com%2Fmember%2F",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "sec-ch-ua": "\"Not.A/Brand\";v=\"8\", \"Chromium\";v=\"114\", \"Google Chrome\";v=\"114\"",
    "sec-ch-ua-platform": "macOS"
}

# 获取登录code
def get_code(location):
    code_pattern = re.compile("(?<=access=).*?(?=&)")
    code = code_pattern.findall(location)[0]
    return code

def logout():
    url = "https://www.payititi.com/member/logout.php?forward="
    resp = session.get(url, headers=headers)
    if resp.status_code == 302 or resp.status_code == 200:
        return True
    return False

def login(_user, _password):
    url = "https://www.payititi.com/member/login/?"
    data = {
        "forward": "https%3A%2F%2Fwww.payititi.com%2Fmember%2F",
        "action": "login",
        "auth": "",
        "username": _user,
        "password": _password,
        "submit": "%E7%99%BB+%E5%BD%95"
    }
    resp = session.post(url, data=data, headers=headers)
    # cookies.update(resp.cookies) # 保存cookie
    page = BeautifulSoup(resp.text, 'html.parser')
    tags = page.find_all('h1')
    # for tag in tags:
    #     if tag.text == 'qinlicang，欢迎使用帕依提提':
    #         return True
    # return False
    return True

def getSignList():
    url = "https://www.payititi.com/member/credit/?action=qiandao"
    resp = session.get(url, headers=headers)
    page = BeautifulSoup(resp.text, 'html.parser')
    # td class="tab" id="action_qiandao"
    sign_action = page.find_all("td", attrs={"class": "tab", "id": "action_qiandao"})
    if(sign_action != None):
        return True
    return False

def autoSign():
    url = "https://www.payititi.com/member/credit"
    data = {
        'action': 'qiandao',
        'submit': '1',
        'title': '%E6%8C%89%E6%97%B6%E7%AD%BE%E5%88%B0%E6%98%AF%E4%B8%AA%E5%A5%BD%E4%B9%A0%E6%83%AF%5E_%5E+%E7%AD%BE%E5%88%B0%E6%8B%BF%E5%88%86%E8%B5%B0%E4%BA%BA',
        'submit': '+%E7%82%B9%E5%87%BB%E7%AD%BE%E5%88%B0+'
    }
    resp = session.post(url, data=data, headers=headers)
    print('autosign resp:' + resp.text)

def pushNotification(sendKey, title, content):
    url = 'https://sctapi.ftqq.com/' + sendKey + '.send'
    data = {
        'title': title,
        'desp': content,
        'channel':'9'
    }
    resp = json.dumps(requests.post(url, data).json(), ensure_ascii=False)
    respData = json.loads(resp)
    print(resp)
    if respData['code'] == 0:
        print(f'server酱发送通知消息成功, pushid:{respData["data"]["pushid"]} readkey:{respData["data"]["readkey"]}')
    elif respData['code'] == 40001:
        print('server酱SEND_KEY错误')
    else:
        print('server酱发送通知失败')

if __name__ == "__main__":
    user = os.environ['PAYITITI_USER']
    password = os.environ['PAYITITI_PASSWORD']
    sendKey = os.environ['SEND_KEY']
    # user = "qinlicang"
    # password = "Qinlc770401"

    login(user, password)
    if getSignList():
        print('click sign')
        autoSign()
        pushNotification(sendKey, "帕依提提自动签到", "【签到结果】完成")


# 登录
# https://www.payititi.com/member/login/?

# data
# forward=https%3A%2F%2Fwww.payititi.com%2Fmember%2F&action=login&auth=&username=qinlicang&password=Qinlc770401&submit=%E7%99%BB+%E5%BD%95

# request headers
# POST /member/login/ HTTP/1.1
# Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
# Accept-Encoding: gzip, deflate, br
# Accept-Language: zh-CN,zh;q=0.9
# Cache-Control: max-age=0
# Connection: keep-alive
# Content-Length: 136
# Content-Type: application/x-www-form-urlencoded
# Cookie: filemanager=4hnj0rgoq0jefm47b6jnipvhv0; Hm_lvt_bb30997862cf435b1de95fb082db233b=1690794103; PHPSESSID=9qblkug6kl753o62t4omrclm15; Dor_last_search=1690795404; Hm_lpvt_bb30997862cf435b1de95fb082db233b=1690873770
# Host: www.payititi.com
# Origin: https://www.payititi.com
# Referer: https://www.payititi.com/member/login/?forward=https%3A%2F%2Fwww.payititi.com%2Fmember%2F
# Sec-Fetch-Dest: document
# Sec-Fetch-Mode: navigate
# Sec-Fetch-Site: same-origin
# Sec-Fetch-User: ?1
# Upgrade-Insecure-Requests: 1
# User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36
# sec-ch-ua: "Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"
# sec-ch-ua-mobile: ?0
# sec-ch-ua-platform: "macOS"

# response headers
# HTTP/1.1 302 Moved Temporarily
# Server: nginx/1.9.9
# Date: Tue, 01 Aug 2023 07:09:35 GMT
# Content-Type: text/html;charset=UTF-8
# Transfer-Encoding: chunked
# Connection: keep-alive
# X-Powered-By: PHP/5.4.16
# Set-Cookie: Dor_auth=d21cLHgh4uRlQqg1rvfTpLcRCX91LVxSKKEya-S-8ALJifMvfL0vPsAVKKks-S-G40GVSrvCzzppaK6OSWWS1ZACyjSCE4isV4vn; expires=Fri, 11-Aug-2023 07:09:35 GMT; path=/; domain=.payititi.com; secure
# Set-Cookie: Dor_username=qinlicang; expires=Thu, 31-Aug-2023 07:09:35 GMT; path=/; domain=.payititi.com; secure
# location: https://www.payititi.com/member/


# 打开每日签到网页
# https://www.payititi.com/member/credit/?action=qiandao

# request headers
# GET /member/credit/?action=qiandao HTTP/1.1
# Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
# Accept-Encoding: gzip, deflate, br
# Accept-Language: zh-CN,zh;q=0.9
# Cache-Control: max-age=0
# Connection: keep-alive
# Cookie: filemanager=4hnj0rgoq0jefm47b6jnipvhv0; Hm_lvt_bb30997862cf435b1de95fb082db233b=1690794103; PHPSESSID=9qblkug6kl753o62t4omrclm15; Dor_last_search=1690795404; Dor_auth=d21cLHgh4uRlQqg1rvfTpLcRCX91LVxSKKEya-S-8ALJifMvfL0vPsAVKKks-S-G40GVSrvCzzppaK6OSWWS1ZACyjSCE4isV4vn; Dor_username=qinlicang; Hm_lpvt_bb30997862cf435b1de95fb082db233b=1690874629
# Host: www.payititi.com
# Sec-Fetch-Dest: document
# Sec-Fetch-Mode: navigate
# Sec-Fetch-Site: none
# Sec-Fetch-User: ?1
# Upgrade-Insecure-Requests: 1
# User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36
# sec-ch-ua: "Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"
# sec-ch-ua-mobile: ?0
# sec-ch-ua-platform: "macOS"

# 查找签到按钮
# <td class="tab" id="action_qiandao"><a href="?action=qiandao"><span>每日签到</span></a></td>


# 调用签到
# https://www.payititi.com/member/credit

# 请求头
# POST /member/credit/ HTTP/1.1
# Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
# Accept-Encoding: gzip, deflate, br
# Accept-Language: zh-CN,zh;q=0.9
# Cache-Control: max-age=0
# Connection: keep-alive
# Content-Length: 219
# Content-Type: application/x-www-form-urlencoded
# Cookie: filemanager=4hnj0rgoq0jefm47b6jnipvhv0; Hm_lvt_bb30997862cf435b1de95fb082db233b=1690794103; PHPSESSID=9qblkug6kl753o62t4omrclm15; Dor_auth=d575q5iTBYFp5JT9tZ2EcIjrKlGP6Je190J-S-h4Z9sbYt5oBye4db-X--S-bw9GfjhOsENtZ7ItuKqtSg-P-y5o2ycCrcGbYusbmoC; Dor_username=qinlicang; Dor_last_search=1690795404; Hm_lpvt_bb30997862cf435b1de95fb082db233b=1690856028
# Host: www.payititi.com
# Origin: https://www.payititi.com
# Referer: https://www.payititi.com/member/credit/?action=qiandao
# Sec-Fetch-Dest: document
# Sec-Fetch-Mode: navigate
# Sec-Fetch-Site: same-origin
# Sec-Fetch-User: ?1
# Upgrade-Insecure-Requests: 1
# User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36
# sec-ch-ua: "Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"
# sec-ch-ua-mobile: ?0
# sec-ch-ua-platform: "macOS"

# cookies
# filemanager	4hnj0rgoq0jefm47b6jnipvhv0
# Hm_lvt_bb30997862cf435b1de95fb082db233b	1690794103	.payititi.com	/	2024-07-31T02:13:47.000Z
# PHPSESSID	9qblkug6kl753o62t4omrclm15
# Dor_auth	d575q5iTBYFp5JT9tZ2EcIjrKlGP6Je190J-S-h4Z9sbYt5oBye4db-X--S-bw9GfjhOsENtZ7ItuKqtSg-P-y5o2ycCrcGbYusbmoC	.payititi.com	/	2023-08-10T09:22:31.231
# Dor_username	qinlicang	.payititi.com	/	2023-08-30T09:22:31.231Z
# Dor_last_search	1690795404	.payititi.com
# Hm_lpvt_bb30997862cf435b1de95fb082db233b	1690856028

