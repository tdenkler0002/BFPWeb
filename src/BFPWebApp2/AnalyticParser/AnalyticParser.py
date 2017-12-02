import pandas as pd
import re
import matplotlib.pyplot as plt
import os

def parse(file_name):

    # Reads CSV if exists
    try:
        df = pd.read_csv('data.csv',index_col=None)

    # If not will make empty data frame
    except FileNotFoundError:
        df = pd.DataFrame(index=None)

    # Has to do graph seperate because cumalative
    try:
        df_graph = pd.read_csv('graph.csv',index_col=0)

    except FileNotFoundError:
        df_graph = pd.DataFrame()

    # Error name and occurances
    data = [['error_name','occurances']]

    try:
        with open(file_name+".txt", "r") as f, open("data.txt","w") as dtxt, open("graph.txt","w") as gtxt:
            # Making temporary files so it can be appended to CSV files later
            for line in f:

                # Removing whitespace
                cleanedLine = line.replace(" ","").strip()

                # Get Customer ID
                if cleanedLine and (cleanedLine.find('Customer') != -1) and (cleanedLine.find('ID') != -1):
                    temp_data=re.split(':|,',cleanedLine)
                    if len(temp_data)> 2:
                        del temp_data[-1]
                        del temp_data[-1]
                        data.append(temp_data)
                    else:
                        data.append(temp_data)

                # Looking for errors (Start point and grabbing all error fields thereafter)
                elif cleanedLine and (cleanedLine.find('Errors')!=-1) and (cleanedLine.find('=')!=-1):
                    temp_data=re.split('=',cleanedLine)
                    data.append(temp_data)

                elif cleanedLine and (cleanedLine.find('Errors')!=-1):
                    for line in f:
                        cleanedLine = line.replace(" ","").strip()
                        if cleanedLine and (cleanedLine.find('=')!=-1):
                            temp_data=re.split('=',cleanedLine)
                            data.append(temp_data)

            f.close()
            # Rename file pulled so we cannot pull from file again
            os.rename(file_name+".txt",file_name+"_done.txt")

            # Writing to the new data file
            for x in range(1, len(data)):
                dtxt.write(str(data[x][0]).lower()+',')

            dtxt.write("\n")

            for x in range(1, len(data)):
                dtxt.write(str(data[x][1]).lower()+',')

            for x in range(0, len(data)):
                if len(data[x])> 1 and x != 1 and x != 2:
                    gtxt.write(str(data[x][0]).lower()+',')
                    gtxt.write(str(data[x][1]).lower())
                    gtxt.write("\n")

        dtxt.close()
        gtxt.close()


        df0 = pd.read_csv('data.txt',index_col=None)
        df1 = pd.read_csv('graph.txt',index_col=0)
        df = df.append(df0)

        # Appending to the CSV files which is used to make DF
        try:
            df_graph = df_graph.add(df1, axis=0,fill_value=0)
        except:
            df_graph = df_graph.append(df1)

        df = df[df.columns.drop(list(df.filter(regex='Unnamed:')))]
        df.fillna(value=0, inplace=True)
        df.to_csv('data.csv',index=False)
        df_graph.to_csv('graph.csv')

    except FileNotFoundError:
        print('No such file')

# For searching the error codes - based on column headers
def df_search(terms):
    return print(df[terms])

q = ''
while q != "no":
    q = input('Parse, Plot, or Search?').lower()
    # Plot - calling csv, sorting based on occuences - high to low
    if q == 'plot':
        df_graph = pd.read_csv('graph.csv',index_col=0)
        df_graph.sort_values(by=['occurances'],ascending=False,inplace=True)
        df_graph.plot(kind='bar', figsize=(15,15), title='Errors', grid=True)
        plt.subplots_adjust(bottom=0.5,wspace=.25)
        plt.xlabel('')
        plt.xticks(rotation=75)
        plt.show()

    # Seach - searching by column header names
    elif q == 'search':
        df = pd.read_csv('data.csv',index_col=None)
        columns = input('Column headers?')
        columns = columns.replace(' ', '').strip()
        columns=columns.split(',')
        if columns[0] == 'All':
            print(df)
        else:
            df_search(columns)
    # PArsing per file name
    elif q == 'parse':
        fn = input('File Name:')
        parse(fn)

    # Hidden but resets all (deletes csv files to create new ones)
    elif q == 'reset':
        os.remove('data.csv')
        os.remove('graph.csv')
