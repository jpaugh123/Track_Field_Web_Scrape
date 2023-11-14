import requests
import re
import pandas as pd
from bs4 import BeautifulSoup

# https://www.tfrrs.org/leagues/49.html
# Scrape the names of teams and links
# find_all a tags, get teams 
# team_links = soup.find_all("a", {"href": re.compile(r'/team/')})
# import re 


import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from scrapeTFFRSteamsBS import get_roster_for_team



def get_divI_teams():
    team_links = []
    team_names = []
    # URL of the webpage to scrape
    url = 'https://www.tfrrs.org/leagues/49.html'

    # Send an HTTP GET request to the URL
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.content, 'html.parser')
        team_links_elements = soup.find_all("a", {"href": re.compile(r'/teams/')})
        for link in team_links_elements:
            team_links.append(link['href'])
            team_names.append(link.text)
        team_rosters = pd.DataFrame({'Team': team_names, 'Link': team_links})
        return team_rosters


years_dict = {
    2023 : "?config_hnd=290",
    2022 : "?config_hnd=254",
    2021 : "?config_hnd=214",
    2020 : "?config_hnd=187",
    2019 : "?config_hnd=158",
    2018 : "?config_hnd=129",
    2017 : "?config_hnd=108"
}

#teams = get_divI_teams()
#teams.to_csv('divI_teams.csv', index=False)
teams = pd.read_csv('divI_teams.csv')
print(len(teams))
i = 0

team_names = []
team_links = []
athlete_genders = []
team_years = []
athlete_names = []
athlete_grades = []
athlete_links = []
batch_number = 1
batch_size = 25

for index, team in teams.iterrows():
    team_name = team['Team']
    team_link = team['Link']
    if "_m_" not in team_link:
        gender = "F"
    else:
        gender = "M"
    #year = 2023
    for year in years_dict :
        year_parameter = years_dict[year]
        team_link_with_year = team_link + year_parameter
        print(team_name, team_link_with_year)
        roster = get_roster_for_team(team_link_with_year)

        for athlete_index, athlete in roster.iterrows():
            team_names.append(team_name)
            team_links.append(team_link)
            team_years.append(year)
            athlete_genders.append(gender)
            athlete_grades.append(athlete["Grade"])
            athlete_names.append(athlete["Name"])
            athlete_links.append(athlete["Link"])

    if i == batch_size:
        all_rosters = pd.DataFrame(
            {'TeamName': team_names, 'TeamLink': team_links, 'TeamYear': team_years, 'AthleteGender': athlete_genders,
             'AthleteName': athlete_names, 'AthleteGrade': athlete_grades, "AthleteLink": athlete_links})
        all_rosters.to_csv('divI_team_rosters' + str(batch_number) + '.csv')
        # clear the data
        team_names = []
        team_links = []
        athlete_genders = []
        team_years = []
        athlete_names = []
        athlete_grades = []
        athlete_links =     []
        i = 0
        batch_number += 1
    else:
        i += 1
# save the final data
all_rosters = pd.DataFrame(
    {'TeamName': team_names, 'TeamLink': team_links, 'TeamYear': team_years, 'AthleteGender': athlete_genders,
     'AthleteName': athlete_names, 'AthleteGrade': athlete_grades, "AthleteLink": athlete_links})
all_rosters.to_csv('divI_team_rosters' + str(batch_number) + '.csv')
