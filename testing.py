import os, json
import dateparser
path_to_json = '/media/rupinder/C49A5A1B9A5A0A76/Users/Rupinder/Desktop/BVR/Data/laptop/raw/'
#path_to_json = input("Enter the folder address containing json files: ")
#json_files = [pos_json for pos_json in os.listdir(path_to_json)]
json_files = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('.json')]
loaded_files = []
count = 0                           #counting files not able to load
not_loaded_files = []
count_reviews = 0                   #counting the length of all reviews
no_review_files = []                #file names with missing reviews
count_title = 0             #counting the length of the title
no_title_files = []         #file names with missing title
count_features = 0             #counting the length of the features
no_features_files = []         #file names with missing features
count_rating = 0             #counting the length of the rating
no_rating_files = []         #file names with missing rating
count_totalRatings = 0             #counting the length of the totalRatings
no_totalRatings_files = []         #file names with missing totalRatings
no_rating_float_files = []          # file names with rating not float
no_reviewText_files = []            # file names with reviewText missing along with number of times missing
no_reviewDate_files = []            # file names with reviewDate missing along with number of times missing
no_reviewTitle_files = []           # file names with reviewTitle missing along with number of times missing
no_reviewerName_files = []          # file names with reviewerName missing along with number of times missing
no_reviewrating_files = []          # file names with no rating within a review missing along with number of times missing
wrong_reviewDate_files = []         # file names with wrong review dates within a review along with number of times wrong
wrong_rating_files = []             # file names with wrong rating langauge within a review  along with number of times wrong 
wrong_ratingFormat_files = []             # file names with wrong rating langauge within a review  along with number of times wrong 
less_reviewText_files = []
for eachFile in json_files:
    try:
        with open(os.path.join(path_to_json, eachFile))  as f:
            new_file = json.load(f)
    except ValueError as err:
        count += 1
        not_loaded_files.append(eachFile)
    else:        
        loaded_files.append(new_file)
        count_reviews = len(new_file['reviews'])
        count_title = len(new_file['title'])
        count_features = len(new_file['features'])
        count_rating = len(new_file['rating'])
        count_totalRatings = len(new_file['totalRatings'])
        count_no_reviewText = 0             # number of reviewText missing in a particular review
        count_no_reviewDate = 0             # number of reviewDate missing in a particular review
        count_no_reviewTitle = 0            # number of reviewTitle missing in a particular review
        count_no_reviewerName = 0           # number of reviewerName missing in a particular review
        count_no_rating = 0                 # number of rating missing in a particular review
        count_wrong_reviewDate = 0          # number of wrong review Dates in a particular review
        count_wrong_rating = 0              # number of wrong rating language in a particular review
        count_wrong_ratingFormat = 0        # number of wrong rating format in a particular review
        count_less_reviewText = 0           # number of reviewText less than 20 characters in a particular review
        if count_reviews == 0:
            no_review_files.append(eachFile)
        else:
            for eachReviewDict in new_file['reviews']:
                if len(eachReviewDict["reviewText"])==0:
                    count_no_reviewText += 1
                elif len(eachReviewDict["reviewText"]) < 20:
                    count_less_reviewText += 1
                if len(eachReviewDict["reviewDate"]) == 0:
                    count_no_reviewDate += 1
                # else:
                #     try:
                #         dateparser.parse(eachReviewDict["reviewDate"], languages=['en'], date_formats=['%B %d %Y'])
                #     except ValueError as err:
                #         count_wrong_reviewDate += 1
                if len(eachReviewDict["reviewTitle"]) == 0:
                    count_no_reviewTitle += 1
                if len(eachReviewDict["reviewerName"]) == 0:
                    count_no_reviewerName += 1
                if len(eachReviewDict["rating"]) == 0:
                    count_no_rating += 1
                elif " out of 5 stars" not in eachReviewDict["rating"]:
                    count_wrong_rating += 1
                else:
                    try:
                        type(float(eachReviewDict["rating"][0:3]))
                    except ValueError as err:
                        count_wrong_ratingFormat += 1
        if count_no_reviewText != 0:
            no_reviewText_files.append([eachFile,count_no_reviewText])
        if count_less_reviewText != 0:
            less_reviewText_files.append([eachFile, count_less_reviewText])
        if count_no_reviewDate != 0:
            no_reviewDate_files.append([eachFile,count_no_reviewDate])
        if count_no_reviewTitle != 0:
            no_reviewTitle_files.append([eachFile,count_no_reviewTitle])
        if count_no_reviewerName != 0:
            no_reviewerName_files.append([eachFile,count_no_reviewerName])
        if count_no_rating != 0:
            no_reviewrating_files.append([eachFile,count_no_rating])
        if count_wrong_reviewDate != 0:
            wrong_reviewDate_files.append([eachFile, count_wrong_reviewDate])
        if count_wrong_rating != 0:
            wrong_rating_files.append([eachFile,count_wrong_rating])
        if count_wrong_ratingFormat != 0:
            wrong_ratingFormat_files.append([eachFile,count_wrong_ratingFormat])
        if count_title == 0:
            no_title_files.append(eachFile)
        if count_features == 0:
            no_features_files.append(eachFile)
        if count_rating == 0:
            no_rating_files.append(eachFile)
        else:
            try:
                rating_float = float(new_file['rating'])
            except ValueError as err:
                no_rating_float_files.append(eachFile)
        if count_totalRatings == 0:
            no_totalRatings_files.append(eachFile)

print(less_reviewText_files)



# No Review - ['B07Y844Z1Z.raw.json', 'B07Z5L46BX.raw.json', 'B07ZT8WQWR.raw.json', 'B081LJ361L.raw.json', 'B0821J62YL.raw.json', 'B0822Z5Q1B.raw.json', 'B0822ZQ44V.raw.json', 'B0824NX7W5.raw.json', 'B083P58R57.raw.json', 'B083P6CPHY.raw.json', 'B083P74ST3.raw.json', 'B083QLBT6X.raw.json', 'B083QN5PJH.raw.json', 'B083QSYNR8.raw.json', 'B083VTBR3H.raw.json', 'B083W2BZPN.raw.json', 'B07WPNWJRV.raw.json']
# No title - []
# No Features - ['B01E9TXWYS.raw.json', 'B07QCG7J67.raw.json', 'B07X9QB4SG.raw.json']
# No Rating - ['B07ZT8WQWR.raw.json', 'B081LJ361L.raw.json', 'B0821J62YL.raw.json', 'B0822Z5Q1B.raw.json', 'B0822ZQ44V.raw.json', 'B0824NX7W5.raw.json', 'B083P58R57.raw.json', 'B083P6CPHY.raw.json', 'B083P74ST3.raw.json', 'B083QN5PJH.raw.json', 'B083QSYNR8.raw.json', 'B083VTBR3H.raw.json', 'B083W2BZPN.raw.json', 'B07WPNWJRV.raw.json']
# No TotalRatings - ['B07ZT8WQWR.raw.json', 'B081LJ361L.raw.json', 'B0821J62YL.raw.json', 'B0822Z5Q1B.raw.json', 'B0822ZQ44V.raw.json', 'B0824NX7W5.raw.json', 'B083P58R57.raw.json', 'B083P6CPHY.raw.json', 'B083P74ST3.raw.json', 'B083QN5PJH.raw.json', 'B083QSYNR8.raw.json', 'B083VTBR3H.raw.json', 'B083W2BZPN.raw.json', 'B07WPNWJRV.raw.json']
# Rating not float - []
# reviewText Missing - [['B01DBGVB7K.raw.json', 1], ['B01N5P6TJW.raw.json', 1], ['B072PSBZQB.raw.json', 2], ['B0778F81ZG.raw.json', 1]]