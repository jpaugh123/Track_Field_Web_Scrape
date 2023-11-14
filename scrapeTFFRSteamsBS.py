import requests
from bs4 import BeautifulSoup
import pandas as pd

# https://www.tfrrs.org/leagues/49.html
# Scrape the names of teams and links
# find_all a tags, get teams 
# team_links = soup.find_all("a", {"href": re.compile(r'/team/')})
# import re 

# URL of the webpage to scrape
url = 'https://www.tfrrs.org/teams/tf/MA_college_m_Boston_College.html?config_hnd=158'


def get_roster_for_team(url):
    athlete_names = []
    athlete_grades = []
    athlete_links = []
    # Send an HTTP GET request to the URL
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.content, 'html.parser')
        table = soup.find_all('table', {'class': 'tablesaw table-striped table-bordered table-hover'})
        # Find the parent container using XPath
        # print(len(table[1]))

        roster_table = table[1].findChildren(recursive=False)[1].findChildren(recursive=False)
        for roster_row in roster_table:
            # print(roster_row)
            # NAME OF SCHOOL NEEDED
            roster_columns = roster_row.findChildren(recursive=False)
            athlete_name = roster_columns[0].findChildren(recursive=False)[0].text
            athlete_link = roster_columns[0].findChildren(recursive=False)[0]["href"]
            athlete_grade = roster_columns[1].text
            athlete_names.append(athlete_name)
            athlete_grades.append(athlete_grade)
            athlete_links.append(athlete_link)
           
        # WRITE TO FILE
        athlete_roster = pd.DataFrame({'Name': athlete_names, 'Grade': athlete_grades, "Link":athlete_links})
        return athlete_roster


roster = get_roster_for_team(url)
roster.to_csv('test_team_roster.csv', index=False)

