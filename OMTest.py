from OMPython import OMCSessionZMQ
from OMPython import ModelicaSystem
from BufClass import Buffer
import ReadResults
import db

def modelSimulation():
  omc = OMCSessionZMQ()
  mod = ModelicaSystem(Buffer.modelPath,Buffer.modelName)
  mod.buildModel()
  mod.simulate(resultfile=Buffer.modelName + ".mat")



if __name__ == '__main__':
  modelSimulation()
  ReadResults.fromMatToCsv()
  db.loadDataToDb()

