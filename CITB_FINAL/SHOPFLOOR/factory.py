import json
import os
import glob
import CITB_API

class Factory:
    def __init__(self):
        self.update_request()
        from WAREHOUSE.warehouse import Warehouse
        self.warehouse = Warehouse()

    def start_manufacturing(self):
        self.get_datasheets()
        self.update_stock()

    def get_datasheets(self):
        print("Currently loading datasheets...")
        ok = 0
        files = CITB_API.getSubdb('Datasheet')
        total = ""
        for item in files:
            if os.path.dirname(item['path']) == "Datasheet":
                ok=1
                total += item['content']
                total += '\n'
                CITB_API.killFile(item['path'])
        if ok == 1:
            print("Datasheets fully loaded.")
            self.get_information(total)

    def update_stock(self):
        print("updating stock...")
        stock = self.get_stock_materials()
        request = {}
        for material in stock:
            if stock[material] < 100:
                request[material] = 100 - stock[material]
        self.make_request(request)
        self.get_materials()
        # ~ self.update_materials(stock)

    def get_information(self, datasheets: str):
        x = datasheets
        x = x.replace("'", '"')
        data = x.rsplit("}")
        for i in data:
            i = i + "}"
            if "UID" in i:
                dict = json.loads(i)
                print(f"Currently processing an item from order with UID: {dict['UID']}")
                needed_materials = self.get_needed_materials(dict["materials"])
                stock = self.get_stock_materials()
                request = {}
                for material in needed_materials:
                    if stock[material] < needed_materials[material] :
                        request[material] = 100 - stock[material] + needed_materials[material]
                    stock[material] -= needed_materials[material]
                self.make_request(request)
                self.get_materials()
                # ~ self.update_materials(stock)
                steps = dict['steps']
                steps = steps.split(",")
                product = steps[-1]
                product = product.replace("assembly ", "")
                product = product.replace(" ", "")
                dict = json.loads(CITB_API.interogateFile("SHOPFLOOR/stock_product")['content'])
                dict[product] +=1
                CITB_API.writeToFile("SHOPFLOOR/stock_product", dict)
                self.warehouse.update_products_stock()


    def get_materials(self):
        data = CITB_API.interogateFile('requests/requested_materials')
        if data['content'] != "{}":
            data = json.loads(data['content'])
            if data['status'] == 1:
                stock = self.get_stock_materials()
                for material in data:
                    if material != 'status':
                        stock[material] += data[material]
                self.update_materials(stock)
                self.update_request()

    def get_needed_materials(self, materials):
        result = {}
        x = []
        y = []
        for i in materials:
            i = i.split(" ")
            x.append(int(i[0]))
            if len(i) == 2:
                y.append(i[1])
            else:
                k = i[1] + " " + i[2]
                y.append(k)
        for i, j in zip(x, y):
            result[j] = i
        return result


    def get_stock_materials(self):
        return json.loads(CITB_API.interogateFile("SHOPFLOOR/stock_materials")['content'])
    def update_materials(self,stock):
        CITB_API.writeToFile('SHOPFLOOR/stock_materials',stock)
    def update_request(self):
        CITB_API.writeToFile("requests/requested_materials", {'status': 2})
    def make_request(self, request):
        request['status'] = 0
        CITB_API.writeToFile("requests/requested_materials", request)
        if len(request) > 1:
            print("Requesting materials...")
            self.warehouse.order_materials()


