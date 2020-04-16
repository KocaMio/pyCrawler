import threading, time, random, urllib.request, re, csv, json
from pyquery import PyQuery as pq
from urllib.parse import urlparse
from urllib.parse import urlencode

MainURL = "https://m.momoshop.com.tw"
AjaxToolURL = 'https://m.momoshop.com.tw/ajax/ajaxTool.jsp'

BrandWithoutName = 0

# ParseGoodsNameAndBrand
def parseGoodsNameAndBrand(title):
    if bool(title) == False:
        return

    result = re.findall(r"【(.*?)】|(\s*[^\n\r]*)", title)

    if len(result) == 0:
        return

    brand = result[0][0]
    product = result[0][1]

    return {
        "brand": brand,
        "product": product
    }

# getGoodsURL
def getGoodsURL(code):
    return MainURL + '/goods.momo?i_code=' + code

# Worker for Parse ProductName, BrandName, Categorys
ResultList = []
def workerParseProductDetail(code):
    url = getGoodsURL(code)

    detail = {
        "name": '',
        "brandTW": '',
        "brandEN": '',
        "categoryList": set()
    }

    #Get BrandName, GoodsCategory
    reqData = {
        "flag": "getGoodsRelCat",
        "data": {
            "goodsCode": code
        }
    }
    
    param = urllib.parse.urlencode({
        "data": json.dumps(reqData)
    })
    
    try:
        req = urllib.request.Request('https://m.momoshop.com.tw/ajax/ajaxTool.jsp?' + param)
        with urllib.request.urlopen(req) as res:
            rtnData = json.loads(res.read().decode("utf-8"))['rtnData']
    except Exception as e:
        print(e)

    reqStartTime = time.time()
    if "strPaths" in rtnData:
        htmlText = rtnData['strPaths'].replace("\\", "")
        brandNameTW = re.search('brandNameChi=\\"(.*?)\\"', htmlText, re.IGNORECASE)
        brandNameEN = re.search('brandNameEng=\\"(.*?)\\"', htmlText, re.IGNORECASE)

        if brandNameEN:
            detail["brandEN"] = brandNameEN.group(1)
        if brandNameTW:
            detail["brandTW"] = brandNameTW.group(1)

        matchList = re.findall(r'<a.*?>(.*?)<\/a>', htmlText, re.IGNORECASE)
        if matchList:
            for matchItem in matchList:
                detail["categoryList"].add(matchItem)

        ResultList.append(detail)

    reqEndTime = time.time()
    print('GoodsCode' + code + "  ReqEndTime: %d" % (reqEndTime - reqStartTime))

# Excute Start
startTime = time.time()

GoodsCodeList = []
with open('csvCodeList.csv', newline='') as csvfile:
  rows = csv.reader(csvfile)
  for row in rows:
    GoodsCodeList.append(row[0])

# Parse ProductName, BrandName, ProductCategory
ThreadList = [] 
for code in GoodsCodeList:
    t = threading.Thread(target=workerParseProductDetail, args=(code, ), daemon=True)
    ThreadList.append(t)

for t in ThreadList:
    # while threading.activeCount() >= 1000:
    #     pass
    
    t.start()

for t in ThreadList:
    t.join()

# Prepare Brand map to Category
brandCategoryList = {}
for row in ResultList:
    tw = row["brandTW"]
    en = row["brandEN"]
    categoryList = row["categoryList"]

    key = en + '|' + tw
    if tw == '' and en == '':
        BrandWithoutName += 1
        continue
    
    if key not in brandCategoryList:
        brandCategoryList[key] = set()
    
    for category in categoryList:
        brandCategoryList[key].add(category)

# Prepare CSV
csvRowList = []
for brandName in brandCategoryList:
    row = []
    row.append(brandName)

    for category in brandCategoryList[brandName]:
        row.append(category)
    
    csvRowList.append(row)

# Write to File
with open('csvBrandWithCategory.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(csvRowList)

# Excute End
endTime = time.time()

print("Total Excute Time: %f sec" % (endTime - startTime))
print("Brand without Name count: %d" %(BrandWithoutName))