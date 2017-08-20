from datetime import date, timedelta
from selenium import webdriver
import urllib.request
import os
import re


def get_espn_game_ids(start=''):

    driver = webdriver.Chrome('./../../chromedriver')
    driver.set_page_load_timeout(30)

    end = date.today() + timedelta(1)
    if start == '':
        start = date(2016, 1, 1)
    else:
        start = date(int(start[0:4]), int(start[4:6]), int(start[6:8]))

    os.system('echo "gameID, date" >> /home/vishnu/Data/espn_game_ids.csv')
    while start != end:
        try:
            url = 'http://www.espn.com/nba/scoreboard/_/date/' + start.strftime('%Y%m%d')
            driver.get(url)
            source = str(driver.page_source)
            if source.find(start.strftime('%B %-d, %Y')) != -1:
                game_ids = {}
                while source.find('/nba/boxscore?gameId=') != -1:
                    source = source[source.find('/nba/boxscore?gameId=') + 21:]
                    game_ids[source[:source.find('"')]] = True
                for key in game_ids:
                    os.system(
                        'echo "' + key + ', ' + start.strftime('%Y%m%d') + '" >> ./../../../Data/espn_game_ids.csv')
            start += timedelta(1)
        except:
            print(start)
            continue
    driver.close()
    return


def get_rotogrinder_game_details():
    file = open('./../../../Data/espn_game_ids.csv', 'r')
    data = file.read().split('\n')
    file.close()
    all_dates = set()
    if data:
        os.system('echo "date, data" > ./../../../Data/rotogrinderData.csv')
        for row in data:
            try:
                row = row.replace(' ', '').split(',')
                if row[0] == 'gameID':
                    continue
                date = row[1][:4] + '-' + row[1][4:6] + '-' + row[1][6:]
                if date not in all_dates:
                    all_dates.add(date)
                    text = str(urllib.request.urlopen('https://rotogrinders.com/lineups/nba?date=' +
                                                      date + '&site=fanduel').read())
                    text = text[text.find('schedules: ') + 11:text.find('startedGames: ')]
                    text = text[:text.find('\\n') - 1]
                    with open('./../../../Data/rotogrinderData.csv', 'a') as file:
                        file.write(row[1]+', '+text+'\n')
            except Exception as error:
                print(row)
                print('error with '+date+' :'+error)
                continue


def get_espn_playbyplay():
    file = open('./../../../Data/espn_game_ids.csv', 'r')
    data = file.read().split('\n')
    file.close()
    if data:
        os.system('echo "gameID, data" > ./../../../Data/espnplaybyplay.csv')
        for row in data:
            try:
                row = row.replace(' ', '').split(',')
                if row[0] == 'gameID':
                    continue
                gameID = row[0]
                text = str(urllib.request.urlopen('http://www.espn.com/nba/playbyplay?gameId='+gameID).read())
                text = text[text.find('<div id="gamepackage-qtrs-wrap">'):]
                text = re.compile(r'<.*?>').sub('#', text[:text.find('</ul>')]).replace('team', '')
                while text.find('##') != -1:
                    text = text.replace('##', '#')
                text = text.split('#')
                del text[0:2]
                data = '#'.join(text)
                with open('./../../../Data/espnplaybyplay.csv', 'a') as file:
                    file.write(gameID + ', ' + data + '\n')
            except Exception as error:
                print(row)
                print('error with '+gameID+' :'+error)
                continue

def get_espn_boxscore():
    file = open('./../../../Data/espn_game_ids.csv', 'r')
    data = file.read().split('\n')
    file.close()
    if data:
        os.system('echo "gameID, data" > ./../../../Data/espn_boxscore.csv')
        for row in data:
            try:
                row = row.replace(' ', '').split(',')
                if row[0] == 'gameID':
                    continue
                gameID = row[0]
                text = str(urllib.request.urlopen('http://www.espn.com/nba/boxscore?gameId='+gameID).read())
                text = text[text.find('<article class="boxscore'):]
                text = re.compile(r'<.*?>').sub('#', text[:text.find('</article>')]).replace('team', '')
                while text.find('##') != -1:
                    text = text.replace('##', '#')
                text = text.split('#')
                del text[0:2]
                data = '#'.join(text)
                with open('./../../../Data/espn_boxscore.csv', 'a') as file:
                    file.write(gameID + ', ' + data + '\n')
            except Exception as error:
                print(row)
                print('error with '+gameID+' :'+error)
                continue

if __name__ == '__main__':
    #get_espn_game_ids('20150101')
    #get_rotogrinder_game_details()
    get_espn_boxscore()