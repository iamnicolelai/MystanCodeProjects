"""
File: webcrawler.py
Name: Nicole Lai
--------------------------
This file collects more data from
https://www.ssa.gov/oact/babynames/decades/names2010s.html
https://www.ssa.gov/oact/babynames/decades/names2000s.html
https://www.ssa.gov/oact/babynames/decades/names1990s.html
Please print the number of top200 male and female on Console
You should see:
---------------------------
2010s
Male Number: 10900879
Female Number: 7946050
---------------------------
2000s
Male Number: 12977993
Female Number: 9209211
---------------------------
1990s
Male Number: 14146310
Female Number: 10644506
"""

import requests
from bs4 import BeautifulSoup


def main():
    for year in ['2010s', '2000s', '1990s']:
        print('---------------------------')
        print(year)
        url = 'https://www.ssa.gov/oact/babynames/decades/names'+year+'.html'
        
        response = requests.get(url)
        html = response.text
        soup = BeautifulSoup(html, features='html.parser')
        tables = soup.find_all('table', {'class': 't-stripe'})
        # ----- Write your code below this line ----- #
        male_total = 0
        female_total = 0
        # starting from tables, scrape to rows(tr), than cols (td) to locate the numbers for each rank_name
        for table in tables:
            rows = table.find_all('tr')
            for row in rows:
                cols = row.find_all('td')
                if len(cols) == 5:
                    # using text.replace to avoid typeerror by taking ',' away for further calculation
                    male_count = int(cols[2].text.replace(',', ''))
                    female_count = int(cols[4].text.replace(',', ''))
                    male_total += male_count
                    female_total += female_count
        print(f'Male Number: {male_total}')
        print(f'Female Number: {female_total}')


if __name__ == '__main__':
    main()
