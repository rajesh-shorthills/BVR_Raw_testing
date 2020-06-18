import os, json, shutil
import dateparser
import csv
import pandas as pd
import time
import datetime
from collections import defaultdict
import copy
from functools import reduce
import numpy as np

'''
Product - Reading file - Red
'''
category_slug_list = ['baby-wipes']


def missingReviewText(eachFile, filename):
    missingReviewText_flag = []
    for eachReviewDict in eachFile['reviews']:
        if len(eachReviewDict["reviewText"]) == 0:
            missingReviewText_flag.append(eachReviewDict)
    return missingReviewText_flag, "Red"

def missingReviewDate(eachFile, filename):    
    missingReviewDate_flag = []
    for eachReviewDict in eachFile['reviews']:
        if len(eachReviewDict["reviewDate"]) == 0:
            missingReviewDate_flag.append(eachReviewDict)
    return missingReviewDate_flag, "Red"

def missingReviewTitle(eachFile, filename):
    missingReviewTitle_flag = []
    for eachReviewDict in eachFile['reviews']:
        if len(eachReviewDict["reviewTitle"]) == 0:
            missingReviewTitle_flag.append(eachReviewDict)
    return missingReviewTitle_flag, "Red"

def missingReviewerName(eachFile, filename):
    missingReviewerName_flag = []
    for eachReviewDict in eachFile['reviews']:
        if len(eachReviewDict["reviewerName"]) == 0:
            missingReviewerName_flag.append(eachReviewDict)
    return missingReviewerName_flag, "Red"

def missingRating(eachFile, filename):
    missingRating_flag = []
    for eachReviewDict in eachFile['reviews']:
        if len(eachReviewDict["rating"]) == 0:
            missingRating_flag.append(eachReviewDict)
    return missingRating_flag, "Red"


def wrongReviewDate(eachFile, filename):
    wrongReviewDate_flag = []
    for eachReviewDict in eachFile['reviews']:
        try:
            dateparser.parse(eachReviewDict["reviewDate"], languages=['en'])
        except:
            wrongReviewDate_flag.append(eachReviewDict)
    return wrongReviewDate_flag, "Red"

def wrongFormatRating(eachFile, filename):
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
    return wrongFormatRating_flag, "Yellow"

def lessReviewText(eachFile, filename):
    lessReviewText_flag = []
    for eachReviewDict in eachFile['reviews']:
        if len(eachReviewDict["reviewText"]) < 20 or len(eachReviewDict["reviewText"].split()) < 5:
            lessReviewText_flag.append(eachReviewDict)
    return lessReviewText_flag, "Yellow"


def countingReviews(eachFile):   
    if len(eachFile['reviews']) == 0:
        result1 = "Red"
        result2 = {"review_flag": "Red", "reason": "There are no reviews in this product"}
    else:
        result1 = "Green"
        result2 = {"review_flag": "Green", "reason": ""}
    return result1, result2

def countingTitle(eachFile):
    if len(eachFile['title']) == 0:
        result1 = "Yellow"
        result2 = {"title_flag": "Yellow", "reason": "There is no title for this product"}
    else:
        result1 = "Green"
        result2 = {"title_flag": "Green", "reason": ""}
    return result1, result2

def countingFeatures(eachFile):
    if len(eachFile['features']) == 0:
        result1 = "Yellow"
        result2 = {"features_flag": "Yellow", "reason": "There are no features for this product available"}
    else:
        result1 = "Green"
        result2 = {"features_flag": "Green", "reason": ""}
    return result1, result2

def countingRating(eachFile):
    if len(eachFile['rating']) == 0:
        result1 = "Yellow"
        result2 = {"rating_flag": "Yellow", "reason": "There is no overall rating available for this product"}
    else:
        result1 = "Green"
        result2 = {"rating_flag": "Green", "reason": ""}
    return result1, result2

def countingTotalRatings(eachFile):
    if len(eachFile['totalRatings']) == 0:
        result1 = "Yellow"
        result2 = {"totalRating_flag": "Yellow", "reason": "There is no totalRating available for this product"}
    else:
        result1 = "Green"
        result2 = {"totalRating_flag": "Green", "reason": ""}
    return result1, result2

def floatRating(eachFile):
    try:
        float(eachFile['rating'])
        result1 = "Green"
        result2 = {"floatRating_flag": "Green", "reason": ""}
    except:
        result1 = "Yellow"
        result2 = {"floatRating_flag": "Yellow", "reason": "The rating of this product is not float/ or not available"}
    return result1, result2

def countingNonRedReviews(nonRedReviews):
    if len(nonRedReviews) == 0:
        result1 = "Red"
        result2 = {"nonRedRating_flag": "Red", "reason":"There are no non-red reviews for this product"}
    elif len(nonRedReviews) < 10:
        result1 = "Yellow"
        result2 = {"nonRedRating_flag": "Yellow", "reason":"There are less than 10 non-red reviews for this product"}
    else:
        result1 = "Green"
        result2 = {"nonRedRating_flag": "Green", "reason":""}
    return result1, result2

def countReviewDates(Reviews):
    today_date = datetime.datetime.now()
    count_GoodReviewDate = 0
    for eachReviewDict in Reviews:
        if len(eachReviewDict["reviewDate"]) > 0:
            try:
                review_date = dateparser.parse(eachReviewDict["reviewDate"], languages=['en'])
                days_up = today_date - review_date 
                if days_up.days < 183:
                    count_GoodReviewDate += 1
            except:
                pass
        if count_GoodReviewDate > 10:
            break
    if count_GoodReviewDate > 10:
        result1 = "Green"
        result2 = {"countReviewDate_flag" : "Green", "reason": ""}
    else:
        result1 = "Yellow"
        result2 = {"countReviewDate_flag" : "Yellow", "reason": "There are less than 10 green review dates which are from last 183 days"}
    return result1, result2

def findingDuplicates(eachFile):
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
        result1 = "Yellow"
        result2 = {"duplicate_flag":"Yellow", "reason": "there are duplicate reviews available in this product"}
        result3 = new_list
    else:
        result1 = "Green"
        result2 = {"duplicate_flag":"Green", "reason": ""}
        result3 = new_list
    return result1, result2, result3

def productLabel(row):
    if  row['loaded_flag'] == "Red" or row['review_flag'] == "Red" or	row['title_flag'] == "Red" or	row['features_flag'] == "Red" or	row['rating_flag'] == "Red" or	row['totalRatings_flag'] == "Red" or	row['floatRating_flag'] == "Red" or	row['nonRedRating_flag'] == "Red" or	row['nonRedReviewDate_flag'] == "Red" or	row['greenReviewDate_flag'] == "Red" or	row['duplicate_flag'] == "Red":
        return "Red"
    elif row['loaded_flag'] == "Yellow" or row['review_flag'] == "Yellow" or	row['title_flag'] == "Yellow" or	row['features_flag'] == "Yellow" or	row['rating_flag'] == "Yellow" or	row['totalRatings_flag'] == "Yellow" or	row['floatRating_flag'] == "Yellow" or	row['nonRedRating_flag'] == "Yellow" or	row['nonRedReviewDate_flag'] == "Yellow" or	row['greenReviewDate_flag'] == "Yellow" or	row['duplicate_flag'] == "Yellow":
        return "Yellow"
    return "Green"




def finalReport(path_to_json):
    start_time = time.time()

    json_files = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('.json')]
    not_loaded_files = []
    loaded_files = []   
    loaded_full_files = []
    loaded_flag = []
    missingReviewTextTotal_flag = {}
    missingReviewDateTotal_flag = {}
    missingReviewTitleTotal_flag = {}
    missingReviewerNameTotal_flag = {}
    missingRatingTotal_flag = {}
    wrongReviewDateTotal_flag = {}
    wrongFormatRatingTotal_flag = {}
    lessReviewTextTotal_flag = {}
    redReviews = {}
    nonRedReviews = {}
    yellowReviews = {}
    greenReviews = {}
    review_flag = []
    review_reason_flag = []    
    title_flag = []
    title_reason_flag = []    
    features_flag = []    
    features_reason_flag = []
    rating_flag = []
    rating_reason_flag = []
    totalRatings_flag = []
    totalRatings_reason_flag = []
    floatRating_flag = []
    floatRating_reason_flag = []
    nonRedRating_flag = []
    nonRedRating_reason_flag = []
    nonRedReviewDate_flag = []
    nonRedReviewDate_reason_flag = []
    greenReviewDate_flag = []
    greenReviewDate_reason_flag = []
    duplicate_flag = []
    duplicate_reason_flag = []
    duplicate_dict = {}


    for filename in json_files:
        try:
            with open(os.path.join(path_to_json, filename)) as f:
                eachFile = json.load(f)
                eachFile['reviews']
                updated_eachFile = copy.deepcopy(eachFile)
                try:
                    loaded_full_files.append(eachFile)
                    loaded_files.append(filename)
                    loaded_flag.append("Green")
                except:
                    not_loaded_files.append(filename)
                    loaded_flag.append("Red")
                finally:
                    missingReviewText_results = missingReviewText(eachFile,filename)
                    if missingReviewText_results[0] != []:
                        missingReviewTextTotal_flag[filename] = missingReviewText_results[0]

                    missingReviewDate_results = missingReviewDate(eachFile, filename)
                    if missingReviewDate_results[0] != []:
                        missingReviewDateTotal_flag[filename] = missingReviewDate_results[0]

                    missingReviewTitle_results = missingReviewTitle(eachFile, filename)
                    if missingReviewTitle_results[0] != []:
                        missingReviewTitleTotal_flag[filename] = missingReviewTitle_results[0]

                    missingReviewerName_results = missingReviewerName(eachFile, filename)
                    if missingReviewerName_results[0] != []:
                        missingReviewerNameTotal_flag[filename] = missingReviewerName_results[0]

                    missingRating_results = missingRating(eachFile, filename)
                    if missingRating_results[0] != []:
                        missingRatingTotal_flag[filename] = missingRating_results[0]

                    wrongReviewDate_results = wrongReviewDate(eachFile, filename)
                    if wrongReviewDate_results[0] != []:
                        wrongReviewDateTotal_flag[filename] = wrongReviewDate_results[0]

                    wrongFormatRating_results = wrongFormatRating(eachFile, filename)
                    if wrongFormatRating_results[0] != []:
                        wrongFormatRatingTotal_flag[filename] = wrongFormatRating_results[0]

                    lessReviewText_results =  lessReviewText(eachFile, filename)
                    if lessReviewText_results[0] != []:
                        lessReviewTextTotal_flag[filename] = lessReviewText_results[0]
                    
                    list_of_red_flags = (missingReviewTextTotal_flag, missingReviewDateTotal_flag,
                                            missingReviewTitleTotal_flag, missingReviewerNameTotal_flag,
                                            missingRatingTotal_flag, wrongReviewDateTotal_flag)
                    
                    list_of_yellow_flags = (wrongFormatRatingTotal_flag, lessReviewTextTotal_flag)
                    
                    redReviews[filename] = []

                    for eachMember in list_of_red_flags:
                        if filename in eachMember.keys():
                            redReviews[filename].append(eachMember[filename])
                            # redReviews[filename]|set(eachMember[filename])
                    
                    #redReviews[filename] = set(redReviews[filename])

                    for eachReview in redReviews[filename]:
                        try:
                            updated_eachFile['reviews'].remove(eachReview)
                        except:
                            pass
                    
                    nonRedReviews[filename] = updated_eachFile['reviews']

                    countingNonRedReviews_results = countingNonRedReviews(nonRedReviews[filename])
                    nonRedRating_flag.append(countingNonRedReviews_results[0])
                    nonRedRating_reason_flag.append(countingNonRedReviews_results[1])

                    nonRedReviewDates_results = countReviewDates(nonRedReviews[filename])
                    nonRedReviewDate_flag.append(nonRedReviewDates_results[0])
                    nonRedReviewDate_reason_flag.append(nonRedReviewDates_results[1])

                    yellowReviews[filename] = []

                    for eachMember in list_of_yellow_flags:
                        if filename in eachMember.keys():
                            yellowReviews[filename].append(eachMember[filename])
                            # yellowReviews[filename]|set(eachMember[filename])
                    
                    for eachReview in yellowReviews[filename]:
                        try:
                            updated_eachFile['reviews'].remove(eachReview)
                        except:
                            pass
                    
                    greenReviews[filename] = updated_eachFile['reviews']

                    greenReviewDates_results = countReviewDates(greenReviews[filename])
                    greenReviewDate_flag.append(greenReviewDates_results[0])
                    greenReviewDate_reason_flag.append(greenReviewDates_results[1])

                    countingReviews_results = countingReviews(eachFile)
                    review_flag.append(countingReviews_results[0])
                    review_reason_flag.append(countingReviews_results[1])
                    
                    countintTitle_results = countingTitle(eachFile)
                    title_flag.append(countintTitle_results[0])
                    title_reason_flag.append(countintTitle_results[1])
                    
                    countingFeatures_results = countingFeatures(eachFile)
                    features_flag.append(countingFeatures_results[0])
                    features_reason_flag.append(countingFeatures_results[1])
                    
                    countingRating_results = countingRating(eachFile)
                    rating_flag.append(countingRating_results[0])
                    rating_reason_flag.append(countingRating_results[1])

                    countingTotalRatings_results = countingTotalRatings(eachFile)
                    totalRatings_flag.append(countingTotalRatings_results[0])
                    totalRatings_reason_flag.append(countingTotalRatings_results[1])
                    
                    countingFloatRating_results = floatRating(eachFile)
                    floatRating_flag.append(countingFloatRating_results[0])
                    floatRating_reason_flag.append(countingFloatRating_results[1])

                    findingDuplicates_results = findingDuplicates(eachFile)
                    duplicate_flag.append(findingDuplicates_results[0])
                    duplicate_reason_flag.append(findingDuplicates_results[1])
                    duplicate_dict[filename] = findingDuplicates_results[2]   

        except:
            not_loaded_files.append(filename)
            loaded_flag.append("Red")
    
    d1 = {"Name": loaded_files, "nonRedRating_flag": nonRedRating_flag,
                "nonRedReviewDate_flag": nonRedReviewDate_flag, "greenReviewDate_flag": greenReviewDate_flag,
                "review_flag": review_flag, "title_flag": title_flag,
                "features_flag": features_flag, "rating_flag": rating_flag,
                "totalRatings_flag": totalRatings_flag, "floatRating_flag": floatRating_flag,
                "duplicate_flag": duplicate_flag}

    d2 = {"Name": loaded_files, "nonRedRating_reason_flag": nonRedRating_reason_flag,
                "nonRedReviewDate_reason_flag": nonRedReviewDate_reason_flag, "greenReviewDate_reason_flag": greenReviewDate_reason_flag,
                "review_reason_flag": review_reason_flag, "title_reason_flag": title_reason_flag,
                "features_reason_flag": features_reason_flag, "rating_reason_flag": rating_reason_flag,
                "totalRatings_reason_flag": totalRatings_reason_flag, "floatRating_reason_flag": floatRating_reason_flag,
                "duplicate_reason_flag": duplicate_reason_flag}
    
    d1_flags = pd.DataFrame(d1)
    d2_flags = pd.DataFrame(d2)

    if not_loaded_files != []:
        # json_files_new  = copy.deepcopy(ReadingFiles()[1])
        for not_loaded in not_loaded_files:
            # test = df_final
            d1_flags = d1_flags.append({"Name": not_loaded, "loaded_flag": "Red"}, ignore_index = True)
            d2_flags = d2_flags.append({"Name": not_loaded, "loaded_flag": {"loaded_flag": "Red", "reason":"Product is not being loaded"}}, ignore_index = True)
    else:
        d1_flags['loaded_flag'] = "Green"
        d2_flags['loaded_flag'] = "{'loaded_flag': 'Green', 'reason': ""}"
            # json_files_new.append(not_loaded)
    # else:
        # json_files_new  = copy.deepcopy(ReadingFiles()[1])
    
    # print(d1_flags)

    # d1_flags.to_csv("d1.csv")
    # d2_flags.to_csv("d12.csv")
    d1_flags["loaded_flag"].fillna("Green", inplace = True) 
    # d2_flags["loaded_flag"].fillna({"loaded_flag": "Green", "reason":""}, inplace = True)
    # new_dict = {"loaded_flag": "Green", "reason": ""}
    
    d2_flags["loaded_flag"].fillna('{"loaded_flag": "Green", "reason": ""}', inplace = True) 

    
    d1_flags["productLabel"] = d1_flags.apply(lambda row: productLabel(row), axis = 1)

    

    productLabel_list = d1_flags["productLabel"].tolist()
    productLabel_reason = []
    for eachElement in productLabel_list:
        if eachElement == "Green":
            productLabel_reason.append({"productLabel": "Green", "reason": ""})
        elif eachElement == "Yellow":
            productLabel_reason.append({"productLabel": "Yellow", "reason": "At least one of the flag is yellow and there is no Red"})
        else:
            productLabel_reason.append({"productLabel": "Red", "reason": "At least one of the flag is Red"})

    
    d2_flags["productLabel_reason"] = productLabel_reason

    count_RedProduct = d1_flags.loc[d1_flags.productLabel == "Red", "productLabel"].count()
    total_products = len(d1_flags.index)
    if total_products == count_RedProduct:
        category_label = "Red"
    elif total_products - count_RedProduct < 10:
        category_label = "Yellow"
    else:
        category_label = "Green"

    final_report1 = d2_flags.set_index('Name').T.to_dict('list')



    
    final_report = {
        'category_slug': category_slug_list[0],
        'status': category_label,
        "products": final_report1
    }

    d1_flags.to_csv("d1.csv")
    d2_flags.to_csv("d12.csv")


    current_path = os.getcwd()
    
    saving_path = os.path.join(current_path, category_slug_list[0])

    if os.path.exists(saving_path):
        shutil.rmtree(saving_path)
    os.makedirs(saving_path)


    with open(os.path.join(saving_path, category_slug_list[0] + '.json'), 'w') as outfile:
        json.dump(final_report, outfile)

    return time.time() - start_time

print(finalReport('/media/rupinder/C49A5A1B9A5A0A76/Users/Rupinder/Desktop/BVR/baby-wipes-in/raw'))