import urllib.request as requests
import json
from pprint import pprint

def fetch_data(username):
    endpoint = f"https://api.github.com/users/{username}/events"
    response = requests.urlopen(endpoint)
    json_string = response.read().decode('utf-8')
    data = json.loads(json_string)
    return data


def save_to_json(filepath, data):
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=4)


if __name__ == "__main__":
   data = fetch_data("torvalds")
   filepath = r"C:\Users\Admin\Documents\Personal Projects\Github-User-Activity\data.json"
   save_to_json(filepath, data)
    