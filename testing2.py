import os, json
import dateparser
import csv
import pandas as pd
import time
import datetime

#path_to_json = input("Enter the folder address containing json files: ")
#json_files = [pos_json for pos_json in os.listdir(path_to_json)]
path_to_json = '/media/rupinder/C49A5A1B9A5A0A76/Users/Rupinder/Desktop/BVR/Data/laptop/raw/'


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

def countingReviews():
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
    title_flag = []    
    for eachFile in loaded_full_files:
        if len(eachFile['title']) == 0:
            title_flag.append("Yellow")
        else:
            title_flag.append("Green")
    d = {"Name":loaded_files, "title_flag": title_flag}
    data_review_flag = pd.DataFrame(d)
    return data_review_flag

def countingFeatures():
    features_flag = []    
    for eachFile in loaded_full_files:
        if len(eachFile['features']) == 0:
            features_flag.append("Yellow")
        else:
            features_flag.append("Green")
    d = {"Name":loaded_files, "features_flag": features_flag}
    data_features_flag = pd.DataFrame(d)
    return data_features_flag

def countingRating():
    rating_flag = []    
    for eachFile in loaded_full_files:
        if len(eachFile['rating']) == 0:
            rating_flag.append("Yellow")
        else:
            rating_flag.append("Green")
    d = {"Name":loaded_files, "rating_flag": rating_flag}
    data_rating_flag = pd.DataFrame(d)
    return data_rating_flag

def countingTotalRatings():
    totalRatings_flag = []    
    for eachFile in loaded_full_files:
        if len(eachFile['totalRatings']) == 0:
            totalRatings_flag.append("Yellow")
        else:
            totalRatings_flag.append("Green")
    d = {"Name":loaded_files, "totalRatings_flag": totalRatings_flag}
    data_totalRatings_flag = pd.DataFrame(d)
    return data_totalRatings_flag

def floatRating():
    floatRating_flag = []
    for eachFile in loaded_full_files:
        try:
            float(eachFile['rating'])
            floatRating_flag.append("Green")
        except:
            floatRating_flag.append("Yellow")
    d = {"Name":loaded_files, "floatRating_flag": floatRating_flag}
    data_floatRating_flag = pd.DataFrame(d)
    return data_floatRating_flag

def countReviewText():
    countReviewText_flag = []
    for eachFile in loaded_full_files:
        count_GoodReviewText = 0
        for eachReviewDict in eachFile['reviews']:
            if len(eachReviewDict["reviewText"]) > 20:
                count_GoodReviewText += 1
            if count_GoodReviewText > 10:
                break
        if count_GoodReviewText >10:
            countReviewText_flag.append("Green")
        else:
            countReviewText_flag.append("Red")
        d = {"Name":loaded_files, "countReviewText_flag": countReviewText_flag}
    data_reviewText_flag = pd.DataFrame(d)
    return data_reviewText_flag

def countReviewTitle():
    countReviewTitle_flag = []
    for eachFile in loaded_full_files:
        count_GoodReviewTitle = 0
        for eachReviewDict in eachFile['reviews']:
            if len(eachReviewDict["reviewTitle"]) > 0:
                count_GoodReviewTitle += 1
            if count_GoodReviewTitle > 10:
                break
        if count_GoodReviewTitle >10:
            countReviewTitle_flag.append("Green")
        else:
            countReviewTitle_flag.append("Yellow")
        d = {"Name":loaded_files, "countReviewTitle_flag": countReviewTitle_flag}
    data_reviewTitle_flag = pd.DataFrame(d)
    return data_reviewTitle_flag

def countReviewerName():
    countReviewerName_flag = []
    for eachFile in loaded_full_files:
        count_GoodReviewerName = 0
        for eachReviewDict in eachFile['reviews']:
            if len(eachReviewDict["reviewTitle"]) > 0:
                count_GoodReviewerName += 1
            if count_GoodReviewerName > 10:
                break
        if count_GoodReviewerName >10:
            countReviewerName_flag.append("Green")
        else:
            countReviewerName_flag.append("Yellow")
        d = {"Name":loaded_files, "countReviewerName_flag": countReviewerName_flag}
    data_reviewerName_flag = pd.DataFrame(d)
    return data_reviewerName_flag


def countFormatRating():
    countFormatRating_flag = []
    for eachFile in loaded_full_files:
        count_GoodFormatRating = 0
        for eachReviewDict in eachFile['reviews']:
            if len(eachReviewDict["rating"]) > 0 and " out of 5 stars" in eachReviewDict["rating"]:
                try:
                    type(float(eachReviewDict["rating"][0:3]))
                    count_GoodFormatRating += 1
                except:
                    pass
            if count_GoodFormatRating > 10:
                break
        if count_GoodFormatRating >10:
            countFormatRating_flag.append("Green")
        else:
            countFormatRating_flag.append("Yellow")
        d = {"Name":loaded_files, "countFormatRating_flag": countFormatRating_flag}
    data_formatRating_flag = pd.DataFrame(d)
    return data_formatRating_flag

def countReviewDate():
    countReviewDate_flag = []
    today_date = datetime.datetime.now()
    for eachFile in loaded_full_files:
        count_GoodReviewDate = 0
        for eachReviewDict in eachFile['reviews']:
            if len(eachReviewDict["reviewDate"]) > 0:
                try:
                    review_date = dateparser.parse(eachReviewDict["reviewDate"], languages=['en']) #, date_formats=['%B %d %Y']
                    if today_date - review_date <183:
                        count_GoodReviewDate += 1
                except:
                    pass
            if count_GoodReviewDate > 10:
                break
        if count_GoodReviewDate >10:
            countReviewDate_flag.append("Green")
        else:
            countReviewDate_flag.append("Yellow")
        d = {"Name":loaded_files, "countReviewDate_flag": countReviewDate_flag}
    data_reviewDate_flag = pd.DataFrame(d)
    return data_reviewDate_flag

def writingFile():
    start_time = time.time()
    data_review_flag = countingReviews()
    data_title_flag = countingTitle()
    data_features_flag = countingFeatures()
    data_rating_flag = countingRating()
    data_totalRatings_flag = countingTotalRatings()
    data_floatRating_flag = floatRating()
    data_reviewText_flag = countReviewText()
    data_reviewTitle_flag = countReviewTitle()
    data_reviewerName_flag = countReviewerName()
    data_formatRating_flag = countFormatRating()
    data_reviewDate_flag = countReviewDate()
    file1 = pd.merge(data_loaded_flag, data_review_flag, on = "Name", how = "left")
    file2 = pd.merge(file1, data_title_flag, on = "Name", how = "left")
    file3 = pd.merge(file2, data_features_flag, on = "Name", how = "left")
    file4 = pd.merge(file3, data_rating_flag, on = "Name", how = "left")
    file5 = pd.merge(file4, data_totalRatings_flag, on = "Name", how = "left")
    file6 = pd.merge(file5, data_floatRating_flag, on = "Name", how = "left")
    file7 = pd.merge(file6, data_reviewText_flag, on = "Name", how = "left")
    file8 = pd.merge(file7, data_reviewTitle_flag, on= "Name", how = "left")
    file9 = pd.merge(file8, data_reviewerName_flag, on= "Name", how = "left")
    file10 = pd.merge(file9, data_formatRating_flag, on= "Name", how = "left")
    final_flag = pd.merge(file10, data_reviewDate_flag, on = "Name", how = "left")
    
    final_flag.to_csv("file_list.csv")
    return time.time() - start_time, final_flag


f = writingFile()[1].iloc[1]
print(f)

