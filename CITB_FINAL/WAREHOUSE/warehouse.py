import json
import os
import CITB_API
class Warehouse:
    def order_materials(self):
        # This function helps the Warehouse communicate with the Shopfloor subsystem.
        # Here we have the requested materials file which starts with 0 if the request is not handled yet
        # and with 1 if the request is already handled but by mistake is is the request_materials file
        # It also updates 0 to 1 if the request was handled and sent to the Shopfloor subsystem
        ok = 0
        requested_materials_dict = json.loads(CITB_API.interogateFile("requests/requested_materials")['content'])
        if requested_materials_dict['status'] == 0:
            ok = 1
            self.verify_stock(requested_materials_dict)

        # self.verify_stock(requested_materials_dict)
        #
        if ok == 0:
            print("We don't have a request")
        else:
            self.delivered_materials()
            requested_materials_dict['status'] = 1
            CITB_API.writeToFile("requests/requested_materials", requested_materials_dict)


    def verify_stock(self, request: dict):
        # this function will verify if the products requested are in our stock, and if one value is less than 0 it will
        # supply the stock
        # it will also decrease the warehouse stock because we deliver materials to the Shopfloor
        # if os.path.basename(os.getcwd()) != "WAREHOUSE":
        #     os.chdir('WAREHOUSE')
        # with open("my_materials.txt", 'r') as my_materials_file:
        #     contents = my_materials_file.read()
        #     my_materials_dict = json.loads(contents)
        my_materials_dict = json.loads(CITB_API.interogateFile("WAREHOUSE/my_materials")['content'])
        for key in request:
            if key in my_materials_dict.keys():
                my_materials_dict[key] -= request[key]
                if my_materials_dict[key] < 0:
                    temp = my_materials_dict[key]
                    my_materials_dict[key] = self.supplier(key)  # suppling the missing material
                    my_materials_dict[key] += temp  # adding because we have to substract a negative number
        self.update_stock(my_materials_dict)

    def supplier(self, material_missing):
        # this function will restock the given missing materials with 500 raw materials of that kind

        my_materials_dict = json.loads(CITB_API.interogateFile('WAREHOUSE/my_materials')['content'])
        my_materials_dict[material_missing] = 0
        my_materials_dict[material_missing] += 500
        return my_materials_dict[material_missing]

    def update_stock(self, stock: dict):
        # this function will update the stock with the given new dictionary
        CITB_API.writeToFile("WAREHOUSE/my_materials", stock)

    def update_products_stock(self):
        my_products_dict = json.loads(CITB_API.interogateFile("WAREHOUSE/my_products")['content'])
        shopfloor_dict = json.loads(CITB_API.interogateFile("SHOPFLOOR/stock_product")['content'])

        for product in shopfloor_dict:
            my_products_dict[product] += shopfloor_dict[product]
            shopfloor_dict[product] = 0

        CITB_API.writeToFile("WAREHOUSE/my_products", my_products_dict)
        CITB_API.writeToFile("SHOPFLOOR/stock_product", shopfloor_dict)

    def delivered_materials(self):
        # the delivery to the Shopfloor was complete and successful
        print("Materials delivered!")

    def get_warehouse_stock(self):
        # this function will print the warehouse stock( materials, products)

        my_materials_dict = json.loads(CITB_API.interogateFile('WAREHOUSE/my_materials')['content'])

        print(f"The available materials in the Warehouse are: {my_materials_dict}")


        my_products_dict = json.loads(CITB_API.interogateFile('WAREHOUSE/my_products')['content'])

        print(f"The available products in the Warehouse are: {my_products_dict}")
