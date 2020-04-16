import csv
import requests
import re
import json
import time

FailList = []
def getBrandName(cateID):
    url = "https://ecapi.pchome.com.tw/cdn/ecshop/cateapi/v1.5/store&id=" + cateID + "&_callback=json_storestyle&5289729"
    response = requests.request("GET", url, headers={}, data = {})
    rawData = response.text
    regResult = re.findall(r"try{.*?\((.*?)\);}catch\(e\){if\(window\.console\){console\.log\(e\);}}", rawData)
    
    try:
        regResult[0]
        json.loads(regResult[0])[0]['Name']
    except Exception as e:
        print(e)
        print(rawData)
        
        FailList.append([cateID])

        return ''

    return json.loads(regResult[0])[0]["Name"]

# get category ids from csv
cateIDSetList = set()
with open('itemListFinal.csv', newline='') as csvfile:
    rows = csv.reader(csvfile)
    for row in rows:
        prodID = row[0]
        cateID = row[1]
        cateName = row[2]
        prodName = row[3]

        cateIDSetList.add(cateID)

# get brandName by cateID
cateIDMapBrandName = {}
for cateID in cateIDSetList:
    brandName = getBrandName(cateID)
    print(cateID, brandName)

    if brandName == '':
        pass

    cateIDMapBrandName[cateID] = brandName

    time.sleep(1)


# write to csv
itemList = []
for cateID in cateIDMapBrandName:
    brandName = cateIDMapBrandName[cateID]
    row = []
    row.append(cateID)
    row.append(brandName)
    itemList.append(row)
    
with open('cateIDMapBrand.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(itemList)

# FailItem write to csv
with open('cateIDMapBrandFail.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(FailList)