import pandas as pd
import csv
from datetime import datetime
import os
import curses


def open_dataframes(path):  # Karolina
    if not os.path.exists(path):
        fieldnames = ['name_of_df', 'csv_path', 'total_records', 'time_added']
        with open('dataframes', mode='w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()


# the show_latest takes the three latest added datasources and calculates the metric for each
# the metric if for the latest year
def show_latest():  # Olesia
    reader = read_csv('dataframes')
    reader = sorted(reader, key=lambda row: row['time_added'], reverse=True)
    show_num = len(reader) if len(reader) < 3 else 3
    if show_num == 0:
        print('No data to show')
    else:
        for i in range(show_num):
            print(
                f'{i + 1}) Datasourсe: {reader[i]['name_of_df']} | {choose_latest_year(reader[i]['csv_path'])} GPM: '
                f'{calc_gpm(reader[i]['csv_path'], choose_latest_year(reader[i]['csv_path']))} %')


# the get_path returns a path as a string. It validates user input for path
# existence with os, it checks is the path is new and if it contains needed columns
def get_path():  # Karolina
    path = input('Enter the path of the csv file: \n>>').strip().strip('""')
    while not os.path.exists(path) or not path.lower().endswith('.csv'):
        path = input('Invalid path or file type not csv. Enter the path of the csv file: \n>>').strip().strip('""')
    dataframes = pd.read_csv('dataframes')
    csv_paths = list(dataframes['csv_path'])
    while os.path.normpath(path) in csv_paths:
        print('Path already in system')
        path = input('Enter the path of the csv file: \n>>').strip().strip('""')
        while not os.path.exists(path) or not path.lower().endswith('.csv'):
            path = input('Invalid path or file type not csv. Enter the path of the csv file: \n>>').strip().strip('""')
    df = pd.read_csv(path, index_col=False)
    df.columns = df.columns.str.strip()
    if 'revenue' not in df.columns:
        print('Not enough data in the csv. \'revenue\' needed')
    elif 'costOfRevenue' not in df.columns:
        print('Not enough data in the csv. \'costOfRevenue\' needed')
    elif 'date' not in df.columns:
        print('Not enough data in the csv. \'date\' needed')
    else:
        return os.path.normpath(path)


def read_csv(path):  # returns a DictReader of type list   # Liza
    path = os.path.normpath(path)
    df = pd.read_csv(path, index_col=False)
    df.columns = df.columns.str.strip()
    df.to_csv(path, index=False)
    with open(path, mode='r', newline='') as csvfile:
        reader = list(csv.DictReader(csvfile))
    return reader


# appends the data of the file to our internal datasource
def note_file(path_of_file):  # Karolina
    df = pd.read_csv(path_of_file, index_col=False)
    total_records = len(df)
    time_added = datetime.now().isoformat()

    with open('dataframes', mode='a', newline='') as file:
        fieldnames = ['name_of_df', 'csv_path', 'total_records', 'time_added']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writerow({
            'name_of_df': os.path.basename(path_of_file),
            'csv_path': path_of_file,
            'total_records': total_records,
            'time_added': time_added
        })


# the display_structure is for the 'adding a new ds' option
# it chows the total number of records and the general overview of columns
def display_structure(path):  # Liza
    path = os.path.normpath(path)
    df = pd.read_csv(path, index_col=False)
    records = len(df)
    print('records: ', records)
    if len(df.columns) > 5:
        print(' | '.join(df.columns[:3]) + ' ... ' + df.columns[-1])
    else:
        print(' | '.join(df.columns))


def choose_latest_year(path):  # -> Timestamp year # Liza
    df = pd.read_csv(path, index_col=False, parse_dates=['date'])
    df.sort_values(by='date', ascending=False, inplace=True)
    date = df['date'].iloc[0]
    return date.year


def calc_gpm(path, year: int):  # Liza
    path = os.path.normpath(path)
    df = pd.read_csv(path, index_col=False, parse_dates=['date'])
    df.columns = df.columns.str.strip()
    if year not in list(df.date.dt.year):
        print('No data for this year')
    else:
        df['grossProfitcalc'] = df['revenue'] - df['costOfRevenue']
        # validating the data
        df.loc[df['revenue'] < 10, 'revenue'] = None
        df.loc[df['costOfRevenue'] < 10, 'costOfRevenue'] = None
        if len(df[(df['revenue'].isna()) | (df['costOfRevenue'].isna())]) != 0:
            print('Invalid values found. Handling the file...')
            df.dropna(subset=['revenue'], inplace=True)
            df.dropna(subset=['costOfRevenue'], inplace=True)

        df['grossProfitMargin'] = (df['grossProfitcalc'] / df['revenue']) * 100
        return round(df[df['date'].dt.year == year]['grossProfitMargin'].iloc[0], 2)


# curses module for keyboard handling
def get_csv_curses(stdscr):  # Olesia
    df = pd.read_csv('dataframes')
    csvs = list(df['name_of_df'])
    current_index = 0
    num_files = len(csvs)

    stdscr.clear()

    while True:
        stdscr.addstr(0, 0, "Use arrow keys to select a data source. Press Enter to confirm. Press 'q' to quit.")
        stdscr.addstr(1, 0, f"Selected data source: {csvs[current_index]}")

        stdscr.refresh()

        key = stdscr.getch()

        if key == curses.KEY_LEFT:
            current_index = (current_index - 1) % num_files
        elif key == curses.KEY_RIGHT:
            current_index = (current_index + 1) % num_files
        elif key == ord('\n'):
            return csvs[current_index]
        elif key == ord('q'):
            return None


# main menu
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
            show_latest()
        elif user_input == '2':
            path = get_path()
            display_structure(path)
            note_file(path)

        elif user_input == '3':
            chosen_csv = curses.wrapper(get_csv_curses)
            if chosen_csv:
                print(f'Selected file: {chosen_csv}')
                df = pd.read_csv(chosen_csv, index_col= False, parse_dates = ['date'])
                print('Valid years: ', list(set(df['date'].dt.year)))
                year_picker = input('Choose the year for calculations: ')
                while not year_picker.isdigit():
                    year_picker = input('Invalid year. Choose the year for calculations: ')
                year_picker = int(year_picker)
                if year_picker in list(set(df['date'].dt.year)):
                    print(f'Calculated GPM:  {calc_gpm(chosen_csv, year_picker)} %')
                else:
                    print('Invalid year')
            else:
                print('No file selected.')

        elif user_input == '4':
            exit()
        else:
            print('Invalid input!')


if __name__ == '__main__':
    menu()
