import requests
from bs4 import BeautifulSoup
import sys
import csv

print(sys.argv)

if len(sys.argv) != 3:
    print("Zadej dva argumenty")


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
cislo_list = []
overflow_name_list = []
url_list = []

# Find all table rows
table_rows = soup.find_all("tr")

# Loop through each row
for row in table_rows:
    # Find all cells in the row
    cells = row.find_all("td")
    
    # If the row has more than one cell
    if len(cells) > 1:
        # Extract the "cislo" and "overflow_name" values
        cislo = cells[0].text.strip()
        overflow_name = cells[1].text.strip()
        
        # Add them to the respective lists
        cislo_list.append(cislo)
        overflow_name_list.append(overflow_name)
        
        # If the third cell has a link
        url_element = cells[2].find("a")
        if url_element is not None: #and "hidden_td" not in cells[2].get("class", []):
            # Build the full URL
            url = base_url + url_element["href"]
            url_list.append(url)

# Create a list of dictionaries containing the scraped data
data = []
for i in range(len(cislo_list)):
    if i < len(url_list):
        # Make the request for the current URL
        #temp_url = url 
        url = url_list[i]
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
    
    # Scrape the data from the table
    table_tags1 = soup.find_all("table", {"id": "ps311_t1"})

    for table_tag in table_tags1:
        td_tags = table_tag.find_all("td")
        volici_v_seznamu = td_tags[3].text
        vydane_obalky = td_tags[4].text
        odevzdane_obalky = td_tags[7].text

    

    strany = soup.find_all("div", {"class": "t2_470"})

    for x in strany:
        rows = x.find_all("tr")
        for row in rows:
            cols = row.find_all("td")
            if len(cols) >= 3 and cols[2].text.strip():  # check that there are at least 3 columns in the row
                politicka_strana = cols[1].text.strip()
                all_votes = cols[2].text.strip()
                print(politicka_strana, all_votes)
    
    # Add the scraped data to the dictionary
    if i < len(url_list):
        data.append({
            "Number": cislo_list[i],
            "City": overflow_name_list[i],
            "URL": url_list[i],
            "Volici v seznamu": volici_v_seznamu,
            "Vydane obalky": vydane_obalky,
            "Odevzdane obalky": odevzdane_obalky,
            #"politicka_strana": politicka_strana,
            #"all_votes": all_votes
        })

# Write the data to a CSV file
with open(csv_file_name, "w", encoding="utf-8", newline="") as csvfile:
    fieldnames = ["Number", "City", "URL", "Volici v seznamu", "Vydane obalky", "Odevzdane obalky"]#, "politicka_strana", "all_votes"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for d in data:
        writer.writerow(d)

print(f"Data has been scraped and saved to {csv_file_name}")
