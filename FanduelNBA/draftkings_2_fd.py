import csv
import pickle
import re
import math
import glob, os
from multiprocessing import Pool

regex = re.compile('[^a-zA-Z]')
file = 'FD.csv'


def lineup_analysis(lineup):
    return True
    for i in range(8):
        lineup[i] -= lineup[i+1]
    flag = 0
    if len([i for i in lineup if i <4000]) < 3:
        flag += 1
    if 2<= len([i for i in lineup if 4000 <= i < 6000]) <= 5:
        flag += 1
    if 2 <= len([i for i in lineup if 6000 <= i < 8000]) <= 5:
        flag += 1
    if len([i for i in lineup if 8000 <= i]) >= 2:
        flag += 1
    if flag == 4:
        return True
    else:
        return False

'''
def lineup_analysis(lineup):
    for i in range(8):
        lineup[i] -= lineup[i+1]
    flag = 0
    if len([i for i in lineup if i <4000]) < 2:
        flag += 1
    if 3<= len([i for i in lineup if 4000 <= i < 6000]) <= 4:
        flag += 1
    if 2 <= len([i for i in lineup if 6000 <= i < 8000]) <= 4:
        flag += 1
    if len([i for i in lineup if 8000 <= i]) >= 2:
        flag += 1
    if flag == 4:
        return True
    else:
        return False
'''

def clear():
    dire = 'C:/Users/v2srivas/Desktop/draftkings/'
    os.chdir(dire)
    for file in glob.glob("*.pkl"):
        os.remove(dire + file)


def game_match_elim(teams):
    dict = {}
    for row in teams:
        if row in dict.keys():
            dict[row] += 1
        else:
            dict[row] = 1
    if max([dict[key] for key in dict.keys()]) < 5:
        return True
    else:
        return False


def read_data_match2(ch):
    f = open('C:/Users/v2srivas/Desktop/draftkings/'+file, 'r')
    reader = list(csv.reader(f))
    for row in reader:
        if row[6] == '' or row[6] == ' ':
            del reader[reader.index(row)]
    reader = sorted(reader, key=lambda l: int(l[6]))
    data_len = len(reader)
    data_pg = []
    data_sg = []
    data_pf = []
    data_sf = []
    data_c = []
    for i in range(0, data_len):
        if reader[i][1] == 'PG' and reader[i][12] == 'y':
            data_pg.append(reader[i])
        elif reader[i][1] == 'SG' and reader[i][12] == 'y':
            data_sg.append(reader[i])
        elif reader[i][1] == 'PF' and reader[i][12] == 'y':
            data_pf.append(reader[i])
        elif reader[i][1] == 'SF' and reader[i][12] == 'y':
            data_sf.append(reader[i])
        elif reader[i][1] == 'C' and reader[i][12] == 'y':
            data_c.append(reader[i])
    if ch == 1:
        return data_pg, data_sg, data_pf, data_sf, data_c
    else:
        return data_pg


def optimal_lineup(start_pg1):
    data_pg, data_sg, data_pf, data_sf, data_c = read_data_match2(1)
    lineup_table = []
    max_sal = 60000
    min_rem_sal = 3000
    total_points = 230
    file_count = 0
    if True:
        start_sg1 = 0
        start_pf1 = 0
        start_sf1 = 0
        start_c = 0
    for pg1 in range(start_pg1, start_pg1+1):
        print(data_pg[pg1])
        if True:
            points_pg1 = float(data_pg[pg1][4])
            salary_pg1 = int(data_pg[pg1][6])
            for pg2 in range(pg1+1, len(data_pg)):
                if True:
                    points_pg2 = points_pg1 + float(data_pg[pg2][4])
                    salary_pg2 = salary_pg1 + int(data_pg[pg2][6])
                    if salary_pg2 > max_sal:
                        break
                    else:
                        for sg1 in range(start_sg1, len(data_sg)-1):
                        #for sg1 in range(5, 6):
                            if True:
                                points_sg1 = points_pg2 + float(data_sg[sg1][4])
                                salary_sg1 = salary_pg2 + int(data_sg[sg1][6])
                                if salary_sg1 > max_sal:
                                    break
                                else:
                                    for sg2 in range(sg1+1, len(data_sg)):
                                    #for sg2 in [x for x in range(start_pf1, len(data_pf)) if x != 5]:
                                        if True:
                                            points_sg2 = points_sg1 + float(data_sg[sg2][4])
                                            salary_sg2 = salary_sg1 + int(data_sg[sg2][6])
                                            if salary_sg2 > max_sal:
                                                break
                                            else:
                                                for pf1 in range(start_pf1, len(data_pf)-1):
                                                #for pf1 in range(6, 7):
                                                    if True:
                                                        points_pf1 = points_sg2 + float(data_pf[pf1][4])
                                                        salary_pf1 = salary_sg2 + int(data_pf[pf1][6])
                                                        if salary_pf1 > max_sal:
                                                            break
                                                        else:
                                                            for pf2 in range(pf1+1, len(data_pf)):
                                                            #for pf2 in [x for x in range(start_pf1, len(data_pf)) if x != 6]:
                                                                if True:
                                                                    points_pf2 = points_pf1 + float(data_pf[pf2][4])
                                                                    salary_pf2 = salary_pf1 + int(data_pf[pf2][6])
                                                                    if salary_pf2 > max_sal:
                                                                        break
                                                                    else:
                                                                        for sf1 in range(start_sf1, len(data_sf)-1):
                                                                            if True:
                                                                                points_sf1 = points_pf2 + float(data_sf[sf1][4])
                                                                                salary_sf1 = salary_pf2 + int(data_sf[sf1][6])
                                                                                if salary_sf1 > max_sal:
                                                                                    break
                                                                                else:
                                                                                    for sf2 in range(sf1+1, len(data_sf)):
                                                                                        if True:
                                                                                            points_sf2 = points_sf1 + float(data_sf[sf2][4])
                                                                                            salary_sf2 = salary_sf1 + int(data_sf[sf2][6])
                                                                                            if salary_sf2 > max_sal:
                                                                                                break
                                                                                            else:
                                                                                                for c in range(start_c, len(data_c)):
                                                                                                    if True:
                                                                                                        points_c = points_sf2 + float(data_c[c][4])
                                                                                                        salary_c = salary_sf2 + int(data_c[c][6])
                                                                                                        if salary_c > max_sal:
                                                                                                            break
                                                                                                        else:
                                                                                                            #print(salary_c, points_c)
                                                                                                            if ((max_sal - salary_c <= min_rem_sal and points_c >= total_points)) and lineup_analysis([salary_c, salary_sf2, salary_sf1, salary_pf2, salary_pf1, salary_sg2, salary_sg1, salary_pg2, salary_pg1]) and game_match_elim([data_pg[pg1][8], data_pg[pg2][8], data_sg[sg1][8], data_sg[sg2][8], data_sf[sf1][8], data_sf[sf2][8], data_pf[pf1][8], data_pf[pf2][8], data_c[c][8]]):
                                                                                                                lineup_table.append([pg1, pg2, sg1+100, sg2+100, sf1+300, sf2+300, pf1+200, pf2+200, c+400,  points_c, salary_c])
                                                                                                                #print('---------------------------added-------------------')
                                                                                                                if len(lineup_table) >100:
                                                                                                                    file_count += 1
                                                                                                                    pickle.dump(lineup_table, open('C:/Users/v2srivas/Desktop/draftkings/lineup_' + str(start_pg1) + '_' + str(file_count) + '.pkl', 'wb'))
                                                                                                                    lineup_table = []
    file_count += 1
    pickle.dump(lineup_table, open('C:/Users/v2srivas/Desktop/draftkings/lineup_' + str(start_pg1) + '_' + str(file_count) + '.pkl', 'wb'))
    print(start_pg1)

if __name__ == '__main__':
    clear()
    with Pool(7) as p:
        match_data = read_data_match2(0)
        len_list = list(range(0, len(match_data)))
        p.map(optimal_lineup, len_list)
        print('done')
