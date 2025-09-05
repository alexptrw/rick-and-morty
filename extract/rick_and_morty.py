import requests
import pandas as pd
import time
from datetime import datetime

DELAY = 0.1
api_request_log = 'requests_log.txt'
exported_data = 'data.csv'
def request(base_url, page=1, session=None):
    if session is None:
        session = requests.Session()

    if page > 1:
        time.sleep(DELAY)

    url = f"{base_url}?page={page}"
    try:
        response = session.get(url)
        with open(api_request_log, 'a') as f:
            # msg = ''
            response_code = response.status_code
            if response_code == 200:
                msg = f"API request to page #{page} made successfully"
            else:
                msg = f"API request to page #{page} not successful"
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"{timestamp} - {msg} - status code: {response_code}\n")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_error:
         print(f"HTTP error occurred: {http_error}")
    except requests.exceptions.ConnectionError as conn_error:
        print(f"Connection error occured: {conn_error}")
    except requests.exceptions.Timeout as timeout_err:
        print(f"Timeout error occurred: {timeout_err}")
    except requests.exceptions.RequestException as generic_error:
        print(f"An error occureed: {generic_error}")

def get_pages(data):
    print("Pages obtained")
    return data['info']['pages']


def parse_json(data):
    charlist = []

    for item in data['results']:
        curr_char_episodes = []
        for i in item['episode']:
            string = i
            char = "/"
            curr_char_episodes.append(int(i.split("/")[-1]))
           

        char = {
            'id': item['id'],
            'name' : item['name'],
            'status': item['status'],
            'species': item['species'],
            'type': item['type'],
            'gender': item['gender'],
            'origin': item['origin']['name'],
            'location': item['location']['name'],
            'episodes_appeared_count': len(item['episode']),
            'episodes_appeared': curr_char_episodes
        }
        charlist.append(char)
        # print(f"Character {item['name']} added successfully")
    return charlist

def to_df(parsed_data):
    return pd.DataFrame(parsed_data)

base_url = "https://rickandmortyapi.com/api/character/"
all_chars = []

with requests.Session() as session:
    get_data = request(base_url, session=session)
    number_pages = get_pages(get_data)
    all_chars = []
    for i in range(1, number_pages + 1):
        get_data = request(base_url, i, session=session)
        all_chars.extend(parse_json(get_data))

df = to_df(all_chars)
df.to_csv(exported_data)
print(len(all_chars))