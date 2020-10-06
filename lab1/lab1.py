import pandas as pd
import graphics
from datetime import datetime

def to_celsius(temperature1):
    b=[]
    for i in range(len(temperature1)):
        celsius = int(temperature1[i] - 32) * 5/9
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

def to_float(number1):
    # change pressure to float     
    k=[]
    for i in range(len(number1)):
        b=number1[i].split(',')
        c='.'.join(map(str, b))
        d=float(c)
        k.append(d)
    return k

def parse(database):
    # parse some databases 
    database['Pressure'] = database['Pressure'].replace(to_replace=list(database['Pressure']),value=to_float(list(database['Pressure'])))
    database['Time'] = pd.to_datetime(database['Time']).apply(lambda x: x.strftime(r'%H:%M'))
    database['Humidity'] = database['Humidity'].replace(to_replace=list(database['Humidity']),value=to_int(list(database['Humidity']), -1))
    database['Wind Speed'] = database['Wind Speed'].replace(to_replace=list(database['Wind Speed']),value=to_int(list(database['Wind Speed']),-4))
    database['Wind Gust'] = database['Wind Gust'].replace(to_replace=list(database['Wind Gust']),value=to_int(list(database['Wind Gust']),-4))
    database['day/month'] = database['day/month'].replace(to_replace=list(database['day/month']),value=change_date(list(database['day/month'])))
    database['Temperature'] = database['Temperature'].replace(to_replace=list(database['Temperature']),value=to_celsius(list(database['Temperature'])))
    return database  
                     
# read from csv
database=pd.read_csv('DATABASE.csv', sep=';')  
# parse database 
parse(database)
# create database depending on your choice of day
def database_day(database, str):
    database1=database.loc[database['day/month'] == str]
    database1.set_index('Time', inplace=True)
    return database1   
# user interaction
print('How many charts do you want to vizualizate?') 
n=int(input())
print('\nWhich column do you want to vizualizate?') 
columns=[]
for j in range(n):
    column=input() 
    columns.append(column)
print('\nDo you want to watch all period or a certain day?(all or dd.mm.yyyy)')
i = input()
# create graphics 
if i=='all':
    # set index     
    database.set_index('day/month', inplace=True)
    graphics.create(database, columns, graphics.show)
else:
    graphics.create(database_day(database, i), columns, graphics.show_one)  
