import csv
import pandas as pd
import os
fileInput = open(r"/home/anshul/Desktop/sem6proj/Attendance.csv")
data = csv.reader(fileInput)
csvData = []
for row in data:
    csvData.append(row)
print(csvData)
fileInput.close()
fileOuput = open("Temp.csv", 'w', newline='')
date = "20/05/2020"
name = "anshul"
writer = csv.writer(fileOuput, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
if csvData[0][-1] != date:
    csvData[0].append(date)
    for i in range(1, len(csvData)):
        csvData[i].append('A')

for i in range(1, len(csvData)):
    if csvData[i][0] == name:
        csvData[i][-1] = 'P'
print(csvData)
for row in csvData:
    writer.writerow(row)
fileOuput.close()
os.remove('Attendance.csv')
os.rename('Temp.csv', 'Attendance.csv')
