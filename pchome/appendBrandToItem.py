import csv
import re

# get itemList from csv
itemList = []
with open('itemListFinal.csv', newline='') as csvfile:
    rows = csv.reader(csvfile)
    for row in rows:
        prodID = row[0]
        cateID = row[1]
        cateName = row[2]
        prodName = row[3]

        itemList.append({
            'prodID': prodID,
            'cateID': cateID,
            'cateName': cateName,
            'prodName': prodName
        })

# get brand from csv
cateIDMapBrand = {}
with open('cateIDMapBrand.csv', newline='') as csvfile:
    rows = csv.reader(csvfile)
    for row in rows:
        cateID = row[0]
        brandName = row[1]
        cateIDMapBrand[cateID] = brandName

# append brand by cateID
for item in itemList:
    brand = ''
    
    try:
        brand = cateIDMapBrand[item["cateID"]]
    except Exception as identifier:
        print(identifier)

    item["brand"] = brand

# write to csv
outputList = []
a = []
a.append("ProdID")
a.append("Main Category")
a.append("Sub Category")
a.append("Product Name")
outputList.append(a)

for item in itemList:
    prodName = item["prodName"]
    brand = item["brand"]
    brand = re.sub(r'&#[0-9]*;|[\s*]|■|．|├|┤|◆|▌|★|－|└|★|=|●|∥|▼|▃|▅|》|《|【|】', '', brand)

    row = []
    row.append(item["prodID"])
    row.append(item["cateName"])
    row.append(brand)
    row.append(item["prodName"])
    outputList.append(row)

with open('result.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(outputList)
