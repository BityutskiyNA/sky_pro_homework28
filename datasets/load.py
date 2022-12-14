import csv
import json


def convert(csv_file, json_file, model):
    result=[]
    with open(csv_file, encoding='utf-8') as csv_f:
        for row in csv.DictReader(csv_f):
            add = {'model': model, 'pk': int(row['Id'] if 'Id' in row else row['id'])}
            if 'id' in row:
                del row['id']
            else:
                del row['Id']

            if 'is_published' in row:
                if row['is_published'] == 'TRUE':
                    row['is_published'] = True
                else:
                    row['is_published'] = False
            if 'price' in row:
                row['price'] = int(row['price'])
            add['fields'] = row
            result.append(add)
    with open(json_file, 'w', encoding='utf-8') as jf:
        jf.write(json.dumps(result, ensure_ascii=False))


convert("ads.csv","ads.json",'ads.ad')
convert("categories.csv","categories.json",'ads.categori')
