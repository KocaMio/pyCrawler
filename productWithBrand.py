import threading, time, random
from pyquery import PyQuery as pq
from urllib.parse import urlparse
from urllib.parse import urlencode
import urllib.request
import re
import csv

MainURL = "https://m.momoshop.com.tw"
CategoryURLList = []
ResultList = []
ThreadList = []

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

# ProcessBrandAndProductName
def processBrandAndProductName(title):
    print(title)
    if bool(title) == False:
        return

    result = re.findall("【(.*?)】(\s*[^\n\r]*)", title)

    if len(result) == 0:
        return

    brand = result[0][0]
    product = result[0][1]

    ResultList.append([brand, product])

# Worker
def worker(url):
    # Skip Particular URL
    parsedURL = urlparse(url)
    if urllib.parse.parse_qs(parsedURL.query)['cn'][0] == '2400000000':
        return
    
    # Prepare Pages URL List for Loop Page
    page = 1
    
    while True:
        time.sleep(random.randrange(5))
        url = getNextPageURL(page, parsedURL)
        doc = pq(getHTML(url))
        
        if isHaveNextPage(doc) == False:
            break

        for element in doc('p.prdName'):
            processBrandAndProductName(element.text)

        page += 1
    
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
with open('outputThread.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(ResultList)