from pyattck_data import GenerateNISTData, PyattckData

pydata = PyattckData()
pydata.save()
pydata.merge()
GenerateNISTData().save()
