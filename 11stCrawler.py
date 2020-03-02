from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
import json

driverPath = './libnative/chromedriver/chromedriver.exe'
shoppingmallUrl = 'http://search.11st.co.kr/Search.tmall?kwd=%25EA%25B0%2595%25EC%2595%2584%25EC%25A7%2580%25EA%25B0%2584%25EC%258B%259D&ab=A'
sortingXpath = '//div[@id="sortLayerContainer"]/ul/li/a[contains(text(), "많은 리뷰순")]'
productListXpath = '//div[@id="product_listing"]/div/div/ul/li'
urlXpath = './div/div[@class="list_info"]/p/a'
productTitleXpath = '//div[@id="productInfoMain"]/div[@class="prdc_heading_v2 no_brand"]/div/h2'
reviewIframeXpath = '//div[@id="tabProductReview"]/div[@class="prdc_review_wrap"]/iframe'
pageAreaXpath = '//div[@class="review_list"]/div[@class="s_paging_v2"]'
nextPageXpath = '//div[@class="review_list"]/div[@class="s_paging_v2"]/a[@id="paging_next"]'
pageElXpath = './span/a'
commentListXpath = '//div[@class="review_list"]/ul/li'
ratioElXpath = './div/div[@class="bbs_top"]/div[@class="top_l"]/div/p/span'
createdAtXpath = './div/div[@class="bbs_top"]/div[@class="top_r"]/span[@class="date"]'
commentIdXpath = './div/div[@class="bbs_cont_wrap"]/div[@class="bbs_cont"]/p[@class="bbs_summary"]'
commentContentXpath = './div/div[@class="bbs_cont_wrap"]/div[@class="bbs_cont"]/p[@class="bbs_summary"]/span/span | ./div/div[@class="bbs_cont_wrap"]/div[@class="bbs_cont"]/p[@class="bbs_summary"]/span/a'

def saveFile(file, commentElList):
    for comment in commentElList:
        ratio = 0
        try:
            ratioEl = comment.find_element_by_xpath(ratioElXpath)
            ratio = int(ratioEl.get_attribute('class').replace('selr_star', '').replace(' ', ''))
            if ratio != 0:
                ratio = ratio / 20
        except Exception as e:
            print(e)
        createdAt = comment.find_element_by_xpath(createdAtXpath).text
        commentId = comment.find_element_by_xpath(commentIdXpath).get_attribute('data-contmapno')
        commentContent = comment.find_element_by_xpath(commentContentXpath).text
        commentObject = {
            "url": product.get("url"),
            "product_id": product.get("product_id"),
            "product_title": product.get("product_title"),
            "date": createdAt,
            "comment_id": commentId,
            "comment_content": commentContent,
            "rating": int(ratio)
        }
        json.dump(commentObject, file, ensure_ascii=False)
        file.write('\n')

def clickNextPage(driver):
    nextPageEl = driver.find_element_by_xpath(nextPageXpath)
    driver.execute_script("arguments[0].click();", nextPageEl)
    time.sleep(10)
    paging = driver.find_element_by_xpath(pageAreaXpath)
    pageElList = paging.find_elements_by_xpath(pageElXpath)
    if len(pageElList) > 0:
        for page in range(len(pageElList)):
            commentElList = driver.find_elements_by_xpath(commentListXpath)
            saveFile(file, commentElList)
            pageElement = driver.find_element_by_xpath(
                '//div[@class="review_list"]/div[@class="s_paging_v2"]/span/a[text()>//div[@class="review_list"]/div[@class="s_paging_v2"]/span/strong][1]')
            driver.execute_script("arguments[0].click();", pageElement)
            time.sleep(10)

driver = webdriver.Chrome(driverPath)
# 암묵적으로 웹 자원이 로드되기까지 기다리는 시간 설정
time.sleep(10)

try:
    # url에 접근 (검색어가 입력된 url)
    driver.get(shoppingmallUrl)
    time.sleep(10)

    # 조건 설정
    searchCondition = driver.find_element_by_xpath(sortingXpath)
    driver.execute_script("arguments[0].click();", searchCondition)
    time.sleep(10)

    # 제품 리스트 (1페이지에 80개 - 20개로 한정)
    productElList = driver.find_elements_by_xpath(productListXpath)
    urllist = []
    print(type(productElList))

    num = 0;
    # productElList를 돌면서 url 저장
    for productEl in productElList:
        num += 1
        urlEl = productEl.find_element_by_xpath(urlXpath)
        urllist.append(urlEl.get_attribute('href'))

    iframeUrlList = []
    # 저장된 url 로 이동
    filenum = 1
    for url in urllist:
        # 크롤링이 중간에 끊겼다면
        # if filenum < 80:
        #    filenum = filenum+1
        #    continue
        print(url)
        driver.get(url)
        # driver.implicitly_wait(10)
        time.sleep(10)
        productTitle = driver.find_element_by_xpath(productTitleXpath).text
        productId = driver.current_url.split('prdNo=')[1].split('&')[0]
        # todo: 객체를 만들어서 상품 정보 저장
        product = {
            "url": url,
            "product_id": productId,
            "product_title": productTitle
        }
        print(driver.current_window_handle)
        # iframe 으로 이동하는 코드
        reviewIframe = driver.find_element_by_xpath(reviewIframeXpath)
        # url 이 about:blank 로 찍히는거 디버깅으로 확인해야함
        iframeUrl = str(reviewIframe.get_attribute('src'))
        driver.switch_to.frame(reviewIframe)
        time.sleep(10)

        # 페이지네이션 구조 (a:이전 -> span/a[@id="paging_page"]:페이지 -> a[@id="paging_next"]:다음 )
        # 페이지 돌면서 iframe 주소 배열에 추가
        # 20페이지까지만 수집
        file = open("./data/star5/11stData" + str(filenum) + ".txt", 'w', encoding="utf-8")
        for pageUrl in iframeUrlList:
            driver.get(pageUrl)
            print(pageUrl)
            time.sleep(10)
        try:
            # todo : rate 선택
            print(driver.current_window_handle)
            star05 = driver.find_element_by_xpath('//input[@id="star05"]')
            driver.execute_script("arguments[0].click();", star05)
            time.sleep(10)

            paging = driver.find_element_by_xpath(pageAreaXpath)
            pageElList = paging.find_elements_by_xpath(pageElXpath)
            if len(pageElList) > 0:
                for page in range(len(pageElList)):
                    commentElList = driver.find_elements_by_xpath(commentListXpath)
                    saveFile(file, commentElList)
                    pageElement = driver.find_element_by_xpath('//div[@class="review_list"]/div[@class="s_paging_v2"]/span/a[text()>//div[@class="review_list"]/div[@class="s_paging_v2"]/span/strong][1]')
                    driver.execute_script("arguments[0].click();", pageElement)
                    time.sleep(10)
        except Exception as e:
            print(e)
        try:
            for i in range(2):
                clickNextPage(driver)

        except Exception as e:
            print("다음 페이지 링크가 없습니다.")

        # iframe에서 빠져나오는 코드
        driver.switch_to.parent_frame()
        print('상품 하나 end')
        file.close()
        filenum = filenum + 1
except Exception as e:
    print(e)
finally:
    driver.close()