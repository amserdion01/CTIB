import os
import json
import glob
import CITB_API


class MES:
    def GetOrders(self):
        files = CITB_API.getSubdb('Orders')
        file_searcher = []
        for item in files:
            file_searcher.append(item['path'])
        return file_searcher
    def SendDatasheet_ANALYTICS(self):
        print("Sending Datasheet to Analytics...")

    def AskForItem(self, item):
        print(f"Asking for stock for {item}")
        return 1

    def SendDatasheet_SHOPFLOOR(self):
        print("Sending Datasheet to ShopFloor...")

    def __init__(self):
        self.orders = self.GetOrders()
        self.list_of_orders = []
        self.uncraftable = ['metal', 'heater', 'motor', 'copper wire',
                            'cpu', 'board', 'LCD', 'pneumatical pump',
                            'small blade', 'handle', 'blade']
    def update(self):
        self.orders = self.GetOrders()

    def ProcessingOrders(self):
        for item in self.orders:
            if os.path.basename(item)[0] != 'x':
                data = json.loads(CITB_API.interogateFile(item)['content'])
                print(f"Processing order with ID: {data['UID']}...")
                self.list_of_orders.append(data)
                self.GetProductFromOrder(data)
                CITB_API.killFile(item)


    def GetProductFromOrder(self, data: dict):
        self.index = 0
        for product in data['Products']:
            if self.GetStock(product) != 0:
                self.GenerateDatasheet(self.index, data['UID'], product)

    def GenerateDatasheet(self, index, uid, product):
        print(f"Generating Datasheet for product: {product} in order {uid}...")

        datasheet = CITB_API.getSubdb('datasheet')
        for file in datasheet:
            if os.path.basename(file['path']) == product:
                data = {"UID": f'{uid}', "steps": '', 'materials': []}
                list_of_steps = file['content'].replace('"','').split(',')
                for i in range(len(list_of_steps)):
                    if list_of_steps[i][0] == ' ':
                        list_of_steps[i] = list_of_steps[i][1:]
                self.index += 1
                for part in list_of_steps:
                    json_data = json.loads(CITB_API.interogateFile('datasheet/component')['content'])
                    item = part.split(' ')
                    if len(item) == 2 and item[1] not in self.uncraftable:
                        for i in json_data[f"{item[1]}"]:
                            data['materials'].append(i)
                    elif len(item) == 3:
                        data['steps'] += f"do {item[1]} {item[2]}, "
                        for i in json_data[f"{item[1]} {item[2]}"]:
                            data['materials'].append(i)
                    elif len(item) == 2 and item[1] in self.uncraftable:
                        data['materials'].append(f"{item[0]} {item[1]}")
                data['steps'] += f'assembly {product}'
                CITB_API.writeToFile(f"Datasheet/ds_{uid}_{self.index}", data)
                print("Datasheet generated successfully.")


    def GetStock(self, item):
        return self.AskForItem(item)