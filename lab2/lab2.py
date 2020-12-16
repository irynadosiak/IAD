#https://raw.githubusercontent.com/VasiaPiven/covid19_ua/master/covid19_by_settlement_dynamics.csv
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import pylab
import geopandas as gpd

def barr(df,col):
        x = list(df.index.values)
        y = list(df[col])
        plt.bar(x,y, label=col)
        plt.xticks(rotation=90)
        plt.title('active_confirm')
        plt.show()

def read_file(file):
    df = pd.read_csv(file, sep = ',', encoding='utf8', parse_dates=[0], decimal = '.')
    return df

def parse(df):
    df['zvit_date'] = pd.to_datetime(df['zvit_date']).dt.strftime('%Y-%m-%d')
    return df

def region_sum(df, area):
    area1 = df.loc[df['registration_area'] == area]
    area_df = area1.groupby('zvit_date').sum()
    area_df = area_df.reset_index() 
    return area_df

def region_cumulative_sum(df, obl):
    df = df.loc[df['registration_area'] == obl]
    df_sum = df.groupby(by=['registration_area', 'zvit_date']).sum()
    df_cum = df.groupby(by=['registration_area', 'zvit_date']).sum().groupby(level=[0]).cumsum()
    df_cum['active_confirm'] = df_sum['active_confirm']
    df_cum = df_cum.reset_index()
    return df_cum

def line(database, col, region):
    x = list(database['zvit_date'])
    y = list(database[col])
    x1 = range(len(x))
    pylab.xticks(x1, x)
    plt.xticks(x1[::10], rotation = 90)
    plt.plot(x1, y, label = region)
    plt.xticks(rotation = 90)
    plt.xlabel('zvit_date') 
    plt.title('Dynamics of ' + col)
    plt.legend(loc = 'upper left')
    
def line_cumulative(database, col, region):
    x = list(database['zvit_date'])
    y = list(database[col])
    x1 = range(len(x))
    pylab.xticks(x1, x)
    plt.xticks(x1[::10], rotation = 90)
    plt.plot(x1, y, label = col)
    plt.title('Dynamics of ' + region)
    plt.legend(loc = 'upper left')
    plt.show()

def print_menu():
    print(34 * " ", "MENU", 35 * " ")
    print("1 -- Show the statistic for one region")
    print("2 -- Compare the statistics of some regions")
    print("3 -- Display the statistics on Ukraine on a map")      
    print("4 -- Display the statistics on Ukraine on a map")   
    print("5 -- Exit")  
    
file = input('Enter path:\n')
df = read_file(file)
parse(df)
loop = True
while(loop):
    print_menu()
    choice = input("Enter your choice:  ")

    if choice == '1':
        cols = ['active_confirm', 'new_susp', 'new_confirm', 'new_death', 'new_recover']
        region = input('Choose region:\n')
        dataframe = region_cumulative_sum(df, region)
        for col in cols:
            line_cumulative(dataframe, col, region)
    elif choice == '2':
        n = input('How many regions?(num or all)\n')
        if n == 'all':
            areas = np.unique(df['registration_area'])
        else:
            areas = input('What area to visualizate?\n').split(", ")
        #column = input('\nChoose: active_confirm, new_susp, new_confirm, new_death, new_recover\n')
        column = 'active_confirm'
        for area in areas:
            line(region_sum(df, area), column, area)
        plt.show()
        excel = input('Do you want to write your dataframe to a file?(yes or no)\n')
        dataframe = pd.DataFrame()
        writer = pd.ExcelWriter('C:/Users/Ira Dosiak/.spyder-py3/example.xlsx', engine='xlsxwriter')
        if excel == 'yes':
            for area in areas:
                dataframe1 = df.loc[df['registration_area'] == area]
                dataframe = dataframe1.groupby('zvit_date').sum() 
                dataframe.to_excel(writer, area)
            print('Successfully saved!')
            writer.save()
    elif choice == '3':
        ukraine = 'C:/Users/Ira Dosiak/.spyder-py3/gadm36_UKR_shp/gadm36_UKR_1.shp'
        regions = gpd.read_file(ukraine)
        regions.loc[:, 'registration_area'] = [['Черкаська'], ['Чернігівська'], ['Чернівецька'], ['Крим'], ['Дніпропетровська'], ['Донецька'], ['Івано-Франківська'], ['Харківська'], ['Херсонська'], ['Хмельницька'], ['Київська'], ['м. Київ'], ['Кіровоградська'], ['Львівська'], ['Луганська'], ['Миколаївська'], ['Одеська'], ['Полтавська'], ['Рівненська'], ['Севастополь'], ['Сумська'], ['Тернопільська'], ['Закарпатська'], ['Вінницька'], ['Волинська'], ['Запорізька'], ['Житомирська']]
        #print(regions)
        #column = input('\nChoose: active_confirm, new_susp, new_confirm, new_death, new_recover\n')
        column = 'active_confirm'
        df1 = df[['zvit_date', 'registration_area', 'registration_region', 'registration_settlement']]
        df1.loc[:, column] = df[column]
        #print(df1)
        day = input('\nChoose date: 2020-03-01 -- 2020-11-16\n')
        df2 = df1.loc[df1['zvit_date'] == day]
        data = df2.groupby('registration_area').sum()
        merged = regions.set_index('registration_area').join(data)
        merged = merged.reset_index()
        #print(merged)
        fig, ax = plt.subplots(1)
        ax.axis('off')
        ax.set_title('Map of ' + column, fontdict={'fontsize': '30', 'fontweight' : '3'})
        color = 'OrRd'
        vmin, vmax = 0, 30000
        sm = plt.cm.ScalarMappable(cmap=color, norm=plt.Normalize(vmin=vmin, vmax=vmax))
        sm._A = []
        cbar = fig.colorbar(sm)
        cbar.ax.tick_params(labelsize=20)
        merged.plot(column, cmap=color, linewidth=0.8, ax=ax, figsize=(40,20))
        plt.show()
    elif choice == '4':
        data = df.groupby('registration_area').sum()
        barr(data,'active_confirm')        
    elif choice == '5':
        print("Exiting..")
        loop = False
    else:
        input("Wrong menu selection. Enter any key to try again..")
