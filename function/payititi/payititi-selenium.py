# -*- coding: utf8 -*-
# python >=3.8

import json,time,os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.common.exceptions import NoAlertPresentException
from datetime import datetime
import requests
# from selenium.webdriver import ActionChains
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC

options = Options()
options.add_argument('--disable-dev-shm-usage') # 在某些VM环境中，/dev/shm分区太小，导致Chrome发生故障或崩溃（请参阅）。 使用此标志解决此问题（临时目录将始终用于创建匿名共享内存文件）
options.add_argument('--no-sandbox') # 对通常为沙盒的所有进程类型禁用沙盒。
options.add_argument('window-size=1920x1080') # 指定浏览器分辨率
options.add_argument('--disable-gpu') # 谷歌文档提到需要加上这个属性来规避bug
options.add_argument('--headless') # 浏览器不提供可视化页面. linux下如果系统不支持可视化不加这条会启动失败
options.add_argument('--hide-scrollbars') #隐藏滚动条, 应对一些特殊页面
options.add_argument('blink-settings=imagesEnabled=false') #不加载图片, 提升速度

# --no-first-run：跳过“首次运行”任务，无论它实际上是否是“首次运行”。 会被kForceFirstRun参数覆盖。这不会删除“首次运行”步骤，因此也不能防止在没有此标志的情况下下次启动chrome时发生首次运行。
# --start-maximized：无论以前的任何设置如何，都以最大化（全屏）的方式启动浏览器。
# --user-data-dir：浏览器存储用户配置文件的目录。
# --disable-software-rasterizer：禁止使用3D软件光栅化器。
# options.add_argument(‘headless’) # 无头模式
# options.add_argument(‘window-size={}x{}’.format(width, height)) # 直接配置大小和set_window_size一样
# options.add_argument(‘disable-gpu’) # 禁用GPU加速
# options.add_argument(‘proxy-server={}’.format(self.proxy_server)) # 配置代理
# options.add_argument(’–no-sandbox’) # 沙盒模式运行
# options.add_argument(’–disable-setuid-sandbox’) # 禁用沙盒
# options.add_argument(’–disable-dev-shm-usage’) # 大量渲染时候写入/tmp而非/dev/shm
# options.add_argument(’–user-data-dir={profile_path}’.format(profile_path)) # 用户数据存入指定文件
# options.add_argument('no-default-browser-check) # 不做浏览器默认检查
# options.add_argument("–disable-popup-blocking") # 允许弹窗
# options.add_argument("–disable-extensions") # 禁用扩展
# options.add_argument("–ignore-certificate-errors") # 忽略不信任证书
# options.add_argument("–no-first-run") # 初始化时为空白页面
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


# def get_web_driver():
#     chromedriver = "/usr/bin/chromedriver"
#     os.environ["webdriver.chrome.driver"] = chromedriver
#     driver = webdriver.Chrome(executable_path=chromedriver, options=options)
#     driver.implicitly_wait(10) # 所有的操作都可以最长等待10s
#     return driver


def getLastSignTime(browser, sendKey):
    signTime = browser.find_element(By.CLASS_NAME,  'px11')
    curDate = datetime.now().strftime('%Y-%m-%d')
    print(f'signTime:{signTime.text} curDate:{curDate}')
    if len(signTime.text) > 10 and signTime.text[0:10] == curDate :
        print(f'invoke pushNotification')
        pushNotification(sendKey, "帕依提提自动签到", f"签到时间:{signTime.text}")

def autoSign(sendKey, user, password):
    print('webdriver.Chrome before')
    browser = webdriver.Chrome(options=options)
    print('webdriver.Chrome successfully')
    browser.get('https://www.payititi.com/member/login/?forward=https%3A%2F%2Fwww.payititi.com%2Fmember%2F')
    print('selenium load login page')

    try:
        browser.find_element(By.NAME, 'username').send_keys(user)
        browser.find_element(By.NAME, 'password').send_keys(password)
        browser.find_element(By.NAME, 'submit').click()
        time.sleep(5)

        # print('selenium click login button')
        # h1 = browser.find_element(By.TAG_NAME, 'h1')
        # print(f"login result:{h1.text}")
        # <h1>qinlicang，欢迎使用帕依提提</h1>

        # get cookies from selenium
        # cookies = browser.get_cookies()
        # for cookie in cookies:
        #     print(f'cookie:{cookie["name"]}:{cookie["value"]}')
            
        browser.get('https://www.payititi.com/member/credit/?action=qiandao')
        time.sleep(5)

        print(f'selenium sign page title:{browser.title} click sign button')
        signButton = browser.find_element(By.XPATH, '//*[@id="dform"]/table/tbody/tr[3]/td[2]/input')
        print('selenium find sign button by xpath successfully')
        signButton.click()
        print('selenium sign button click successfully')

        # browser.find_element(By.CSS_SELECTOR, 'input[type="submit"][name="submit"][class="btn"]').click()
        # print('selenium find sign button by CSS_SELECTOR successfully')
        time.sleep(5)
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

    autoSign(sendKey, user, password)
