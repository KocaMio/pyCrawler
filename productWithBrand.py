import threading, time, random
from pyquery import PyQuery as pq
from urllib.parse import urlparse
from urllib.parse import urlencode
import urllib.request
import re
import csv

MainURL = "https://m.momoshop.com.tw"
CategoryURLList = []
GoodsCodeList = set()

ResultList = []
ThreadList = []

# Excute Start
startTime = time.time()

# Get HTML 
def getHTML(url):
    result = ''

    try:
        result = urllib.request.urlopen(url, timeout=5).read().decode('UTF-8')
    except Exception as e:
        print(url + ' :error: ' +str(e))
    
    return result

# Get Category URL List
def getCategoryURLList(doc):
    for element in doc('.sortBtnArea li a'):
        href = element.attrib['href']
        
        if href == '':
            continue

        CategoryURLList.append(href)
# parse category url list
def parseCategoryURLList():
    pass

# Get Page Page
def getPageURL(page, parsedURL):
    newQueryParams = dict(urllib.parse.parse_qsl(parsedURL.query))
    newQueryParams.update({'page':str(page)})
    newURL = list(parsedURL)

    newURL[4] = urllib.parse.urlencode(newQueryParams)

    return urllib.parse.urlunparse(newURL)

# Get Page URL List
def isPageAvaliable(htmlText):
    findall = re.findall(r'<dt id="rightBtn" class="rightBtn">', htmlText, re.IGNORECASE)
    return bool(findall)

# ProcessBrandAndProductName
def processBrandAndProductName(title):
    if bool(title) == False:
        return

    result = re.findall(r"【(.*?)】(\s*[^\n\r]*)", title)

    if len(result) == 0:
        return

    brand = result[0][0]
    product = result[0][1]

    ResultList.append([brand, product])

#parseBrandAndProductName
def parseBrandAndProductName(htmlText):
    if htmlText == '':
        return
    
    findallList = re.findall(r'<input type="hidden" name="goodsCode" id="goodsCode" value=\'([0-9]*)\'/>|<p class="prdName">(?:.*?【(.*?)】(.*?))<\/p>', htmlText)
    if findallList:
        for item in findallList:
            code = item[0]
            brand = item[1]
            product = item[2]
            if item != '':
                GoodsCodeList.add(code)
                pass
            if brand != '' or product != '':
                ResultList.append([brand, product])
                pass

# getGoodsCode
def processGoodsCode(element):
    code = pq(element).find('input[name="goodsCode"]')[0].value
    GoodsCodeList.add(code)

# Worker
def worker(CategoryURL):
    # parse query parameters
    parsedURL = urlparse(CategoryURL)
    parameters = urllib.parse.parse_qs(parsedURL.query)

    # Skip Particular Category URL
    if parameters['cn'][0] == '2400000000':
        return
    
    # Prepare Pages URL List for Loop Page
    page = 0
    
    while True:
        time.sleep(random.randrange(5))
        
        # Prepare
        url = getPageURL(page, parsedURL)
        
        htmlText = getHTML(url)
        if isPageAvaliable(htmlText) == False:
            break
        
        startTime = time.time()
        parseBrandAndProductName(htmlText)
        
        page += 1
    
        endTime = time.time()
        print(url + ' Finish Time: %d sec' % (endTime - startTime))
    return

# Prepare Category URL List
getCategoryURLList(pq(getHTML(MainURL + '/main.momo')))

# Parse Product Name in Every Sub Page
for path in CategoryURLList:
    url = MainURL + path

    t = threading.Thread(target=worker, args=(url, ), daemon=True)
    ThreadList.append(t)


for t in ThreadList:
    while threading.activeCount() >= 10:
        pass
    
    t.start()

for t in ThreadList:
    t.join()

# Write to File
with open('csvProductWithBrand.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(ResultList)

# Write code to file
codeRowList = []
for code in GoodsCodeList:
    row = []
    row.append(code)
    codeRowList.append(row)

with open('csvCodeList.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(codeRowList)

# Excute End
endTime = time.time()

print("Total Excute Time: %f sec" % (endTime - startTime))