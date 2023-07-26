from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import csv

# Configure Chrome options for headless scraping (no GUI)
chrome_options = Options()

"""chrome_options.add_argument('window-size=2000x1500')
chrome_options.add_argument("--headless=new")  # Ensure GUI is off
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")"""

# Prompt user for search term and amount of tweets
print("Enter the search term you would like to scrape: ")
search_term = input()
print("Enter the amount of tweets you'd like to return: ")
amount = int(input())

# URLs
login_url = "https://twitter.com/login"
search_url = "https://twitter.com/search?q=" + str(search_term) + "&src=typed_query"

# Initialize Chrome driver with the configured options
driver = webdriver.Chrome(options=chrome_options)
#driver = webdriver.Firefox()

# Function to save tweet data to a CSV file
def save_to_csv(tweet_data):
    filename = "tweets.csv"
    fieldnames = ["username", "datetime", "tweet_text", "replies", "retweets", "likes"]  # Update fieldnames to match dictionary keys

    with open(filename, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for tweet in tweet_data:
            writer.writerow(tweet)  # Write the tweet dictionary directly

    print("Tweet data saved to", filename)

# Function to perform login
def login():
    driver.get(login_url)
    time.sleep(2)
    driver.find_element("xpath", '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[5]/label/div/div[2]/div/input').send_keys('YOUR-USERNAME')
    time.sleep(1)
    driver.find_element("xpath", '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[6]/div').click()
    time.sleep(2)
    driver.find_element("xpath", '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[3]/div/label/div/div[2]/div[1]/input').send_keys('YOUR-PASSWORD')
    time.sleep(1)
    driver.find_element("xpath", '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div/div/div/div').click()
    time.sleep(2)

# Function to perform the search and scrape tweets
def search():
    driver.get(search_url)
    time.sleep(5)
    start_time = time.time()
    tweet_data = []

    while len(tweet_data) < amount:
        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
        time.sleep(1)
        resp = driver.page_source
        new_tweets = parse(resp, tweet_data)
        tweet_data.extend(new_tweets)

        elapsed_time = time.time() - start_time
        if elapsed_time >= amount/10:
            break

    print("Number of tweets found:", len(tweet_data))
    return tweet_data[:amount]

# Function to parse tweet HTML and extract relevant information
def parse(resp, tweet_data):
    soup = BeautifulSoup(resp, 'html.parser')
    tweets = soup.find_all("div", {"data-testid": "cellInnerDiv"})
    result = []

    for tweet in tweets:
        tweet_info = {}

        try:
            tweet_info["username"] = tweet.find("div", {"data-testid": "User-Name"}).text
        except AttributeError:
            tweet_info["username"] = None
        
        try:
            tweet_info["datetime"] = tweet.find("time").get("datetime")  # Extract the "datetime" attribute value
        except AttributeError:
            tweet_info["datetime"] = None

        try:
            tweet_info["tweet_text"] = tweet.find("div", {"data-testid": "tweetText"}).text
        except AttributeError:
            tweet_info["tweet_text"] = None
        
        try:
            tweet_info["replies"] = tweet.find("div", {"data-testid": "reply"}).text
        except AttributeError:
            tweet_info["replies"] = None
        
        try:
            tweet_info["retweets"] = tweet.find("div", {"data-testid": "retweet"}).text
        except AttributeError:
            tweet_info["retweets"] = None
        
        try:
            tweet_info["likes"] = tweet.find("div", {"data-testid": "like"}).text
        except AttributeError:
            tweet_info["likes"] = None

        if not tweet_info["tweet_text"] in tweet_data:
            result.append(tweet_info)

    return result

# Main program flow
login()
tweet_data = search()
driver.close()
save_to_csv(tweet_data)
