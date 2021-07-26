#Test task by ***
#Task received 16.07.2021 10:30
#Programmer: Chetyrbok Ivan i_ingar@mail.ru
#github.com/fraIoann
#Python 3.8.8

import pandas as pd
import datetime
from dateutil.relativedelta import relativedelta
import matplotlib.pyplot as plt

def hampel_filter (df, column):
    #function applies Hampel filter (with IQR frame) to data frame  
    #function gets data frame and name of column for analisis and returns
    #new data frame without excluded rows
    #calculing 1, 3 quantilies and quantile range
    q1 = df[column].quantile(0.25)                 
    q3 = df[column].quantile(0.75)
    iqr = q3 - q1
    #filtering
    filter = (df[column] >= q1 - 1.5 * iqr) & (df[column] <= q3 + 1.5 * iqr)
    return df.loc[filter]  
    
def sum_per_reactor (df, column):
    #function calculates a sum of values for called column 
    #function gets data frame and name of column and returns
    #sum of data 
    return df.groupby([column]).sum()

def sum_per_material (df, column_1, column_2):
    #funtion calculates a sum of mass value for each material and equipment
    #function gets data frame name of equipment column and name of materials 
    #column, returns data frame 
    #let's get set of materials and empty dict
    materials = list(sorted(set(df[column_2].tolist())))
    result = {}
    #first sort data frame by materials, second by equipment
    #then gather colums to our dict and convert in to data frame
    for material in materials:
        temp = df.loc[df[column_2].isin([material])]
        temp = temp.groupby(column_1).sum()
        result[material] = temp['Масса, кг']
    return pd.DataFrame(result)

def seasonality (df, column_1, column_2):
    materials = sorted(set(df[column_1].tolist()))
    reactors = sorted(set(df[column_2].tolist()))
    weeks = pd.date_range('2020-1-1','2021-1-1', freq='W').strftime("%Y-%m-%w").tolist()
    date = datetime.datetime(2020, 1, 1, 0, 0, 0)
    result = pd.DataFrame(index = reactors, columns = materials) 
    
    for reactor in reactors:
        temp = pd.DataFrame(index = weeks[:52])
        for material in materials: 
            t = []
            for i in range(52):
                start = date + i * relativedelta(weeks =+ 1)
                end = start + relativedelta(weeks =+ 1) 
                m = df[(df['Начало обработки'] >= start) & (df['Начало обработки'] < end) 
                       & (df[column_1] == material)]
                t.append(m['Масса, кг'].mean())
            
            result.loc[reactor, material] = t#.fillna(0)  
    acorr_weeks = pd.DataFrame.from_dict({reactor: [result[reactor][material].autocorr(lag = 1) 
                                for material in materials] for reactor in reactors}, orient = 'Index', columns = materials)
    acorr_months = pd.DataFrame.from_dict({reactor: [result[reactor][material].autocorr(lag = 4) 
                                for material in materials] for reactor in reactors}, orient = 'Index', columns = materials)
    return {'res': result, 'ac_w': acorr_weeks, 'ac_m': acorr_months}
            
def plotting (df, column_1, column_2):
    #function plotting four plots for each reactor
    #function get data frame and two colums: first for sorting by equipment
    #and second for X-axis
    #make a sorted set of names
    reactors = sorted(set(df[column_1].tolist()))
    #set an index
    i = 1
    for reactor in reactors:
        #plot a field of four histograms
        plt.subplot(2, 2, i)
        #prepeare a copy of desired data
        temp = df.loc[df[column_1].isin([reactor])]
        #plotting histogramms with titles
        plt.hist(temp[column_2].tolist())
        plt.title(reactor, fontsize = 7)
        plt.xlabel('Время, мин', fontsize = 7)
        plt.ylabel('Количество загрузок', fontsize = 7)
        #go to next cell on plot
        i += 1
    plt.savefig('./time_destrrib.pdf')    
    return plt.show()     
    
def stat_sig(df, column, level, n1, n2):
    #function defines statistical significance of two random values 
    #by column usung t-test with level of significance
    #in hipothesis of they normal distribution
    #H_0 hypotesis means that two sets have not statistically different
    #function gets dataframe, name of column for analysis, level of significance (%) 
    #and two indexes of sets. returns boolean result 
    #gets desireble rows
    df_1 = df[df['Оборудование'].isin(['Реактор_{x}'.format(x = n1)])][column]
    df_2 = df[df['Оборудование'].isin(['Реактор_{x}'.format(x = n2)])][column]
    #calculate common std variance
    std_1 = df_1.var() 
    std_2 = df_2.var()
    #calculate mean of each random value
    mean_1 = df_1.mean()
    mean_2 = df_2.mean()
    #define and compare levels
    result = abs(mean_1 - mean_2)/((std_1 + std_2) ** .5) < level / 100
    return(result)

#open tables to DataFrames
table_1 = pd.read_excel('./Таблица_1.xlsx', sheet_name='Sheet1')
table_2 = pd.read_excel('./Таблица_2.xlsx', sheet_name='Sheet1')

#make dictionary from table_1 for simple searching in nomenclature
batch_material = dict(zip(table_1['Партия'].tolist(), table_1['Материал'].tolist()))

#try to delete rows with nan
table_2 = table_2.dropna()

#insert empty column with materials
table_2.insert(2, 'Материал', [0 for _ in range(table_2['Партия'].size)])

#insert new material names linked with batch
for batch in table_1['Партия'].tolist():
    table_2['Партия'].isin([batch]).apply(lambda x: batch_material[batch])
    
#plot a mass distribution   
boxplot = table_2.boxplot(column = 'Масса, кг')
plt.savefig('./boxplot.pdf')

#filtering extremal ejections to exclude it from analysis
table = hampel_filter(table_2, 'Масса, кг')

#calculate a total load for reactors
total_per_reactor = sum_per_reactor(table, 'Оборудование')
print('\n Суммарная масса, переработанная в каждом реакторе: ') 
print(total_per_reactor)

#calculate a total load by materials for reactors 
total_per_material_equip = sum_per_material(table, 'Оборудование', 'Материал')
print('\n Масса, переработанная в каждом реакторе, по виду материала: ') 
print(total_per_material_equip)

#insert last column with processing time for each operation and 
#redused to minutes (float type)
table.insert(6, 'Продолжительность', (table['Окончание обработки'] 
            - table['Начало обработки']) / datetime.timedelta(minutes=1))

#mean processing time per reactor
mean_time_per_reactor = table.groupby(['Оборудование']).mean()
mean_time_per_reactor = mean_time_per_reactor['Продолжительность']
print('\n Среднее время обработки партии материала по каждому реактору: ') 
print(mean_time_per_reactor)

#plot histogramms
plot = plotting(table, 'Оборудование', 'Продолжительность')

#table.insert(7, 'Сезонность', [0 for _ in range(table['Партия'].size)])
#season = seasonality(table, 'Материал', 'Оборудование')

#check statistical significance by t-test with significance level 5 
significance = stat_sig(table, 'Продолжительность', 5, 1, 2)

if significance:
    print('\n Среднее время 1 и 2 реакторов не различаются статистически значимо')
    print('Уровень значимости 5%')
else:
    print('\n Среднее время 1 и 2 реакторов различаются статистически значимо')
    print('Уровень значимости 5%')

#Save our results to xlsx in work dir each result to differente list in book
writer = pd.ExcelWriter('./Result.xlsx')
table.to_excel(writer, 'Итоговая таблица')
total_per_reactor.to_excel(writer, 'Масса')
total_per_material_equip.to_excel(writer, 'Масса по материалам')
mean_time_per_reactor.to_excel(writer, 'Среднее время')
writer.save()
