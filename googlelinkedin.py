from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time
options = Options()
options.headless = True
driver = webdriver.Chrome(options=options)
driver.get('https://www.linkedin.com')
username=driver.find_element_by_class_name('login-email')
id=str(input("Enter User id for Linkedin"))
passj=str(input("Enter Password for linkedin"))
id1=str(input("Enter User id for Google"))
passj1=str(input("Enter Password for Google"))
username.send_keys(id)
password = driver.find_element_by_class_name("login-password")
password.send_keys(passj)
log_in_button = driver.find_element_by_xpath('//*[@type="submit"]')
log_in_button.click()
driver.get("https://www.google.com/")
time.sleep(1)
sign=driver.find_element_by_id("gb_70").click()
time.sleep(1)
email=driver.find_element_by_class_name("whsOnd")
email.send_keys(id1)
email.send_keys(Keys.RETURN)
time.sleep(2)
passw=driver.find_element_by_class_name("whsOnd")
passw.send_keys(passj1)
passw.send_keys(Keys.RETURN)
time.sleep(1)
ExcelFile = r"Excelfile.xlsx" #Mention Excel according to preference
# You have to check columns index before applying
df=pd.read_excel(ExcelFile, sheet_name=0, index_col=0)
len=df.size
for i in range (0,len):
    name=df["Name"][i]
    driver.get("https://www.google.com/")
    google_search =name+" "+"linkedin"
    search_query = driver.find_element_by_name('q')
    search_query.send_keys(google_search)
    search_query.send_keys(Keys.RETURN)
    linkedin = driver.find_elements_by_class_name('iUh30')
    linkedin[0].click()
    time.sleep(0.5)
    linkedinurl=driver.current_url
    df["Linkedin"][i]=linkedinurl
df.to_excel("W:\file_name.xlsx", "EditedSheet")