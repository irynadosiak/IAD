import pandas
import graphics
from datetime import datetime

def to_celsius(temperature1):
    b=[]
    for i in range(len(temperature1)):
        celsius = int((temperature1[i] - 32) * 5/9)
        b.append(celsius)
    return b

def change_date(date1):
    # change date    
    b=[]
    for i in range(len(date1)):
        a = datetime.strptime(date1[i], '%d.%b').strftime('%d.%m.2019')
        b.append(a) 
    return b
   
def to_int(list1, x):
    # delete mph etc      
    list2 = []
    for i in range(len(list1)):
        list2.append(int(str(list1[i])[:x]))
    return list2

def parse(database):
    # parse some databases 
    database['Time'] = pandas.to_datetime(database['Time']).apply(lambda x: x.strftime(r'%H:%M'))
    database['Humidity'] = to_int(list(database['Humidity']), -1)
    database['Wind Speed'] = to_int(list(database['Wind Speed']),-4)
    database['Wind Gust'] = to_int(list(database['Wind Gust']),-4)
    database['day/month'] = change_date(list(database['day/month']))
    database['Temperature'] = to_celsius(list(database['Temperature']))
    return database  
                     
# read from csv
database=pandas.read_csv('DATABASE.csv', sep=';',decimal=',')  
# parse database 
parse(database)
# create database depending on your choice of day
def database_day(database, str):
    database1=database.loc[database['day/month'] == str]
    return database1
# user interaction
print('Do you want to specify column names to visualize? (Yes or No)')
while True:
    choose = input()
    if choose == 'Yes':
        print('How many charts do you want to visualize?')
        while True:
            n = input()
            try:
                if int(n) <= 0:  
                    print("Sorry, input must be a positive integer, try again")
                    continue
                break
            except:
                print('There must be a positive number!')  
        data=[]
        for i in range(int(n)):
            column = str(input())
            data.append(column)
    elif choose == 'No': 
        data = None
    else:
        print('Yes or No')
        continue
    break
print('Do you want to specify index? (Yes or No)')
while True:
    choose = input()
    if choose == 'Yes':
        print('Give index:')
        index = str(input())
        if index == 'Time':
            print('Set a specific day (16.07.2019)')
            day = str(input())
            database = database_day(database,day)
    elif choose == 'No': 
        index = 'day/month'
    else:
        print('Yes or No')
        continue
    break
print('Do you want to specify kind of chart? (Yes or No)')
while True:
    choose = input()
    if choose == 'Yes':
        print('1 - line chart')
        print('2 - scatter chart')
        print('3 - histogram')        
        print('4 - pie chart')        
        print('Give index:')
        kind = int(input())
    elif choose == 'No': 
        kind = 1
    else:
        print('Yes or No')
        continue
    break
graphics.plotting(database, data, index, kind)
