from influxdb import InfluxDBClient
import csv
import os
from BufClass import Buffer
import time

# Проверка значения на вещественное
def isfloat(value):
    try:
        float(value)
        return True
    except:
        return False

# Загрузка всех данных из файла
def allData(columnsNames,row):
    fieldsValues = {}
    for value in columnsNames:
        valueBuf = 0
        if value in row:
            valueBuf = float(row[value]) if isfloat(row[value]) else row[value]
        fieldsValues[value] = valueBuf
    return fieldsValues

# Загрузка выбранных данных из файла
def selectedData(columnsNames,row):
    fieldsValues = {}                                     # Значения параметров в строке
    for value in columnsNames:
        valueBuf = 0
        if value in row and value in Buffer.fields:
            valueBuf = float(row[value]) if isfloat(row[value]) else row[value]
            fieldsValues[value] = valueBuf
    return fieldsValues

# Загрузка данных в базу
def loadDataToDb():
    #Создание базы данных и выгрузка данных из csv файла
    client = InfluxDBClient(host=Buffer.host, port=Buffer.port)
    if Buffer.createDB == True:
        client.create_database(Buffer.dbName)                               # Создание базы данных, если ее нет
    client.switch_database(Buffer.dbName)                                # Смена базы данных
    filePath = os.path.abspath(os.curdir) + "\\" + Buffer.modelName + ".csv"    #Путь до csv файла
    with open(filePath) as fp:                                           # Чтение файла
        reader = csv.DictReader(fp, delimiter=";")                       # ; - разделитель данных в csv
        columnsNames = reader.fieldnames                                 # Наименования параметров
        data_read = [row for row in reader]                              # Массив содержащий все данные из файла

    # Работа с данными

    dataToWrite = []                                                      # Данные для записи в массив
    count = 0
    for row in data_read:

        #tagsValues = {}                                                   # Массив тегов
        #for tag in Buffer.tags:                                           
            #value = 'ID0100'                                              # Значение тегов
            #if tag in row:
                #v = row[t]
                #pass
            #tagsValues[tag] = value
        
        fieldsValues = {}                                                   # Значения параметров в строке

                                                  # Проверка режима вывода данных
        fieldsValues = allData(columnsNames,row)           

        timestamp = time.time()                                             # Временная метка
        newTimestamp = round(timestamp * 10000)
        timestamp = newTimestamp      
        timestamp = timestamp + count
        
        data = {"measurement": Buffer.measurementName, "time": timestamp, "fields": fieldsValues}   # Запрос для загрузки в базу в json формате
        dataToWrite.append(data)
        count = count + 1

    # Отправка запроса в базу данных и вывод информации

    if len(dataToWrite) > 0:
        print("Количество данных в файле: ",len(data_read))
        print("Количество загружаемых данных: ",len(dataToWrite))
        ok = client.write_points(dataToWrite)
        if ok == True:
            print("Данные успешно загружены")
        else:
            print("Произошла ошибка во время загрузки данных")
            exit(1)    

if __name__ == '__main__':
  loadDataToDb()

