import threading, time, random, urllib.request, re, csv, json, hashlib

result = []

def hashBrandWithCategory():
    with open('csvBrandWithCategory.csv', newline='', encoding='UTF-8') as csvfile:
        rows = csv.reader(csvfile)
        
        for row in rows:
            brandENTW = row[0].split('|')
            en = brandENTW[0]
            tw = brandENTW[1]

            hashBrand = ''
            if en is not '' or tw is not '':
                concateBrand = en + tw
                hashBrand = hashlib.md5(concateBrand.encode('UTF-8')).hexdigest()
        
            item = []
            item.append(hashBrand)
            item.append(en)
            item.append(tw)
            item += row[1:]
            result.append(item)

    # Write to File
    with open('csvBrandWithCategoryHash.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(result)

def hashProductWithBrand():
    with open('csvProductWithBrand.csv', newline='', encoding='UTF-8') as csvfile:
        rows = csv.reader(csvfile)
        
        for row in rows:
            brandEN = row[0]
            brandTW = row[1]
            name = row[2]

            if name == '':
                continue

            hashBrand = ''
            if brandEN is not '' or brandTW is not '':
                concateBrand = brandEN + brandTW
                hashBrand = hashlib.md5(concateBrand.encode('UTF-8')).hexdigest()
        
            item = []
            item.append(hashBrand)
            item.append(brandEN)
            item.append(brandTW)
            item.append(name)

            result.append(item)

    # Write to File
    with open('csvProductWithBrandHash.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(result)


hashBrandWithCategory()