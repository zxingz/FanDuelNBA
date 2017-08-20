try:
    import urllib.request as urllib2
except ImportError:
    import urllib2
import re
import sqlite3

TAG_RE = re.compile(r'<[^>]+>')


def insert_data(query):
    conn = sqlite3.connect('golfstats_dk.db')
    conn.execute(query)
    conn.commit()
    conn.close()


def get_data(year, seq):
    url = 'https://www.golfstats.com/horses/?tid='+str(seq)+str(year)+'&course=&years=1&rounds=0&points=dk&dmax=7500&vmax=600000&sticky=2&charli=&submit=GO'
    try:
        response = urllib2.urlopen(url)
        html = str(response.read())
    except:
        return -1
    title = html[html.find('<tbody><tr><td><span title='):].replace('<tbody><tr><td><span title="','')
    title = title[:title.find(',')]
    html = html[html.find('<tbody><tr><td><span title="'):html.find('<div id="footer" class="footer">')]
    html = TAG_RE.sub(' ', html).split('  ')
    start = 2
    try:
        while html[start + 1] == '( P / T / Y )':
            query = 'insert into course_single_data values("' + title + '","'
            query += html[start] + '",'
            query += str(year) + ','
            query += str(seq) + ','
            query += html[start + 3] + ','
            query += html[start + 4] + ','
            query += html[start + 5].split('/')[0] + ','
            query += html[start + 6] + ','
            query += html[start + 7] + ','
            query += html[start + 8] + ','
            query += html[start + 9] + ','
            query += html[start + 10] + ','
            query += html[start + 11] + ','
            query += html[start + 12] + ','
            query += html[start + 13] + ','
            query += html[start + 14] + ','
            query += html[start + 15] + ','
            query += html[start + 16] + ','
            query += html[start + 17]
            query += ')'
            start += 19
            insert_data(query)
    except:
        return -1
    return 0



if __name__ == '__main__':
    for year in range(2015,2018):
        for seq in range(1, 200):
            ret = get_data(year, seq)
            if ret == -1:
                print(year, seq)



    '''
    url = 'http://espn.go.com/golf/leaderboard11/controllers/ajax/playerDropdown?xhr=1&playerId=' + id + '&tournamentId=' + str(num)
    try:
        response = urllib2.urlopen(url)
        html = str(response.read())
        file = open(path + '\\' + str(num) + '\\players\\' + id + '.html', 'w')
        file.write(html)
        file.close()
        True
    except:
        True
    '''