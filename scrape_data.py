import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pandas as pd
from bs4 import BeautifulSoup
import re

def get_tables_from_ncaa():
    url = 'https://www.ncaa.com/standings/football/fbs'
    teamList = ['Notre Dame', 'Missouri', 'Rutgers', 'Miami', 'Cornell', 'UNC']
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all tables
    tables = soup.find_all('table')
    # print(table)

    headers = [
        'School', 
        'Conference W', 
        'Conference L', 
        'Overall W', 
        'Overall L', 
        'PF', 
        'PA', 
        'HOME', 
        'AWAY', 
        'STREAK'
    ]
    rows = []
    for table in tables:
        # if 'standings' in table['class']:
        #     break
        for row in table.find_all('tr')[2:]:  # Skip the header rows
            cells = row.find_all('td')
            row_data = [cell.text.strip() for cell in cells]
            rows.append(row_data)

    # Create DataFrame
    df = pd.DataFrame(rows, columns=headers)
    filtered_df = df[df['School'].isin(teamList)]
    print(filtered_df)

def get_tables_from_espn():
    
    team_abbr = ['ND', 'MIZ', 'RUTG', 'MIA', 'COR', 'UNC']
    
    url = 'https://www.espn.com/college-football/schedule'
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Referer': 'https://www.google.com/'
    }
    
    session = requests.Session()
    response = session.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all date headers and tables
    date_headers = soup.find_all('div', class_='Table__Title')
    tables = soup.find_all('table', class_='Table')

    all_tables = []

    # Loop through each date header and corresponding table
    for date_header, table in zip(date_headers, tables):
        date = date_header.text.strip()
        
        headers = [header.text.strip() for header in table.find_all('th')]
        headers.append('Date')
        rows = table.find_all('tr')[1:]  # Skip the header row

        all_rows = []
        for row in rows:
            cells = row.find_all('td')
            row_data = [cell.text.strip() for cell in cells]
            row_data = [row_data[0] + ' ' + row_data[1], *row_data[2:]]
            row_data.append(date)  # Add the date to the row data
            all_rows.append(row_data)
            
        table = pd.DataFrame(all_rows, columns=headers)
        all_tables.append(table)

    # Concatenate all tables
    df = pd.concat(all_tables)

    # Reset the index
    df.reset_index(drop=True, inplace=True)
    # Filter rows based on team names list]
    df.fillna('', inplace=True)
    filtered_df = df[df['result'].str.contains(r'\b(?:{})\b'.format('|'.join(team_abbr)), regex=True)]
    # filtered_df = df[df['result'].str.contains('|'.join(team_abbr))]

    print(filtered_df)
    # Save DataFrame to CSV
    # df.to_csv('college_football_schedule.csv', index=False)

    # print(df)

if __name__ == '__main__':
    # get_tables_from_ncaa()
    get_tables_from_espn()
# with open('data.json', 'w') as f:
#     json.dump(data, f)
