__author__ = 'v2srivas'
import csv

file = open('C:/Users/v2srivas/Desktop/draftkings/fd_temp.csv', 'r')
reader = list(csv.reader(file))
file.close()
file = open('C:/Users/v2srivas/Desktop/draftkings/lineups.csv', 'r')
data = list(csv.reader(file))
file.close()
new_reader = []
for i in range(7, len(reader)):
    new_reader.append([reader[i][10], reader[i][13]+' '+reader[i][15]])
new_data = []
names = [val[1] for val in new_reader]
for record in data:
    new_record = []
    for row in record:
        if row in names:
            new_record.append(new_reader[names.index(row)][0])
        else:
            print('error: ', row)
    new_data.append(new_record)
file = open('C:/Users/v2srivas/Desktop/draftkings/lineups_upload.csv', 'w', newline="")
wr = csv.writer(file)
wr.writerow(["PG", "PG", "SG", "SG", "SF", "SF", "PF", "PF", "C"])
for row in new_data:
    wr.writerow(row)
file.close()
True
