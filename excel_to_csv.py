import pandas as pd
import os

def processData(year):
   
    xls_file = f"Data/excel/{year}.xls"
    print("XLS")
    print(xls_file)
    if os.path.exists(xls_file):
        print("File exists.")
    else:
        print("File does not exist.")
        xls_file = f"Data/excel/{year}.xlsx"
        print(xls_file)
        print("XLSX")
    if os.path.exists(xls_file):
        print("File exists.")
        level_dict = {
            'Steg 1':1,
            'Kan inte simma': 1,
            'kan inte simma': 1,
            'Steg 1- nybörjare, kan ej simma': 1,
            'Steg 1 - nybörjare, kan inte simma':1,
            'Steg 2':2,
            'Steg 2 - kan simma 5-25 m bröstsim':2,
            'Kan simma 5-25 m': 2,
            'Steg 3': 3,
            'Kan simma 25-50 m': 3,
            'Steg 4': 4,
            'Steg 4 ':4,
            'Steg 2 - kan simma 5-25 m': 2,
            'Steg 3 - kan simma 25 - 50 m': 3,
            'Steg 3 - kan simma 25-50 m':3,
            'Steg 3 - kan simma 25 - 50 m bröstsim':3,
            'Steg 3 - kan simma 25-50 m bröstsim':3,
            'Steg 4 - mer än 50 bröstsim, mindre än 25 m ryggsim': 4,
            'Steg 4 - mer än 50 m bröstsim, mindre än 25 m ryggsim':4,
            'Steg 4 - kan simma mer än 50 m men ej ryggsim': 4,
            'Kan simma längre äm 50 m': 5,
            'Kan simma längre än 50 m ': 5,
            'Kan simma längre än 50 m': 5,
            'Kan simma längre än 50m ': 5,
            'Kan simma längre än 50m': 5,
            'Steg 5': 5,
            'Steg 5 - mer än 50 m bröstsim, 25 m ryggsim, flyta 1 min, märkestagning': 5,
            'Steg 5 - mer än 50 m bröstsim, 25 m ryggsim, flyta 1 min, kunna dyka från kanten': 5,
            'Steg 5 - mer än 50 m bröstsim, mindre än 25 m ryggsim': 5,
            'Steg 5 - märkestagning, mer än 50 m bröstsim, 25 m ryggsim, flyta 1 min, kunna dyka från kanten': 5
        }
        df = pd.read_excel(xls_file, header=0, usecols="A,B,C")
        df.dropna(how='any', inplace=True)
        print(df)
        df1 = pd.DataFrame(columns=df.columns)
        filename1 =  f"Data/csv/data{year}_p1.txt"
        df1.to_csv(filename1, sep=',',header=0, index=False, encoding='utf-8')
        df2 = pd.DataFrame(columns=df.columns)
        filename2 =  f"Data/csv/data{year}_p2.txt"
        df2.to_csv(filename2, sep=',',header=0, index=False, encoding='utf-8')
        for index in df.index:
            print(f"{df.loc[index, 'Period']}, {df.loc[index, 'Busshållsplats']}, {df.loc[index, 'Simmkunighetidag']}")
            if df.loc[index, 'Period'] == "P1" or df.loc[index, 'Period'] == "P2":
                bus_stop = df.loc[index, 'Busshållsplats']
                #route = a[0:1]
                bus_split = bus_stop.split(sep = " ",maxsplit=1)
                print(bus_split)
                route = bus_split[0]
                location = bus_split[1]
                level = level_dict[df.loc[index, 'Simmkunighetidag']]
                print(f"ROUTE NUMBER: {route}")
                print(f"LOCATION: {location}")
                print(f"LEVEL: {level}")
                print(f"PERIOD: {df.loc[index, 'Period']}")
            
                if df.loc[index, 'Period'] == "P1": #int(df.loc[index, 'Period']) == 1:
                    #int(df.loc[index, 'Period']), 
                    data1 = [[location, level, route]]   

                    df1 = pd.DataFrame(data1, columns=['location','level','route'])
                    df1.to_csv(filename1, mode='a', sep=',',header=0, index=False, encoding='utf-8')
                if df.loc[index, 'Period'] == "P2":
                    data2 = [[location, level, route]]
                    
                    df2 = pd.DataFrame(data2, columns=['location','level','route'])
                    df2.to_csv(filename2, mode='a', sep=',',header=0, index=False, encoding='utf-8')
            else:
                print("SOMETHING WRONG WITH PERIOD")
    
processData("2021")