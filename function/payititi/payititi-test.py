# -*- coding: utf8 -*-
# python >=3.8

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# chrome_options = Options()
# chrome_options.add_argument('--no-sandbox') # 解决DevToolsActivePort文件不存在的报错
# chrome_options.add_argument('window-size=1920x1080') # 指定浏览器分辨率
# chrome_options.add_argument('--disable-gpu') # 谷歌文档提到需要加上这个属性来规避bug
# chrome_options.add_argument('--headless') # 浏览器不提供可视化页面. linux下如果系统不支持可视化不加这条会启动失败


if __name__ == "__main__":
    caps = webdriver.DesiredCapabilities.CHROME.copy() 
    caps['acceptInsecureCerts'] = True
    driver = webdriver.Chrome(desired_capabilities=caps)    
    driver = webdriver.Chrome()
    print('selenium load web driver successfully')
    driver.get('https://www.payititi.com')
    print(f'selenium load payititi page:{driver.title}')
