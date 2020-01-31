from selenium import webdriver
from selenium.webdriver.common.keys import  Keys

driver = webdriver.Chrome("./libnative/chromedriver")
driver.get('http://www.naver.com')

driver.quit()

