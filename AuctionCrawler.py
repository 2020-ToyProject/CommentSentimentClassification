from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.common.keys import  Keys

driver = webdriver.Chrome("./libnative/chromedriver")
try:

    driver.get('http://browse.auction.co.kr/search?keyword=%eb%8b%ad%ea%b0%80%ec%8a%b4%ec%82%b4&itemno=&nickname=&frm'
               '=hometab&dom=auction&isSuggestion=No&retry=&Fwk=%eb%8b%ad%ea%b0%80%ec%8a%b4%ec%82%b4&acode=SRP_SU_0100'
               '&arraycategory=&encKeyword=%eb%8b%ad%ea%b0%80%ec%8a%b4%ec%82%b4&s=8')
    time.sleep(5)

    # 아이템 리스트 XPath
    elements = driver.find_elements_by_xpath('//span[@class="text--itemcard_title ellipsis"]')

    urls = []

    # 한 페이지에 100개정도의 아이템이 넘어온다.
    for element in elements:
        ele = element.find_element_by_xpath('./a')
        urls.append(ele.get_attribute("href"))

    print(len(urls))
except Exception as e:
    print(e)
finally:
    driver.close()




