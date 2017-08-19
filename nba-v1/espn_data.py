from datetime import date, timedelta
from selenium import webdriver
import mysql.connector


def get_game_ids(start=''):

    cnx = mysql.connector.connect(user='root', password='root', database='nba-v1')
    cursor = cnx.cursor()
    driver = webdriver.Chrome()

    end = date.today() + timedelta(1)
    if start == '':
        start = date(2016, 1, 1)
    else:
        start = date(int(start[0:4]), int(start[4:6]), int(start[6:8]))

    while start != end:
        url = 'http://www.espn.com/nba-v1/scoreboard/_/date/' + start.strftime('%Y%m%d')
        driver.get(url)
        source = str(driver.page_source)
        if source.find(start.strftime('%B %-d, %Y')) != -1:
            game_ids = {}
            while source.find('/nba-v1/boxscore?gameId=') != -1:
                source = source[source.find('/nba-v1/boxscore?gameId=')+21:]
                game_ids[source[:source.find('"')]] = True
            for key in game_ids:
                try:
                    cursor.execute('INSERT INTO gameIDs VALUES ( "'+start.strftime('%Y%m%d')+'", "' + key + '");')
                except:
                    continue
        cnx.commit()
        start += timedelta(1)

    driver.close()
    cursor.close()
    cnx.close()
    return


if __name__ == '__main__':
    get_game_ids('20150101')