import matplotlib.pyplot as plt
import numpy as np
from sys import exit

def is_numeric(df, data):
    if df[data].dtype == np.int64 or df[data].dtype == np.float:
        return True
    else:
        return False

def validation(df, data, kind):
    for i in range(0,len(data)):
        if kind == 3 or kind == 1 and (not is_numeric(df, data[i])):
            valid = False
        else:
            valid = True
    return valid

def plotting(df, data, index, kind):   
    check = validation(df, data, kind)
    while not check:
        print('This kind of plot can\'t use not scalar value!')
        exit()
    if data == None:
        data = ['Temperature','Dew Point', 'Humidity', 'Wind Speed', 'Wind Gust', 'Pressure', 'Precip.', 'Precip Accum']
    if index != 'Time' and kind == 1:
        df = df.groupby(df['day/month']).mean().reset_index()   
    if index in data:
        print('We can\'t plot a chart with the same values of x and y!')
        print('We will exchange x to default day/month!')        
        df.set_index('day/month', inplace=True)   
    else:
        df.set_index(index, inplace=True)  
    if kind == 1:
        x = list(df.index.values)
        for col in data:
            if 'Wind' in data or 'Condition' in data:
                plt.figure()
            y = list(df[col])
            plt.plot(x,y, label=col)
            plt.xticks(rotation=90)
            plt.xlabel(index) 
            plt.legend()
            plt.title('Line chart')
        plt.show()
    elif kind == 2:
        x = list(df.index.values)
        for col in data:
            if 'Wind' in data or 'Condition' in data:
                plt.figure()
            y = list(df[col])
            plt.scatter(x,y, label=col)
            plt.xticks(rotation=90)
            plt.xlabel(index) 
            plt.legend()
            plt.title('Scatter chart')
        plt.show()
    elif kind == 3:
        for col in data:
            df[col].plot.hist(alpha=0.5)
            plt.legend()
            plt.title('Histogram')
            plt.show()  
    elif kind == 4:
        for col in data:
            plt.figure()
            df.groupby(col)[col].count().plot.pie(autopct='%1.1f%%')
            plt.title('Pie Chart')

