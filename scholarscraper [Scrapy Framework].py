from time import sleep
import pandas as pd
from csv import writer
import scholarly
import os

# Instructions:
# 1> Place the excel file in the same directory as the code
# 2>Modify the name of the file to suit the name of the dataset

# Scratchpad:
# author-
#     affiliation
#     citedby
#     cites_per_year
#     email
#     hindex
#     hindex5y
#     i10index
#     i10index5y
#     id
#     interests
#     publications-
#         bib-
#             abstract
#             author
#             eprint
#             journal
#             publisher
#             title
#             url
#             year
#         citedby

max_publications_per_author = 30
threshold = 40
path_of_xlsx = os.getcwd() + "/Final-DSP.xlsx"

def main(path_of_xlsx):
    df = pd.read_excel(path_of_xlsx)
    start = int(input("Enter the start: "))
    stop = int(input("Enter the stop: "))
    #stop-start should not exceed 35 at all times!
    if stop-start<=threshold:
        scrape_is_go(df, start, stop)
    else:
        return print("\nThreshold exceeded. Aborted for safety. Retry.")
    print("\nScraping done. Give and take a break")
    return

def scrape_is_go(df, start, stop):
    names = df.loc[start:stop,"Reporter Name"].tolist()
    with open(f"file{start}-{stop}.csv", "w+",encoding="utf-8") as file:#Here added the encoding as utf-8 to avoid encoding error while scrapping
        total_records = len(names)
        records_done = 1
        records_lost = 0
        csv_writer = writer(file)
        csv_writer.writerow(["Name","Affiliation", "Citedby", "cites_per_year","email", "hindex", "hindex5y", "i10index", "i10index5y", "id", "interests", "Publications"])
        for c, name in enumerate(names, 1):
            name, affil, citedby, cites_per_year, email, hindex, hindex5y, i10index, i10index5y, id, interests, publications = scrape_individual(name, max_publications_per_author)
            csv_writer.writerow([name, affil, citedby, cites_per_year, email, hindex, hindex5y, i10index, i10index5y, id, interests, publications])
            print(f"\n{c}/{len(names)} records done")
            sleep(3)
    return

def scrape_individual(name, max_publications_per_author):
    search = scholarly.search_author(name)
    try:
        query = next(search)
    except:
        print(f"\n{name} got no records. Try manually.")
        return (name, "", "", "", "", "", "", "", "", "", "", "")
    author = query.fill()
    try:
        affil = author.affiliation
    except:
        affil = ""
    try:
        citedby = author.citedby
    except:
        citedby = -1    #-1 Means not available
    try:
        cites_per_year = author.cites_per_year
    except:
        cites_per_year ="{}"
    try:
        email = author.email
    except:
        email = ""
    try:
        hindex = author.hindex
    except:
        hindex = -1    #-1 Means not available
    try:
        hindex5y = author.hindex5y
    except:
        hindex5y = -1
    try:
        i10index = author.i10index
    except:
        i10index = -1
    try:
        i10index5y = author.i10index5y
    except:
        i10index5y = -1
    try:
        id = author.id
    except:
        id = ""
    try:
        interests = author.interests
    except:
        interests = "[]"
    publications = []
    pub_c = 0
    total_publications = author.publications
    print(f"{name} got {len(total_publications)} publications")
    for pub in total_publications:
        if pub_c<max_publications_per_author:
            try:
                pub_body = pub.fill()
                pub_title = pub_body.bib["title"]
                pub_text = pub_body.bib["abstract"]
                try:
                    pub_author = pub_body.bib["author"]
                except:
                    pub_author = ""
                try:
                    pub_eprint = pub_body.bib["eprint"]
                except:
                    pub_eprint = ""
                try:
                    pub_publisher = pub_body.bib["publisher"]
                except:
                    pub_publisher = ""
                try:
                    pub_year = pub_body.bib["year"]
                except:
                    pub_year = ""
                try:
                    pub_citedby = pub_body.citedby
                except:
                    pub_citedby = ""
                #Please do not modify the formatted_line as it will jeopardize pipelining
                formatted_line = "|Title|"+str(pub_title)+"|Body|"+str(pub_text)+"|Author|"+str(pub_author)+"|Year|"+str(pub_year)+"|Publisher|"+str(pub_publisher)+"|Citedby|"+str(pub_citedby)+"|Eprint|"+str(pub_eprint)
                publications.append(formatted_line)
                pub_c+=1
            except:
                continue
        else:
            break
    return name, affil, citedby, cites_per_year, email, hindex, hindex5y, i10index, i10index5y, id, interests, publications




if __name__=="__main__":
    main(path_of_xlsx)
