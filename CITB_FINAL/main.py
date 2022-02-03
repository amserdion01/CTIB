import os

import CITB_API

from MES.MES import MES

from SHOPFLOOR.factory import Factory

def short_unit_tests():
    CITB_API.writeToFile('Orders/10001', {"UID": "10001", "Products": ["boxhub", "cutter"], "Name": "Rosalim Sorin Ionut", "Adress": "Str. Cimitirului nr. 1, Selimbar, Sibiu"})
    CITB_API.writeToFile('Orders/10002', {"UID": "10002", "Products": ["boxhub", "boiler", "cutter"], "Name": "Ianchis Bogdan","Adress": "Str. Brutariei nr. 1, Zalau, Salaj"})
def long_unit_tests():
    CITB_API.writeToFile('Orders/10001',
                {"UID": "10003", "Products": ["boxhub", "cutter", "peeler"], "Name": "Rosalim Sorin Ionut",
                 "Adress": "Str. Cimitirului nr. 1, Selimbar, Sibiu"})
    CITB_API.writeToFile('Orders/10002',
                {"UID": "10004", "Products": ["boxhub", "peeler"], "Name": "Ianchis Bogdan",
                 "Adress": "Str. Brutariei nr. 3, Zalau, Salaj"})
    CITB_API.writeToFile('Orders/10003',
                         {"UID": "10003", "Products": ["boxhub", "fryer", "peeler"], "Name": "Andoni Laurentiu",
                          "Adress": "Str. Bunavointa nr. 5, Constanta, Constanta"})
    CITB_API.writeToFile('Orders/10004',
                         {"UID": "10004", "Products": ["boxhub", "peeler", "boiler"], "Name": "Gurita Marius",
                          "Adress": "Str. Cimitirului nr. 1, Simian, Drobeta Turnu Severin"})
    CITB_API.writeToFile('Orders/10005',
                         {"UID": "10005", "Products": ["boxhub", "fryer", "peeler"], "Name": "Marian Alexandra",
                          "Adress": "Str. Strazilor nr. 7, Baia Mare, Maramures"})

short_unit_tests()

MES = MES()
MES.ProcessingOrders()

Factory = Factory()
Factory.start_manufacturing()






