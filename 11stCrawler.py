from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome('./libnative/chromedriver/chromedriver.exe')
# 암묵적으로 웹 자원이 로드되기까지 기다리는 시간 설정
driver.implicitly_wait(3)

def printComment(commentElList):
    for commentEl in commentElList:
        contmapno = commentEl.get_attribute('data-contmapno')
        prdno = commentEl.get_attribute('data-prdno')
        contno = commentEl.get_attribute('data-contno')
        newCommentPage = "http://www.11st.co.kr/product/SellerProductDetail.tmall?method=getProductReviewDetailv2&contMapNo=" + contmapno + "&prdNo=" + prdno + "&contNo=" + contno
        print(newCommentPage)
        #driver.get(newCommentPage)

try:
    # url에 접근 (검색어가 입력된 url)
    driver.get('http://search.11st.co.kr/Search.tmall?kwd=%25EC%2595%2584%25EA%25B8%25B0%25EB%25AC%25BC%25ED%258B%25B0%25EC%258A%2588')
    time.sleep(5)

    # 조건 설정
    print('//div[@id="sortLayerContainer"]/ul/li/a[contains(text(), "많은 리뷰순")]')
    searchCondition = driver.find_element_by_xpath('//div[@id="sortLayerContainer"]/ul/li/a[contains(text(), "많은 리뷰순")]')
    driver.execute_script("arguments[0].click();", searchCondition)
    time.sleep(5)

    # 제품 리스트 (1페이지에 80개 - 20개로 한정)
    productElList = driver.find_elements_by_xpath('//div[@id="product_listing"]/div/div/ul/li')
    urllist = []
    print(type(productElList))

    num = 0;
    # productElList를 돌면서 url 저장
    for productEl in productElList:
        num += 1
        urlEl = productEl.find_element_by_xpath('./div/div[@class="list_info"]/p/a')
        urllist.append(urlEl.get_attribute('href'))
        if num == 20:
            break
    iframeUrlList = []
    # 저장된 url 로 이동
    for url in urllist:
        print(url)
        driver.get(url)
        time.sleep(5)

        # iframe 으로 이동하는 코드
        reviewIframe = driver.find_element_by_xpath('//div[@id="tabProductReview"]/div[@class="prdc_review_wrap"]/iframe')
        # url 이 about:blank 로 찍히는거 디버깅으로 확인해야함
        iframeUrl = str(reviewIframe.get_attribute('src'))
        driver.switch_to.frame(reviewIframe)
        time.sleep(5)

        # 페이지네이션 구조 (a:이전 -> span/a[@id="paging_page"]:페이지 -> a[@id="paging_next"]:다음 )
        # 페이지 돌면서 iframe 주소 배열에 추가
        # 20페이지까지만 수집
        paging = driver.find_element_by_xpath('//div[@class="review_list"]/div[@class="s_paging_v2"]')
        startpage = 1
        commentIframeUrl = iframeUrl.replace('page=1', 'page=' + str(startpage), 1)
        iframeUrlList.append(commentIframeUrl)
        startpage += 1
        
        try:
            pageElList = paging.find_elements_by_xpath('./span/a')
            if len(pageElList) > 0:
                # todo: 클릭 이벤트 iframe intercepted 오류나는 부분 주석처리
                # for page in range(len(pageElList)):
                #     # 클릭 이후에 iframe 들어가서 잡아줬던 webBrowser 변수들을 다시 잡아줘야함
                #     if page == 0:
                #         print('1페이지')
                #         # todo: 댓글 목록 저장
                #     else:
                #         print(str(page+1)+'페이지')
                #         currentPageEl = paging.find_element_by_xpath(
                #             './span/a[text()>//div[@class="review_list"]/div[@class="s_paging_v2"]/span/strong[text()]][1]')
                #         if currentPageEl.is_enabled():
                #             currentPageEl.click()
                #         time.sleep(5)
                #         paging = driver.find_element_by_xpath('//div[@class="review_list"]/div[@class="s_paging_v2"]')

                for page in range(len(pageElList)):
                    commentIframeUrl = iframeUrl.replace('page=1', 'page=' + str(startpage+page), 1)
                    iframeUrlList.append(commentIframeUrl)
                startpage += len(pageElList)
        except Exception as e:
            print("페이지 요소가 없습니다.")

        try:
            nextPageEl = paging.find_element_by_xpath('./a[@id="paging_next"]')
            nextPageEl.click()
            time.sleep(5)
            commentIframeUrl = iframeUrl.replace('page=1', 'page=' + str(startpage), 1)
            iframeUrlList.append(commentIframeUrl)
            startpage += 1
            paging = driver.find_element_by_xpath('//div[@class="review_list"]/div[@class="s_paging_v2"]')
            pageElList = paging.find_elements_by_xpath('./span/a')

            if len(pageElList) > 0:
                for page in range(len(pageElList)):
                    commentIframeUrl = iframeUrl.replace('page=1', 'page=' + str(startpage + page), 1)
                    iframeUrlList.append(commentIframeUrl)
                startpage += len(pageElList) - 1
        except Exception as e:
            print("다음 페이지 링크가 없습니다.")

        # iframe에서 빠져나오는 코드
        driver.switch_to.parent_frame()

        print('상품 하나 end')
    for pageUrl in iframeUrlList:
        print(pageUrl)
except Exception as e:
    print(e)
finally:
    driver.close()