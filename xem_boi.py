from selenium import webdriver
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import csv
import time
import string

sims = []
filename = 'sim-list.csv'
with open(filename,'r') as csvfile:
    datareader = csv.reader(csvfile)
    next(csvfile)
    for row in datareader:
        sim = row[0].translate({ord(c): None for c in string.whitespace})
        sims.append(sim)


web = webdriver.Chrome()
web.get("https://xemvanmenh.net/xem-boi-so-dien-thoai.html")

time.sleep(5)



input_select =  Select(web.find_element('xpath','//*[@id="main_wrap"]/div/div/section[1]/div/div[2]/form/div[1]/div[1]/div[2]/div[1]/select'))
input_select.select_by_index(8)

input_date =  Select(web.find_element('xpath','//*[@id="main_wrap"]/div/div/section[1]/div/div[2]/form/div[1]/div[1]/div[2]/div[3]/select'))
input_date.select_by_index(5)

input_month =  Select(web.find_element('xpath','//*[@id="main_wrap"]/div/div/section[1]/div/div[2]/form/div[1]/div[1]/div[2]/div[5]/select'))
input_month.select_by_index(3)

input_year =  Select(web.find_element('xpath','//*[@id="namsinh"]'))
input_year.select_by_index(51)

for sim in sims:
    input_sdt = web.find_element('xpath','//*[@id="main_wrap"]/div/div/section[1]/div/div[2]/form/div[1]/div[1]/div[1]/div[1]/input')
    input_sdt.clear()
    input_sdt.send_keys(sim)
    submit_bt = web.find_element('xpath','//*[@id="btn_xemboisim"]')
    submit_bt.click()
    time.sleep(2)
    content = web.page_source.encode('utf-8').strip()
    soup = BeautifulSoup(content,"html.parser")
    result = soup.find('p', class_ = 'td_diem')
    print(f'{sim} - {result.text}')

web.quit()




