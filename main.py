from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import time

# site to make soup
SOURCE = "https://www.zillow.com/seattle-wa/rentals/1-_beds/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C" \
         "%22usersSearchTerm%22%3A%22seattle%2C%20wa%22%2C%22mapBounds%22%3A%7B%22west%22%3A-122.73549679394532%2C" \
         "%22east%22%3A-121.95409420605469%2C%22south%22%3A47.41421176274155%2C%22north%22%3A47.811371672572996%7D%2C" \
         "%22regionSelection%22%3A%5B%7B%22regionId%22%3A16037%2C%22regionType%22%3A6%7D%5D%2C%22isMapVisible%22" \
         "%3Atrue%2C%22filterState%22%3A%7B%22ah%22%3A%7B%22value%22%3Atrue%7D%2C%22fr%22%3A%7B%22value%22%3Atrue%7D" \
         "%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value" \
         "%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore" \
         "%22%3A%7B%22value%22%3Afalse%7D%2C%22pmf%22%3A%7B%22value%22%3Afalse%7D%2C%22pf%22%3A%7B%22value%22%3Afalse" \
         "%7D%2C%22mp%22%3A%7B%22max%22%3A2000%7D%2C%22price%22%3A%7B%22max%22%3A616134%7D%2C%22beds%22%3A%7B%22min" \
         "%22%3A1%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A11%7D "

# selenium boilerplate and site
FORM = "https://docs.google.com/forms/d/e/1FAIpQLSeP4NnMUsoRLPHlK0uD4EqOGmNZf8j8WtonnXZYNRVFVxd2qg/viewform?usp=sf_link"
DRIVER_PATH = "/home/nyxfox/Work/Automation/chrome-driver/chromedriver"  # driver path

# Headers obtained from myhttpheader.com
ACCEPT_LANGUAGE = "en-US,en;q=0.5"  # your input
USER_AGENT = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:83.0) Gecko/20100101 Firefox/83.0"  # your input

# making the zillow get header
zillow_header = {
    "User-Agent": USER_AGENT,
    "Accept-Language": ACCEPT_LANGUAGE,
}

# scraping zillow and making soup
zillow_query = requests.get(SOURCE, headers=zillow_header)
response = zillow_query.text
soup = BeautifulSoup(response, "html.parser")

# grab data by class
data_mess = soup.find_all(name="ul", class_="photo-cards photo-cards_wow photo-cards_short")
rental_addy = soup.find_all(name="address", class_="list-card-addr")
rental_prices = soup.find_all(name="div", class_="list-card-price")
rental_links = soup.find_all(name="a", class_="list-card-link list-card-link-top-margin list-card-img")

# turn data into lists
prices = [item.getText() for item in rental_prices]
addresses = [item.getText() for item in rental_addy]
links = [item.get("href") for item in rental_links]
website = "https://www.zillow.com"

# start up the webdriver
driver = webdriver.Chrome(executable_path=DRIVER_PATH)

while len(addresses) >= 0:
    driver.get(FORM)  # init the webpage
    time.sleep(1)
    if addresses == 0:
        driver.quit()
        break
    try:
        property_click = driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div')
        property_click.click()
        price = prices.pop(0)  # use pop to remove items from lists
        addy = addresses.pop(0)
        link = links.pop(0)
        if website not in link:  # if condition for incomplete links
            link = website + link

        property_input = driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div['
                                                      '2]/div/div[1]/div/div[1]/input')
        property_input.send_keys(addy)
        price_click = driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div['
                                                   '2]/div/div[1]')
        price_click.click()

        price_input = driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div['
                                                   '2]/div/div[1]/div/div[1]/input')
        price_input.send_keys(price)

        lnk_click = driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]')
        lnk_click.click()
        lnk_input = driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div['
                                                 '1]/div/div[1]/input')
        lnk_input.send_keys(link)

        submit_btn = driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div/div/span')
        submit_btn.click()
        time.sleep(1)
    except:
        pass
