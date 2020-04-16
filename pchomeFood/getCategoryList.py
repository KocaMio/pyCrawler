import requests
import json
import re
import csv

url = "https://ecapi.pchome.com.tw/cdn/ecshop/cateapi/v1.5/region&sign=h24%252Ffood&_callback=cb_ecshopCategoryRegion&5289728"

payload = {}
headers = {
  'Referer': 'https://24h.m.pchome.com.tw/region/DBAE',
  'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36'
}

response = requests.request("GET", url, headers=headers, data = payload)

rawData = response.text
regResult = re.findall(r"try{.*?\((.*?)\);}catch\(e\){if\(window\.console\){console\.log\(e\);}}", rawData)
jsonObject = json.loads(regResult[0])

# Write to csv
rowList = []
for item in jsonObject:
    row = []
    row.append(item["Id"])

    # trim whitespace
    name = re.sub(r'[\s+]', '', item["Name"].strip())
    row.append(name)
    rowList.append(row)

with open('category.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(rowList)



 