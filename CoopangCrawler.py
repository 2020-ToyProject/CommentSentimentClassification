from urllib import parse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import ElementNotInteractableException
import time
import logging.handlers
import traceback
import json

KEYWORD = '이어폰'
PAGE_MAX_SIZE = 3
DOCS_PER_PAGE = 72
COMMENTS_PAGE_MAX_SIZE = 50
FILE_NAME = './data/coopang_earphone_comments.txt'
LOG_FILE_NAME = './logs/crawler.log'
CHROME_PATH = './libnative/chromedriver.exe'
PRODUCT_URL_FORMAT = 'https://www.coupang.com/vp/products/{productId}'
SORT_BY_LATELY_BUTTON_SELECTOR = '.sdp-review__article__order__sort__newest-btn.js_reviewArticleNewListBtn.js_reviewArticleSortBtn'
REVIEW_TAG_LIST = '.sdp-review__article__list.js_reviewArticleReviewList'
RATING_TAG = '.sdp-review__article__list__info__product-info__star-orange.js_reviewArticleRatingValue'
DATETIME_TAG = 'sdp-review__article__list__info__product-info__reg-date'
REVIEW_ID_TAG = '.sdp-review__article__list__help.js_reviewArticleHelpfulContainer'
COMMENT_TITLE_TAG = 'sdp-review__article__list__headline'
COMMENT_CONTENT_TAG = '.sdp-review__article__list__review__content.js_reviewArticleContent'
PAGINATION_CONTAINER_TAG = '.sdp-review__article__page.js_reviewArticlePagingContainer'

#logger instance
logger = logging.getLogger(__name__)
streamHandler = logging.StreamHandler()
fileHandler = logging.handlers.RotatingFileHandler(LOG_FILE_NAME, maxBytes=1024 * 1024 * 10, backupCount=10)
logger.addHandler(streamHandler)
logger.addHandler(fileHandler)
logger.setLevel(level=logging.DEBUG)

#web driver (headless)
options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")
options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")

driver = webdriver.Chrome(CHROME_PATH, chrome_options=options)
driver.implicitly_wait(0)

#file open
file = open(FILE_NAME, mode='w', encoding='UTF-8')

try:
    for pageIdx in range(1, PAGE_MAX_SIZE + 1) :
        prodListPage = 'https://www.coupang.com/np/search?isPriceRange=false&filterSetByUser=true&channel=user&sorter=saleCountDesc&'
        prodListPage += 'q={keyword}&'.format(keyword=parse.quote(KEYWORD))
        prodListPage += 'page={idx}&'.format(idx=pageIdx)
        prodListPage += 'listSize=72'.format(listSize=DOCS_PER_PAGE)
        driver.get(prodListPage)

        productIds = []
        for prodTag in driver.find_elements(By.CLASS_NAME, 'search-product-link') :
            productIds.append(prodTag.get_attribute('data-product-id'))

        for productId in productIds :
            prodPage = PRODUCT_URL_FORMAT.format(productId=productId)
            driver.get(prodPage)

            time.sleep(2)
            driver.find_element(By.XPATH, '//*[@id="btfTab"]/ul[1]/li[2]').click()
            time.sleep(3)

            prodInfo = {
                'product_id': productId,
                'url': prodPage,
                'product_title': driver.find_element(By.CLASS_NAME, 'prod-buy-header__title').text
            }

            try:
                driver.find_element(By.CSS_SELECTOR, SORT_BY_LATELY_BUTTON_SELECTOR).click()
            except UnexpectedAlertPresentException:
                continue
            except ElementNotInteractableException:
                continue

            currCommPageIdx = 0

            while True:
                try:
                    currCommPageIdx += 1

                    time.sleep(2)
                    reviewList = driver.find_elements(By.CSS_SELECTOR, REVIEW_TAG_LIST)
                    time.sleep(4)

                    for reviewTag in reviewList:
                            review = prodInfo.copy()
                            review['rating'] = reviewTag.find_element(By.CSS_SELECTOR, RATING_TAG).get_attribute(
                                'data-rating')
                            review['date'] = reviewTag.find_element(By.CLASS_NAME,
                                                                    DATETIME_TAG).text
                            review['comment_id'] = reviewTag.find_element(By.CSS_SELECTOR,
                                                                          REVIEW_ID_TAG).get_attribute('data-review-id')

                            if len(reviewTag.find_elements(By.CLASS_NAME, COMMENT_TITLE_TAG)) != 0:
                                review['comment_title'] = reviewTag.find_element(By.CLASS_NAME,
                                                                                 COMMENT_TITLE_TAG).text

                            if len(reviewTag.find_elements(By.CSS_SELECTOR,
                                                           COMMENT_CONTENT_TAG)) != 0:
                                review['comment_content'] = reviewTag.find_element(By.CSS_SELECTOR,
                                                                                   COMMENT_CONTENT_TAG).text

                            #logger.info(review)
                            json.dump(review, file, ensure_ascii=False)
                            file.write('\n')

                    if len(driver.find_elements(By.CSS_SELECTOR,
                                                PAGINATION_CONTAINER_TAG)) == 0:
                        break;

                    endCommPageIdx = driver.find_element(By.CSS_SELECTOR,
                                                         PAGINATION_CONTAINER_TAG).get_attribute(
                        'data-end')
                    pageNextIsEnabled = driver.find_element(By.CLASS_NAME, 'js_reviewArticlePageNextBtn').is_enabled()
                    endCommPageIdx = int(endCommPageIdx)

                    print(currCommPageIdx)
                    print(endCommPageIdx)

                    if currCommPageIdx >= COMMENTS_PAGE_MAX_SIZE or (
                            currCommPageIdx == endCommPageIdx and not pageNextIsEnabled):
                        break
                    elif currCommPageIdx % 10 == 0:
                        driver.find_element(By.CSS_SELECTOR,
                                            '.sdp-review__article__page__next.js_reviewArticlePageNextBtn').click()
                    else:
                        if len(driver.find_elements(By.CLASS_NAME, 'sdp-review__article__page__num')) < (
                                (currCommPageIdx % 10) + 1):
                            break;
                        driver.find_elements(By.CLASS_NAME, 'sdp-review__article__page__num')[
                            (currCommPageIdx % 10)].click()
                except UnexpectedAlertPresentException:
                    logger.error(traceback.format_exc())
                    driver.find_elements(By.CLASS_NAME, 'sdp-review__article__page__num')[
                        (currCommPageIdx % 10)].click()
                    continue
                except StaleElementReferenceException:
                    #element 값 load 오류시 다시 진행
                    logger.error(traceback.format_exc())
                    continue
                except Exception:
                    logger.error(traceback.format_exc())
                    break

except Exception:
    logger.error(traceback.format_exc())
finally:
    driver.quit()
    file.close()