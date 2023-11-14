import selenium
from bs4 import BeautifulSoup
import time
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
import math

import pickle

from selenium.webdriver.common.keys import Keys

from requests_html import HTMLSession

from requests_html import AsyncHTMLSession
import re

## https://medium.com/swlh/web-scraping-using-selenium-and-beautifulsoup-adfc8810240a

import nest_asyncio

import time

import pandas as pd


def scrape():
    print("scrape")

    from selenium import webdriver

    driver = webdriver.Chrome()
    driver.get("https://www.athletic.net/team/20955/track-and-field-outdoor/2023")

    # driver.switch_to.frame("cible")

    # wait = WebDriverWait(driver, 10)
    # wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'td.resultatIntitule')))

    # print(driver.page_source)

    # soup = BeautifulSoup(driver.page_source, 'lxml')
    # print(soup)
    time.sleep(10)

    athlete_name = driver.find_element(By.className("btn btn-link px-0 py-1"))
    print(athlete_name)


def scrape2():
    url = "https://www.athletic.net/team/20955/track-and-field-outdoor/2023"
    session = HTMLSession()
    response = session.get(url)
    response.html.render()

    print(response.content)


async def get_html(url):
    session = AsyncHTMLSession()
    r = await session.get(url)
    await r.html.arender()
    h1 = r.html.find('h1', first=True)
    print(h1.text)


def scrape3():
    url = "https://www.athletic.net/team/20955/track-and-field-outdoor/2023"
    nest_asyncio.apply()

    session = HTMLSession()
    response = session.get(url)
    response.html.render()

    # print(response.content)

    print(response.text)
    # print(response.html)


from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException


## https://www.zenrows.com/blog/dynamic-web-pages-scraping-python#selenium
## https://stackoverflow.com/questions/26566799/wait-until-page-is-loaded-with-selenium-webdriver-for-python

def scrape4():
    url = "https://www.athletic.net/team/20955/track-and-field-outdoor/2023"
    driver = webdriver.Chrome(service=ChromeService(
        ChromeDriverManager().install()))

    driver.get(url)
    print(driver.page_source)

"""
def get_page_old(url, headless=True, elementXPath=None):
    chrome_options = Options()
    if headless:
        chrome_options.add_argument("--headless")

    driver = webdriver.Chrome(options=chrome_options, service=ChromeService(
        ChromeDriverManager().install()))

    driver.get(url)

    if elementXPath is not None:
        delay = 6  # seconds
        try:
            myElem = WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.XPATH, elementXPath)))
            # print("Page is ready!")
        except TimeoutException:
            print("Loading took too much time!", url)

        return driver.page_source
"""
""" https://github.com/SergeyPirogov/webdriver_manager/issues/536
"" https://www.techbeamers.com/selenium-webdriver-waits-python/
"""

def get_page(url, headless=True, elementXPath=None, implicit_delay=None):
    chrome_options = Options()
    if headless:
        chrome_options.add_argument("--headless")

    driver = webdriver.Chrome(options=chrome_options, service=Service(executable_path="/chromedriver-linux64/chromedriver"))

    if implicit_delay is not None:
        driver.implicitly_wait(implicit_delay)

    driver.get(url)

    if elementXPath is not None:
        delay = 6  # seconds
        try:
            myElem = WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.XPATH, elementXPath)))
            # print("Page is ready!")
        except TimeoutException:
            print("Loading took too much time!", url)

        return driver.page_source
    else:
        return driver.page_source




def get_athletes_for_team(url):
    athletes = []
    content = get_page(url, elementXPath="//a[starts-with(@href,'/athlete')]")

    soup = BeautifulSoup(content, "html.parser")
    athlete_links = soup.find_all("a", {"class": "btn btn-link px-0 py-1"})
    # print(athlete_links)
    # print(len(athlete_links))
    # print(athlete_links)

    for athlete_link in athlete_links:
        athlete = {'name': athlete_link.text, 'link': athlete_link['href']}
        athletes.append(athlete)

    return athletes


def get_teams_div1():
    teams = {}
    url = "https://www.athletic.net/TrackAndField/College/NCAA/D1.aspx"
    content = get_page(url, elementXPath="//a[starts-with(@href,'/team/')]")

    soup = BeautifulSoup(content, "html.parser")
    team_links = soup.find_all("a", {"href": re.compile(r'/team/')})

    for team_link in team_links:
        # team = {'name': team_link.text, 'link': team_link['href']}
        # teams.append(team)
        teams[team_link.text] = team_link['href']

    return teams


def get_division1():
    years = ['2023', '2022', '2021', '2020', '2019', '2018']

    teams = get_teams_div1()
    print(teams)
    print("Found total # of teams :" + str(len(teams)))

    div1_althletes = []

    i = 1
    for key in teams.keys():
        print(key, teams[key])
        i = i + 1

        for year in years:
            team_url = "https://www.athletic.net" + teams[key] + "/" + year
            atheletes = get_athletes_for_team(team_url)
            # print(team_url, year, atheletes)
            for athletes_on_team in atheletes:
                div1_althletes.append([key, teams[key], year, athletes_on_team['name'], athletes_on_team['link']])
        # if i > 3:
        #    break

    # print(div1_althletes)

    # convert to a dataframe
    df_div1 = pd.DataFrame(div1_althletes, columns=['Team', 'TeamLink', 'Year', 'AthleteName', 'AthleteLink'])
    df_div1.to_csv('Division1Players.csv')


def get_division1_decade(max_teams_to_get = -1):
    years = list(range(2013, 2024, 1))
    print("Range is ", str(years))

    teams = get_teams_div1()
    print(teams)
    print("Found total # of teams :" + str(len(teams)))

    div1_althletes = []

    i = 1
    for key in teams.keys():
        print(key, teams[key])
        i = i + 1

        for year in years:
            team_url = "https://www.athletic.net" + teams[key] + "/" + str(year)
            atheletes = get_athletes_for_team(team_url)
            # print(team_url, str(year), atheletes)
            for athletes_on_team in atheletes:
                div1_althletes.append([key, teams[key], year, athletes_on_team['name'], athletes_on_team['link']])
        if max_teams_to_get != -1 and i > max_teams_to_get:
            break

    # print(div1_althletes)

    # convert to a dataframe
    df_div1 = pd.DataFrame(div1_althletes, columns=['Team', 'TeamLink', 'Year', 'AthleteName', 'AthleteLink'])
    df_div1.to_csv('Division1PlayersDecade.csv')



def test_get_division1():
    years = ['2023', '2022', '2021', '2020', '2019', '2018']

    teams = get_teams_div1()
    for key in teams.keys():
        print(key, teams[key])

        for year in years:
            team_url = "https://www.athletic.net" + teams[key] + "/" + year

            team_page = get_page(team_url, True)

            soup = BeautifulSoup(team_page, "html.parser")
            athlete_links = soup.find_all("a", {"class": "btn btn-link px-0 py-1"})
            print(key, teams[key], year, len(athlete_links))




def get_texas_uil_6a_teams():
    teams = {}
    url = "https://www.athletic.net/TrackAndField/Texas/UIL6A.aspx"
    content = get_page(url, elementXPath="//a[starts-with(@href,'/team/')]")

    soup = BeautifulSoup(content, "html.parser")
    team_links = soup.find_all("a", {"href": re.compile(r'/team/')})

    for team_link in team_links:
        # team = {'name': team_link.text, 'link': team_link['href']}
        # teams.append(team)
        teams[team_link.text] = team_link['href']

    return teams


def get_texas_uil_6a_athelete_times():
    return None


## https://stackoverflow.com/questions/3945750/find-a-specific-tag-with-beautifulsoup

# https://www.geeksforgeeks.org/beautifulsoup-find-all-children-of-an-element/


def get_times_for_athlete():
    url = "https://www.athletic.net/athlete/16283783/track-and-field/high-school"
    content = get_page(url, elementXPath="//a[starts-with(@href,'TrackAndField/meet')]")

    soup = BeautifulSoup(content, "html.parser")
    result = get_athlete_bio_results(soup)
    return result


def get_athlete_bio_results(soup):
    seasons = []
    events = []
    placements = []
    times = []
    dates = []
    meetNames = []
    meetLinks = []
    meetCode = []
    meetCodeDescription = []

    shared_athlete_bio_results = soup.find_all("shared-athlete-bio-results")
    topDivs = shared_athlete_bio_results[0].findChildren(recursive=False)
    for topDiv in topDivs:
        event_table = topDiv.find("shared-athlete-bio-result-table-tf")
        event_children = event_table.findChildren(recursive=False)
        # event name is every other so...
        is_event_name = True

        for event_table in event_children:
            if is_event_name:
                event_name = event_table.text
                is_event_name = False
            else:
                event_rows = event_table.find_all("tr")
                for event_row in event_rows:
                    result_tds = event_row.find_all("td")

                    seasons.append(topDiv.find(class_="mb-0").text)
                    events.append(event_name)

                    placements.append(result_tds[0].text)
                    times.append(result_tds[2].text)
                    dates.append(result_tds[3].text)
                    meetNames.append(result_tds[4].text)
                    meetCode.append(result_tds[5].text)
                is_event_name = True

    zipped = list(zip(seasons, events, placements, times, dates, meetNames, meetCode))
    df = pd.DataFrame(zipped, columns=["Season", "Event", "placement", "Time", "Date", "MeetName", "MeetCode"])
    return (df)
    print(zipped)

    print("seasons", seasons)
    print("events", events)
    print("placements", placements)
    print("times", times)
    print("dates", dates)
    print("meetNames", meetNames)
    print("meetCode", meetCode)

"""
def get_failed_url():
    div1_althletes = []

    failed_url = pd.read_csv("failed_url.csv")
    # print(failed_url)
    for team_url in failed_url:
        atheletes = get_athletes_for_team(team_url)
        # print(team_url, year, atheletes)
        for athletes_on_team in atheletes:
            div1_althletes.append([key, teams[key], year, athletes_on_team['name'], athletes_on_team['link']])

        # print(div1_althletes)

        # convert to a dataframe
    df_div1 = pd.DataFrame(div1_althletes, columns=['Team', 'TeamLink', 'Year', 'AthleteName', 'AthleteLink'])
    df_div1.to_csv('Division1PlayerFailed.csv')
"""

def get_athletes_from_div1_file(batch_size=1000,
                                max_records=-1,
                                records_read=0,
                                batch_number=1,
                                input_file_name="Division1Players.csv",
                                output_file_name="Division1PlayerDetail"):
    """
    Reads from the file Division1Players.csv and writes out csv to file Division1PlayerDetailX.csv
    :param file_count: ignore
    :param batch_size: The number of records per file. E.g. if you set this to 100 then after 100 athletes, the function will created a file
    :param max_records: The maximum records to read. Not that records_read is actually an index. So if you pass records_read = 1 and max_records = 100, it will read the first 100 records. If you pass records_read=100 and max_records = 100, it will not read any records. If you pass records_read=100 and max_records=200, it will read records 100 to 200
    :param records_read: the starting index from the file Division1Players.csv. Set to 1 to start at the beginning. Set to a higher value to start after the begginning of the file
    :param batch_number: tthis indicates the starting index of the file. E.g. if you pass in batch_number=10 the first file will be DivisionPlayersDetail10.csv. Use this to control the names of the files that are generated

    :return:nothing returned. It write out to csv file files based on batch_number.
    """
    div1_athletes = pd.read_csv(input_file_name)

    athelete_link = []
    seasons = []
    events = []
    placements = []
    times = []
    dates = []
    meetNames = []
    meetLinks = []
    meetCode = []
    meetCodeDescription = []

    # get the list of athlete_links PRIOR to the current index
    athlete_links_prior = set(div1_athletes[:records_read]["AthleteLink"])
    print("Found count of prior athelete records based on index :" + str(len(athlete_links_prior)))


    while (records_read < max_records or max_records == -1) and records_read < len(div1_athletes):
        print(div1_athletes.iloc[records_read])

        # read the record
        athlete_record = div1_athletes.iloc[records_read]
        url = "https://athletic.net" + athlete_record["AthleteLink"] + "/all"

        current_athlete = athlete_record["AthleteLink"]
        if not current_athlete in athlete_links_prior:

            try:
                content = get_page(url, elementXPath="//a[starts-with(@href,'TrackAndField/meet')]")
                soup = BeautifulSoup(content, "html.parser")

                shared_athlete_bio_results = soup.find_all("shared-athlete-bio-results")
                topDivs = shared_athlete_bio_results[0].findChildren(recursive=False)
                for topDiv in topDivs:
                    event_table = topDiv.find("shared-athlete-bio-result-table-tf")
                    event_children = event_table.findChildren(recursive=False)
                    # event name is every other so...
                    is_event_name = True

                    for event_table in event_children:
                        if is_event_name:
                            event_name = event_table.text
                            is_event_name = False
                        else:
                            event_rows = event_table.find_all("tr")
                            for event_row in event_rows:
                                result_tds = event_row.find_all("td")

                                seasons.append(topDiv.find(class_="mb-0").text)
                                events.append(event_name)

                                placements.append(result_tds[0].text)
                                times.append(result_tds[2].text)
                                dates.append(result_tds[3].text)
                                meetNames.append(result_tds[4].text)
                                meetCode.append(result_tds[5].text)
                            is_event_name = True
            except:
                print("Cannot load bio data for athlete: row=" + str(records_read) + " Athlete= " + athlete_record[
                   "AthleteLink"])
        athlete_links_prior.add(current_athlete)

        if records_read > 0 and records_read % batch_size == 0:
            print("Write out the file")
            zipped = list(zip(athelete_link, seasons, events, placements, times, dates, meetNames, meetCode))
            df = pd.DataFrame(zipped,
                              columns=["AtheleteLink", "Season", "Event", "placement", "Time", "Date", "MeetName",
                                       "MeetCode"])
            file_name = output_file_name + str(batch_number) + ".csv"
            df.to_csv(file_name)
            batch_number = batch_number + 1
            print("Reinitialize the data")

            athelete_link = []
            seasons = []
            events = []
            placements = []
            times = []
            dates = []
            meetNames = []
            meetLinks = []
            meetCode = []
            meetCodeDescription = []

        records_read = records_read + 1

    print("Write out any remaining data")
    zipped = list(zip(athelete_link, seasons, events, placements, times, dates, meetNames, meetCode))
    df = pd.DataFrame(zipped,
                      columns=["AtheleteLink", "Season", "Event", "placement", "Time", "Date", "MeetName", "MeetCode"])
    file_name = output_file_name + str(batch_number) + ".csv"
    df.to_csv(file_name)

def get_swimming_div1_teams():
    teams = {}
    url = "https://swimswam.com/swimulator-ncaa-d1-team-rankings-teams/"
    content = get_page(url, elementXPath="//a[starts-with(@href,'http://swimulator.herokuapp.com/teamstats/')]")

    soup = BeautifulSoup(content, "html.parser")
    team_links = soup.find_all("a", {"href": re.compile(r'http://swimulator.herokuapp.com/teamstats/')})

    for team_link in team_links:
        # team = {'name': team_link.text, 'link': team_link['href']}
        # teams.append(team)
        teams[team_link.text] = team_link['href']

    return teams

from selenium.webdriver.support.select import Select

def get_top_athletes(username, password):

    driver = login_athletics(username, password)

    # so now we should be on the original page. but we are going to load it again directly (like normal)
    # get it again now that we logged in, check for detail element not login element

    elementXPath = "//a[starts-with(@href,'/athlete/')]"
    url = "https://www.athletic.net/TrackAndField/Division/Event.aspx?DivID=98249&Event=2"
    get_page_with_driver(driver, elementXPath, url)

    soup = BeautifulSoup(driver.page_source, "html.parser")
    result = get_athlete_data(soup)
    return result


def get_page_with_driver(driver, elementXPath, url, headless=True):
    driver.get(url)
    delay = 10  # seconds
    try:
        myElem = WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.XPATH, elementXPath)))
        # print("Page is ready!")
    except TimeoutException:
        print("Loading took too much time!", url)


def login_athletics(username,password, headless=True):
    # get the page so we can login
    start_url = "https://www.athletic.net/account/login"
    elementXPath = "//input[starts-with(@type,'email')]"

    chrome_options = Options()
    if headless:
        chrome_options.add_argument("--headless")

    driver = webdriver.Chrome(options=chrome_options,
                              service=Service(executable_path="/chromedriver-linux64/chromedriver"))
    driver.implicitly_wait(5)
    driver.get(start_url)
    delay = 6  # seconds
    try:
        myElem = WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.XPATH, elementXPath)))
        # print("Page is ready!")
    except TimeoutException:
        print("Loading took too much time!", url)
    # enter the email + password to login, this redirects back to the original page too
    driver.find_element(By.XPATH, "//input[starts-with(@type,'email')]").send_keys(username)
    driver.find_element(By.XPATH, "//input[starts-with(@type,'password')]").send_keys(password)
    submitButton = driver.find_elements(By.XPATH, "//button[starts-with(@type,'submit')]")
    submitButton[0].click()

    # wait for it to process the login request
    elementXPath =  "//*[contains(text(), 'Followers')]"
    try:
        myElem = WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.XPATH, elementXPath)))
        # print("Page is ready!")
    except TimeoutException:
        print("Loading took too much time!", url)
    return driver


def get_top_athletes_with_login():

    url = "https://www.athletic.net/TrackAndField/Division/Event.aspx?DivID=98249&Event=2"
    content = get_page(url, elementXPath="//a[starts-with(@href,'/account')]", implicit_delay=10)
    #content = get_page(url, implicit_delay=5)

    soup = BeautifulSoup(content, "html.parser")
    result = get_athlete_data(soup)
    return result

def get_athlete_data(soup):

    ages = []
    grades = []
    athlete_names = []
    athlete_links = []
    times = []
    states = []
    team_names = []
    team_links = []
    dates = []

    athlete_data =  soup.find_all("table", {"class": re.compile(r'HLData')})
    rows = athlete_data[0].find_all("tr", attrs={"class":None})

    for athlete_row in rows:
        result_tds = athlete_row.find_all("td")
        if len(result_tds) > 1 :
            ages.append(result_tds[2].text)
            grades.append(result_tds[3].text)
            athlete_link_in_cell = result_tds[4].find_all("a")[0]
            athlete_names.append(athlete_link_in_cell.text)
            athlete_links.append(athlete_link_in_cell['href'])
            times.append(result_tds[5].text)
            states.append(result_tds[6].text)
            team_link = result_tds[7].find_all("a")
            if len(team_link) > 0:
                team_links.append(team_link[0]['href'])
                team_names.append(team_link[0].text)
            else:
                team_links.append("")
                team_names.append(result_tds[7].text)
            dates.append(result_tds[8].text)

    zipped = list(zip(ages, grades, athlete_names, athlete_links, times, states, team_names, team_links, dates))
    #zipped = list(zip(seasons, events, placements, times, dates, meetNames, meetCode))
    df = pd.DataFrame(zipped, columns=["Age", "Grade", "AthleteName", "AthleteLink", "Time", "State", "TeamName", "TeamLink", "Date"])
    return (df)


def get_events_for_ranked_athletes(username,
                                password,
                                batch_size=1000,
                                max_records=-1,
                                records_read=0,
                                batch_number=1,
                                input_file_name = ".\Athletes\Div1TrackFieldTopAthletesAllClean.csv",
                                output_file_name="RankedAthleteEvents"):


    df_ranked_athletes = pd.read_csv(input_file_name)
    #print(df_ranked_athletes.head())


    driver = login_athletics(username,password, headless=True)

    athlete_links_prior = set()

    athelete_link = []
    seasons = []
    events = []
    placements = []
    times = []
    dates = []
    meetNames = []
    #meetLinks = []
    meetCode = []
    #meetCodeDescription = []

    for index, row in df_ranked_athletes.iterrows():
        # we only want high school events
        url = row["AthleteLink"]
        if isinstance(url,str) and not url in athlete_links_prior:
            url = url + "/high-school"
            print(url )
            try:
                get_page_with_driver(driver=driver, url=url,
                                     elementXPath="//a[starts-with(@href,'TrackAndField/meet')]")
                soup = BeautifulSoup(driver.page_source, "html.parser")

                shared_athlete_bio_results = soup.find_all("shared-athlete-bio-results")
                topDivs = shared_athlete_bio_results[0].findChildren(recursive=False)
                for topDiv in topDivs:
                    event_table = topDiv.find("shared-athlete-bio-result-table-tf")
                    event_children = event_table.findChildren(recursive=False)
                    # event name is every other so...
                    is_event_name = True

                    for event_table in event_children:
                        if is_event_name:
                            event_name = event_table.text
                            is_event_name = False
                        else:
                            event_rows = event_table.find_all("tr")
                            for event_row in event_rows:
                                result_tds = event_row.find_all("td")

                                athelete_link.append(url)

                                seasons.append(topDiv.find(class_="mb-0").text)
                                events.append(event_name)

                                placements.append(result_tds[0].text)
                                times.append(result_tds[2].text)
                                dates.append(result_tds[3].text)
                                meetNames.append(result_tds[4].text)
                                meetCode.append(result_tds[5].text)
                            is_event_name = True
            except:
                print("Cannot load bio data for athlete: row=" + str(records_read) + " Athlete= " + url)
        athlete_links_prior.add(url)

        if records_read > 0 and records_read % batch_size == 0:
            print("Write out the file")
            zipped = list(zip(athelete_link, seasons, events, placements, times, dates, meetNames, meetCode))
            df = pd.DataFrame(zipped,
                              columns=["AtheleteLink", "Season", "Event", "placement", "Time", "Date", "MeetName",
                                       "MeetCode"])
            file_name = output_file_name + str(batch_number) + ".csv"
            df.to_csv(file_name)
            batch_number = batch_number + 1
            print("Reinitialize the data")

            athelete_link = []
            seasons = []
            events = []
            placements = []
            times = []
            dates = []
            meetNames = []
            meetLinks = []
            meetCode = []
            meetCodeDescription = []

        records_read = records_read + 1

    print("Write out any remaining data")
    zipped = list(zip(athelete_link, seasons, events, placements, times, dates, meetNames, meetCode))
    df = pd.DataFrame(zipped,
                      columns=["AtheleteLink", "Season", "Event", "placement", "Time", "Date", "MeetName", "MeetCode"])
    file_name = output_file_name + str(batch_number) + ".csv"
    df.to_csv(file_name)



