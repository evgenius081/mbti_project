import os
from pathlib import Path
import csv
import json

# base data path. You should place directories containing textes to be predicted.
dataset_path = str(Path.home())+ '/data/idrlabs/'

with open('gpt-query.csv', 'w', newline='') as csvfile:
    with open('gpt-query.json', 'w', newline='') as jsonfile:
        csvwriter = csv.writer(csvfile, delimiter=' ',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)

        for file_name in os.listdir(dataset_path):
            file_path = os.path.join(dataset_path, file_name)
            if os.path.isfile(file_path) and file_name.endswith('.csv'):
                type = file_name.split('.')[0].split('-')[1]
                counter = -1
                with open(file_path, newline='') as csvfile:
                    spamreader = csv.reader(csvfile, delimiter=',', quotechar='\"')
                    for row in spamreader:
                        counter += 1
                        if counter == 0:
                            continue

                        order = row[0]
                        url = row[1]
                        quote = row[2]
                        clean_quote = quote.replace('[', '').replace(']', '').replace('\"', '')
                        csvwriter.writerow([type, clean_quote])
                        jsonfile.write(json.dumps({'type': type, 'quote': clean_quote}) + '\n')
