from selenium import webdriver
import time
from bs4 import BeautifulSoup
import pandas as pd


driver = webdriver.Chrome()
url= "https://vietteltelecom.vn/di-dong/sim-so"
driver.maximize_window()
driver.get(url)

time.sleep(10)

driver.find_element('xpath','//*[@id="close-button-1454703513202"]').click()
more_sim =  driver.find_element('xpath','//*[@id="sim-tt"]/div/div/a').click()

time.sleep(5)

content = driver.page_source.encode('utf-8').strip()
soup = BeautifulSoup(content,"html.parser")
table = soup.find("table",{"class":"sim-number__table"})

headers=[]
titles = []



#get all header of table
headers = table.find_all('th')
for header in headers:
    titles.append(header.text)

df = pd.DataFrame(columns=titles)

rows = table.find_all('tr')
for row in rows[1:]:
    data = row.find_all('td')
    #get from each row in table to array
    row = [tr.text for tr in data ]
    #add new array to df
    l = len(df)
    df.loc[l] = row
    
df2 = df.drop(df.columns[[0,2]],axis=1)    

print("data frame")
print(df2)
df2.to_csv('sim-list.csv',index=False)

driver.quit()