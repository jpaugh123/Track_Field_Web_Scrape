# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from ScrapeIt import *
from FindHSAthleteCollege import *

from bs4 import BeautifulSoup
import pandas as pd


import aiohttp
import asyncio #to run async funtions you need to import asyncio


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('Get track and field data')
    username = "username"
    password = "passsword"


    #content = get_page("https://www.athletic.net/team/20591/track-and-field-outdoor/2023", headless=True,
    #                   elementXPath="//a[starts-with(@href,'/athlete')]")
    #print(content)

    #content = get_page("https://www.athletic.net/TrackAndField/College/NCAA/D1.aspx", headless=True,
    #                   elementXPath="//a[starts-with(@href,'/team/')]")
    #print(content)
    #get_division1()

    #teams = get_texas_uil_6a()
    #print(teams)

    #get_times_for_athlete().to_csv('Kennedy.csv')

    #
    #get_failed_url()
    #get_athletes_from_div1_file()
    #get_athletes_from_div1_file(batch_number=17, records_read=16001)
    #get_athletes_from_div1_file(batch_number=6, records_read=4748)
    #get_athletes_from_div1_file( batch_size=3, records_read=35630, max_records=35636)

    #get_division1_decade(max_teams_to_get=20)
    #get_athletes_from_div1_file(input_file_name="Division1PlayersDecade.csv", output_file_name="Division1PlayerDetailDecade")

    #get_swimming_div1_teams()
    #print("API Key", get_openai_api_key())
    #test_call_chatgpt()

    #get_top_athletes()

    #my_completion = initialize_chatgpt()
    #chat_response = ask_chatgpt(question="What is track and field?", completion=my_completion)
    #print(chat_response)

    #get_events_for_ranked_athletes()
    #times = get_times_for_athlete()
    #print(times)

    #df = get_top_athletes(username, password)
    #print(df.shape[0])

    # for men
    #get_events_for_ranked_athletes(username, password)

    # for women
    get_events_for_ranked_athletes(username, password,
                                   input_file_name = ".\Athletes\Div1TrackFieldTopAthletesAllCleanF.csv",
                                   output_file_name="RankedAthleteEventsF")

    #get_top_athletes(username, password)











