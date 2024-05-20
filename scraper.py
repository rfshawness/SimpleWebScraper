from bs4 import BeautifulSoup
import time
import requests
from random import randint
from html.parser import HTMLParser
import threading
import json
from requests.exceptions import ChunkedEncodingError

USER_AGENT = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}

class SearchEngine:
    @staticmethod
    def search(query, sleep=True):
        if sleep: # Prevents loading too many pages too soon
            time.sleep(10)
        temp_url = '+'.join(query.split()) #for adding + between words for the query
        url = 'http://www.bing.com/search?q=' + temp_url

        max_retries = 3
        for attempt in range(max_retries):
            try:
                soup = BeautifulSoup(requests.get(url, headers=USER_AGENT).text, "html.parser")
                new_results = SearchEngine.scrape_search_result(soup)
                # print(new_results)
                return new_results
            
            except ChunkedEncodingError as e:
                print(f"ChunkedEncodingError: {e}. Retrying...")
                time.sleep(5)
            except Exception as e:
                print(f"An error occurred: {e}")
                break
    
        print(f"Request failed after {max_retries} attempts.")

    @staticmethod
    def scrape_search_result(soup):
        raw_results = soup.find_all("li", class_="b_algo")
        results = []
        #implement a check to get only 10 results and also check that URLs must not be duplicated 
        count = 0;
        for result in raw_results:
            link = result.find("a").get("href")
            if link in results:
                continue
            results.append(link)
            if len(results) >= 10:
                break

        return results
    


# Driver Code
try:
    with open("hyperlinkresults.json", "r") as json_file:
        existing_data = json.load(json_file)
except FileNotFoundError:
    existing_data = {}

data = {}
with open("100QueriesSet1.txt", "r") as file:
    current_query = file.readline()
    count = 1

    while current_query:
        value = SearchEngine.search(current_query.strip())
        data[current_query] = value
        print("Q" + str(count))
        count+=1
        current_query = file.readline()

existing_data.update(data)

with open("hyperlinkresults.json", "w") as json_file:
    json.dump(existing_data, json_file, indent=4)
# End Driver Code

