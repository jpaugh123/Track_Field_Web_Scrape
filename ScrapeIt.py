from bs4 import BeautifulSoup
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
import re

## https://medium.com/swlh/web-scraping-using-selenium-and-beautifulsoup-adfc8810240a


import pandas as pd



from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException


## https://www.zenrows.com/blog/dynamic-web-pages-scraping-python#selenium
## https://stackoverflow.com/questions/26566799/wait-until-page-is-loaded-with-selenium-webdriver-for-python



def get_page(url, headless=True, elementXPath=None, implicit_delay=None):
    """
    Gets the name page HTML for the url provided using selenium webdriver with Chrome
    :param url: The url to get the page for
    :param headless: True for running selenium without opening chrome (faster). False to open CHrome (good for debugging)
    :param elementXPath: The XPath for an element whose presence will tell seleium that the page is properly loaaded
    :param implicit_delay: Delay setting
    :return: the html for the page, pulled after the page is finished loading
    """
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
    """
    Get the athletes for a team
    :param url: the url for a team
    :return: THe list of urls for athletes on the team - the link is to athletic.net
    """
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
    """
    Get the list of teams for division 1 track and field using the athletic.net page (thi is hard coded below)
    :return: The list of division 1 team urls in athletic.net
    """
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
    """
    Get the list of of athletes for D1 track and field for years provider below in years (variable defined below). THis uses athletic.net web page definition of teams and rosters
    The list of athletes - for each a team, team link, athlete name, and athlete link is returned
    The result is written to a csv file Division1Players.csv
    :return: none
    """
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
    """
    THis is the same as get_division1 - returns the list of athletes on teams for D1 track and field.
    The list of athletes is written to a dataframe Division1PlayersDecade.csv - a dataframe - for each a team, team link, athlete name, and athlete link is returned
    :param max_teams_to_get: Maxmimum teams to iterate through before stopping. -1 default value is all teams
    :return: none
    """
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
    """
    THis is a test function for getting D1. Dont need this
    :return:
    """
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
    """
    Get the list of texas uil 6a teams (high school).
    :return:
    """
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

## https://stackoverflow.com/questions/3945750/find-a-specific-tag-with-beautifulsoup

# https://www.geeksforgeeks.org/beautifulsoup-find-all-children-of-an-element/


def get_athlete_bio_results(soup):
    """
    Get the athletic event results from the provided HTML from athletic.net for an individual athlete
    :param soup: The beautiful soup (HTML) for an athlete from athletics.net
    :return: A dataframe
    """
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
    """
    THis code was not working
    :return:
    """
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
    """
    Get the list of top athletes using the url below (top athletes for 200 meters event for example)
    In the end I just copy/pasted this data into a spread-sheet since it's only 3 pages of data
    :param username: username for athletic.net. If you dont use an account for this it will only pull the first couple events
    :param password: password for athletic.net.
    :return:
    """

    driver = login_athletics(username, password)

    # so now we should be on the original page. but we are going to load it again directly (like normal)
    # get it again now that we logged in, check for detail element not login element

    elementXPath = "//a[starts-with(@href,'/athlete/')]"
    url = "https://www.athletic.net/TrackAndField/Division/Event.aspx?DivID=98249&Event=2"
    get_page_with_driver(driver, elementXPath, url)

    soup = BeautifulSoup(driver.page_source, "html.parser")
    result = get_athlete_data(soup)
    return result


def get_page_with_driver(driver, elementXPath, url, headless=True, delay=10):
    """
    Uses driver.get to pull the data from the url. Since this function accepts a driver it is faster. After using this function, driver.page_source can provide the data
    The idea is to use login_athletics first to create the driver and login, and then use this method to pull data from a page using this logged in session. This was the
    further scrapping is done using a particular user (and gets all the data)
    :param driver: a selenium driver object
    :param elementXPath: The html element whose presence tells selenium that the page is loaded fully
    :param url: the url to pull data from
    :param headless: ignored
    :param delay: delay before returning (in addition to elementXPath
    :return: nothing is returned but the driver now has the driver.page_source with the html
    """
    driver.get(url)
    #delay = 10  # seconds
    try:
        myElem = WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.XPATH, elementXPath)))
        # print("Page is ready!")
    except TimeoutException:
        print("Loading took too much time!", url)


def login_athletics(username,password, headless=True):
    """
    Log in to athletic.net using the provided password. This also cretes a selenium driver object that is returned
    :param username: username for login
    :param password: password for login
    :param headless: If true, does not create a browser (which slows things down). Browser is good for debugging sometimes though
    :return:
    """
    # get the page so we can login
    start_url = "https://www.athletic.net/account/login"
    elementXPath = "//input[starts-with(@type,'email')]"

    chrome_options = Options()
    if headless:
        chrome_options.add_argument("--headless")

    #driver = webdriver.Chrome(options=chrome_options,
    #                          service=Service(executable_path="/chromedriver-linux64/chromedriver"))

    driver = webdriver.Chrome(options=chrome_options)

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
    """
    Get the list of top athletes with login - this was not used
    :return:
    """

    url = "https://www.athletic.net/TrackAndField/Division/Event.aspx?DivID=98249&Event=2"
    content = get_page(url, elementXPath="//a[starts-with(@href,'/account')]", implicit_delay=10)
    #content = get_page(url, implicit_delay=5)

    soup = BeautifulSoup(content, "html.parser")
    result = get_athlete_data(soup)
    return result


def get_athlete_data(soup):
    """
    Get the athlete data from the top athletes (athletes ranked by something) from athletic.net. THis was not used
    :param soup:
    :return:
    """

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
    """
    Get the events for the top ranked athletes. This takes the athletic.net username and password as a parameter - these are necessary to get all events for an athlete.
    THe results are written to the output_file_name
    THe input_file_name has the list of athletes to scrape events for
    The steps used in the paper are :
    1) get the ranked athletes list from the athletic.net site by copy/paste into a spread sheet
    2) fill in the D1 result per athlet
    3) take that spread sheet and convert each tab to a csv (one for male 2019, male 2020, female 2019, female 2020)
    4) upload those csvs to google drive
    5) use the notebook RankedAthletes.ipynb to convert the list of athletes into /content/gdrive/MyDrive/TrackFieldData/RankedAthletes/Div1TrackFieldTopAthletesAllClean.csv
    6) take that csv and pull it down locally
    7) run this fuct ion with the ranked athletes file as input to get the event data for those athletes (writes out the csv)
    8) take the csv file and upload it back to google drive and pull it in using the RankedAthletes.ipynb (it's the second part of that notebook)
    9) that notebook will analyze the data - events and such, for those athletes

    :param username: athletic.net username
    :param password: athletic.net password
    :param batch_size: the number of athletes to scrape data for before writting to a file
    :param max_records: the maximum records - use for testing
    :param records_read: could of records already read (good for restart)
    :param batch_number: the current batch number (good for restart)
    :param input_file_name: the file name to read the list of athletes from
    :param output_file_name: the file name to write the results to
    :return: nothing
    """


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
                                     elementXPath="//a[starts-with(@href,'/TrackAndField/meet')]")
                soup = BeautifulSoup(driver.page_source, "html.parser")

                shared_athlete_bio_results = soup.find_all("shared-athlete-bio-results")
                topDivs = shared_athlete_bio_results[0].findChildren(recursive=False)
                for topDiv in topDivs:

                    # = topDiv.find("shared-athlete-bio-result-table-tf")
                    event_children = topDiv.find_all("tbody")
                    # event name is every other so...

                    for event_table in event_children:
                        event_rows = event_table.find_all("tr")
                        is_event_name = True

                        for event_row in event_rows:
                            if is_event_name:
                                event_name = event_row.text
                                is_event_name = False
                            else:
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


