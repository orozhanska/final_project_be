import pandas as pd
import csv
from datetime import datetime
import os


def open_dataframes(path):
    if not os.path.exists(path):
        fieldnames = ['name_of_df', 'csv_path', 'total_records', 'metric', 'time_added']
        with open('dataframes', mode='w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()


def show_latest(path):
    reader = read_csv('dataframes')
    reader = sorted(reader, key=lambda row: row['time_added'], reverse=True)
    show_num = len(reader) if len(reader) < 3 else 3
    if show_num == 0:
        print('No data to show')
    else:
        for i in range(show_num):
            print(f'{i + 1}) Datasourse: {reader[i]['name_of_df']} | Metric: {reader[i]['metric']}')


def get_path():
    pass
    # get the path and validate it with the next finction


def validate_path(path):
    pass
    # validate the path the user is giving you 1) if it exists 2) if it contains columns wu need for calculations


def read_csv(path):  # returns a DictReader of type list
    with open(path, mode = 'r', newline='') as csvfile:
        reader = list(csv.DictReader(csvfile))
    return reader


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
    open_dataframes('dataframes')
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
            # show_lates()
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
