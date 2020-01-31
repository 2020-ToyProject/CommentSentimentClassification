from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.common.keys import  Keys

driver = webdriver.Chrome("./libnative/chromedriver.exe")
try:

    driver.get('http://browse.auction.co.kr/search?keyword=%eb%8b%ad%ea%b0%80%ec%8a%b4%ec%82%b4&itemno=&nickname=&frm'
               '=hometab&dom=auction&isSuggestion=No&retry=&Fwk=%eb%8b%ad%ea%b0%80%ec%8a%b4%ec%82%b4&acode=SRP_SU_0100'
               '&arraycategory=&encKeyword=%eb%8b%ad%ea%b0%80%ec%8a%b4%ec%82%b4&s=8')
    time.sleep(5)

    elements = driver.find_element_by_xpath(By.XPATH, '//span[@class="text--itemcard_title ellipsis"]')

    for element in elements:
        ele = element.find_element_by_xpath(By.XPATH, './a')
        print(ele.get_attribute("href"))
except:
    print(x)
finally:
    driver.close()




