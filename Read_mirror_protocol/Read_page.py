from selenium import webdriver
from bs4 import BeautifulSoup
import time
import pandas as pd
import os
import datetime



driver = webdriver.Chrome('./chromedriver')

driver.get('https://mirrorprotocol.app/#/trade')

time.sleep(6)

file_title = datetime.datetime.now().strftime('%Y-%m-%d_')
while 1:
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    stocks = soup.select('#mirror > div > div.Container_container__lHqDY > article > div > table > tbody > tr')
    Time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print('Now Time : ', Time)
    index = ['time']
    premium = [Time]
    try:
        for stock in stocks[1:]:

            name = stock.select_one('td:nth-child(1) > article > header > h1').text
            price = float(stock.select_one('td:nth-child(4) > span').text.replace('%',''))

            index.append(name)

            premium.append(price)

        df = pd.DataFrame(data=premium, index=index)

        df = df.transpose()

        if not os.path.exists(file_title+'output.csv'):

            df.to_csv(file_title+'output.csv', index=False, mode='w', encoding='utf-8-sig')

        else:

            df.to_csv(file_title+'output.csv', index=False, mode='a', encoding='utf-8-sig', header=False)
    except:
        print(name + " has error")
        pass
    driver.refresh()
    time.sleep(30)
