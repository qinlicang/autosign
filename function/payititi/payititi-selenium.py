# -*- coding: utf8 -*-
# python >=3.8

import json,time,os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.support.wait import WebDriverWait
from datetime import datetime
import requests
from bs4 import BeautifulSoup

# from selenium.webdriver import ActionChains
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support import expected_conditions as EC

options = Options()
options.add_argument('--disable-dev-shm-usage') # 在某些VM环境中，/dev/shm分区太小，导致Chrome发生故障或崩溃（请参阅）。 使用此标志解决此问题（临时目录将始终用于创建匿名共享内存文件）
options.add_argument('--no-sandbox') # 沙盒模式运行 对通常为沙盒的所有进程类型禁用沙盒。
options.add_argument('window-size=1920x1080') # 指定浏览器分辨率
options.add_argument('--disable-gpu') # 禁用GPU加速 谷歌文档提到需要加上这个属性来规避bug
options.add_argument('--headless') # 浏览器不提供可视化页面. linux下如果系统不支持可视化不加这条会启动失败
options.add_argument('--hide-scrollbars') #隐藏滚动条, 应对一些特殊页面
options.add_argument("–no-first-run") # 初始化时为空白页面
# options.add_argument('blink-settings=imagesEnabled=false') #不加载图片, 提升速度

# options.add_argument(‘window-size={}x{}’.format(width, height)) # 直接配置大小和set_window_size一样
# options.add_argument(‘proxy-server={}’.format(self.proxy_server)) # 配置代理
# options.add_argument(’–disable-setuid-sandbox’) # 禁用沙盒
# options.add_argument(’–disable-dev-shm-usage’) # 大量渲染时候写入/tmp而非/dev/shm
# options.add_argument(’–user-data-dir={profile_path}’.format(profile_path)) # 用户数据存入指定文件
# options.add_argument('no-default-browser-check) # 不做浏览器默认检查
# options.add_argument("–disable-popup-blocking") # 允许弹窗
# options.add_argument("–disable-extensions") # 禁用扩展
# options.add_argument("–ignore-certificate-errors") # 忽略不信任证书
# options.add_argument(’–start-maximized’) # 最大化启动
# options.add_argument(’–disable-notifications’) # 禁用通知警告
# options.add_argument(’–enable-automation’) # 通知(通知用户其浏览器正由自动化测试控制)
# options.add_argument(’–disable-xss-auditor’) # 禁止xss防护
# options.add_argument(’–disable-web-security’) # 关闭安全策略
# options.add_argument(’–allow-running-insecure-content’) # 允许运行不安全的内容
# options.add_argument(’–disable-webgl’) # 禁用webgl
# options.add_argument(’–homedir={}’) # 指定主目录存放位置
# options.add_argument(’–disk-cache-dir={临时文件目录}’) # 指定临时文件目录
# options.add_argument(‘disable-cache’) # 禁用缓存
# options.add_argument(‘excludeSwitches’, [‘enable-automation’]) # 开发者模式
headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    "Content-Type": "application/x-www-form-urlencoded",
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
session = requests.session()

def logout():
    url = "https://www.payititi.com/member/logout.php"
    resp = session.get(url, headers=headers)
    if resp.status_code == 302 or resp.status_code == 200:
        return True
    return False

def login(user, password):
    url = "https://www.payititi.com/member/login/?"
    data = {
        "forward": "https%3A%2F%2Fwww.payititi.com%2Fmember%2F",
        "action": "login",
        "auth": "",
        "username": user,
        "password": password,
        "submit": "%E7%99%BB+%E5%BD%95"
    }

    print('login before', session.cookies)
    resp = session.post(url, data=data, headers=headers)
    print(f'login after Cookies:{session.cookies} resp:{resp.content}')
    # cookies.update(resp.cookies) # 保存cookie
    # page = BeautifulSoup(resp.text, 'html.parser')
    # tags = page.find_all('h1')
    # for tag in tags:
    #     if tag.text == 'qinlicang，欢迎使用帕依提提':
    #         return True
    # return False
    return True

def getLastSignTime(browser, sendKey):
    signTime = browser.find_element(By.CLASS_NAME,  'px11')
    curDate = datetime.now().strftime('%Y-%m-%d')
    print(f'signTime:{signTime.text} curDate:{curDate}')
    if len(signTime.text) > 10 and signTime.text[0:10] == curDate :
        print(f'invoke pushNotification')
        pushNotification(sendKey, "帕依提提自动签到", f"签到时间:{signTime.text}")

def autoSign(sendKey, user, password):
    try:
        print('webdriver.Chrome before')
        browser = webdriver.Chrome(options=options)
        print('webdriver.Chrome successfully')
        browser.get('https://www.payititi.com/member/login/?forward=https%3A%2F%2Fwww.payititi.com%2Fmember%2F')
        # time.sleep(5)
        print(f'selenium login page title:{browser.title}')

        unloginTitle = browser.title

        browser.find_element(By.NAME, 'username').send_keys(user)
        browser.find_element(By.NAME, 'password').send_keys(password)
        # browser.find_element(By.NAME, 'submit').click()
        loginButton = browser.find_element(By.XPATH, '//*[@id="signin-form"]/div[3]/form/input[4]')
        loginButton.click()
        # time.sleep(5)
        # print(f'loginButton:{loginButton.get_attribute("innerHTML")}')
        # loginDiv = browser.find_element(By.XPATH, '//*[@id="signin-form"]')
        # print(f'loginDiv:{loginDiv.get_attribute("innerHTML")}')

        print(f'selenium logined page title:{browser.title}')
        if unloginTitle == browser.title:
            login(user, password)

        # browser.save_screenshot("./logined.png")

        # print('selenium click login button')
        # h1 = browser.find_element(By.TAG_NAME, 'h1')
        # print(f"login result:{h1.text}")
        # <h1>qinlicang，欢迎使用帕依提提</h1>

        # get cookies from selenium
        # cookies = browser.get_cookies()
        # for cookie in cookies:
        #     print(f'cookie:{cookie["name"]}:{cookie["value"]}')
        
        browser.get('https://www.payititi.com/member/credit/?action=qiandao')
        # time.sleep(5)
        print(f'selenium sign page title:{browser.title}')

        # signButton = browser.find_element(By.XPATH, '//*[@id="dform"]/table/tbody/tr[3]/td[2]/input')
        # print('selenium find sign button by xpath successfully')
        # signButton.click()
        # print('selenium sign button click successfully')
        # formTable = browser.find_element(By.CSS_SELECTOR, 'div[class="bd"]')
        # print(f'sign list table:{formTable.get_attribute("innerHTML")}')

        signButton = browser.find_element(By.CSS_SELECTOR, 'input[type="submit"][name="submit"][class="btn"]')
        signButton.click()
        print(f'selenium sign page title:{browser.title} click successfully')
        print(f'signButton:{signButton.get_attribute("innerHTML")}')

        # time.sleep(5)
        getLastSignTime(browser, sendKey)

    except UnexpectedAlertPresentException as e:
        print('UnexpectedAlertPresentException:' + e.msg)
        if 'Alert' in str(e):
            getLastSignTime(browser, sendKey)
        #     try:
        #         # 进入窗口，获取窗口信息（获取信息后取消）
        #         alertTip = browser.switch_to.alert  # 切换到弹窗
        #         print(alertTip.text)
        #         # # 点击取消按钮
        #         # alertTip.dismiss()
        #         # 点击确定按钮
        #         alertTip.accept()
        #     except NoAlertPresentException as e:
        #         print('NoAlertPresentException:' + e.msg)
        #     finally:
        #         print('browser.switch_to.alert')
    except NoSuchElementException as e:
        print('NoSuchElementException:' + e.msg)
    finally:
        browser.close()
        browser.quit()
        print('selenium browser quit')

def pushNotification(sendKey, title, content):
    url = 'https://sctapi.ftqq.com/' + sendKey + '.send'
    data = {
        'title': title,
        'desp': content,
        'channel':'9'
    }

    print(f'pushNotification request: url:{url} data:{data}')
    resp = json.dumps(requests.post(url, data).json(), ensure_ascii=False)
    print('pushNotification response:' + resp)
    respData = json.loads(resp)
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
    # sendKey = "SCT218351TZ85R81jSICq5lvWiMK7RsWdq"

    logout()
    autoSign(sendKey, user, password)
