import threading, time, random, urllib.request, re, csv, json
from pyquery import PyQuery as pq
from urllib.parse import urlparse
from urllib.parse import urlencode

MainURL = "https://m.momoshop.com.tw"
AjaxToolURL = 'https://m.momoshop.com.tw/ajax/ajaxTool.jsp'
CategoryURLList = []
GoodsInfoList = []

ResultList = []
ThreadList = []

GoodsCodeList = []

# Get HTML
def getHTML(url):
    try:
        result = urllib.request.urlopen(url, timeout=5).read().decode('UTF-8')
    except Exception as e:
        print(str(e))
    
    return result

# Get Category URL List
def getCategoryURLList(doc):
    for element in doc('.sortBtnArea li a'):
        href = element.attrib['href']
        
        if href == '':
            continue

        CategoryURLList.append(href)

# Get Next Page
def getNextPageURL(page, parsedURL):
    newQuery = dict(urllib.parse.parse_qsl(parsedURL.query))
    newQuery.update({'page':str(page)})

    newURL = list(parsedURL)
    newURL[4] = urllib.parse.urlencode(newQuery)

    return urllib.parse.urlunparse(newURL)

# Get Page URL List
def isHaveNextPage(doc):
    return bool(doc('a[name=nextPage][page=nextPage]'))

# ParseGoodsNameAndBrand
def parseGoodsNameAndBrand(title):
    if bool(title) == False:
        return

    result = re.findall("【(.*?)】(\s*[^\n\r]*)", title)

    if len(result) == 0:
        return

    brand = result[0][0]
    product = result[0][1]

    return {
        "brandNameTw": brand,
        "brandNameEn": brand,
        "productName": product
    }

# ParseGoodsURL
def parseGoodsURL(goodsCode):
    if bool(goodsCode) == False:
        return

    path = MainURL + '/goods.momo?i_code=' + goodsCode

    return path

# getyGoodsURL
def getyGoodsURL(element):
    goodsURL = parseGoodsURL(pq(element).find('input[name="goodsCode"]')[0].value)

    return goodsURL

# Worker for Getting Product Urls
def workerParseGoodsURL(url):
    # Skip Particular URL
    parsedURL = urlparse(url)
    if urllib.parse.parse_qs(parsedURL.query)['cn'][0] == '2400000000':
        return
    
    # Prepare Pages URL List for Loop Each Page
    page = 1
    
    while True:
        time.sleep(random.randrange(5))
        url = getNextPageURL(page, parsedURL)
        doc = pq(getHTML(url))
        
        if isHaveNextPage(doc) == False:
            break

        for element in doc('article.prdListArea li'):
            url = getyGoodsURL(element)

            GoodsInfoList.append({
                "url": url
            })

        page += 1
        break #Testing
    
    return


# Prepare Category URL List
getCategoryURLList(pq(getHTML(MainURL + '/main.momo')))

# Parse Categories
for path in CategoryURLList:
    url = MainURL + path

    t = threading.Thread(target=workerParseGoodsURL, args=(url, ), daemon=True)
    ThreadList.append(t)


# for t in ThreadList:
#     while threading.activeCount() >= 10:
#         pass
    
#     t.start()

# for t in ThreadList:
#     t.join()

ThreadList[1].start()
ThreadList[1].join()

# Worker for Parse ProductName, BrandName, Categorys
def workerParseProductDetail(url):
    # time.sleep(random.randrange(5))

    detail = {
        "name": '',
        "brandTW": '',
        "brandEN": '',
        "categoryList": set()
    }

    #Get GoodsName
    doc = pq(getHTML(url))
    detail["name"] = doc('#goodsName')[0].text

    #Get BrandName, GoodsCategory
    reqData = {
        "flag": "getGoodsRelCat",
        "data": {
            "goodsCode": "6305793"
        }
    }
    
    param = urllib.parse.urlencode({
        "data": json.dumps(reqData)
    })

    req = urllib.request.Request('https://m.momoshop.com.tw/ajax/ajaxTool.jsp?' + param)
    with urllib.request.urlopen(req) as res:
        rtnData = json.loads(res.read().decode("utf-8"))['rtnData']

    if "strPaths" in rtnData:
        doc = pq(rtnData['strPaths'])
        detail["brandTW"] = doc('a.brandNameTxt').attr('brandnamechi')
        detail["brandEN"] = doc('a.brandNameTxt').attr('brandnameeng')

        categoryList = set()
        def each(index, element):
            categoryList.add(element.text)
        doc('dl dl dd a').each(each)

        print(categoryList)


# Parse ProductName, BrandName, ProductCategory
ThreadList = [] 
for good in GoodsInfoList:
    t = threading.Thread(target=workerParseProductDetail, args=(good["url"], ), daemon=True)
    ThreadList.append(t)

ThreadList[1].start()
ThreadList[1].join()

# Write to File
with open('outputThread.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(ResultList)