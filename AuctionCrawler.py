from selenium import webdriver
import re
import json

from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome("./libnative/chromedriver")
#driver = webdriver.Chrome("./libnative/chromedriver.exe")
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

        # 아이템 제목
        title = driver.find_element_by_xpath("//h1[@class='itemtit']/span[@class='text__item-title']").text

        # ProductID
        productId = re.sub(r".*itemno=", "", url)

        # 구매후기 클릭
        driver.find_element_by_xpath('//li[@id="tap_moving_2"]/a').click()
        time.sleep(1)

        # 최신순 선택
        driver.find_element_by_xpath("//li[@class='list-item']/a[@class='link js-link']").click()
        time.sleep(1)

        for x in range(10):
            reviews = driver.find_elements_by_xpath("//ul[@class='list__review']/li[@class='list-item']")
            for review in reviews:
                commentId = review.get_attribute("id")
                box_info = review.find_element_by_xpath(
                    "./div[@class='box__review-item']/div[@class='box__content']/div[@class='box__info']")

                # 이용자 평점 x점
                star = box_info.find_element_by_xpath("./div[@class='box__star']").text
                m = re.search("[0-9]", star)
                star = m.group(0)

                writer = box_info.find_element_by_xpath("./p[@class='text__writer']").text
                date = box_info.find_element_by_xpath("./p[@class='text__date']").text
                comment = ""
                try:
                    comment = review.find_element_by_xpath(
                        "./div[@class='box__review-item']/div[@class='box__content']/div[@class='box__review-text']").text
                except Exception as e:
                    continue

                item = {
                    "url" : url,
                    "product_title" : title,
                    "product_id" : productId,
                    "date" : date,
                    "comment_id" : commentId,
                    "comment_content" : comment,
                    "rating" : star
                }

                with open("./data/auctionComment.json", "a", encoding="utf-8") as fp:
                    json.dump(item, fp, ensure_ascii=False)


                #print(
                #    "url={0}, productId={1}, productTitle={2}, commentId={3}, star={4}, writer={5}, date={6}, comment={7}".format(
                #        url, productId, title, commentId, star, writer, date, comment))

            # next button
            driver.find_element_by_xpath("//div[@class='box__pagination']//a[@class='link__page-move link__page-next']").click()

except Exception as e:
    print(e)
finally:
    driver.close()




