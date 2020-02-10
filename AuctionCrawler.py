from selenium import webdriver
import re
import json

from selenium.webdriver.common.by import By
import time

#driver = webdriver.Chrome("./libnative/chromedriver")
driver = webdriver.Chrome("./libnative/chromedriver.exe")

ITEM_PAGE = 6
COMMENT_PAGE = 20

try:
    urls = []

    for idx in range(1, ITEM_PAGE):
        url = 'http://browse.auction.co.kr/list?category=19040000&s=8k=0&p={0}'.format(idx)
        driver.get(url)
        print(url)
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

        for x in range(COMMENT_PAGE):
            try:
                reviews = driver.find_elements_by_xpath("//ul[@class='list__review']/li[@class='list-item']")
                for review in reviews:
                    try:

                        commentId = review.get_attribute("id")
                        box_info = review.find_element_by_xpath(
                            "./div[@class='box__review-item']/div[@class='box__content']/div[@class='box__info']")

                        # 이용자 평점 x점
                        star = box_info.find_element_by_xpath("./div[@class='box__star']/span[@class='sprite__vip image__star']/span[@class='sprite__vip image__star-fill']").get_attribute("style")
                        if ("width: 0%" in star) :
                            star = 0
                        elif ("width: 20%" in star) :
                            star = 1
                        elif ("width: 40%" in star):
                            star = 2
                        elif ("width: 60%" in star):
                            star = 3
                        elif ("width: 80%" in star):
                            star = 4
                        elif ("width: 100%" in star):
                            star = 5

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

                        with open("data/auctionComment_영양제.json", "a", encoding="utf-8") as fp:
                            json.dump(item, fp, ensure_ascii=False)
                            fp.write("\n")
                    except Exception as e:
                        print(e)
                # next button
                driver.find_element_by_xpath(
                            "//div[@class='box__pagination']//a[@class='link__page-move link__page-next']").click()
            except Exception as e:
                print(e)

                print(
                       "url={0}, productId={1}, productTitle={2}, commentId={3}, star={4}, writer={5}, date={6}, comment={7}".format(
                            url, productId, title, commentId, star, writer, date, comment))



except Exception as e:
    print(e)
finally:
    driver.close()




