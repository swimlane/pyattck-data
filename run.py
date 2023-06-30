from generate_data.generatenistdata import GenerateNISTData
from generate_data.pyattckdata import PyattckData

from data_collector import Collector

Collector().collect()

pydata = PyattckData()
pydata.save()
pydata.merge()
GenerateNISTData().save()
