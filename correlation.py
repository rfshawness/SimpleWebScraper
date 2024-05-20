import csv
import json


#open both json files
google_data = {}
bing_data = {}

with open("Google_Result1.json", "r") as json_file:
    google_data = json.load(json_file)
with open("hyperlinkresults.json", "r") as json_file:
    bing_data= json.load(json_file)


count = 1 # to help print out query number in csv
overlap_avg = 0 # running total of the overlap
percent_avg = 0 # running total of the percent
spcoeff_avg = 0 # running total of the spear coef
data = [
    ["Queries", "Number of Overlapping Results", "Percent Overlap", "Spearman Coefficent"]
]

# loop through json
for query in bing_data:
    queryG = query.strip()
    urls1 = bing_data[query]
    urls2 = google_data.get(queryG, [])

    # Create dictionaries to store the indices of URLs in each array
    index_dict1 = {url: index for index, url in enumerate(urls1)}
    index_dict2 = {url: index for index, url in enumerate(urls2)}

    shared_urls = set(urls1).intersection(urls2)

    squared_differences = [(index_dict2[url] - index_dict1[url]) ** 2 for url in shared_urls]

    # Calculate Y as total num of matched results
    Y = len(shared_urls)

    # Calculate D as sqaured differences in indices
    D = squared_differences

    # Calculate W as sum of all squared differences
    W = sum(D)

   
    if Y == 0:  # if no results match
        result = 0
    elif Y == 1: # if 1 results match
        if W == 0:
            result = 1 # if same index
        else:
            result = 0 # if different index
    else:
        result = 1 - ((6 * W) / (Y * (Y ** 2 - 1))) # Calculate the final result using the formula

    percent = Y/10
    new_row = ["Query " + str(count), str(Y), str(percent), str(round(result, 2))]
    percent_avg+=percent
    spcoeff_avg+=result
    overlap_avg+=Y
    count+=1

    data.append(new_row)



last_row = ["Averages", str(round(overlap_avg/100, 2)), str(round(percent_avg/100, 2)), str(round(spcoeff_avg/100, 2))]
data.append(last_row)



# write to csv
with open("hyperlinkresults.csv", "w", newline="") as csv_file:
    writer = csv.writer(csv_file)
    
    for row in data:
        writer.writerow(row)