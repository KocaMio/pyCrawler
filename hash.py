import threading, time, random, urllib.request, re, csv, json, hashlib

result = []

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