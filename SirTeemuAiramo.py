import requests
from bs4 import BeautifulSoup
import time
import csv
import sys


CompanyName = []
Location = []
DotNumber = []
SafetyLink = []
td_data =[]
querlink = []

PageStartingLink = 'https://www.fmcsa.dot.gov'
with open('TestingZip.csv', newline='') as csvfile:
     data = csv.DictReader(csvfile)

    #File Open and company name on browser

     for row in data:
         zip_code = (row['zip'])
         #print(zip_code)

        #Create Link to Open Pages.
        #for Large Vechicles
         query = 'https://www.fmcsa.dot.gov/safety/passenger-safety/search-results/vehicle-search?&state=&type=MC&zip='+ zip_code
         print(query)
         #querlink.append(query)

         r = requests.get(query)
         soup = BeautifulSoup(r.content, 'html5lib')

         if soup.find(class_='sticky-enabled'):
             ist_page_data = soup.find(class_='sticky-enabled')
             #print(ist_page_data)
             alltr = soup.find_all("tr", class_=['odd', 'even'])
             for x in alltr:
                 safetylink = x.find('a').get('href')
                 SafetyLink.append(safetylink)
                #print(safetylink)


             for tr in alltr:  # for each row
                 td = tr.find_all('td')  # find all cells
                 if len(td) < 4:
                     continue
                 row = [i.text for i in td]
                 cname = row[0]
                 CompanyName.append(cname)
                 loction = row[1]
                 Location.append(loction)
                 dotnum = row[2]
                 DotNumber.append(dotnum)
                 #print(row)

             #print('Content Found')
             try:
                 if soup.find(class_='pager'):
                    pages = soup.findAll(class_='pager-item')
                    #print(pages)
                    for div in pages:
                        MakeProperLink = PageStartingLink + div.find("a").get("href")
                        #print(MakeProperLink)
                        r = requests.get(MakeProperLink)
                        soup = BeautifulSoup(r.content, 'html5lib')
                        alltr = soup.find_all("tr", class_=['odd', 'even'])
                        for x in alltr:
                            safetylink = x.find('a').get('href')
                            SafetyLink.append(safetylink)
                        # print(safetylink)

                        for tr in alltr:  # for each row
                            td = tr.find_all('td')  # find all cells
                            if len(td) < 4:
                                continue
                            row = [i.text for i in td]
                            cname = row[0]
                            CompanyName.append(cname)
                            #print(cname)
                            loction = row[1]
                            Location.append(loction)
                            dotnum = row[2]
                            DotNumber.append(dotnum)


                 else:
                     print("NO paginations")
             except:
                 pass



         else:
            print('Sorry, No Information against Zip Code')

print(CompanyName)
print(DotNumber)
print(Location)
print(SafetyLink)

with open('FMCSA.csv','w',newline='',encoding='utf-8') as csvfile:
    fieldsName = ['CompanyName','Location','DotNumber','SafetyLink']
    writer = csv.DictWriter(csvfile, fieldnames=fieldsName)
    writer.writeheader()
    for CN,Loc,DN,Sl in zip(CompanyName,Location,DotNumber,SafetyLink):
        writer.writerow({'CompanyName':CN , 'Location':Loc, 'DotNumber':DN,'SafetyLink':Sl})


sys.exit()


