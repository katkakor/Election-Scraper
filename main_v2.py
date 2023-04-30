import requests
from bs4 import BeautifulSoup
import sys
import csv

"""
novy porgram je v souboru main_v2.py
problem je ze nevim jak do csv souboru dostat platne hlasy https://www.volby.cz/pls/ps2017nss/ps311?xjazyk=CZ&xkraj=12&xobec=506761&xvyber=7103
pokud je to jak z linku vyse, tak to mam ve funkci get_pocet_volicov_na_stranu, problem je ze je to jeden dlhy list a nevim jak to dostat do csv souboru spravne do radku ku kazde strane
druhy problem je ze bych potrebovala dalsi funkci napriklad get_pocet_volicov_na_stranu_sum ktera mi zpocita soucty v okrskech napriklad https://www.volby.cz/pls/ps2017nss/ps33?xjazyk=CZ&xkraj=12&xobec=589276
tady jsou dva okrsky a to potrebuji scitat a hodit do csv.

Priklad funkci kde toto delam pro volici v seznamu, odevzdane obalky a platne hlasy get_volici_obalky a get_volici_obalky_sum, logika programu je v tom ze jednu nebo druhou funkci 
volam na zaklade toho jestli url obsahuje "xvyber" - if "xvyber" not in url:

Cili problem je: 
1. jestli je spravne funkce get_pocet_volicov_na_stranu
2. nemam funkci get_pocet_volicov_na_stranu_sum
3. nevim jak to pak zapsat oboje co csv
4. indexy jsou out of range
"""


# URL to scrape
# enter input
#url = input("zadaj URL>>> ")
url = "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103"
#a brno jeste mene
#url = "https://www.volby.cz/pls/ps2017nss/ps311?xjazyk=CZ&xkraj=12&xobec=506761&xvyber=7103"

#enter input
#csv_file_name = input("zadaj nazov csv suboru>>> ")
csv_file_name = "data.csv"

# url where will be continuing X URL added 
base_url = "https://www.volby.cz/pls/ps2017nss/"

# Make the request


# Lists to store the data
cislo_obce_list = []
nazev_obce_list = []
url_list = []
volici_v_seznamu_list = []
vydane_obalky_list = []
platne_hlasy_list = []
seznam_stran_list = []



def get_nazvy_stran(temp_url):
    
    response = requests.get(temp_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    td_elements = soup.find_all('td', class_='overflow_name')

    headers = []
    for td in td_elements:
        headers.append(td.text.strip())
        #print(td.text.strip())
    return headers

volici = []
def get_pocet_volicov_na_stranu(temp_url):
    #print("HELLOOOOOOOOOOOOO")
    response = requests.get(temp_url)
    soup = BeautifulSoup(response.content, "html.parser")
    td_elements = soup.find_all('td', class_='cislo', headers='t1sa2 t1sb3')
    td_elements_2 = soup.find_all('td', class_='cislo', headers='t2sa2 t2sb3')
    #print("TA ELEMENTS: ", td_elements)
    
    for td in td_elements:
        volici.append(td.text.strip())
        #print(td.text.strip())
    for td in td_elements_2:
        volici.append(td.text.strip())
        #print(td.text.strip())
    # split volici list into sublists of length 30
    #volici_split = [volici[i:i+30] for i in range(0, len(volici), 30)]
    return volici
 

#sem ide funkcia def get_volici_obalky(temp_url):
def get_volici_obalky(temp_url):
    response = requests.get(temp_url)
    soup = BeautifulSoup(response.content, "html.parser")
    volici_v_seznamu = soup.find('td', class_='cislo', headers='sa2').text.strip()
    vydane_obalky = soup.find('td', class_='cislo', headers='sa3').text.strip()
    platne_hlasy = soup.find('td', class_='cislo', headers='sa6').text.strip()

    volici_v_seznamu_list.append(volici_v_seznamu)
    vydane_obalky_list.append(vydane_obalky)
    platne_hlasy_list.append(platne_hlasy)

def get_volici_obalky_sum(temp_url):
    response = requests.get(temp_url)
    soup = BeautifulSoup(response.content, "html.parser")
    volici_v_seznamu = soup.find('td', class_='cislo', headers='sa2').text.strip()
    vydane_obalky = soup.find('td', class_='cislo', headers='sa3').text.strip()
    platne_hlasy = soup.find('td', class_='cislo', headers='sa6').text.strip()
    
    volici_v_seznamu_temp = int(volici_v_seznamu.replace('\xa0', ''))
    vydane_obalky_temp = int(vydane_obalky.replace('\xa0', ''))
    platne_hlasy_temp = int(platne_hlasy.replace('\xa0', ''))

    return volici_v_seznamu_temp, vydane_obalky_temp, platne_hlasy_temp


#main code start
response = requests.get(url)

# Parse the HTML content
soup = BeautifulSoup(response.content, "html.parser")
# Find all table rows
table_rows = soup.find_all("tr")


# Loop through each row
for row in table_rows:
    # Find all cells in the row
    cells = row.find_all("td")

    # If the row has more than one cell
        # If the row has more than one cell and not a hidden_td
    if len(cells) > 1 and 'hidden_td' not in cells[0]['class']:
        # Extract the "cislo" and "overflow_name" values
        cislo_obce = cells[0].text.strip()
        nazev_obce = cells[1].text.strip()
        
        # Add them to the respective lists
        cislo_obce_list.append(cislo_obce)
        nazev_obce_list.append(nazev_obce)
        
        # If the third cell has a link
        url_element = cells[2].find("a")
        print(cislo_obce, nazev_obce)
        
        if url_element is not None: 
            # Build the full URL
            url = base_url + url_element["href"]
            #print("URL IN MIDDLE: ", url)
            
            if "xvyber" not in url:
                # Make another request to the URL
                response2 = requests.get(url)
                # Parse the HTML content
                soup2 = BeautifulSoup(response2.content, "html.parser")
                table = soup2.find("table", class_="table")

                sum_volici = 0
                sum_obalky = 0
                sum_hlasy = 0

                for td in table.find_all("td", class_="cislo"):
                    temp_url_element = td.find("a")
                    if temp_url_element is not None:
                        temp_url = base_url + temp_url_element["href"]

                        #print("uz posledna url>>>>>> ", temp_url)
                        
                        get_volici_obalky_sum(temp_url)
                        volici_v_seznamu_temp, vydane_obalky_temp, platne_hlasy_temp = get_volici_obalky_sum(temp_url)
                        sum_volici += volici_v_seznamu_temp
                        sum_obalky += vydane_obalky_temp
                        sum_hlasy += platne_hlasy_temp
                        
                        #url_list.append(temp_url)
                #print("Volici: ", sum_volici, " obalky: ", sum_obalky, " hlasy: ", sum_hlasy)
                
                volici_v_seznamu_list.append(sum_volici)
                vydane_obalky_list.append(sum_obalky)
                platne_hlasy_list.append(sum_hlasy)

            else:   
                #get_volici_obalky(url)
                volici_split = get_pocet_volicov_na_stranu(url)
                #print("list volicov: ",volici)
                url_list.append(url)

headers_list = get_nazvy_stran(url_list[0])
#data_list = get_nazvy_stran(url_list[0])
# Write the data to a CSV file
"""
if len(cislo_obce_list) != len(nazev_obce_list) or len(cislo_obce_list) != len(volici_v_seznamu_list) or len(cislo_obce_list) != len(vydane_obalky_list) or len(cislo_obce_list) != len(platne_hlasy_list) or len(cislo_obce_list) != len(headers_list):
    print("Error: Lists have different lengths.")
else:
"""
with open(csv_file_name, mode='w', encoding='utf-8', newline='') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(["cislo_obce", "nazev_obce", "volici_v_seznamu", "vydane_obalky", "platne_hlasy"] + headers_list)
    for i in range(len(cislo_obce_list)):
        writer.writerow([cislo_obce_list[i], nazev_obce_list[i], volici_v_seznamu_list[i], vydane_obalky_list[i], platne_hlasy_list[i]])

print(f"Data has been scraped and saved to {csv_file_name}")




