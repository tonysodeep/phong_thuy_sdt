from selenium import webdriver
import time
from bs4 import BeautifulSoup
import pandas as pd
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait



driver = webdriver.Chrome()
url= "https://vietteltelecom.vn/di-dong/sim-so"
driver.maximize_window()
driver.get(url)

#tat pop up cua thg viettel toi 30s tim cach tat khi show pop up
# time.sleep(20)
# driver.find_element('xpath','//*[@id="close-button-1454703513202"]').click()

time.sleep(5)
more_sim =  driver.find_element('xpath','//*[@id="sim-tt"]/div/div/a').click()

driver.find_element('xpath','//*[@id="app"]/div[1]/div[16]/div[2]/div[4]/div[2]/div/div[1]/div[1]/input').send_keys('08*')
time.sleep(5)
driver.find_element('xpath','//*[@id="app"]/div[1]/div[16]/div[2]/div[4]/div[2]/div/div[1]/div[2]/a').click()
time.sleep(5)

content = driver.page_source.encode('utf-8').strip()
soup = BeautifulSoup(content,"html.parser")
table = soup.find("table",{"class":"sim-number__table"})

headers=[]
titles = []

headers = table.find_all('th')
for header in headers:
    titles.append(header.text)

df = pd.DataFrame(columns=titles)



count = 0
while count < 5:
    try:
        rows= table.find_all('tr')
        for row in rows[1:]:
            data = row.find_all('td')
            #get from each row in table to array
            row = [tr.text for tr in data ]
            #add new array to df
            l = len(df)
            df.loc[l] = row
        time.sleep(10)
        driver.execute_script("return arguments[0].scrollIntoView(true);", WebDriverWait(driver, 20).
                              until(EC.element_to_be_clickable((By.XPATH, '//*[@id="sim-tt"]/div/div/div/div/ul/li[9]/button'))))
        driver.find_element('xpath','//*[@id="sim-tt"]/div/div/div/div/ul/li[9]/button').click()
        count = count + 1
        print(f'data set {len(df.index)}')
        print("Navigating to Next Page")
    except (TimeoutException, WebDriverException) as e:
        print("Last page reached")
        print(f'ERROR {e}')
        break


df2 = df.drop(df.columns[[0,2]],axis=1)    

print("data frame")
print(df2)
df2.to_csv('sim-list.csv',index=False)

driver.quit()