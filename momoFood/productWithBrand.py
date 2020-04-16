import threading, time, random, urllib.request, re, csv, json
from pyquery import PyQuery as pq
from urllib.parse import urlparse
from urllib.parse import urlencode

FailList = set()
# Get HTML 
def getHTML(url):
    result = ''

    try:
        result = urllib.request.urlopen(url, timeout=5).read().decode('UTF-8')
    except Exception as e:
        print(url + ' :error: ' +str(e))
        FailList.add(url)
    
    return result

# Worker for Parse ProductName, BrandName, Categorys
ResultList = []
def workerParseProductDetail(code):
    time.sleep(random.randrange(3))

    url = "https://m.momoshop.com.tw/goods.momo?i_code=" + code
    htmlText = getHTML(url)

    if htmlText == '':
        return

    detail = {
        "name": '',
        "brandTW": '',
        "brandEN": ''
    }

    executeStartTime = time.time()

    brandNameTW = re.search(r'brandnamechi=\"(.*?)\"', htmlText, re.IGNORECASE)
    brandNameEN = re.search(r'brandnameeng=\"(.*?)\"', htmlText, re.IGNORECASE)
    productName = re.search(r'<h2 id="goodsName">(.*?)<\/h2>', htmlText, re.IGNORECASE)

    if productName:
        detail["name"] = productName.group(1)
    if brandNameEN:
        detail["brandEN"] = brandNameEN.group(1)
    if brandNameTW:
        detail["brandTW"] = brandNameTW.group(1)

    ResultList.append(detail)

    executeEndTime = time.time()
    
    print('GoodsCode: ' + code + "  ExecuteEndTime: %d" % (executeEndTime - executeStartTime))

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
    while threading.activeCount() >= 15:
        pass
    
    t.start()

for t in ThreadList:
    t.join()

# Prepare CSV
csvRowList = []
for goods in ResultList:
    row = []
    row.append(goods['brandEN'])
    row.append(goods['brandTW'])
    row.append(goods['name'])
    csvRowList.append(row)

# Write to File
with open('csvProductWithBrand.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(csvRowList)

#Write fail to csv
rowList = []
for url in FailList:
    row = []
    row.append(url)
    rowList.append(row)

with open('csvProductWithBrandFail.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(rowList)

# Excute End
endTime = time.time()

print("Total Excute Time: %f sec" % (endTime - startTime))