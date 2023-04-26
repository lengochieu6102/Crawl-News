from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
DRIVER_PATH = "D:\chromedriver\chromedriver.exe"
options = Options()
# options.headless = True
# options.add_argument("--window-size=1920,1200")

ser = Service(DRIVER_PATH)
driver = webdriver.Chrome(service=ser)
driver.get("https://baomoi.com/")


# crawl_topics = ['thế giới', 'xã hội', 'văn hóa', 'kinh tế', 'giáo dục', 'thể thao', 'giải trí', 'pháp luật', 'công nghệ', 'khoa học', 'đời sống', 'xe cộ', 'nhà đất']
crawl_topics = [  'văn hóa', 'kinh tế', 'giáo dục', 'thể thao', 'giải trí', 'pháp luật', 'công nghệ',]

dropdown_topic = driver.find_elements(By.XPATH, '//button[@class="bm_CG undefined"]')[2]
dropdown_topic.click()

# topics driver
topics = driver.find_elements(By.XPATH, '//li[@class="bm_IY"]/a')

info_topic = []
for topic in topics:
    info_topic.append({
        'topic_name': topic.text.lower(),
        'url': topic.get_attribute('href')
    })

topics_name = list(map(lambda ele: ele['topic_name'], info_topic))
for topic in crawl_topics:
    if topic in topics_name:
        print(f'Ready for crawl "{topic}"')    
    else:
        print(f'Dont find topic "{topic}"')

info_topic = list(filter(lambda ele: ele['topic_name'] in crawl_topics, info_topic))

def crawl_info_news_topic(topic_name, url):
    driver.get(url)
    list_news = []
    try:
        while True:
            for i in range(100):
                time.sleep(0.01)
                javaScript = "window.scrollTo(0, document.body.scrollHeight);"
                driver.execute_script(javaScript)
            
            list_news_driver = driver.find_elements(By.XPATH, '//div[@class="bm_Ab"]/div[@class="bm_R"]')
            for news in list_news_driver:
                
                url = news.find_element(By.XPATH, './a[last()]').get_attribute('href')
                title = news.find_element(By.XPATH, './a[last()]').get_attribute('title')
                publisher = news.find_element(By.XPATH, './a[1]').get_attribute('title')
                try:
                    datetime = news.find_element(By.XPATH, './time').get_attribute('datetime')
                except NoSuchElementException:
                    datetime = ""
                list_news.append(
                    {
                        'url':url,
                        'title':title,
                        'publisher':publisher,
                        'time':datetime
                    }
                )
            driver.find_element(By.XPATH, '//button[@class="bm_CG bm_Ge bm_Gc undefined"]').click()
            time.sleep(1)
    except NoSuchElementException:
        df_news = pd.DataFrame(list_news)
        df_news.to_csv(f'{topic_name}.csv',index=False)
        print(f'Finish crawl info data {topic_name}')

for topic in info_topic:
    crawl_info_news_topic(topic['topic_name'],topic['url'])

driver.close()