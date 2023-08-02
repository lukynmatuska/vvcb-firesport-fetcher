import requests
from bs4 import BeautifulSoup
from flask import Flask
from flask_cors import CORS
import datetime
import os

app = Flask(__name__)

CORS(app)

def get_data_from_url(url):
    response = requests.get(url)
    response.encoding = 'windows-1250'
    soup = BeautifulSoup(response.text, 'html.parser')

    tables = {
        'muzi': '#tab1151',
        'zeny': '#tab124',
        'veterani': '#tab1104',
        'dorostenci': '#tab184'
    }

    for table_key in tables.keys():
        table = soup.select(tables[table_key])
        if len(table) == 0:
            tables[table_key] = []
            continue

        table = table[0]
        table_data = []
        # headers = [header.text.strip() for header in table.find_all('th')]
        headers = []
        for header in table.find_all('th'):
            h = header.text.strip()
            if h == 'Tým a jméno':
                h = 'team'
            elif h == 'Okr.':
                h = 'district'
            elif h == 'Poř.':
                h = 'place'
            elif h == 'Výs.čas':
                h = 'final_time'
            elif h == 'Media':
                h = 'media'
            elif h == "1":
                h = "left_time"
            elif h == "2":
                h = "right_time"
            headers.append(h)

        rows = table.find_all('tr')
        for row in rows[1:]:
            cells = row.find_all('td')
            row_data = [cell.text.strip() for cell in cells]
            table_data.append(dict(zip(headers, row_data)))

        tables[table_key] = table_data

    return tables


@app.route('/')
def hello_world():
    return {
        'message': 'Hello world!',
        'time': datetime.datetime.utcnow(),
    }


@app.route('/results/<path:url>')
def results(url):
    data = get_data_from_url(url)
    if not data:
        return {}
    return data


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=os.environ['PORT']
    )
