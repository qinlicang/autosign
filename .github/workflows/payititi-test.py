# -*- coding: utf8 -*-
# python >=3.8

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

if __name__ == "__main__":
    caps = webdriver.DesiredCapabilities.CHROME.copy() 
    caps['acceptInsecureCerts'] = True
    driver = webdriver.Chrome(desired_capabilities=caps)    
    driver = webdriver.Chrome()
    print('selenium load web driver successfully')
    driver.get('https://www.payititi.com')
    print(f'selenium load payititi page:{driver.title}')
