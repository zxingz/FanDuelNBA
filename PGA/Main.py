import csv
import pickle
from multiprocessing import Pool
import os
import glob
from random import shuffle


parameters = {}


def load_parameters():
    parameters['directory'] = 'C:\\Users\\v2srivas\\Desktop\\pga\\'  # file location
    parameters['filename'] = 'DKSalaries_pga.csv'  # file name
    parameters['g_pos'] = 6  # group starting position (columns starts from "0")
    parameters['max_sal'] = 50000  # maximum allowed salary
    parameters['min_rem'] = 1000  # minimum remaining salary
    parameters['run_lineup'] = 1  # run lineup builder ?
    parameters['run_analysis'] = 1 # run analysis ?
    parameters['schuffle'] = 0  # schuffle for minimum entry ?
    parameters['schuffle_times'] = 10000  # schuffle for minimum entry ?
    parameters['match_num'] = 4  # maximum number of players to match
    parameters['lineup_directory'] = 'C:\\Users\\v2srivas\\Desktop\\pga\\lineups\\'  # lineups file location
    print('reading data from file : ' + parameters['directory'] + parameters['filename'])
    print('lineup file location : ' + parameters['lineup_directory'] + parameters['filename'])
    print('starting position for group is (columns starts from "0") : ' + str(parameters['g_pos']))
    print('maximum allowed salary : ' + str(parameters['max_sal']))
    print('minimum remain salary : '+str(parameters['min_rem']))
    print('run lineup builder ? : ' + str(parameters['run_lineup']))
    print('run analysis ? : ' + str(parameters['run_analysis']))
    print('schuffle for minimum entry ? : ' + str(parameters['schuffle']))
    if parameters['schuffle'] == 1:
        print('how many times schuffle ? : ' + str(parameters['schuffle_times']))
    print('maximum number of players to match : ' + str(parameters['match_num']))

    parameters['data'] = read_data(parameters['directory'] + parameters['filename'], parameters['g_pos'])  # getting data from the file

'''
Nomenclature for constraints:
==========================================

'''

def lineup_analysis(lineup):
    for i in range(5):
        lineup[i] = int(lineup[i])-int(lineup[i+1])
    return True


def read_data(file, g_pos):
    istream = open(file, 'r')
    reader = list(csv.reader(istream))
    istream.close()
    if reader[0][0] == 'Position':
        del reader[0]
    for i in range(len(reader)):
        if g_pos == -1:
            constraints = []
        else:
            constraints = reader[i][g_pos:]
        reader[i] = [reader[i][1], reader[i][2], reader[i][4], constraints]
    reader = sorted(reader, key=lambda l: int(l[1]))
    return reader


def form_lineups(passing_data):
    process_num = passing_data[0]
    parameters = passing_data[1]
    data = parameters['data']
    data_len = len(data)
    max_sal = parameters['max_sal']
    min_rem_sal = parameters['min_rem']
    lineup_table = []
    file_count = 0
    print('starting process : '+str(process_num))
    for pga1 in range(process_num, process_num+1):
        points_pga1 = float(data[pga1][2])
        salary_pga1 = int(data[pga1][1])
        for pga2 in range(pga1+1, data_len-4):
            points_pga2 = points_pga1 + float(data[pga2][2])
            salary_pga2 = salary_pga1 + int(data[pga2][1])
            if salary_pga2 > max_sal:
                break
            else:
                for pga3 in range(pga2 + 1, data_len-3):
                    points_pga3 = points_pga2 + float(data[pga3][2])
                    salary_pga3 = salary_pga2 + int(data[pga3][1])
                    if salary_pga3 > max_sal:
                        break
                    else:
                        for pga4 in range(pga3 + 1, data_len-2):
                            points_pga4 = points_pga3 + float(data[pga4][2])
                            salary_pga4 = salary_pga3 + int(data[pga4][1])
                            if salary_pga4 > max_sal:
                                break
                            else:
                                for pga5 in range(pga4 + 1, data_len-1):
                                    points_pga5 = points_pga4 + float(data[pga5][2])
                                    salary_pga5 = salary_pga4 + int(data[pga5][1])
                                    if salary_pga5 > max_sal:
                                        break
                                    else:
                                        for pga6 in range(pga5 + 1, data_len):
                                            points_pga6 = points_pga5 + float(data[pga6][2])
                                            salary_pga6 = salary_pga5 + int(data[pga6][1])
                                            if salary_pga6 > max_sal:
                                                break
                                            else:
                                                if (max_sal - salary_pga6 <= min_rem_sal) and lineup_analysis([salary_pga6, salary_pga5, salary_pga4, salary_pga3, salary_pga2, salary_pga1, data[pga1][3], data[pga2][3], data[pga3][3], data[pga4][3], data[pga5][3], data[pga6][3]]):
                                                    lineup_table.append([pga1, pga2, pga3, pga4, pga5, pga6, points_pga6, salary_pga6])
                                                    # print('---------------------------added-------------------')
                                                    if len(lineup_table) >100:
                                                        file_count += 1
                                                        pickle.dump(lineup_table, open(parameters['lineup_directory'] + 'lineup_' + str(process_num) + '_' + str(file_count) + '.pkl', 'wb'))
                                                        lineup_table = []
    file_count += 1
    pickle.dump(lineup_table, open(parameters['lineup_directory']+'lineup_' + str(process_num) + '_' + str(file_count) + '.pkl', 'wb'))
    print('ending process : ' + str(process_num))


def read_lineups():
    main_table = []
    dire = parameters['lineup_directory']
    os.chdir(dire)
    for file in glob.glob("*.pkl"):
        lineup_table = pickle.load(open(dire + file, 'rb'))
        for cont in range(0, len(lineup_table)):
            main_table.append(lineup_table[cont])
    main_table = sorted(main_table, key=lambda l: l[6], reverse=True)
    return main_table


def filtering_lineups(l_board):
    if l_board == []:
        return []
    top = l_board[0]
    lineup_new = [top]
    del l_board[0]
    while l_board != []:
        count = 0
        while count < len(l_board):
            if len(frozenset(l_board[count][0:6]).intersection(top[0:6])) > parameters['match_num']:
                del l_board[count]
                count -= 1
            count += 1
        if l_board == []:
            break
        else:
            top = l_board[0]
            lineup_new.append(top)
            del l_board[0]
    return lineup_new


def running_analysis():
    lineups = read_lineups()
    for i in range(0, min([5, len(lineups)])):
        print(lineups[i])
    mini = len(lineups) + 1
    print('total generated lineups = ' + str(mini-1))
    lineups = sorted(lineups, key=lambda l: l[6], reverse=True)
    if parameters['schuffle'] == 0:
        runtime = 1
    else:
        runtime = parameters['schuffle_times']
    while runtime > 0:
        if parameters['schuffle'] == 1:
            shuffle(lineups)
        l_board = lineups[:]
        l_board = filtering_lineups(l_board)
        n = len(l_board)
        if n < mini:
            mini = n
            file = open(parameters['directory']+'lineups.csv', 'w')
            wr = csv.writer(file, lineterminator='\n')
            print(n)
            l_board = sorted(l_board, key=lambda l: l[6], reverse=True)
            for rank in range(0, n):
                string = []
                for i in range(0, 6):
                    nos = l_board[rank][i]
                    # print(match_data[indx_corr(nos)][2] + ' ' + match_data[indx_corr(nos)][3])
                    string.append(parameters['data'][nos][0])
                string.append(str(l_board[rank][6]))
                string.append(str(l_board[rank][7]))
                wr.writerow(string)
            file.close()
        runtime -= 1


def clear():
    os.chdir(parameters['lineup_directory'])
    for file in glob.glob("*.pkl"):
        os.remove(parameters['lineup_directory'] + file)


if __name__ == '__main__':
    load_parameters()
    if parameters['run_lineup'] == 1:
        clear()
        passing_data = []
        for i in range(len(parameters['data'])-5):
            passing_data.append([i, parameters])
        print('creating lineups...')
        with Pool(7) as p:
            p.map(form_lineups, passing_data)
    if parameters['run_analysis'] == 1:
        print('running analysis...')
        running_analysis()
    print('-----------------program terminated--------------------------')

#golfstat hack = https://www.golfstats.com/horses/?tid=22017&course=&years=1&rounds=0&points=dk&dmax=7500&vmax=600000&sticky=2&charli=&submit=GO