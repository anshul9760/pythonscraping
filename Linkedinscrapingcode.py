#Make sure to have Selenium, Webdriver, Beautifulsoup before running
#Change location of chromedriver accordingly
from selenium import webdriver
import bs4
from bs4 import BeautifulSoup as soup
import time
address="chromedriver.exe"
address1="W:/"                           #To avoid /c
driver = webdriver.Chrome(address1+address)
driver.get('https://www.linkedin.com')
username=driver.find_element_by_class_name('login-email')
id=str(input("Enter Email id with connections\n"))
passj=str(input("Enter Password\n"))
username.send_keys(id)
password = driver.find_element_by_class_name("login-password")
password.send_keys(passj)
log_in_button = driver.find_element_by_xpath('//*[@type="submit"]')
log_in_button.click()
#Empty declaration to avoid Exceptions
Company_Name=''
Employee_first_name=''
Employee_Last_name=''
location=''
Designation=''
links=["https://www.linkedin.com/company/expertise-events",
    "https://www.linkedin.com/company/jscstone",
    "https://www.linkedin.com/company/exhibitions-&-trade-fairs",
    "https://www.linkedin.com/company/penton-media-europe",
    "https://www.linkedin.com/company/transworld-exhibits",
    "https://www.linkedin.com/company/motor-trend-auto-shows-inc",
    "https://www.linkedin.com/company/show-group-enterprises-pty-limited",
    "https://www.linkedin.com/company/golden-triangle-angelnet",
    "https://www.linkedin.com/company/scoop-international",
    "https://www.linkedin.com/company/iaapa",
    "https://www.linkedin.com/company/thetoyassociation"]
print("Respective links are already listed as per assignment\n")
value=str(input("To add more links to scrap type yes\n"))
if value=="yes":
    nm=int(input("Enter no. of URLs"))
    for i in range(0,nm):
        value1=str(input("Enter one by one\n"))
        links.append(value1)
else:
    pass
lenoflink=len(links)
l=['Event Co-ordinator', 'Marketing director', 'Financial controller','PR consultant', 'Event portfolio director', 'Marketing Manager', 'Event Manager', 'Marcom manager', 'Brand Marketing Manager', 'Group Marketing Manager', 'Digital Marketing Manager', 'Brand Director', 'Project Manager', 'Senior marketing manager','General Manager - Consumer Events at Expertise Events']
print("Designations are already listed as per assignment\n")
value=str(input("To add more type yes\n"))
if value=="yes":
    nm=int(input("Enter no. of Designations"))
    for i in range(0,nm):
        value1=str(input("Enter one by one\n"))
        l.append(value1)
else:
    pass

for i in range(0,lenoflink):
    driver.get(links[i])
    pagetemp=driver.page_source
    title_soup=soup(pagetemp, features="lxml")
    title=title_soup.body
    company=title.findAll("span",{"dir":"ltr"})
    companyname=company[0].text
    employ=""
    employ = driver.find_element_by_class_name("v-align-middle")
    if employ=="":
        break
    else:
        employ.click()
        time.sleep(2)

    page=driver.page_source
    page_soup=soup(page, features = "lxml")
    body=page_soup.body
    e=body.findAll("div",{"class":"blended-srp-results-js pt0 pb4 ph0 container-with-shadow"})
    num=e[0].h3.text.strip().split()
    num[1]
    num1=int(num[1])
    if num1%10==0:
        next=int(num1/10)+1
    else:
        next=int(num1/10)+2
    url=driver.current_url
    urltemp=url 

    for n in range(1,next):
        m=str(n)
        page1=driver.page_source
        page_soup1=soup(page1, features = "lxml")
        body1=page_soup1.body
        data=body1.findAll("div",{"class":"search-result__info pt3 pb4 ph0"})
        for i in l :
            for p in range(0,len(data)):
                des=data[p].findAll("span",{"dir":"ltr"})
                if i in des[0].text:
                    nametemp = data[p].findAll("span",{"class":"actor-name"})
                    name=nametemp[0].text.split()
                    if name[0]=='Linkedin':
                        print("Given Id is without connections")
                        Employee_first_name=name[0]
                        break
                    else:
                        file="linkedin.csv"
                        f = open(file, "w")
                        headers = "Company_Name, Employee_first_name, Employee_Last_name, profile Url, Designation, location"
                        f.write(headers)
                        Company_Name=companyname
                        Employee_first_name=name[0]
                        Employee_Last_name=name[1]
                        location=des[1].text
                        Designation=i
                        f.write( '"' + Company_Name + '","' + Employee_first_name + '","' + Employee_Last_name + '","' + location + '","' + Designation + '"\n' )
        driver.get(url+'&page='+m) 
        url=urltemp
        f.close()
