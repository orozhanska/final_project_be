import pandas as pd
import csv
from datetime import datetime
import os

# creating a table
fieldnames = ['name_of_df', 'csv_path', 'total_records', 'metric', 'time_added']
with open('dataframes', mode='w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

# writing to the table after getting user input

with open('dataframes', mode='a', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writerow(
        {'name_of_df': 'dudu', 'csv_path': 'bububub', 'total_records': 200, 'metric': 0, 'time_added': datetime.now()})

with open('dataframes', mode='a', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writerow(
        {'name_of_df': 'balbla', 'csv_path': 'krara', 'total_records': 300, 'metric': 2, 'time_added': datetime.now()})

with open('dataframes', mode='a', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writerow({'name_of_df': 'bubu', 'csv_path': 'banhladesh', 'total_records': 3044, 'metric': 111,
                     'time_added': datetime.now()})

with open('dataframes', mode='a', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writerow(
        {'name_of_df': 'krakra', 'csv_path': 'kuku', 'total_records': 102, 'metric': 3, 'time_added': datetime.now()})

with open('dataframes', mode='a', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writerow(
        {'name_of_df': 'first', 'csv_path': 'must', 'total_records': 3, 'metric': 3, 'time_added': datetime.now()})

# showing the first three csv files

with open('dataframes', mode='r') as csvfile:
    reader = list(csv.DictReader(csvfile))
    reader = sorted(reader, key=lambda row: row['time_added'], reverse=True)
    show_num = len(reader) if len(reader) < 3 else 3
    if show_num == 1:
        print('No data to show')
    for i in range(show_num):
        print(f'{i + 1}) Datasourse: {reader[i]['name_of_df']} | Metric: {reader[i]['metric']}')
