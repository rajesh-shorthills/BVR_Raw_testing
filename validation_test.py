import os, json
import dateparser
import csv
import pandas as pd
import time
from cerberus import Validator

#path_to_json = input("Enter the folder address containing json files: ")
#json_files = [pos_json for pos_json in os.listdir(path_to_json)]
path_to_json = '/media/rupinder/C49A5A1B9A5A0A76/Users/Rupinder/Desktop/BVR/Data/laptop/raw/'

json_files = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('.json')]

v = Validator()

v.schema = {'features': {"type": "list"}, 
                'reviewsAspects': {"type": "list"},
                'productInformation': {"type": "list"},
                "productDescription": {"type": "string"},
                "reviews": {"type": "list"},
                "qAndA": {"type": "list"},
                "time": {"type": "list"},
                "productURL":{"type": "string"},
                "ASIN": {"type": "string"},
                "title": {"type": "string"},
                "manufacturer": {"type": "string"},
                "currentPrice": {"type": "string"},
                "rating": {"type": "string"},
                "totalRatings": {"type": "string"},
}

count = 0
start_time = time.time()
for eachFile in json_files:
    try:
        with open(os.path.join(path_to_json, eachFile)) as f:
                new_file = json.load(f)
                print(v.validate(new_file,v.schema))
    except ValueError:
        count += 1

print(count, time.time()-start_time)


