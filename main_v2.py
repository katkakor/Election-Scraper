import requests
from bs4 import BeautifulSoup
import sys
import csv

#nezabudnut zahrnut kontrolu systemovu z main suboru
#print(sys.argv)

#if len(sys.argv) != 3:
#    print("Zadej dva argumenty")


# URL to scrape
# enter input
url = "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103"

# CSV file name
#enter input
csv_file_name = "data.csv"

# url where will be continuing X URL added 
base_url = "https://www.volby.cz/pls/ps2017nss/"

# Make the request
response = requests.get(url)

# Parse the HTML content
soup = BeautifulSoup(response.content, "html.parser")

# Lists to store the data
cislo_obce_list = []
nazev_obce_list = []
url_list = []
volici_v_seznamu = []
vydane_obalky = []
odevzdane_obalky = []

# Find all table rows
table_rows = soup.find_all("tr")

def if_content_is_none(temp):
    if temp is not None:
        temp = temp.text.strip()
        print(temp)
    else:
        temp = "N/A"

def get_volici_obalky(temp_url):
    
    response = requests.get(temp_url)
    soup = BeautifulSoup(response.content, "html.parser")
    
    # Scrape the data from the table
    volici_v_seznamu = soup.find('td', class_='cislo', headers='sa2')
    print("VOLICI V SEZNAMU ", volici_v_seznamu.text.strip())
    #if_content_is_none(volici_v_seznamu)
 
    vydane_obalky = soup.find('td', class_='cislo', headers='sa3')
    print("VYDANE OBALKY ", vydane_obalky.text.strip())
    #if_content_is_none(vydane_obalky)
  
    odevzdane_obalky = soup.find('td', class_='cislo', headers='sa5')
    print("ODEVZDANE OBALKY ", odevzdane_obalky.text.strip())
    #if_content_is_none(odevzdane_obalky)

    #print("Volici v seznamu, vydane obalky, odevzdane obalky: ",volici_v_seznamu.text.strip(),vydane_obalky.text.strip(), odevzdane_obalky.text.strip())

# Loop through each row
for row in table_rows:
    # Find all cells in the row
    cells = row.find_all("td")
    
    # If the row has more than one cell
    if len(cells) > 1:
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
            #print("URL ELEMENT", url_element["href"])
            url = base_url + url_element["href"]
            if "xvyber" not in url:
                # Make another request to the URL
                #url = "https://www.volby.cz/pls/ps2017nss/ps33?xjazyk=CZ&xkraj=12&xobec=589276"
                response2 = requests.get(url)
                
                # Parse the HTML content
                soup2 = BeautifulSoup(response2.content, "html.parser")
                # NIEKDE V TEJTO CASTI JE CHYBA, MUSIM PRIST NA TO PRECO MI TO TAM DAVA VIAC URL AKO BY MALO
                vnorene_url = soup.find_all("td", class_="cislo")
                for x in vnorene_url:
                    temp_url = x.find("a")
                    #if temp_url is not None:
                    url = base_url + temp_url["href"]
                    url_list.append(url)
                    print("Vnorena url: ", url)
            else:
                
                url_list.append(url)
                #print("Zakladna url: ", url)
                #get_volici_obalky(url)

# Write the data to a CSV file
with open(csv_file_name, mode='w', encoding='utf-8', newline='') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(["cislo_obce", "nazev_obce", "url"])
    for i in range(len(cislo_obce_list)):
        writer.writerow([cislo_obce_list[i], nazev_obce_list[i], url_list[i]])

print(f"Data has been scraped and saved to {csv_file_name}")
