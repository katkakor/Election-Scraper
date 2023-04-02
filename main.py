"""
projekt_3.py: třetí projekt do Engeto Online Python Akademie
author: Katerina Kordiovska
email: kordiovskak@gmail.com
discord: Petr Svetr#4490
"""

import requests
from bs4 import BeautifulSoup
import sys

print(sys.argv)

if len(sys.argv) != 3:
    print("Zadej tri argumenty")

url = f"https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103"

odpoved_serveru = requests.get(url)

soup = BeautifulSoup(odpoved_serveru.text, "html.parser")
print(soup.prettify())
table_tag = soup.find("div", {"class": "t3"})
print(table_tag.prettify())
vsechny_tr = table_tag.find("tr")
len(vsechny_tr)
print(vsechny_tr.text)
td_na_radku = vsechny_tr[1].find_all("td")
print(td_na_radku[4].get_text())
print(td_na_radku[2].text())