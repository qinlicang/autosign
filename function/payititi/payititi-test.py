# -*- coding: utf8 -*-
# python >=3.8

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

if __name__ == "__main__":
    chrome_options = Options()
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--no-sandbox') # 解决DevToolsActivePort文件不存在的报错
    chrome_options.add_argument('window-size=1920x1080') # 指定浏览器分辨率
    chrome_options.add_argument('--disable-gpu') # 谷歌文档提到需要加上这个属性来规避bug
    chrome_options.add_argument('--headless') # 浏览器不提供可视化页面. linux下如果系统不支持可视化不加这条会启动失败

    chrome_options.add_argument('--hide-scrollbars') #隐藏滚动条, 应对一些特殊页面
    chrome_options.add_argument('blink-settings=imagesEnabled=false') #不加载图片, 提升速度


    # chromedriver = "/usr/bin/chromedriver"
    print('webdriver.Chrome before')
    driver = webdriver.Chrome(options=chrome_options) # executable_path=chromedriver, 
    print('webdriver.Chrome successfully')
    driver.get('https://www.baidu.com')
    print(f'selenium load baidu page:{driver.title}')
    time.sleep(5)
    # driver.close()
    driver.quit()
    print('driver.quit successfully')
