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
        
            row = []
            row.append(hashBrand)
            row.append(en)
            row.append(tw)
            row.append(row[1:])

            result.append(row)

    # Write to File
    with open('csvBrandWithCategoryHash.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(result)

    print(result[0])
    print(result[10])
    print(result[20])

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
        
            row = []
            row.append(hashBrand)
            row.append(brandEN)
            row.append(brandTW)
            row.append(name)

            result.append(row)

    # Write to File
    with open('csvProductWithBrandHash.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(result)


hashBrandWithCategory()