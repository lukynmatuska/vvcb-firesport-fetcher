import requests
from bs4 import BeautifulSoup
import json
from flask import Flask

app = Flask(__name__)

def get_data_from_table(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    tables = soup.findAll('table')
    
    if not tables:
        return None
    
    data = []
    for table in tables[1:-3]:
        table_data = []
        # print(table)
        headers = [header.text.strip() for header in table.find_all('th')]

        rows = table.find_all('tr')
        for row in rows[1:]:
            cells = row.find_all('td')
            row_data = [cell.text.strip() for cell in cells]
            table_data.append(dict(zip(headers, row_data)))
        data.append(table_data)

    return data

@app.route("/")
def hello_world():
    return {
        "message": "Hello, World!"
    }

@app.route("/results/<path:url>")
def results(url):
    return get_data_from_table(url) or {}

# if __name__ == "__main__":
    
#     # url = "https://vcbl.firesport.eu/vysledek-ostrov-u-macochy-12991.html"
#     url = "https://vcbl.firesport.eu/vysledek-cernovice-12995.html"
#     data = get_data_from_table(url)

#     if data:
#         json_data = json.dumps(data, indent=4) #, ensure_ascii=False)
#         # print(json_data)

#         # Writing to sample.json
#         with open("output.json", "w") as outfile:
#             outfile.write(json_data)

#     else:
#         print("Data not found.")
