import pandas as pd
import csv
from datetime import datetime
import os
import curses


def open_dataframes(path):
    if not os.path.exists(path):
        fieldnames = ['name_of_df', 'csv_path', 'total_records', 'time_added']
        with open('dataframes', mode='w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()


def show_latest():
    reader = read_csv('dataframes')
    reader = sorted(reader, key=lambda row: row['time_added'], reverse=True)
    show_num = len(reader) if len(reader) < 3 else 3
    if show_num == 0:
        print('No data to show')
    else:
        for i in range(show_num):
            print(
                f'{i + 1}) Datasource: {reader[i]['name_of_df']} | {choose_latest_year(reader[i]['csv_path'])} GPM: {calc_gpm(reader[i]['csv_path'], choose_latest_year(reader[i]['csv_path']))} %')


def get_path():
    path = input('Enter the path of the csv file: \n>>').strip().strip('""')
    while not os.path.exists(path) or not path.lower().endswith('.csv'):
        path = input('Invalid path or file type not csv. Enter the path of the csv file: \n>>').strip().strip('""')
    dataframes = pd.read_csv('dataframes')
    csv_paths = list(dataframes['csv_path'])
    while path in csv_paths:
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
        return path


def read_csv(path):  # returns a DictReader of type list
    df = pd.read_csv(path, index_col=False)
    df.columns = df.columns.str.strip()
    df.to_csv(path, index=False)
    with open(path, mode='r', newline='') as csvfile:
        reader = list(csv.DictReader(csvfile))
    return reader


def note_file(path_of_file):
    df = pd.read_csv(path_of_file, index_col=False)
    total_records = len(df)
    time_added = datetime.now()

    with open('dataframes', mode='a', newline='') as file:
        fieldnames = ['name_of_df', 'csv_path', 'total_records', 'time_added']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writerow({
            'name_of_df': os.path.basename(path_of_file),
            'csv_path': path_of_file,
            'total_records': total_records,
            'time_added': time_added
        })


def display_structure(path):
    df = pd.read_csv(path, index_col=False)
    records = len(df)
    print('records: ', records)
    col_to_show = len(list(df.columns)) if len(list(df.columns)) <= 5 else 3
    l_col = list(df.columns)
    if col_to_show == 3:
        for ind in range(col_to_show):
            print(f'{l_col[ind]} | ', end='')
        print('... | ', end='')
        print(l_col[-1])
    else:
        for ind in range(col_to_show):
            print(f'{l_col[ind]} | ', end='')


def choose_latest_year(path):  # -> year
    df = pd.read_csv(path, index_col=False, parse_dates=['date'])
    df.sort_values(by='date', ascending=False, inplace=True)
    date = df['date'].iloc[0]
    return date.year


def calc_gpm(path, year: int):
    df = pd.read_csv(path, index_col=False, parse_dates=['date'])
    df.columns = df.columns.str.strip()
    df['grossProfitcalc'] = df['revenue'] - df['costOfRevenue']
    df.loc[df['revenue'] < 10, 'revenue'] = None
    df.loc[df['costOfRevenue'] < 10, 'costOfRevenue'] = None
    if len(df[(df['revenue'].isna()) | (df['costOfRevenue'].isna())]) != 0:
        print('Invalid values found. Handling the file...')
        df.dropna(subset=['revenue'], inplace=True)
        df.dropna(subset=['costOfRevenue'], inplace=True)

    df['grossProfitMargin'] = (df['grossProfitcalc'] / df['revenue']) * 100
    if year not in list(df.date.dt.year):
        print('No data')
    else:
        return round(df[df['date'].dt.year == year]['grossProfitMargin'].iloc[0], 2)


def get_csv_curses(stdscr):
    df = pd.read_csv('dataframes')
    csvs = list(df['name_of_df'])
    # Initial setup
    current_index = 0
    num_files = len(csvs)

    # Clear screen
    stdscr.clear()

    while True:
        # Display instructions
        stdscr.addstr(0, 0, "Use arrow keys to select a data source. Press Enter to confirm. Press 'q' to quit.")
        stdscr.addstr(1, 0, f"Selected data source: {csvs[current_index]}")

        # Refresh to display text
        stdscr.refresh()

        # Wait for user input
        key = stdscr.getch()

        if key == curses.KEY_LEFT:
            current_index = (current_index - 1) % num_files
        elif key == curses.KEY_RIGHT:
            current_index = (current_index + 1) % num_files
        elif key == ord('\n'):
            return csvs[current_index]
        elif key == ord('q'):
            return None


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
