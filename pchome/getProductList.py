import requests
import re
import json
import csv
import time
import threading

ItemList = {}
FailList = []

def getList(cateID, page, cateName):
    url = "https://ecshweb.pchome.com.tw/searchplus/v1/index.php/all/category/" + cateID + "/results?sort=sale/dc&show=list&page=" + str(page) + "&callback=json_search"

    payload = {}
    headers = {
    'Referer': 'https://24h.m.pchome.com.tw/region/' + cateID,
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36'
    }

    response = requests.request("GET", url, headers=headers, data = payload)

    rawData = response.text
    regResult = re.findall(r"try{.*?\((.*?)\);}catch\(e\){if\(window\.console\){console\.log\(e\);}}", rawData)
    
    try:
        regResult[0]
        json.loads(regResult[0])['prods']
    except Exception as e:
        print(e)
        print(rawData)
        
        FailList.append({
            'cateID': cateID,
            'page': page,
            'cateName': cateName
        })

        return json.loads('{"totalPage":0,"prods":[]}')

    return json.loads(regResult[0])

def prepareItemList(objs, cateName):
    for item in objs["prods"]:
        itemID = item["Id"]

        if itemID in ItemList:
            pass

        ItemList[itemID] = {
            'id': itemID,
            'cateId': item["cateId"],
            'name': item["name"],
            'cateName': cateName
        }
        
def workerGetList(cateID, cateName, totalPage):
    for pageNum in range(1, totalPage):
        print(cateID, cateName, pageNum)

        objs = getList(cateID, pageNum, cateName)
        prepareItemList(objs, cateName)

        time.sleep(3)

## Get Categories with totalPage from csv
Categories = {}
with open('categoryWithTotalPage.csv', newline='') as csvfile:
    rows = csv.reader(csvfile)
    for row in rows:
        cateID = row[0]
        cateName = row[1]
        totalPage = row[2]

        Categories[cateID] = {
            'id': cateID,
            'name': cateName,
            'totalPage': int(totalPage)
        }

# Multithread fetch products by categoryID
ThreadList = [] 
for cateID in Categories:
    cate = Categories[cateID]
    cateName = cate["name"]
    totalPage = cate["totalPage"]

    t = threading.Thread(target=workerGetList, args=(cateID, cateName, totalPage), daemon=True)
    ThreadList.append(t)

for t in ThreadList:
    while threading.activeCount() >= 2:
        pass
    
    t.start()

for t in ThreadList:
    t.join()


# Write to csv
itemList = []
for key in ItemList:
    item = ItemList[key]
    row = []
    row.append(item["id"])
    row.append(item["cateId"])
    row.append(item["cateName"])
    row.append(item["name"])
    itemList.append(row)
    
with open('itemList.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(itemList)


# FailItem write to csv
itemList = []
for failItem in FailList:
    row = []
    row.append(failItem["cateID"])
    row.append(failItem["page"])
    row.append(failItem["cateName"])
    itemList.append(row)

with open('failList.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(itemList)