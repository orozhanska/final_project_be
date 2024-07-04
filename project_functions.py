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
    path = input('Enter the path of the csv file: \n>>').strip().strip('""')
    while not os.path.exists(path):
        path = input('Enter the path of the csv file: \n>>').strip().strip('""')
    df = pd.read_csv(path, index_col=False)
    if 'revenue' not in df.columns:
        print('Not enough data in the csv. \'revenue\' needed')
    elif 'costOfRevenue' not in df.columns:
        print('Not enough data in the csv. \'costOfRevenue\' needed')
    else:
        return path




def read_csv(path):  # returns a DictReader of type list
    df = pd.read_csv(path, index_col=False)
    df.columns=df.columns.str.strip()
    df.to_csv(path, index= False)
    with open(path, mode = 'r', newline='') as csvfile:
        reader = list(csv.DictReader(csvfile))
    return reader


def note_file(path_of_file, note_to_df):
    pass
    # after validating the path you should get the needed info from the file (records, metric)
#   and write this in the 'dataframes' file


def calc_gpm(path, year: int):
    df = pd.read_csv(path, index_col = False, parse_dates = ['date'])
    df.columns = df.columns.str.strip()
    df['grossProfitcalc'] = df['revenue'] - df['costOfRevenue']
    df.loc[df['revenue']<10, 'revenue'] = None
    df.loc[df['costOfRevenue'] < 10, 'costOfRevenue'] = None
    if len(df[df['revenue'].isna()|df['costOfRevenue'].isna()]) != 0:
        print('Invalid values found. Handling the file...')
        df.dropna(subset = ['revenue'], inplace = True)
        df.dropna(subset = ['costOfRevenue'], inplace = True)

    df['grossProfitMargin'] = (df['grossProfitcalc'] / df['revenue']) * 100
    if year not in list(df.date.dt.year):
        print('No data')
    else:
        return df.loc[df['date'].dt.year == year, 'grossProfitMargin']


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


# if __name__ == '__main__':
#     menu()


