import demjson
import urllib.request
import pickle
import csv


def player_details(temp, team, oppteam, match, his,pro, mode):
    try:
        firstname = temp['player']['data']['first_name']
        lastname = temp['player']['data']['last_name']
        status = temp['position']
        position = temp['player']['data']['position']
        salary = 999999
        for row in temp['player']['data']['salaries']['collection']:
            if row['data']['site_id'] == 2:
                salary = str(row['data']['salary'])
                break
        if mode == 'hispro':
            score = temp['player']['data']['game_stats']['collection'][0]['data']['stats']['fpts']['2']
            projection = temp['player']['data']['projected_stats']['collection'][0]['data']['stats']['fpts']['2']
            his.append(['None',position, firstname, lastname, score,'None', salary, match, team, oppteam, status,'None', 'y'])
            pro.append(['None', position, firstname, lastname, projection,'None', salary, match, team, oppteam, status, 'None', 'y'])
        else:
            score = temp['player']['data']['projected_stats']['collection'][0]['data']['stats']['fpts']['2']
            pro.append(['None',position, firstname, lastname, score,'None', salary, match, team, oppteam, status,'None', 'y'])
    except:
        print(temp)
    True


def process(mode,data,dates):
    his = []
    pro = []
    for row in data['schedules'].keys():
        teamaw = data['schedules'][row]['data']['team_away']['data']['hashtag']
        teamh = data['schedules'][row]['data']['team_home']['data']['hashtag']
        match = max(teamaw,teamh)+min(teamaw, teamh)
        for player in data['schedules'][row]['data']['team_away']['data']['lineups']['collection'].keys():
            player_details(data['schedules'][row]['data']['team_away']['data']['lineups']['collection'][player]['data'], teamaw, teamh, match,his,pro, mode)
            True
        print(data['schedules'][row]['data']['team_home']['data']['hashtag'])
        for player in data['schedules'][row]['data']['team_home']['data']['lineups']['collection']:
            player_details(data['schedules'][row]['data']['team_home']['data']['lineups']['collection'][player]['data'], teamh, teamaw, match, his,pro, mode)
    file = open('C:/Users/v2srivas/Desktop/draftkings/FD_proj_' + dates + '.csv', 'w')
    wr = csv.writer(file, lineterminator='\n')
    for row in pro:
        wr.writerow(row)
    file.close()
    if mode == 'hispro':
        file = open('C:/Users/v2srivas/Desktop/draftkings/FD_historic_'+dates+'.csv', 'w')
        wr = csv.writer(file, lineterminator='\n')
        for row in his:
            wr.writerow(row)
        file.close()

if __name__ == '__main__':
    #mode = input(' enter mode (hispro, pro) :')
    mode = 'pro'
    #dates = input('Enter Date in DDMMYY format : ')
    dates = '070217'
    text = str(urllib.request.urlopen('https://rotogrinders.com/lineups/nba-v1?date=20' + dates[4:] + '-' + dates[2:4] + '-' + dates[0:2] + '&site=fanduel').read())
    text = '{' + text[text.index('isGameToggle: true'):text.index('teamsOff')] + 'teamsOff: []}'
    text = text.replace('\\n', '')
    data = demjson.decode(text)
    pickle.dump(data, open('C:\\Users\\v2srivas\\Desktop\\rotodata.pkl', 'wb'))
    data = pickle.load(open('C:\\Users\\v2srivas\\Desktop\\rotodata.pkl', 'rb'))
    process(mode, data, dates)
