from datetime import date, timedelta
from selenium import webdriver
import urllib.request
import os


def get_espn_game_ids(start=''):

    driver = webdriver.Chrome('/home/vishnu/PycharmProjects/chromedriver')
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
                        'echo "' + key + ', ' + start.strftime('%Y%m%d') + '" >> /home/vishnu/Data/espn_game_ids.csv')
            start += timedelta(1)
        except:
            print(start)
            continue
    driver.close()
    return


def get_rotogrinder_game_details():
    file = open('/home/vishnu/Data/espn_game_ids.csv', 'r')
    data = file.read().split('\n')
    file.close()
    all_dates = set()
    if data:
        os.system('echo "date, data" > /home/vishnu/Data/rotogrinderData.csv')
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
                    with open('/home/vishnu/Data/rotogrinderData.csv', 'a') as file:
                        file.write(row[1]+', '+text+'\n')
            except Exception as error:
                print(row)
                print('error with '+date+' :'+error)
                continue


if __name__ == '__main__':
    #get_espn_game_ids('20150101')
    #get_rotogrinder_game_details()
    stdout = os.popen('pwd')
    print(stdout.read())