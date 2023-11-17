import pandas as pd
from pathlib import Path
import math
import numpy as np
from google.oauth2 import service_account
import gspread
from ..sheet_reader import frame_converter
import json

class Extractor:
    def __init__(self) -> None:
        # f = open(Path(__file__).resolve().parent.parent / "config/django-connection-1008-5f931d8f4038.json")
        # google_json = json.load(f)
        # credentials = service_account.Credentials.from_service_account_info(google_json)
        # scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
        # creds_with_scope = credentials.with_scopes(scope)
        # client = gspread.authorize(creds_with_scope)
        # spreadsheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1CDnIivm8hatRQjG7nvbMxG-AuP19T-W2bNAhbFwEuE0")
        
        # self.OMS_AdditionalUOM = pd.read_csv(Path(__file__).resolve().parent.parent / "config/OMS_DB/OMS_AdditionalUOM.csv")
        # self.OMS_AdditionalUOM = frame_converter(spreadsheet.get_worksheet(3).get_all_records())

        # self.OMS_Customers = pd.read_csv(Path(__file__).resolve().parent.parent / "config/OMS_DB/OMS_Customers.csv", index_col = False)
        # self.OMS_Customers = frame_converter(spreadsheet.get_worksheet(0).get_all_records())
        self.OMS_Customers = None

        # self.OMS_InventoryList = pd.read_csv(Path(__file__).resolve().parent.parent / "config/OMS_DB/OMS_InventoryList.csv")
        # self.OMS_InventoryList = frame_converter(spreadsheet.get_worksheet(1).get_all_records())
        self.OMS_InventoryList = None

        # self.OMS_PaymentTerm = pd.read_csv(Path(__file__).resolve().parent.parent / "config/OMS_DB/OMS_PaymentTerm.csv")
        # self.OMS_PaymentTerm = frame_converter(spreadsheet.get_worksheet(2).get_all_records())

        # self.OMS_UoM = pd.read_csv(Path(__file__).resolve().parent.parent / "config/OMS_DB/OMS_UOM.csv")
        # self.OMS_UoM = frame_converter(spreadsheet.get_worksheet(4).get_all_records())
        self.length = 0
        self.vendor_customer = [
            "Buc-ee's",
            "Dollarama",
            "Family Dollar",
            "Gabe's",
            "Walmart US",
            "Big Lots Stores", 
            "TARGET",
            "Five Below",
            "Lekia",
            "Meijers",
            "MICHAELS",
            'Fred Meyer'
        ]


    def extractor(self, matching_res, customer_name, spreadsheet):
        self.OMS_Customers = frame_converter(spreadsheet.get_worksheet(0).get_all_records())
        self.OMS_InventoryList = frame_converter(spreadsheet.get_worksheet(1).get_all_records())
        
        
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
            # print(matching_res[0]["Currency"], "********")
            if matching_res[0]["Currency"][0] == "US Dollar":
                customer_name = customer_name + " US"
        # print(customer_name, "Walmart US")
        payment_term = list(self.OMS_Customers[self.OMS_Customers["Name"] == customer_name]["PaymentTerm"])[0]
        
        for content in matching_res:
            self.length = len(content.keys())

            temp_inventory = []

            for product in list(content["Vendor Style"])[1:]:
                if type(product) != str: product = str(product)
                if customer_name not in self.vendor_customer:
                    temp_inventory.append(list(self.OMS_InventoryList["ProductCode"]))
                    continue
                else:
                    temp = []
                    for product_ in list(self.OMS_InventoryList["ProductCode"]):
                        if type(product_) != str: product_ = str(product_)
                        if product in product_:
                            temp.append(product_)
                    
                temp_inventory.append(temp)

            # print(len(temp_inventory))

            equal_inventorylist.append(temp_inventory)

        return {
            "OMS_Inventory_List": equal_inventorylist,
            "OMS_Payment_term": payment_term
        }