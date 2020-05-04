import os, json
import dateparser
import csv
import pandas as pd


#path_to_json = input("Enter the folder address containing json files: ")
#json_files = [pos_json for pos_json in os.listdir(path_to_json)]
path_to_json = '/media/rupinder/C49A5A1B9A5A0A76/Users/Rupinder/Desktop/BVR/Data/laptop/raw/'

def readingJsonFiles(path_to_json):
    json_files = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('.json')]
    not_loaded_files = []
    loaded_files = []
    loaded_full_files = []
    loaded_flag = []
    for eachFile in json_files:
        try:
            with open(os.path.join(path_to_json, eachFile)) as f:
                new_file = json.load(f)
                loaded_full_files.append(new_file)
                loaded_files.append(eachFile)
                loaded_flag.append("Green")
        except ValueError:
            not_loaded_files.append(eachFile)
            loaded_flag.append("Red")
    d = {"Name": json_files, "loaded_flag":loaded_flag}
    data_loaded_flag = pd.DataFrame(d)
    return json_files, not_loaded_files, loaded_full_files, loaded_files, data_loaded_flag

def countingReviews():
    loaded_files = readingJsonFiles(path_to_json)[3]
    loaded_full_files = readingJsonFiles(path_to_json)[2]
    review_flag = []    
    for eachFile in loaded_full_files:
        if len(eachFile['reviews']) == 0:
            review_flag.append("Red")
        else:
            review_flag.append("Green")
    d = {"Name":loaded_files, "review_flag": review_flag}
    data_review_flag = pd.DataFrame(d)
    return data_review_flag

def countingTitle():
    loaded_files = readingJsonFiles(path_to_json)[3]
    loaded_full_files = readingJsonFiles(path_to_json)[2]
    title_flag = []    
    for eachFile in loaded_full_files:
        if len(eachFile['title']) == 0:
            title_flag.append("Yellow")
        else:
            title_flag.append("Green")
    d = {"Name":loaded_files, "title_flag": title_flag}
    data_review_flag = pd.DataFrame(d)
    return data_review_flag





def writingFile():
    data_loaded_flag =  readingJsonFiles(path_to_json)[4]
    data_review_flag = countingReviews()
    data_title_flag = countingTitle()
    file1 = pd.merge(data_loaded_flag, data_review_flag, on = "Name", how = "left")
    final_flag = pd.merge(file1, data_title_flag, on = "Name", how = "left")

    final_flag.to_csv("file_list.csv")
    return "File is printed"


f = writingFile()
print(f)
