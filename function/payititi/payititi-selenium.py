# -*- coding: utf8 -*-
# python >=3.8

import json,time,os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.common.exceptions import NoAlertPresentException
from datetime import datetime
import requests
# from selenium.webdriver import ActionChains
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC

chrome_options = Options()
chrome_options.add_argument('--no-sandbox') # 解决DevToolsActivePort文件不存在的报错
chrome_options.add_argument('window-size=1920x1080') # 指定浏览器分辨率
chrome_options.add_argument('--disable-gpu') # 谷歌文档提到需要加上这个属性来规避bug
chrome_options.add_argument('--headless') # 浏览器不提供可视化页面. linux下如果系统不支持可视化不加这条会启动失败

def get_web_driver():
    chromedriver = "/usr/bin/chromedriver"
    os.environ["webdriver.chrome.driver"] = chromedriver
    driver = webdriver.Chrome(executable_path=chromedriver, options=chrome_options)
    driver.implicitly_wait(10) # 所有的操作都可以最长等待10s
    return driver


def getLastSignTime(browser, sendKey):
    signTime = browser.find_element(By.CLASS_NAME,  'px11')
    curDate = datetime.now().strftime('%Y-%m-%d')
    print(f'signTime:{signTime.text} curDate:{curDate}')
    if len(signTime.text) > 10 and signTime.text[0:10] == curDate :
        print(f'invoke pushNotification')
        pushNotification(sendKey, f"帕依提提自动签到", "【签到时间】{signTime.text}")

def autoSign(sendKey, user, password):
    browser = get_web_driver()
    print('selenium load web driver successfully')
    # browser = webdriver.Chrome()
    browser.get('https://www.payititi.com/member/login/?forward=https%3A%2F%2Fwww.payititi.com%2Fmember%2F')
    print('selenium load login page')

    try:
        browser.find_element(By.NAME, 'username').send_keys(user)
        browser.find_element(By.NAME, 'password').send_keys(password)
        browser.find_element(By.NAME, 'submit').click()
    finally:
        time.sleep(5)

    print('selenium click login button')
    h1 = browser.find_element(By.TAG_NAME, 'h1')
    print(f"login result:{h1.text}")
    # <h1>qinlicang，欢迎使用帕依提提</h1>

    # get cookies from selenium
    # cookies = browser.get_cookies()
    # for cookie in cookies:
    #     print(f'cookie:{cookie["name"]}:{cookie["value"]}')
        
    browser.get('https://www.payititi.com/member/credit/?action=qiandao')
    try:
        print('selenium click sign button')
        browser.find_element(By.CSS_SELECTOR, 'input[name="submit"][class="btn"]').click()
        time.sleep(1)
        getLastSignTime(browser, sendKey)

    except UnexpectedAlertPresentException as e:
        print('UnexpectedAlertPresentException:' + e.msg)
        if 'Alert' in str(e):
            try:
                # 进入窗口，获取窗口信息（获取信息后取消）
                alertTip = browser.switch_to.alert  # 切换到弹窗
                print(alertTip.text)
                # # 点击取消按钮
                # alertTip.dismiss()
                # 点击确定按钮
                alertTip.accept()
            except NoAlertPresentException as e:
                print('NoAlertPresentException:' + e.msg)
            finally:
                print('browser.switch_to.alert')

            getLastSignTime(browser, sendKey)
            print('getLastSignTime finished')

    browser.close()

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

    autoSign(sendKey, user, password)
