import requests
import pandas as pd
import json


def request(base_url, page=1):
    page_number = f'?page={page}'
    try:
        r = requests.get(base_url + page_number)
        print(f"API request to page #{page} made successfully")
        return r.json()
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
            curr_char_episodes.append(int(string[string.rfind(char) +1 :]))
           

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
get_data = request(base_url)
number_pages = get_pages(get_data)
all_chars = []
for i in range(1, number_pages + 1):
    get_data = request(base_url, i)
    all_chars.extend(parse_json(get_data))
df = to_df(all_chars)
print(len(all_chars))