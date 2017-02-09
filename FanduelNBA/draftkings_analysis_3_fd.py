import pickle
import csv
import glob
import os
from random import shuffle


data_pg = []
data_sg = []
data_pf = []
data_sf = []
data_c = []
file = 'FD.csv'


def read_data_match():
    global data_sf, data_pf, data_pg, data_sg, data_c
    f = open('C:/Users/v2srivas/Desktop/draftkings/'+file, 'r')
    reader = list(csv.reader(f))
    for row in reader:
        if row[6] == '' or row[6] == ' ':
            del reader[reader.index(row)]
    reader = sorted(reader, key=lambda l: int(l[6]))
    data_len = len(reader)
    for i in range(0, data_len):
        if reader[i][1] == 'PG' and reader[i][12] == 'y':
            data_pg.append(i)
        elif reader[i][1] == 'SG' and reader[i][12] == 'y':
            data_sg.append(i)
        elif reader[i][1] == 'PF' and reader[i][12] == 'y':
            data_pf.append(i)
        elif reader[i][1] == 'SF' and reader[i][12] == 'y':
            data_sf.append(i)
        elif reader[i][1] == 'C' and reader[i][12] == 'y':
            data_c.append(i)

    return reader


def indx_corr(indx):
    global data_sf, data_pf, data_pg, data_sg, data_c
    if indx in range (0,100):
        return data_pg[indx]
    elif indx in range (100,200):
        return data_sg[indx-100]
    elif indx in range(200,300):
        return data_pf[indx-200]
    elif indx in range(300,400):
        #return data_sf[indx-300]
        try:
            return data_sf[indx-300]
        except:
            print(indx)
    elif indx in range (400,500):
        return data_c[indx-400]


def display_dist(match_data, player_list, player_count):
    count = 0
    for i in player_list:
        print(match_data[indx_corr(i)][1]+':'+ str(player_count[count]))
        count += 1


def find_top_10():
    main_table = []
    dire = 'C:/Users/v2srivas/Desktop/draftkings/'
    os.chdir(dire)
    for file in glob.glob("*.pkl"):
        lineup_table = pickle.load(open(dire + file, 'rb'))
        for cont in range(0, len(lineup_table)):
            main_table.append(lineup_table[cont])
    main_table = sorted(main_table, key=lambda l: l[9], reverse=True)
    return main_table


def filtering_append(l_board):
    total_lineups = len(l_board)
    lineup_new = []
    while l_board != [] and len(lineup_new) < total_lineups:
        #print(len(l_board), len(lineup_new))
        if lineup_new != []:
            flag = 0
            for row in lineup_new:
                if len(frozenset(l_board[0][0:9]).intersection(row[0:9])) > 7:
                    flag = 1
                    break
            if flag != 1:
                lineup_new.insert(0, l_board[0])
        else:
            lineup_new.append(l_board[0])
        del(l_board[0])
        total_lineups = len(l_board)
    return lineup_new


def fix_players(l_board):
    new_l = []
    include_list = []
    exclude_list = []
    for row in l_board:
        temp1 = row[0:9]
        if exclude_list != []:
            pex = len(frozenset(temp1).intersection(exclude_list))
            if pex == 0:
                new_l.append(row)
        if include_list != []:
            pex = len(frozenset(temp1).intersection(include_list))
            if pex != 0:
                new_l.append(row)
    return new_l


match_data = read_data_match()
lineups = find_top_10()
for i in range(0,min([5, len(lineups)])):
    print(lineups[i][9:11])
print(lineups[:5])
min = len(lineups)+1
print('total generated lineups = '+ str(min))
lineups = sorted(lineups, key=lambda l: l[9], reverse=True)
while 1:
    #shuffle(lineups)
    l_board = lineups[:]
    l_board = filtering_append(l_board)
    n = len(l_board)
    if n < min:
        min = n
        file = open('C:/Users/v2srivas/Desktop/draftkings/lineups.csv', 'w')
        wr = csv.writer(file, lineterminator='\n')
        print(n)
        l_board = sorted(l_board, key=lambda l: l[9], reverse=True)
        for rank in range(0, n):
            string = []
            for i in range(0,9):
                nos = l_board[rank][i]
                #print(match_data[indx_corr(nos)][2] + ' ' + match_data[indx_corr(nos)][3])
                string.append(match_data[indx_corr(nos)][2] + ' ' + match_data[indx_corr(nos)][3])
            string.append(str(l_board[rank][9]))
            string.append(str(l_board[rank][10]))
            wr.writerow(string)
        file.close()
    #break