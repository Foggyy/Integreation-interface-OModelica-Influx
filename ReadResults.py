import DyMat
import pandas as pd
import numpy as np
import datetime
from pytz import timezone
from BufClass import Buffer

# Заполнение недостающих значений, если необходимо загрузить несколько полей с разным количеством элементов
def fillingMissingData(res, maxCount):
    for var in res:
        if len(res[var]) != maxCount:
            supMas = []
            while(len(res[var])+len(supMas) != maxCount):
                supMas.append(res[var][-1])
            res[var] = np.concatenate((res[var],supMas))
    return res


# Выгрузка данных из .mat файла и сохранение в .csv
def fromMatToCsv():  
    myfile = DyMat.DyMatFile(Buffer.modelName + ".mat")
    data = myfile.names()
    varNames = list()                                                           # Список всех параметров модели
    for varName in data:
        varNames.append(varName)
    res = dict()
    maxCount = -1                                                                # Максимальное кол-во элементов, которое должно быть в csv файле
                                                                                 # Определяется в цикле по выбранным полям
    res['simulationTime'] = myfile.abscissa(varNames[0], valuesOnly=True)        # Время симуляции (если будет выдавать ошибку, поменять индекс varNames)

    for varName in varNames:                                                     # Заполнение словаря данными
        if Buffer.allData == True:
            res[varName] = myfile.data(varName)
            if len(res[varName]) > maxCount:
                maxCount = len(res[varName])
        else:
            if varName in Buffer.fields:
                res[varName] = myfile.data(varName)   
                if len(res[varName]) > maxCount:
                    maxCount = len(res[varName])

    if Buffer.allData == True:                                                  # Заполнение недостающих значений
        res = fillingMissingData(res, maxCount)
                
    pd.DataFrame(res).to_csv(Buffer.modelName + '.csv', index=False, sep=';')    # Сохранение в файл .csv с названием модели

if __name__ == '__main__':
  fromMatToCsv()