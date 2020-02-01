from selenium import webdriver
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome("./libnative/chromedriver.exe")
try:
    urls = []

    for idx in range(0, 1):
        print(idx)
        url = 'http://browse.auction.co.kr/search?keyword=%eb%8b%ad%ea%b0%80%ec%8a%b4%ec%82%b4&itemno=&nickname=&frm=hometab&dom=auction&isSuggestion=No&retry=&Fwk=%eb%8b%ad%ea%b0%80%ec%8a%b4%ec%82%b4&acode=SRP_SU_0100&arraycategory=&encKeyword=%eb%8b%ad%ea%b0%80%ec%8a%b4%ec%82%b4&s=8&k=0&p={0}'.format(idx)
        driver.get(url)
        time.sleep(5)
        # 아이템 리스트 XPath
        elements = driver.find_elements_by_xpath('//span[@class="text--itemcard_title ellipsis"]')

        # 한 페이지에 100개정도의 아이템이 넘어온다.
        for element in elements:
            ele = element.find_element_by_xpath('./a')
            urls.append(ele.get_attribute("href"))

    for url in urls:
        # URL 접속
        driver.get(url)
        time.sleep(3)

        # 구매후기 클릭
        driver.find_element_by_xpath('//li[@id="tap_moving_2"]/a').click()
        time.sleep(1)

        # 최신순 선택
        driver.find_element_by_xpath("//li[@class='list-item']/a[@class='link js-link']").click()
        time.sleep(1)

        reviews = driver.find_elements_by_xpath("//ul[@class='list__review']/li[@class='list-item']")
        for review in reviews:
            productId = review.get_attribute("id")
            box_info = review.find_element_by_xpath(
                "./div[@class='box__review-item']/div[@class='box__content']/div[@class='box__info']")
            star = box_info.find_element_by_xpath("./div[@class='box__star']").text
            writer = box_info.find_element_by_xpath("./p[@class='text__writer']").text
            date = box_info.find_element_by_xpath("./p[@class='text__date']").text
            content = ""
            try:
                content = review.find_element_by_xpath(
                    "./div[@class='box__review-item']/div[@class='box__content']/div[@class='box__review-text']").text
            except Exception as e:
                print(e)

            print("productId={0}, star ={1}, writer={2}, date={3}, content = {4}".format(productId, star, writer, date, content))

except Exception as e:
    print(e)
finally:
    driver.close()




