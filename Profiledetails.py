# Libraries used : Selenium, BeautifulSoup
import bs4
import requests
from selenium import webdriver
from bs4 import BeautifulSoup as soup
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

# Headless in order to prevent browser opening
options = Options()
options.headless = True


address85='https://www.ai-expo.net/europe/speakers/'
headr = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Cafari/537.36'}
my_url = address85
page = requests.get(my_url, headers=headr)
page_html = soup(page.content, "lxml")
body = page_html.body
sec=body.find_all('div', {"class": "speaker-expand"})
print("Total Names found :",len(sec)-1)


# Starting File from here
filename = "database.csv"
f = open(filename, "w", encoding="utf-8")
headers = "Event Name, Speaker Name, Display Pic url,Designation, Company, Short Bio, City, Country, Linkedin, Twitter, Wikipedia, Facebook, Website\n"
f.write(headers)
print("Creating your CSV file, Please Wait\n")

# Main Scraping Loop
for i in range(len(sec)-1):
    driver = webdriver.Chrome(options=options)
    Speaker_Name = sec[i].h3.text                                                      # BS4 is used here 
    Event_Name="AI & Big Data Expo"
    profile=sec[i].find_all('h4')
    Designation = profile[0].text
    Company = profile[1].text                                                          # Name, Designation, Company scrapped

    driver.get('https://www.google.com/')
    search_query = driver.find_element_by_name('q')
    search_query.send_keys(Speaker_Name+" "+Designation+" "+Company+" "+"Linkedin")
    search_query.send_keys(Keys.RETURN)
    linkedin_urls = driver.find_elements_by_class_name('iUh30')
    lurl=linkedin_urls[0].text                                                         # Linkedin Scrapped

    driver.get('https://www.google.com/')
    search_query = driver.find_element_by_name('q')
    search_query.send_keys(Speaker_Name+" "+Designation+" "+Company+" "+"twitter")
    search_query.send_keys(Keys.RETURN)
    twitter_urls = driver.find_elements_by_class_name('iUh30')
    turl=twitter_urls[0].text                                                          # Twitter Scrapped

    driver.get('https://www.google.com/')
    search_query = driver.find_element_by_name('q')
    search_query.send_keys(Speaker_Name+" "+ "facebook")
    search_query.send_keys(Keys.RETURN)
    fburl = driver.find_elements_by_class_name('iUh30')
    facebook=fburl[0].text                                                             # Facebook Scrapped

    driver.get('https://www.google.com/')
    search_query = driver.find_element_by_name('q')
    search_query.send_keys(Speaker_Name+" "+ "ai-expo speaker")
    search_query.send_keys(Keys.RETURN)
    dburl = driver.find_elements_by_class_name('iUh30')
    ppurl=dburl[0].text
    pageb = requests.get(ppurl, headers=headr)
    page_htmlb = soup(pageb.content, "lxml")
    bodyb = page_htmlb.body
    p=bodyb.find_all('p') 
    try:
        para=p[1].text    
    except (IndexError):
        para="Not Available on expo"
    pic=bodyb.find('img',{'alt':Speaker_Name})
    picsrc=pic['src']                                                                  # Profile pic link and Description Scrapped

    driver.get(lurl)
    cit=driver.find_elements_by_class_name("t-16")
    try:
        cit[1].text
        if "," in cit[1].text:
            city=cit[1].text.split(",")
            er=city[-2]
            country=city[-1]
        else:                   
            country=cit[1].text
            er="Not Available" 
    except (IndexError):
        er="Not Available"
        country="Not Available"                                                            # City and Country Scrapped

    driver.get('https://www.google.com/')
    search_query = driver.find_element_by_name('q')
    search_query.send_keys(Company)
    search_query.send_keys(Keys.RETURN)
    wiki=driver.find_elements_by_class_name('iUh30')
    wikilink=''
    for i in wiki:
        if 'wiki' in i.text:
            wikilink=i.text
    weblink=wiki[0].text                                                               # Wikipedia page and Website Scrapped

    print("Profile :",i.text,Speaker_Name," succesfully scrapped")                            # End of Loop
    driver.close()

    f.write( '"' + Event_Name + '","' + Speaker_Name + '","' + picsrc + '","' + Designation + '","' + Company + '","' + para + '","' + er + '","' + country + '","' + lurl + '","' + turl + '","' + wikilink + '","' + facebook + '","' + weblink + '","' + '"\n' )
f.close()
