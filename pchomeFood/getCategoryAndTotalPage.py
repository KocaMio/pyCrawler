import requests
import json
import re
import csv
import time

def getList(categoryID, page):
    url = "https://ecshweb.pchome.com.tw/searchplus/v1/index.php/all/category/" + categoryID + "/results?sort=sale/dc&show=list&page=" + str(page) + "&callback=json_search"

    payload = {}
    headers = {
    'Referer': 'https://24h.m.pchome.com.tw/region/' + categoryID,
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36'
    }

    response = requests.request("GET", url, headers=headers, data = payload)

    rawData = response.text
    regResult = re.findall(r"try{.*?\((.*?)\);}catch\(e\){if\(window\.console\){console\.log\(e\);}}", rawData)
    
    try:
        regResult[0]
    except Exception as e:
        print(e)
        print(rawData)

    return json.loads(regResult[0])


## Get Categories from csv
rowList = []
with open('category.csv', newline='') as csvfile:
    rows = csv.reader(csvfile)
    for row in rows:
        cateID = row[0]
        cateName = row[1]
        totalPage = getList(cateID, 1)["totalPage"]
        
        print(cateID, cateName, totalPage)

        anotherRow = []
        anotherRow.append(cateID)
        anotherRow.append(cateName)
        anotherRow.append(totalPage)
        rowList.append(anotherRow)
        time.sleep(3)
        

# Write to csv
with open('categoryWithTotalPage.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(rowList)