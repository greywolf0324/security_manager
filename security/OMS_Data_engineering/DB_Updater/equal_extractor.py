import pandas as pd
from pathlib import Path
import math
import numpy as np
from google.oauth2 import service_account
import gspread
from ..sheet_reader import frame_converter
import json
from ...models import OMS_Customers, OMS_Inventory_List, Ocustomer_fields, Oinventory_fields
from ..util import modelto_dataframe

class Extractor:
    def __init__(self) -> None:
        # self.OMS_Customers = None
        # OMS_inventorylist = None
        self.length = 0
        self.SKU_list = [
            "Buc-ee's",
            "Family Dollar",
            "Gabe's",
            "Walmart US",
            "Big Lots Stores", 
            "TARGET",
            "Five Below",
            "Lekia",
            "Meijers",
            "MICHAELS",
            'Fred Meyer',
            "buy buy BABY",
            "BJ's Wholesale Club. Inc"
        ]


    def extractor(self, customer_name, matching_res):
        OMS_customers = modelto_dataframe(OMS_Customers, Ocustomer_fields)
        OMS_inventorylist = modelto_dataframe(OMS_Inventory_List, Oinventory_fields)
        # self.OMS_Customers = frame_converter(spreadsheet.get_worksheet(0).get_all_records())
        # OMS_inventorylist = frame_converter(spreadsheet.get_worksheet(1).get_all_records())
        
        equal_inventorylist = []

        if customer_name == "Pepco":
            if matching_res[0]["Currency"][0] == "CNY":
                customer_name = customer_name + " - RMB"
            
            else:
                customer_name = customer_name + " - " + matching_res[0]["Currency"][0]
        
        elif customer_name == "THE WORKS":
            if matching_res[0]["Currency"][0] == "USD":
                customer_name = customer_name + " - USD"
            
            else:
                customer_name = customer_name + "-GBP"
        
        elif customer_name == "Walmart":
            if matching_res[0]["Currency"][0] == "US Dollar":
                customer_name = customer_name + " US"

        payment_term = list(OMS_customers[OMS_customers["Name"] == customer_name]["PaymentTerm"])[0]
        
        for i, content in enumerate(matching_res):
            self.length = len(content.keys())

            temp_inventory = []
            for k, product in enumerate(list(content["Vendor Style"])[1:]):
                if customer_name not in self.SKU_list:
                    # if str(content["Buyers Catalog or Stock Keeping #"][k + 1]) in list(OMS_inventorylist["SupplierProductCode"]):
                    #     temp_inventory.append(list(OMS_inventorylist[OMS_inventorylist["SupplierProductCode"] == str(content["Buyers Catalog or Stock Keeping #"][k + 1])]["ProductCode"]))
                    # else:
                    temp_inventory.append(list(OMS_inventorylist["ProductCode"]))
                    # continue
                else:
                    temp = []
                    for product_ in list(OMS_inventorylist["ProductCode"]):
                        if type(product) != str: product = str(int(float(product)))
                        if type(product_) != str: product_ = str(product_)
                        if product in product_:
                            temp.append(product_)
                    
                    temp_inventory.append(temp)

            equal_inventorylist.append(temp_inventory)

        return {
            "OMS_Inventory_List": equal_inventorylist,
            "OMS_Payment_term": payment_term
        }