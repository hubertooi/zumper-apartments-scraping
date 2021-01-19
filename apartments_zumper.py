# import needed packages
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

# User inputs on city, state code, max price, min price and no of pages
city = input("Enter the city for apartment: ")
state = input("Enter the state for apartment: ")
price_max = input("Enter the upper price: ")
price_min = input("Enter the lower price: ")
pages = input("Enter the page number: ")

# apartment list to store data
apartment_list = []

# for loop to iterate through pages 1 to the input pages
for page in range(1, int(pages) + 1, 1):
    # url of zumper website with input parameters
    url = f"https://www.zumper.com/apartments-for-rent/{city}-{state}/1-beds/price-{price_min},{price_max}?page={page}"
    print(url) # print statement to for user to check if url exist
    r = requests.get(url) # requests.get(url)
    bs = BeautifulSoup(r.content, 'html.parser') # beautifulsoup parsing

    # find all apartments with bs.find_all with its associating tags and class
    apartments = bs.find_all('div', class_="Listables_listItemContainer__2j0Fo")

    # for loop to iterate thru each apartments
    for each in apartments:
        # name data
        name_or_address = each.find('a', {'aria-hidden': 'false'}).text.strip()
        # price data
        price = each.find('div', {'class': 'ListItemMobileView_price__1IH5H'}).text.strip()
        # hybrid if else statement to obtain phone_num
        phone_num = each.find('a', {
            'class': 'button_baseBtn__2y4lB button_zBtn__2zryS button_zBtnSecondary__3yZg6 Contact_phoneBtn__11zs-'}).attrs[
            'href'] if (each.find('a', {
            'class': 'button_baseBtn__2y4lB button_zBtn__2zryS button_zBtnSecondary__3yZg6 Contact_phoneBtn__11zs-'}) is not None) else "none"
        # link data
        link = "https://www.zumper.com" + each.find('a', {'class': 'ListItemMobileView_address__B8pfK'}).attrs['href']
        # neigborhood data
        neigborhood = each.find('div', {'class': 'ListItemMobileView_address__B8pfK'}).text.strip()
        # using regular expression sub method to substitute a none word characters with comma
        # [^a-zA-Z\s\-]+ exclude none word characters and plus white space, \s and dash, \-
        # "," replaces the none word characters with a comma
        area = re.sub('[^a-zA-Z\s\-]+',',', neigborhood)

        # apartment information set up for the csv file
        apartment_info = {
            'name/address': name_or_address,
            'neighborhood': area,
            'price': price,
            'phone number': phone_num,
            'link': link
        }

        # apartment_info is appended to apartment_list
        apartment_list.append(apartment_info)

df = pd.DataFrame(apartment_list)  # set up a pd dataframe tabular data format
# path location to save csv file to your desire path
path = 'C:\\Users\\Hubert\\Desktop\\Apartment-Hunt\\'+f'apartments_{city}_{state}.csv'
print(f"\nThe path of save file {path}") # 
df.to_csv(path, index=False)  # save df to_csv format without the indexing from pandas library