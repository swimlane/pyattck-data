from generate_data.generatenistdata import GenerateNISTData
from generate_data.pyattckdata import PyattckData

pydata = PyattckData()
pydata.save()
pydata.merge()
GenerateNISTData().save()
