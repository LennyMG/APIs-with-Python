import requests 
import json

#make API call
url = "https://hacker-news.firebaseio.com/v0/item/19155826.json"
r = requests.get(url)
print(f'Status code:{r.status_code}')

# explore structure of data
response_dict = r.json()
readable_file = "/Users/bluegeezer/workspace/API_test/readable_hn_data.json"
with open(readable_file, 'w') as f:
    json.dump(response_dict, f, indent=4)

