class Buffer:
    dbName = "ModelMinVenTest"                           # Название базы данных
    createDB = True                                 # Создать базу данных в инфлюксе
    measurementName = "SimulationData"                       # Название измерения
    modelName = "MinVen6"                                 # Название модели, без расширения ".mo"
    modelPath = "D:/Programming/Python/OMInterface/Console/models/MinVen6.mo"       # Путь до директории модели (с файлом модели)
    fields = ['simulationTime','horshaft1.mediums[1].T', 'shaft1.mediums[1].T', 'der(shaft1.mediums[1].T)']   # Название параметров модели, данные из которых необходимо загрузить
                                                     # Для вывода времени симуляции ввести "simulationTime"
    allData = False                                  # True - загрузить все данные из модели (fields - не учитывается)
                                                     # False - загрузить выбранные данные (Fields - учитывается)
    tags = ['well']                                  # Теги (пока отключены)
    host = "localhost"                               # Адрес для подключения к InfluxDB
    port = 8086                                      # Порт для подключения к InfluxDB
