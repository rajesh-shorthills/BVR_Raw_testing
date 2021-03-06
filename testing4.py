import os, json
import dateparser
import csv
import pandas as pd
import time
import datetime
from collections import defaultdict
import copy
from functools import reduce
#path_to_json = input("Enter the folder address containing json files: ")
#json_files = [pos_json for pos_json in os.listdir(path_to_json)]
path_to_json = '/media/rupinder/C49A5A1B9A5A0A76/Users/Rupinder/Desktop/BVR/Data/laptop1/raw/'

'''
Product - Reading file - Red
'''

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
deepCopy_loaded_full_files = copy.deepcopy(loaded_full_files)
deepCopy_green_loaded_full_files = copy.deepcopy(loaded_full_files)


'''
Reviews - Red
'''

def missingReviewText():
    missingReviewTextTotal_flag = {}
    for (eachFile, filename) in zip(loaded_full_files, loaded_files):
        missingReviewText_flag = []
        for eachReviewDict in eachFile['reviews']:
            if len(eachReviewDict["reviewText"]) == 0:
                missingReviewText_flag.append(eachReviewDict)
        if missingReviewText_flag != []:
            missingReviewTextTotal_flag[filename] = missingReviewText_flag
    return missingReviewTextTotal_flag, "Red"


def missingReviewDate():
    missingReviewDateTotal_flag = {}
    for (eachFile, filename) in zip(loaded_full_files, loaded_files):
        missingReviewDate_flag = []
        for eachReviewDict in eachFile['reviews']:
            if len(eachReviewDict["reviewDate"]) == 0:
                missingReviewDate_flag.append(eachReviewDict)
        if missingReviewDate_flag != []:
            missingReviewDateTotal_flag[filename] = missingReviewDate_flag
    return missingReviewDateTotal_flag, "Red"


'''
Reviews - Red later yellow
'''

def missingReviewTitle():
    missingReviewTitleTotal_flag = {}
    for (eachFile, filename) in zip(loaded_full_files, loaded_files):
        missingReviewTitle_flag = []
        for eachReviewDict in eachFile['reviews']:
            if len(eachReviewDict["reviewTitle"]) == 0:
                missingReviewTitle_flag.append(eachReviewDict)
        if missingReviewTitle_flag != []:
            missingReviewTitleTotal_flag[filename] = missingReviewTitle_flag
    return missingReviewTitleTotal_flag, "Red"

def missingReviewerName():
    missingReviewerNameTotal_flag = {}
    for (eachFile, filename) in zip(loaded_full_files, loaded_files):
        missingReviewerName_flag = []
        for eachReviewDict in eachFile['reviews']:
            if len(eachReviewDict["reviewerName"]) == 0:
                missingReviewerName_flag.append(eachReviewDict)
        if missingReviewerName_flag != []:
            missingReviewerNameTotal_flag[filename] = missingReviewerName_flag
    return missingReviewerNameTotal_flag, "Red"

def missingRating():
    missingRatingTotal_flag = {}
    for (eachFile, filename) in zip(loaded_full_files, loaded_files):
        missingRating_flag = []
        for eachReviewDict in eachFile['reviews']:
            if len(eachReviewDict["rating"]) == 0:
                missingRating_flag.append(eachReviewDict)
        if missingRating_flag != []:
            missingRatingTotal_flag[filename] = missingRating_flag
    return missingRatingTotal_flag, "Red"

'''
Reviews - Red
'''

def wrongReviewDate():
    wrongReviewDateTotal_flag = {}
    for (eachFile, filename) in zip(loaded_full_files, loaded_files):
        wrongReviewDate_flag = []
        for eachReviewDict in eachFile['reviews']:
            try:
                dateparser.parse(eachReviewDict["reviewDate"], languages=['en'])
            except:
                wrongReviewDate_flag.append(eachReviewDict)
        if wrongReviewDate_flag != []:
            wrongReviewDateTotal_flag[filename] = wrongReviewDate_flag
    return wrongReviewDateTotal_flag, "Red"


'''
Review - Yellow
'''

def wrongFormatRating():
    wrongFormatRatingTotal_flag = {}
    for (eachFile, filename) in zip(loaded_full_files, loaded_files):
        wrongFormatRating_flag = []
        for eachReviewDict in eachFile['reviews']:
            if " out of 5 stars" not in eachReviewDict["rating"] or " out of 5" not in eachReviewDict["rating"]:
                try:
                    type(float(eachReviewDict["rating"][0:3]))
                except:
                    wrongFormatRating_flag.append(eachReviewDict)
            else:
                try:
                    type(float(eachReviewDict["rating"][0:3]))
                except:
                    wrongFormatRating_flag.append(eachReviewDict)
        if wrongFormatRating_flag != []:
            wrongFormatRatingTotal_flag[filename] = wrongFormatRating_flag
    return wrongFormatRatingTotal_flag, "Yellow"

def lessReviewText():
    lessReviewTextTotal_flag = {}
    for (eachFile, filename) in zip(loaded_full_files, loaded_files):
        lessReviewText_flag = []
        for eachReviewDict in eachFile['reviews']:
            if len(eachReviewDict["reviewText"]) < 20 or len(eachReviewDict["reviewText"].split()) < 5:
                lessReviewText_flag.append(eachReviewDict)
        if lessReviewText_flag != []:
            lessReviewTextTotal_flag[filename] = lessReviewText_flag
    return lessReviewTextTotal_flag, "Yellow"


''' 
Product - Red
'''

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

'''
Product - Yellow
'''

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

'''
Product - Yellow
'''

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

'''
Product - Yellow
5. number of non-RED reviews less than a configurable threshold / YELLOW
'''



def combiningRedReviews():
    missing_ReviewText = missingReviewText()
    missing_ReviewDate = missingReviewDate()
    missing_ReviewTitle = missingReviewTitle()
    missing_ReviewerName = missingReviewerName()
    wrong_ReviewDate = wrongReviewDate()
    missing_Rating = missingRating()
    wrong_FormatRating = wrongFormatRating()
    less_ReviewText = lessReviewText()
    list_of_flags = []
    for eachList in (missing_ReviewText, missing_ReviewDate, missing_ReviewTitle, missing_ReviewerName, wrong_ReviewDate, missing_Rating, wrong_FormatRating, less_ReviewText):
        if eachList[1] == "Red":
            list_of_flags.append(eachList[0])
    list_of_flags = tuple(list_of_flags)
    redDict = defaultdict(list)
    for dict in list_of_flags:
        for key, value in dict.items():
            if value not in redDict[key]:
                redDict[key].append(value)
    return redDict

def combiningNonRedReviews():
    missing_ReviewText = missingReviewText()
    missing_ReviewDate = missingReviewDate()
    missing_ReviewTitle = missingReviewTitle()
    missing_ReviewerName = missingReviewerName()
    wrong_ReviewDate = wrongReviewDate()
    missing_Rating = missingRating()
    wrong_FormatRating = wrongFormatRating()
    less_ReviewText = lessReviewText()
    new_loaded_full_files = deepCopy_loaded_full_files
    list_of_flags = []
    nonRed_loaded_full_files = []
    for eachList in (missing_ReviewText, missing_ReviewDate, missing_ReviewTitle, missing_ReviewerName, wrong_ReviewDate, missing_Rating, wrong_FormatRating, less_ReviewText):
        if eachList[1] == "Red":
            list_of_flags.append(eachList[0])
    list_of_flags = tuple(list_of_flags)
    for (filename, eachFile) in zip(loaded_files, new_loaded_full_files):
        for eachMember in list_of_flags:
            if filename in eachMember:
                for eachReview in eachMember[filename]:
                    try:
                        eachFile['reviews'].remove(eachReview)
                    except:
                        pass
        nonRed_loaded_full_files.append(eachFile)
    return nonRed_loaded_full_files

def combiningGreenReviews():
    missing_ReviewText = missingReviewText()
    missing_ReviewDate = missingReviewDate()
    missing_ReviewTitle = missingReviewTitle()
    missing_ReviewerName = missingReviewerName()
    wrong_ReviewDate = wrongReviewDate()
    missing_Rating = missingRating()
    wrong_FormatRating = wrongFormatRating()
    less_ReviewText = lessReviewText()
    new_loaded_full_files = deepCopy_green_loaded_full_files
    list_of_flags = (missing_ReviewText, missing_ReviewDate, missing_ReviewTitle, missing_ReviewerName, wrong_ReviewDate, missing_Rating, wrong_FormatRating, less_ReviewText)
    green_loaded_full_files = []
    for (filename, eachFile) in zip(loaded_files, new_loaded_full_files):
        for eachMember in list_of_flags:
            if filename in eachMember:
                for eachReview in eachMember[filename]:
                    try:
                        eachFile['reviews'].remove(eachReview)
                    except:
                        pass
        green_loaded_full_files.append(eachFile)
    return green_loaded_full_files

def countingNonRedReviews():
    red_Reviews = combiningRedReviews()
    nonRedRating_flag = []
    for (filename, eachFile) in zip(loaded_files, loaded_full_files):
        count_totalReviews = len(eachFile['reviews'])
        count_redReviews = 0
        if filename in red_Reviews:
            count_redReviews = max(len(red_Reviews[filename]), len(red_Reviews[filename][0]))
        count_greenReviews = count_totalReviews - count_redReviews
        if count_greenReviews == 0:
            nonRedRating_flag.append("Red")
        elif count_greenReviews < 10:
            nonRedRating_flag.append("Yellow")
        else:
            nonRedRating_flag.append("Green")
    d = {"Name":loaded_files, "nonRedRating_flag": nonRedRating_flag}
    data_nonRedrating_flag = pd.DataFrame(d)
    return data_nonRedrating_flag

def countingNonRedReviews2(): # does the same thing but doesn't keep the Red Reviews
    nonRed_loaded_full_files = combiningNonRedReviews()
    nonRed_flag = []
    for eachFile in nonRed_loaded_full_files:
        if len(eachFile['reviews']) == 0:
            nonRed_flag.append("Red")
        elif len(eachFile['reviews']) < 10:
            nonRed_flag.append("Yellow")
        else:
            nonRed_flag.append("Green")
    d = {"Name":loaded_files, "nonRed_flag": nonRed_flag}
    data_nonRed_flag = pd.DataFrame(d)
    return data_nonRed_flag


def greenReviewDates():
    green_loaded_full_files = combiningGreenReviews()
    countReviewDate_flag = []
    today_date = datetime.datetime.now()
    for eachFile in green_loaded_full_files:
        count_GoodReviewDate = 0
        for eachReviewDict in eachFile['reviews']:
            if len(eachReviewDict["reviewDate"]) > 0:
                try:
                    review_date = dateparser.parse(eachReviewDict["reviewDate"], languages=['en']) #, date_formats=['%B %d %Y']
                    days_up = today_date - review_date 
                    if days_up.days < 183:
                        count_GoodReviewDate += 1
                except:
                    pass
            if count_GoodReviewDate > 10:
                break
        if count_GoodReviewDate > 10:
            countReviewDate_flag.append("Green")
        else:
            countReviewDate_flag.append("Yellow")
    d = {"Name":loaded_files, "countReviewDate_flag": countReviewDate_flag}
    data_ReviewDateGreen_flag = pd.DataFrame(d)
    return data_ReviewDateGreen_flag

def nonRedReviewDates():
    nonRed_loaded_full_files = combiningNonRedReviews()
    countReviewDate_flag = []
    today_date = datetime.datetime.now()
    for eachFile in nonRed_loaded_full_files:
        count_GoodReviewDate = 0
        for eachReviewDict in eachFile['reviews']:
            if len(eachReviewDict["reviewDate"]) > 0:
                try:
                    review_date = dateparser.parse(eachReviewDict["reviewDate"], languages=['en']) #, date_formats=['%B %d %Y']
                    days_up = today_date - review_date 
                    if days_up.days < 183:
                        count_GoodReviewDate += 1
                except:
                    pass
            if count_GoodReviewDate > 10:
                break
        if count_GoodReviewDate > 10:
            countReviewDate_flag.append("Green")
        else:
            countReviewDate_flag.append("Yellow")
    d = {"Name":loaded_files, "countReviewDate_flag": countReviewDate_flag}
    data_nonRedReviewDate_flag = pd.DataFrame(d)
    return data_nonRedReviewDate_flag


def findingDuplicates():
    duplicate_flag = []
    duplicate_dict = {}
    for (filename, eachFile) in zip(loaded_files, loaded_full_files):
        new_set = set()
        count_duplicate = 0
        new_list = []
        for eachDict in eachFile["reviews"]:
            t = tuple(eachDict.items())
            if t not in new_set:
                new_set.add(t)
            else:
                count_duplicate += 1
                new_list.append(eachDict)
        if count_duplicate > 0:
            duplicate_flag.append("Yellow")
            duplicate_dict[filename] = new_list
        else:
            duplicate_flag.append("Green")
    d = {"Name":loaded_files, "duplicate_flag": duplicate_flag}
    data_duplicate_flag = pd.DataFrame(d)
    return data_duplicate_flag

def productLabel(row):
    if row['loaded_flag'] == "Red" or row['review_flag'] == "Red" or	row['title_flag'] == "Red" or	row['features_flag'] == "Red" or	row['rating_flag'] == "Red" or	row['totalRatings_flag'] == "Red" or	row['floatRating_flag'] == "Red" or	row['nonRedRating_flag'] == "Red" or	row['countReviewDate_flag_x'] == "Red" or	row['countReviewDate_flag_y'] == "Red" or	row['duplicate_flag'] == "Red":
        return "Red"
    elif row['loaded_flag'] == "Yellow" or row['review_flag'] == "Yellow" or	row['title_flag'] == "Yellow" or	row['features_flag'] == "Yellow" or	row['rating_flag'] == "Yellow" or	row['totalRatings_flag'] == "Yellow" or	row['floatRating_flag'] == "Yellow" or	row['nonRedRating_flag'] == "Yellow" or	row['countReviewDate_flag_x'] == "Yellow" or	row['countReviewDate_flag_y'] == "Yellow" or	row['duplicate_flag'] == "Yellow":
        return "Yellow"
    return "Green"


def finalResult():
    start_time = time.time()
    data_review_flag =  countingReviews()
    data_title_flag =  countingTitle()
    data_features_flag =  countingFeatures()
    data_rating_flag  =  countingRating()
    data_totalRatings_flag  =  countingTotalRatings()
    data_floatRating_flag =   floatRating()
    data_nonRedrating_flag  =  countingNonRedReviews()
    data_ReviewDateGreen_flag  =  greenReviewDates()
    data_duplicate_flag  =  findingDuplicates()
    data_nonRedReviewDate_flag = nonRedReviewDates()
    dfs = [data_loaded_flag,
                data_review_flag, 
                data_title_flag, 
                data_features_flag, 
                data_rating_flag, 
                data_totalRatings_flag, 
                data_floatRating_flag, 
                data_nonRedrating_flag, 
                data_ReviewDateGreen_flag, 
                data_nonRedReviewDate_flag, 
                data_duplicate_flag]
    df_final = reduce(lambda left,right: pd.merge(left,right,on='Name'), dfs)
    df_final["productLabel"] = df_final.apply(lambda row: productLabel(row), axis = 1)
    count_RedProduct = df_final.loc[df_final.productLabel == "Red", "productLabel"].count()
    total_products = len(df_final.index)
    if total_products == count_RedProduct:
        category_label = "Red"
    elif total_products - count_RedProduct < 10:
        category_label = "Yellow"
    else:
        category_label = "Green"
    df_final.to_csv(category_label+".csv")
    return time.time() - start_time


f = finalResult()
print(f)