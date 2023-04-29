"""
projekt_3.py: třetí projekt do Engeto Online Python Akademie
author: Katerina Kordiovska
email: kordiovskak@gmail.com
discord: Petr Svetr#4490
"""

import requests
from bs4 import BeautifulSoup
import sys
import csv

print(sys.argv)

if len(sys.argv) != 3:
    print("Zadej tri argumenty")

"""

url = f"https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103"

odpoved_serveru = requests.get(url)

soup = BeautifulSoup(odpoved_serveru.text, features="html.parser")
table_tag = soup.find("div", {"class": "topline"})
td_tags = table_tag.find_all("td")

for i, td in enumerate(td_tags):
    if td.text.strip() and not td.has_attr("class") or "hidden_td" not in td["class"]:
        if i % 3 != 2:
            print(td.text)
"""
            


"""
urls = ["https://www.volby.cz/pls/ps2017nss/ps311?xjazyk=CZ&xkraj=12&xobec=506761&xvyber=7103", "https://www.volby.cz/pls/ps2017nss/ps311?xjazyk=CZ&xkraj=12&xobec=589268&xvyber=7103", "https://www.volby.cz/pls/ps2017nss/ps33?xjazyk=CZ&xkraj=12&xobec=589276", "https://www.volby.cz/pls/ps2017nss/ps311?xjazyk=CZ&xkraj=12&xobec=589284&xvyber=7103"]

for url in urls:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    table_tags1 = soup.find_all("table", {"id": "ps311_t1"})
"""


 # toto potrebuju zabalit do neceho aby mi to proslo vsechny xka v na ten strance = for cyklus

url = 'https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103'
response = requests.get(url)

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')

# Find all the URLs in the "td" elements with class "center"
td_elements = soup.find_all('td', {'class': 'center'})
#tu mam ulozene nove url 
urls = [f"https://www.volby.cz/pls/ps2017nss/{td_element.a['href']}" for td_element in td_elements]
#zistujem koniec url, podla ktorej zistim ci sa mam zanorit do novej stranky

    

# Connect to each URL 
for url in urls:
    
    if not url.endswith("&amp;xvyber=7103"):
        response = requests.get(url)
        soup2 = BeautifulSoup(response.text, 'html.parser')
        #tu musi byt ulozena kratka url
        redirected_url = f"https://www.volby.cz/pls/ps2017nss/{soup2.find('form')['action']}&amp;xvyber=7103"
        response = requests.get(redirected_url)

    odpoved_serveru1 = requests.get(url)
    print(f"URL: {url}")
    soup1 = BeautifulSoup(odpoved_serveru1.text, features="html.parser")
    table_tags1 = soup1.find_all("table", {"id": "ps311_t1"})

    for table_tag in table_tags1:
        td_tags = table_tag.find_all("td")
        print("upraveno: ",td_tags[3].text)
        print("upraveno: ",td_tags[4].text)
        print("upraveno: ",td_tags[7].text)

    strany = soup1.find_all("div", {"class": "t2_470"})

    for x in strany:
        rows = x.find_all("tr")
        for row in rows:
            cols = row.find_all("td")
            if len(cols) >= 3 and cols[2].text.strip():  # check that there are at least 3 columns in the row
                col2 = cols[1].text.strip()
                col3 = cols[2].text.strip()
                print(col2, col3)

    print("================================")



        
"""
    for table_tag in table_tags1:
        td_tags = table_tag.find_all("td")
        for td in td_tags[4]:
            print(td.text)

    for table_tag in table_tags1:
        td_tags = table_tag.find_all("td")
        for td in td_tags[7]:
            print(td.text)

"""