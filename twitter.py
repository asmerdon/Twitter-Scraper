from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

print("Enter the search term you would like to scrape: ")
search_term = input()
print("Enter the amount of tweets you'd like to return: ")
amount = input()
login_url = "https://twitter.com/login"
search_url = "https://twitter.com/search?q="+str(search_term)+"&src=typed_query"


driver=webdriver.Chrome()

def login():
    driver.get(login_url)
    time.sleep(3)
    driver.find_element("xpath", '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[5]/label/div/div[2]/div/input').send_keys('theDataDON13')
    time.sleep(2)
    driver.find_element("xpath", '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[6]/div').click()
    time.sleep(3)
    driver.find_element("xpath", '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[3]/div/label/div/div[2]/div[1]/input').send_keys('yYzVm2MdYhSQ2FA')
    time.sleep(2)
    driver.find_element("xpath", '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div/div/div/div').click()
    time.sleep(3)

login()
driver.get(search_url)
time.sleep(3)
resp = driver.page_source
driver.close()

print(resp)
"""l=list()
o={}

soup=BeautifulSoup(resp,'html.parser')
try:
    o["profile_name"]=soup.find("div",{"class":"r-1vr29t4"}).text
except:
    o["profile_name"]=None

try:
    o["profile_handle"]=soup.find("div",{"class":"r-1wvb978"}).text
except:
    o["profile_handle"]=None

l.append(o)
print(l)"""