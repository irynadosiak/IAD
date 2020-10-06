import matplotlib.pyplot as plt
import pylab
def show(database, column,c):
    # different graphics 
    a=['greenyellow', 'olive', 'yellow', 'red', 'green', 'plum', 'yellow']
    x = list(database.index.values)
    y = list(database[column])
    plt.scatter(x,y, label=column, color=a[c])
    plt.xticks(rotation=90)
    plt.ylabel(column)
    plt.legend()
    plt.grid()
    plt.show()
        
def show_one(database,column,c):
    if column == 'Wind Speed':
        x = list(database.index.values)
        y = list(database[column])
        database[column].plot.bar(color = 'gold')
        plt.ylabel(column)
        plt.xticks(rotation=90)
        plt.legend()
        plt.grid()
        plt.show()   
    elif column == 'Humidity':
        x = list(database.index.values)
        y = list(database[column])
        database[column].plot.area(color='palevioletred')
        plt.ylabel(column)
        plt.xticks(rotation=90)
        plt.legend()
        plt.show() 
    elif column == 'Wind' or column == 'Condition':
        a=['greenyellow', 'olive', 'yellow', 'red', 'green', 'plum', 'yellow']
        x = list(database.index.values)
        y = list(database[column])
        plt.scatter(x,y, label=column, color=a[c])
        plt.xticks(rotation=90)
        plt.ylabel(column)
        plt.grid()
        plt.legend()
        plt.show()
    else:
        x = list(database.index.values)
        y = list(database[column])
        x1 = range(len(x))
        pylab.xticks(x1, x)
        plt.xticks(x1,rotation=90)
        plt.plot(x1, y, label=column)
        plt.scatter(x,y)
        plt.xticks(rotation=90)
        plt.ylabel(column)
        plt.legend()
        plt.show()

def create(database, columns, how_show):
    # create graphics 
    x=1
    c=0
    if len(columns) == 1:
        for column in columns:
            how_show(database, column, c)
            c=c+1 
    elif len(columns) == 2:
        if 'Wind' in columns or 'Condition' in columns:
            for column in columns:
                plt.subplot(len(columns), 1, x)
                how_show(database, column, c)
                x=x+1
                c=c+1
        else:
            for column in columns:
                how_show(database, column, c)
                c=c+1 
    else:
        for column in columns:
            plt.subplot(len(columns), 1, x)
            how_show(database, column, c)
            x=x+1
            c=c+1
        
        