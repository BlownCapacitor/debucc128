from selenium import webdriver
from bs4 import BeautifulSoup
import time 
import csv
import time
from flask import request
start_url = 'https://exoplanets.nasa.gov/discovery/exoplanet-catalog/'
browser = webdriver.Chrome('/Users/swatiahuja/Desktop/c127/venv/chromedriver')
browser.get(start_url)
time.sleep(10)
headers = ['name','light_years_from_earth', 'planet_mass','stellar_magnitude','discovery_date', 'hyperlink', 'planet_type', 'orbital_radius', 'orbital_period', 'detection_method', 'eccentricity']
planetData  = []
newPlanetData = []
def scrape():
    for i in range(0,5):
        soup = BeautifulSoup(browser.page_source, 'html.parser')
        for ul_tags in soup.find_all('ul',attrs={'class', 'exoplanet'}):
            li_tag = ul_tags.find_all('li')
            temp_list = []
            for index,li_tags in enumerate(li_tag):
                if index == 0:
                    temp_list.append(li_tags.find_all('a')[0].contents[0])
                else:
                    try:
                        temp_list.append(li_tags.contents[0])
                    except:
                        temp_list.append('')
            planetData.append(temp_list)

            hyperlink_li = li_tag[0]
            temp_list.append('https://exoplanets.nasa.gov/discovery'+ hyperlink_li.find_all('a', href = True)[0]['href'])
            planetData.append(temp_list)
        browser.find_element_by_xpath('//*[@id="primary_column"]/div[1]/div[2]/div[1]/div/nav/span[2]/a').click()
def scrape_more_data(hyperlink):
        try:
            page = request.get(hyperlink)
            soup = BeautifulSoup(page.content, 'html.parser')
            temp_list2 = []
            for tr_tags in soup.find_all('tr',attrs={'class': 'fact_row'}):
                td_tags = tr_tags.find_all('td')
                for td_tag in td_tags:
                    try:
                        temp_list2.append(td_tag.find_all('div',attrs={'class':'value'})[0].contents[0])
                    except:
                        temp_list2.append('')
                newPlanetData.append(temp_list2)
        except:
            time.sleep(1)
            scrape_more_data(hyperlink)
scrape()  
for index,data in enumerate(planetData):
    scrape_more_data(data[5])
    print('page 2 done')
final_planetData = []
for index,planet in enumerate(planetData):
    final_planetData.append(planet+final_planetData[index])
    
with open('FINAL.csv','w') as f:
    csvWriter = csv.writer(f)
    csvWriter.writerow(headers)
    csvWriter.writerows(final_planetData)
           
