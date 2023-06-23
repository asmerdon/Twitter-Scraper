from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

print("Enter the search term you would like to scrape: ")
search_term = input()
print("Enter the amount of tweets you'd like to return: ")
amount = int(input())
login_url = "https://twitter.com/login"
search_url = "https://twitter.com/search?q="+str(search_term)+"&src=typed_query"


driver=webdriver.Chrome()

def login():
    driver.get(login_url)
    time.sleep(2)
    driver.find_element("xpath", '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[5]/label/div/div[2]/div/input').send_keys('theDataDON13')
    time.sleep(1)
    driver.find_element("xpath", '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[6]/div').click()
    time.sleep(2)
    driver.find_element("xpath", '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[3]/div/label/div/div[2]/div[1]/input').send_keys('yYzVm2MdYhSQ2FA')
    time.sleep(1)
    driver.find_element("xpath", '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div/div/div/div').click()
    time.sleep(2)

def search():
    scroll_distance = amount * 1000
    driver.get(search_url)
    time.sleep(5)
    scroll_height = driver.execute_script("return document.documentElement.scrollHeight")
    start_time = time.time()
    while scroll_height < scroll_distance:
        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
        time.sleep(1)
        new_scroll_height = driver.execute_script("return document.documentElement.scrollHeight")
        if new_scroll_height == scroll_height:
            time.sleep(1)
            elapsed_time = time.time() - start_time
            if elapsed_time >= 5:
                break
        scroll_height = new_scroll_height
    print("Scroll distance(entered):")
    print(scroll_distance)
    print("Scroll height:")
    print(scroll_height)
    time.sleep(5)

def parse(resp, amount):
    soup = BeautifulSoup(resp, 'html.parser')
    tweets = soup.find_all("div", {"data-testid": "cellInnerDiv"})
    result = []

    for tweet in tweets[:amount]:
        tweet_info = {}

        try:
            tweet_info["username"] = tweet.find("div", {"data-testid": "User-Name"}).text
        except AttributeError:
            tweet_info["username"] = None

        try:
            tweet_info["tweet_text"] = tweet.find("div", {"data-testid": "tweetText"}).text
        except AttributeError:
            tweet_info["tweet_text"] = None

        result.append(tweet_info)

    print("Number of tweets found:", len(tweets))
    return result

login()
search()
resp = driver.page_source
driver.close()

tweet_data = parse(resp, amount)
for tweet in tweet_data:
    print("Username:", tweet["username"])
    print("Tweet text:", tweet["tweet_text"])
    print("---")
