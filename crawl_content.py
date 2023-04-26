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
import tqdm
import sys
DRIVER_PATH = "D:\chromedriver\chromedriver.exe"
options = Options()
# options.headless = True
options.add_argument("start-maximized")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
# options.add_argument("--window-size=1920,1200")

ser = Service(DRIVER_PATH)
driver = webdriver.Chrome(service=ser, options = options)
crawl_topics = ['thế giới', 'xã hội', 'văn hóa', 'kinh tế', 'giáo dục', 'thể thao', 'giải trí', 'pháp luật', 'công nghệ', 'khoa học', 'đời sống', 'xe cộ', 'nhà đất']
crawl_topics = [ 'văn hóa', 'kinh tế', 'giáo dục', 'thể thao', 'giải trí', 'pháp luật', 'công nghệ', 'khoa học', 'đời sống', 'xe cộ', 'nhà đất']


def get_content(url):
    driver.get(url)
    # time.sleep(0.4)
    body_content = driver.find_elements(By.XPATH, '//div[@class="bm_s"]/h3 | //div[@class="bm_s"]//p[@class="bm_Am"]')
    body_content = list(map(lambda ele: ele.text + '\n', body_content))
    whole_content =''.join(body_content)
    return whole_content


for topic in crawl_topics:
    df_news = pd.read_csv(f'full_data/{topic}.csv')
    dict_news = df_news.to_dict('records')
    try:
        for news in dict_news:
            if news.get('content') is None or pd.isnull(news.get('content')):   
                try:
                    news['content'] = get_content(news['url'])
                except:
                    pass
                print(news['title'])
    except KeyboardInterrupt:
        print('KeyboardInterrupt')
        df_news =  pd.DataFrame(dict_news)
        df_news.to_csv(f'full_data/{topic}.csv',index=False)
        print('Saved progress')
        sys.exit()
    df_news =  pd.DataFrame(dict_news)
    df_news.to_csv(f'full_data/{topic}.csv',index=False)
driver.close()