# -*- coding: utf8 -*-
# python >=3.8

import json,time,os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.common.exceptions import NoAlertPresentException
from datetime import datetime

def getLastSignTime(browser):
    signTime = browser.find_element(By.CLASS_NAME,  'px11')
    print(f'signTime:{signTime.text}')
    curDate = datetime.now().strftime('%Y-%m-%d')
    if len(signTime.text) > 10 and signTime.text[0:10] == curDate :
        pushNotification(sendKey, "帕依提提自动签到", "【签到结果】完成")

def autoSign(_user, _password):
    browser = webdriver.Chrome()
    browser.get('https://www.payititi.com/member/login/?forward=https%3A%2F%2Fwww.payititi.com%2Fmember%2F')

    try:
        browser.find_element(By.NAME, 'username').send_keys('qinlicang')
        browser.find_element(By.NAME, 'password').send_keys('Qinlc770401')
        browser.find_element(By.NAME, 'submit').click()
    finally:
        time.sleep(5)

    h1 = browser.find_element(By.TAG_NAME, 'h1')
    print(f"login:{h1.text}")
    # <h1>qinlicang，欢迎使用帕依提提</h1>

    # get cookies from selenium
    cookies = browser.get_cookies()
    for cookie in cookies:
        print(f'cookie:{cookie["name"]}:{cookie["value"]}')
        
    browser.get('https://www.payititi.com/member/credit/?action=qiandao')
    try:
        browser.find_element(By.CSS_SELECTOR, 'input[name="submit"][class="btn"]').click()
        time.sleep(1)
        getLastSignTime(browser)

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

            getLastSignTime(browser)
            print('getLastSignTime finished')

    browser.close()

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
    # sendKey = "SCT218351TZ85R81jSICq5lvWiMK7RsWdq"

    autoSign(user, password)
    
