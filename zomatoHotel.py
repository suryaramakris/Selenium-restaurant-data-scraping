from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

import pandas as pd
import time
from time import sleep

website = 'https://www.zomato.com/bangalore/hsr-restaurants'
path = "/path/to/chromedriver"

service = Service(executable_path=path)
driver = webdriver.Chrome(service=service)
driver.get(website)
sleep(2)

#to load the complete webpage
height = 0
while True:
    driver.find_element(by='xpath',value = '//body').send_keys(Keys.END)
    sleep(2)
    newheight = driver.execute_script("return document.body.scrollHeight")
    if (height == newheight) or (height > 10000):
        print('here',height,newheight)
        break
    height = newheight

#to store the data and convert to csv file later
namels = []
ratingls = []
costls = []
dishls = []
deliveryls = []
ordersls = []

for i in range(10,600):
    hotels = driver.find_elements(by='xpath',value=f'//*[@id="root"]/div/div[{i}]')
    j = 1
    print(400 - i,' hotels remaining')
    if len(hotels)==0:
        break
    for hotel in hotels:
        try:
            name = hotel.find_element(by='xpath',value=f'./div/div[{j}]/div/div/a[2]/div[1]/h4').text
            rating = hotel.find_element(by='xpath',value=f'./div/div[{j}]/div/div/a[2]/div[1]/div/div/div/div/div/div[1]').text
            cost = hotel.find_element(by='xpath',value=f'./div/div[{j}]/div/div/a[2]/div[2]/p[2]').text
            dish = hotel.find_element(by='xpath',value=f'./div/div[{j}]/div/div/a[2]/div[2]/p[1]').text
            delivery = hotel.find_element(by='xpath',value=f'./div/div[{j}]/div/div/a[1]/p').text
            order = hotel.find_element(by='xpath',value=f'./div/div[{j}]/div/div/a[2]/div[4]/div[1]/div/div[1]/p').text
        except:
            pass
        print(name,' scraping')
        
        namels.append(name)
        ratingls.append(rating)
        costls.append(cost)
        dishls.append(dish)
        deliveryls.append(delivery)
        ordersls.append(order)

        j += 1
        if j == 4:
            break
driver.quit()

df = pd.DataFrame({'names':namels,'ratings':ratingls,'cost':costls,'dish':dishls,'deliveryin_min':deliveryls,'order':ordersls})
print(df.head())
df.to_csv('zomato_hotel.csv')