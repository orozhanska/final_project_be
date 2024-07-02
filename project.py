import pandas as pd
import csv
from datetime import datetime
import os

# creating a table
fieldnames = ['name_of_df','csv_path', 'total_records', 'metric', 'time_added']
with open('dataframes', mode = 'w', newline = '') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()


# writing to the table after getting user input

with open('dataframes', mode = 'a', newline = '') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames = fieldnames)
    writer.writerow({'name_of_df': 'dudu', 'csv_path': 'bububub', 'total_records': 200, 'metric': 0, 'time_added': datetime.now()})

with open('dataframes', mode = 'a', newline = '') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames = fieldnames)
    writer.writerow({'name_of_df': 'balbla', 'csv_path': 'krara', 'total_records': 300, 'metric': 2, 'time_added': datetime.now()})

with open('dataframes', mode = 'a', newline = '') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames = fieldnames)
    writer.writerow({'name_of_df': 'bubu', 'csv_path': 'banhladesh', 'total_records': 3044, 'metric': 111, 'time_added': datetime.now()})

with open('dataframes', mode = 'a', newline = '') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames = fieldnames)
    writer.writerow({'name_of_df': 'krakra', 'csv_path': 'kuku', 'total_records': 102, 'metric': 3, 'time_added': datetime.now()})

with open('dataframes', mode = 'a', newline = '') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames = fieldnames)
    writer.writerow({'name_of_df': 'first', 'csv_path': 'must', 'total_records': 3, 'metric': 3, 'time_added': datetime.now()})

# showing the first three csv files

with open('dataframes', mode = 'r') as csvfile:
    reader = list(csv.DictReader(csvfile))
    reader = sorted(reader, key = lambda row: row['time_added'], reverse = True)
    show_num = len(reader) if len(reader) < 3 else 3
    if show_num == 1:
        print('No data to show')
    for i in range(show_num):
        print(f'{i+1}) Datasourse: {reader[i]['name_of_df']} | Metric: {reader[i]['metric']}')

# What you need to do:
def open_dataframes(path):
    pass
        # this is the code to be run just after user opens the program
        # it should check if our csv files with table's info exists and if it doesn't the function  should write the csv
        # you can use the first block of code '#create a table' here

def show_latest(path):
    pass
    # you can use the previous blocks of code here

def get_path():
    pass
    # get the path and validate it with the next finction
def validate_path(path):
    pass
    #validate the path the user is giving you

def read_csv(path):
    pass
    # this function should read the file into the dict reader object and return this object
def note_file(path_of_file, note_to_df):
    pass
    # after validating the path you should get the needed info from the file (records, metric)
#   and write this in the 'dataframes' file

def calc_gpm(path):
    pass
    # firstly read csv (with the function above) and try to calculate a gpm of it

def show_gpm():
    pass
    # it shows the gpm of the dataframe
    # it just receives this info from 'dataframes', this function does not calculate it
def menu():
    while True:
        user_input = input('''
        1. Check existing information
        2. Add a new data source (file)
        3. Calculate metric
        4. Exit
        Choose an Option:
        ''')

        if user_input == '1':
            continue
            #show_lates()
        elif user_input == '2':
            continue
            # get_path, validate_path, note_file
        elif user_input == '3':
            continue
            # show_gpm()
        elif user_input == '4':
            exit()
        else:
            print('Invalid input!')

if __name__ == '__main__':
    menu()

