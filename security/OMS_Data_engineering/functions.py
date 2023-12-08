import datetime
import uuid
from .OCR.parse import BUCEE_Parsing, PEPCO_Parsing, PEPCO_Add_Parsing, Walgreens_Parsing, Dollarama_Parsing, Family_Dollar_Parsing, Gabes_Parsing, TEDI_Parsing, Walmart_Parsing, Ollies_Parsing, ORBICO_Parsing, EXCEL_Parsing, CVS_Parsing, GiantTiger_Parsing, HOBBYlobby_Parsing, Lekia_Parsing
from .Original_SalesImport_Generation.matching import PO_Match_BUCEE, PO_Match_PEPCO, PO_Match_PEPCO_Add, PO_Match_Walgreens, PO_Match_Dollarama, PO_Match_Family_Dollar, PO_Match_Gabes, PO_Match_TEDI, PO_Match_Walmart, PO_Match_Ollies, PO_Match_ORBICO, PO_Match_EXCEL, PO_Match_CVS, PO_Match_GiantTiger, PO_Match_HOBBYlobby, PO_Match_Lekia
from .DB_Updater.equal_extractor import Extractor
from .DB_Updater.customers_updater import customer_fields_updater
from .DB_Updater.auto_SKU import AutoDB
from .SalesImport_Generation.Integrator import Integrate_All
from .SalesImport_Generation.SalesImport_updater import SalesImport_Updater
from csv import DictWriter
import json
import pandas as pd
import csv
from openpyxl import load_workbook
import xlsxwriter
import os
from pathlib import Path
from os.path import exists
import re
from decimal import Decimal
from google.oauth2 import service_account
import gspread
from .sheet_reader import frame_converter

class SalesImport_Generator:
    def __init__(self) -> None:
        self.matching_dic = {
            "Buc-ee's": {
                "parser": "BUCEE_Parsing", 
                "matcher": "PO_Match_BUCEE",
            },
            "Pepco": {
                "parser": "PEPCO_Parsing",
                "matcher": "PO_Match_PEPCO",
            },
            "Poundland": {
                "parser": "PEPCO_Add_Parsing",
                "matcher": "PO_Match_PEPCO_Add",
            },
            "Walgreens": {
                "parser": "EXCEL_Parsing",
                "matcher": "PO_Match_EXCEL",
            },
            "Dollarama": {
                "parser": "Dollarama_Parsing",
                "matcher": "PO_Match_Dollarama",
            },
            "Family Dollar": {
                "parser": "Family_Dollar_Parsing",
                "matcher": "PO_Match_Family_Dollar"
            },
            "Gabe's": {
                "parser": "Gabes_Parsing",
                "matcher": "PO_Match_Gabes" 
            },
            "TEDI": {
                "parser": "TEDI_Parsing",
                "matcher": "PO_Match_TEDI",
            },
            # "THE WORKS": {
            #     "parser": "THE_WORKS_Parsing",
            #     "matcher": "PO_Match_THE_WORKS"
            # },
            "Walmart": {
                "parser": "Walmart_Parsing",
                "matcher": "PO_Match_Walmart"
            },
            "Ollies": {
                "parser": "Ollies_Parsing",
                "matcher": "PO_Match_Ollies",
            },
            "ORBICO": {
                "parser": "ORBICO_Parsing",
                "matcher": "PO_Match_ORBICO"
            },
            "Big Lots Stores": {
                "parser": "EXCEL_Parsing",
                "matcher": "PO_Match_EXCEL"
            },
            "TARGET": {
                "parser": "EXCEL_Parsing",
                "matcher": "PO_Match_EXCEL"
            },
            "CVS": {
                "parser": "CVS_Parsing",
                "matcher": "PO_Match_CVS"
            },
            "Five Below": {
                "parser": "EXCEL_Parsing",
                "matcher": "PO_Match_EXCEL"
            },
            "Giant Tiger": {
                "parser": "GiantTiger_Parsing",
                "matcher": "PO_Match_GiantTiger"
            },
            "Hobby Lobby": {
                "parser": "HOBBYlobby_Parsing",
                "matcher": "PO_Match_HOBBYlobby"
            },
            "Lekia": {
                "parser": "Lekia_Parsing",
                "matcher": "PO_Match_Lekia"
            },
            "Meijers": {
                "parser": "EXCEL_Parsing",
                "matcher": "PO_Match_EXCEL"
            },
            "MICHAELS": {
                "parser": "EXCEL_Parsing",
                "matcher": "PO_Match_EXCEL"
            },
            "Fred Meyer": {
                "parser": "EXCEL_Parsing",
                "matcher": "PO_Match_EXCEL"
            },
            "Tar Heel Trading": {
                "parser": "EXCEL_Parsing",
                "matcher": "PO_Match_EXCEL"
            }
        }

        self.customer_name = ""
        self.auto_dic = []
        self.matching_res = []
        self.SKU_list = ["Buc-ee's", "Dollarama", "Family Dollar", "Gabe's", "Walmart", "Big Lots Stores", "TARGET", "Five Below", "Lekia", "Meijers", "MICHAELS", "Fred Meyer"]
        self.customer_SKU_list = ["Pepco", "Poundland", "Walgreens", "Ollies", "CVS", "Giant Tiger"]

        self.top_lis = ["PO Number", "PO Date", "Dept #", "Retailers PO", "Delivery Dates", "Ship Dates", "Ship To Location", "PO purpose", "PO Type", "Vendor #", "Payment Terms %", "Payment Terms Disc Days Due", "Payment Terms Desc", "Contact Phone", "Ship To Name", "Ship To Address 1", "Ship To City", "Ship To State", "Ship to Zip", "Bill To Name", "Bill To Address 1", "Bill To City", "Bill To Zip", "Bill To Country", "PO Total Amount", "PO Total Weight ", "PO Total UOM "]
        self.all_mid_lis = ["PO Number", "PO Line #", "Qty Ordered", "Unit of Measure", "Unit Price", "Buyers Catalog or Stock Keeping #", "Product/Item Description", "Pack Size", "Pack Size UOM", "Number of Inner Packs", "GTIN"]
        self.header_keys = {
            "PO#": "PO Number", 
            "PO Date": "PO Date", 
            "Dept": "Dept #", 
            "Ship Date": "Ship Dates", 
            "Cancel Date": "Cancel Date", 
            "Payment Terms": "Payment Terms Disc Days Due",
            "PO Total": ""
        } # CustomerName exists
        self.item_keys = {
            "Buyers Catalog or Stock Keeping #": "Buyers Catalog or Stock Keeping #",
            "UPC": "UPC/EAN", 
            "Vendor Style": "Vendor Style", 
            "Retail Price": "Retail Price",  
            "Unit Of Measure": "Unit of Measure", 
            "Number of Pcs per Case Pack": "Pack Size UOM",
            "Quantity Ordered": "Qty Ordered",
            "Total Case Pack Qty": "",
            "Unit Price": "Unit Price", 
            "Pack Size": "", 
            "Number of Pcs per Inner Pack": "Number of Pcs per Inner Pack",
            "Number of Inner Packs": "Number of Inner Packs",  
            "Price Total Amount": ""
        }
        self.input_item_keys = ["Buyers Catalog or Stock Keeping #", "UPC", "Vendor Style", "Retail Price", "Unit Of Measure", "Unit Price", "Quantity Ordered", "Total Case Pack Qty", "Pack Size", "Number of Pcs per Case Pack", "Number of Pcs per Inner Pack", "Number of Inner Packs", "Price Total Amount"]
        
        # self.spreadsheet = None
        # self.inventory_matching = None
        
        # self.inventory_matching = pd.read_csv(Path(__file__).resolve().parent / "config/OMS_DB/OMS_InventoryList.csv", index_col = False)
        f = open(Path(__file__).resolve().parent / "config/django-connection-1008-5f931d8f4038.json")
        google_json = json.load(f)
        credentials = service_account.Credentials.from_service_account_info(google_json)
        scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
        creds_with_scope = credentials.with_scopes(scope)
        client = gspread.authorize(creds_with_scope)
        self.spreadsheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1CDnIivm8hatRQjG7nvbMxG-AuP19T-W2bNAhbFwEuE0")
        self.customers = frame_converter(self.spreadsheet.get_worksheet(0).get_all_records())
        self.inventory_matching = frame_converter(self.spreadsheet.get_worksheet(1).get_all_records())
        self.stocklocations = frame_converter(self.spreadsheet.get_worksheet(5).get_all_records())
        self.filenames = []
        # self.filename = None
        # self.path = None

    def str_converter(self, input):
        temp = []
        for item in list(input):
            temp.append(str(item))

        return temp
    
    def auto_matching_DB_viewer(self, customer_name):
        if exists(Path(__file__).resolve().parent / f"config/AutoFill_DB/{customer_name}.csv"):
            
            auto_df = pd.read_csv(Path(__file__).resolve().parent / f"config/AutoFill_DB/{customer_name}.csv", index_col = False)
            temp = []
            for item in auto_df["PO"]:
                if type(item) == float:
                    temp.append(int(item))
                else:
                    temp.append(item)
            UOM_options = ["Case", "Each"]
            location_options = list(self.stocklocations["Locations"])
            vendor_options = {}
            if customer_name in self.SKU_list:
                for sku in auto_df["PO"]:
                    temp = []
                    for item in self.inventory_matching["ProductCode"]:
                        if str(sku) in item:
                            temp.append(item)
                    vendor_options.update({
                        str(sku): temp
                    })
            else:
                for sku in auto_df["PO"]:
                    vendor_options.update({
                        str(sku): list(self.inventory_matching["ProductCode"])
                    })
            print("________________________")
            target = self.str_converter(auto_df["Vendor Style from OMS_equal"])
            print("========================")
            # print({"PO": list(auto_df["PO"]), "UOM": list(auto_df["Unit of Measure"]), "LOCATION": list(auto_df["StockLocation"]), "TARGET": list(auto_df["Vendor Style from OMS_equal"])})
            return {"PO": list(auto_df["PO"]), "UOM": list(auto_df["Unit of Measure"]), "LOCATION": list(auto_df["StockLocation"]), "TARGET": target, "UOM_options": UOM_options, "location_options": location_options, "vendor_options": vendor_options}
        
        else: 
            return "non-exists"
        
    def auto_matching_DB_changer(self, customer_name, db):
        print("updating vendor style matching DB...")
        # print(customer_name)
        # print(db)
        # print(Path(__file__).resolve().parent / f"config/AutoFill_DB/{customer_name}.csv")
        pd.DataFrame(db[0]).to_csv(Path(__file__).resolve().parent / f"config/AutoFill_DB/{customer_name}.csv", index = False)

    def uploadFile(self, data):
        self.paths = []
        
        for file in data:
            current_datetime = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
            random_string = str(uuid.uuid4().hex)
            filename = f'{current_datetime}_{random_string}'
            self.filenames.append(filename)
            extension = file.name.split(".")[-1]
            path = Path(__file__).resolve().parent.parent.parent / f'process/inputs/{filename}.{extension}'
            self.paths.append(path)
        
            with open(path, 'wb') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)

        # return [self.paths, self.filename]
    
    def parseUpload(self, data, customer_name = None, currency = None):
        print("==============================================================================================================")
        print("CustomerFields Updating...")
        customer_fields_updater()

        self.customer_name = customer_name
        # customer_name = "Buc-ee's"
        # paths = []
        # for file in data:
        self.uploadFile(data)
        paths = self.paths
            # paths.append(self.path)

        # OCR: PDF parsing
        print("==============================================================================================================")
        print("On PDF parsing...")
        parser = eval(self.matching_dic[customer_name]["parser"])(customer_name)
        PO_res = parser.PO_parser(paths, currency)

        # print(PO_res)
        # Data_Integration : Generate SalesImport_Original
        print("==============================================================================================================")
        print("On Match Operating...")
        matcher = eval(self.matching_dic[customer_name]["matcher"])()
        matching_res = matcher.match_final(PO_res)
        self.matching_res = matching_res
        
        # print(len(list(matching_res[0].keys())))
        # print(matching_res[0])
        # # Extract equal OMS
        print("==============================================================================================================")
        print("tracking equal things...")
        extract = Extractor()
        OMS_equal = extract.extractor(matching_res, customer_name, self.spreadsheet)

        self.auto_dic = AutoDB().DB_tester(customer_name, matching_res)

        print("==============================================================================================================")
        print("Displaying...")
        # print(self.auto_dic)
        # print(OMS_equal)
        if (self.customer_name == "Pepco" or self.customer_name == "Poundland") and matching_res[0]["Currency"][0] == "CNY":
                self.customer_name = self.customer_name + " - RMB"

        else:
            if self.customer_name == "Pepco":
                self.customer_name = self.customer_name + " - " + matching_res[0]["Currency"][0]
            
            elif self.customer_name == "Walmart":
                if matching_res[0]["Currency"][0] == "US Dollar":
                    self.customer_name = self.customer_name + " US"
        
        field_names = [
            'PO Number',
            'Release Number',
            'PO Date',
            'Dept #',
            'Retailers PO',
            'Requested Delivery Date',
            'Delivery Dates',
            'Ship Dates',
            'Cancel Date',
            'Carrier',
            'Carrier Details',
            'Ship To Location',
            'PO Line #',
            'Qty Ordered',
            'Unit of Measure',
            'Unit Price',
            'Buyers Catalog or Stock Keeping #',
            'UPC/EAN',
            'Vendor Style',
            'Retail Price',
            'Product/Item Description',
            'Color',
            'Size',
            'Pack Size',
            'Pack Size UOM',
            'Number of Inner Packs',
            'Number of Pcs per Inner Pack',
            'Store #',
            'Qty per Store #',
            'Record Type',
            'PO purpose',
            'PO Type',
            'Contract Number',
            'Currency',
            'Ship Status',
            'Letter of Credit',
            'Vendor #',
            'Division #',
            'Cust Acct #',
            'Customer Order #',
            'Promo #',
            'Ticket Description',
            'Other Info / #s',
            'Frt Terms',
            'Carrier Service Level',
            'Payment Terms %',
            'Payment Terms Disc Due Date',
            'Payment Terms Disc Days Due',
            'Payment Terms Net Due Date',
            'Payment Terms Net Days',
            'Payment Terms Disc Amt',
            'Payment Terms Desc',
            'Contact Phone',
            'Contact Fax',
            'Contact Email',
            'Allow/Charge Type',
            'Allow/Charge Service',
            'Allow/Charge Amt',
            'Allow/Charge %',
            'Allow/Charge Rate',
            'Allow/Charge Qty',
            'Allow/Charge Desc',
            'Ship To Name',
            'Ship To Address 1',
            'Ship To Address 2',
            'Ship To City',
            'Ship To State',
            'Ship to Zip',
            'Ship To Country',
            'Ship To Contact',
            'Bill To Name',
            'Bill To Address 1',
            'Bill To Address 2',
            'Bill To City',
            'Bill To State',
            'Bill To Zip',
            'Bill To Country',
            'Bill To Contact',
            'Buying Party Name',
            'Buying Party Location',
            'Buying Party Address 1',
            'Buying Party Address 2',
            'Buying Party City',
            'Buying Party State',
            'Buying Party Zip',
            'Buying Party Country',
            'Buying Party Contact',
            'Ultimate Location',
            'Notes/Comments',
            'Ship To Additional Name',
            'Ship To Additional Name 2',
            'Bill To Additional Name',
            'Bill To Additional Name 2',
            'Buyer Additional Name',
            'Buyer Additional Name 2',
            'GTIN',
            'PO Total Amount',
            'PO Total Weight ',
            'PO Total UOM ',
            'Shipping account number',
            'Mark for Name',
            'Mark for Address 1',
            'Mark for Address 2',
            'Mark for City',
            'Mark for State',
            'Mark for Postal',
            'Mark for Country',
            'Shipping Container Code',
            'National Drug Code',
            'Expiration Date',
            'Dist',
            'Scheduled Quantity',
            'Scheduled Qty UOM',
            'Required By Date',
            'Must Arrive By',
            'Entire Shipment',
            'Agreement Number',
            'Additional Vendor Part #',
            'Buyer Part Number',
            'Carrier Details Special Handling',
            'Restrictions/Conditions'
        ]
        if os.path.isfile("sales_origin.xlsx"):
            os.remove("sales_origin.xlsx")
        book = xlsxwriter.Workbook("sales_origin.xlsx")
        sheet = book.add_worksheet("cont_excel")
        # keys = list(sales_import[0].keys())
        for idx, header in enumerate(field_names):
            sheet.write(0, idx, header)

        book.close()

        book = load_workbook("sales_origin.xlsx")
        sheet = book.get_sheet_by_name("cont_excel")
        # print(keys, type(keys[0]))
        # print("*****")
        # print(field_names, type(field_names[0]))
        for num, dic in enumerate(matching_res):
            keys = list(dic.keys())

            for i in range(len(dic[keys[0]])):
                temp = []

                for key in field_names:
                    if key in keys:
                        temp.append(dic[key][i])
                    else:
                        temp.append("")

                sheet.append(temp)

        output = Path(__file__).resolve().parent.parent.parent / f'sales_origin.xlsx'
        
        book.save(filename = output)

        return [matching_res, OMS_equal, self.auto_dic, list(self.stocklocations["Locations"]), self.customer_name]
    # def requiredFields(self, matching_res):
    #     noticer = NOTICER()
    #     addition = noticer.getter(matching_res)

    #     return addition

    def res_viewer(self, data, matching_res, customer_name = None, term = None):
        # paths = []
        # for file in data:
        #     # res = self.uploadFile(file)
        #     path = self.path
        #     paths.append(path)
        #     filename = self.filename
        print(self.filenames, "+++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        filename = self.filenames[0]
        #Fields being filled from selected Vendor Style: Pack Size UOM, Number of Inner Packs, Number of Pcs per Inner Pack
        for invoice in matching_res:
            for i in range(len(invoice[list(invoice.keys())[0]])):
                if i != 0:
                    temp = self.inventory_matching[self.inventory_matching["ProductCode"] == invoice["Vendor Style"][i]]["DefaultUnitOfMeasure"]
                    # print("**********")
                    # print(temp)
                    # print(temp.values[0])
                    # print("**********")
                    if temp.values[0] == "Unit":
                        invoice["Pack Size UOM"][i] = 1
                        invoice["Number of Pcs per Inner Pack"][i] = 1
                        invoice["Number of Inner Packs"][i] = 1
                    
                    else:
                        nums = re.sub(r"[a-zA-Z]", "", temp.values[0]).replace(" ", "").split(",")
                        try:
                            invoice["Pack Size UOM"][i] = nums[0]
                            invoice["Number of Pcs per Inner Pack"][i] = nums[1]
                            invoice["Number of Inner Packs"][i] = int(int(float(invoice["Pack Size UOM"][i])) / int(float(invoice["Number of Pcs per Inner Pack"][i])))
                        except:
                            invoice["Pack Size UOM"][i] = nums[0]
                            invoice["Number of Pcs per Inner Pack"][i] = 1
                            invoice["Number of Inner Packs"][i] = int(int(float(invoice["Pack Size UOM"][i])) / int(float(invoice["Number of Pcs per Inner Pack"][i])))

        #Create View
        print("==============================================================================================================")
        print("Creating View...\n")
        # print(matching_res)

        header_details = []
        item_details = []
        temp_item_details = []

        for i in range(len(matching_res)):
            header_details.append({})

            for key in self.header_keys:
                header_details[i].update(
                    {
                        key: []
                    }
                )

            temp_item_details.append({})

            for key in self.item_keys:
                temp_item_details[i].update(
                    {
                        key: []
                    }
                )

        PO_total = []

        # print(matching_res[0])
        for i, invoice in enumerate(matching_res):
            PO_total.append(0)

            for key in self.item_keys:
                if key == "Price Total Amount":
                    for j in range(len(invoice[self.item_keys["UPC"]]) - 1):
                        PO_total[i] += float(Decimal(str(float(invoice["Unit Price"][j + 1]))) * int(float(invoice["Qty Ordered"][j + 1])))
                        temp_item_details[i][key].append(float(Decimal(str(float(invoice["Unit Price"][j + 1]))) * int(float(invoice["Qty Ordered"][j + 1]))))

                elif key == "Pack Size":
                    for j in range(len(invoice[self.item_keys["UPC"]]) - 1):
                        temp_item_details[i][key].append(1)
                    # for j in range(len(invoice[self.item_keys["UPC"]]) - 1):
                    #     temp_item_details[i][key].append(int(float(invoice["Qty Ordered"][j + 1])) / int(float(invoice["Pack Size UOM"][j + 1])))

                elif key == "Quantity Ordered":
                    for item in invoice[self.item_keys[key]][1:]:
                        temp_item_details[i][key].append(int(float(item)))
                
                elif key == "Number of Pcs per Case Pack":
                    for item in invoice[self.item_keys[key]][1:]:
                        temp_item_details[i][key].append(item)

                elif key == "Total Case Pack Qty":
                    if invoice[self.item_keys["Unit Of Measure"]][1] == "Case":
                        for j in range(len(invoice[self.item_keys["UPC"]]) - 1):
                            temp_item_details[i][key].append(temp_item_details[i]["Quantity Ordered"][j])
                    else:
                        for j in range(len(invoice[self.item_keys["UPC"]]) - 1):
                            temp_item_details[i][key].append(temp_item_details[i]["Quantity Ordered"][j] / int(temp_item_details[i]["Number of Pcs per Case Pack"][j]))
                
                elif key == "Unit Of Measure":
                    if invoice[self.item_keys[key]][1] == "Case":
                        for item in invoice[self.item_keys[key]][1:]:
                            temp_item_details[i][key].append(item)
                    
                    else:
                        for item in invoice[self.item_keys[key]][1:]:
                            temp_item_details[i][key].append("Each")
                    
                else:
                    for item in invoice[self.item_keys[key]][1:]:
                        temp_item_details[i][key].append(item)
        
        for i, invoice in enumerate(matching_res):
            for key in self.header_keys:
                if key == "Payment Terms":
                   header_details[i][key].append(term[0])
                
                elif key == "PO Total":
                    header_details[i][key].append(PO_total[i])

                else: 
                    header_details[i][key].append(invoice[self.header_keys[key]][0])

        for i in range(len(matching_res)):
            item_details.append({})

            for key in self.input_item_keys:
                item_details[i].update(
                    {
                        key: temp_item_details[i][key]
                    }
                )

        print(customer_name, header_details, item_details)

        res = [customer_name, header_details, item_details]
        with open(Path(__file__).resolve().parent.parent.parent / f'process/views/{filename}.json', 'w') as f:
            json.dump(res, f)
        

        # print("printing item_details...")
        # print(header_details)
        # print(item_details)
        return [customer_name, header_details, item_details]
    
    def processFile(self, data, matching_res, extra, customer_name, terms):
        f = open(Path(__file__).resolve().parent / "config/django-connection-1008-5f931d8f4038.json")
        google_json = json.load(f)
        credentials = service_account.Credentials.from_service_account_info(google_json)
        scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
        creds_with_scope = credentials.with_scopes(scope)
        client = gspread.authorize(creds_with_scope)
        self.spreadsheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1CDnIivm8hatRQjG7nvbMxG-AuP19T-W2bNAhbFwEuE0")
        
        # paths = []
        # for file in data:
        #     # res = self.uploadFile(file)
        #     path = self.path
        #     paths.append(path)
        #     filename = self.filename
        path = self.paths[0]
        filename = self.filenames[0]
        sku_match = {}

        if customer_name in self.SKU_list:
            for dic, dic_self in zip(self.matching_res, matching_res):
                for key, uom, location, target in zip(list(dic["Vendor Style"])[1:], list(dic_self["Unit of Measure"])[1:], list(dic_self["StockLocation"])[1:], list(dic_self["Vendor Style"])[1:]):
                    sku_match.update(
                        {
                            str(key): [uom, location, target]
                        }
                    )
        
        else:
            for dic, dic_self in zip(self.matching_res, matching_res):
                for key, uom, location, target in zip(list(dic["Buyers Catalog or Stock Keeping #"])[1:], list(dic_self["Unit of Measure"])[1:], list(dic_self["StockLocation"])[1:], list(dic_self["Vendor Style"])[1:]):
                    sku_match.update(
                        {
                            str(key): [uom, location, target]
                        }
                    )
            

        #DB_Updater: Update automatching DB
        print("==============================================================================================================")
        print("updating Auto matching DB ...")
        # print(sku_match)
        AutoDB().auto_DB_updater(sku_match, customer_name)

        # Integration_Add : Generate SalesImport
        print("==============================================================================================================")
        print("Integrating...")

        integrator = Integrate_All(customer_name=customer_name)
        sales_import = integrator.Integrate_final(matching_res, customer_name, terms, self.spreadsheet)
        print("==============================================================================================================")
        print("Updating SalesImport...")
        updater = SalesImport_Updater()
        sales_import = updater.updater(sales_import)
                

        print("==============================================================================================================")
        print("Just a second, writing...")
        f = open(Path(__file__).resolve().parent / "config/fieldnames_SalesImport.json")

        field_names = json.load(f)

        # generate excel output file
        if os.path.isfile("SalesImport.xlsx"):
            os.remove("SalesImport.xlsx")
        book = xlsxwriter.Workbook("SalesImport.xlsx")
        sheet = book.add_worksheet("cont_excel")
        # keys = list(sales_import[0].keys())
        for idx, header in enumerate(field_names):
            sheet.write(0, idx, header)

        book.close()

        book = load_workbook("SalesImport.xlsx")
        sheet = book.get_sheet_by_name("cont_excel")
        # print(keys, type(keys[0]))
        # print("*****")
        # print(field_names, type(field_names[0]))
        for num, dic in enumerate(sales_import):
            keys = list(dic.keys())

            for i in range(len(dic[keys[0]])):
                temp = []

                for key in field_names:
                    if key in keys:
                        temp.append(dic[key][i])
                    else:
                        temp.append("")

                sheet.append(temp)

        output = Path(__file__).resolve().parent.parent.parent / f'process/outputs/{filename}.xlsx'
        
        book.save(filename = output)
        df = pd.read_excel(output)
        df.to_csv(Path(__file__).resolve().parent.parent.parent / f'process/outputs/{filename}.csv', index=False)
        output = Path(__file__).resolve().parent.parent.parent / f'process/outputs/{filename}.csv'

        return [path, output]

    def live_save(self, matching_res, customername, terms):
        worksheet = self.spreadsheet.get_worksheet(6)
        leng = int(self.spreadsheet.get_worksheet(7).get_values()[0][0])
        f = open(Path(__file__).resolve().parent / "config/fieldnames_SalesImport.json")

        #Getting Invoice Numbers
        dt = worksheet.get_all_records()
        Inumbers = []

        for invoice in dt:
            Inumbers.append(invoice["InvoiceNumber*"])

        integrator = Integrate_All(customer_name=customername)
        sales_import = integrator.Integrate_final(matching_res, customername, terms, self.spreadsheet)

        print("==============================================================================================================")
        print("Updating SalesImport...")
        updater = SalesImport_Updater()
        sales_import = updater.updater(sales_import)

        field_names = json.load(f)
        
        Ignore_invoice_nums = []
        Ignore_invoices = []

        res = []
        for dic in sales_import:
            if dic["InvoiceNumber*"][0] in Inumbers:
                Ignore_invoice_nums.append(dic["InvoiceNumber*"][0])
                Ignore_invoices.append(dic)
                continue

            length = len(dic[list(dic.keys())[0]])
            keys = list(dic.keys())
            for i in range(length):
                temp = []

                for key in field_names:
                    if key in keys:
                        temp.append(str(dic[key][i]))
                    else:
                        temp.append("")
                
                res.append(temp)

        worksheet.update(f'{leng + 1}:{leng + len(res)}', res)

        write_sheet = self.spreadsheet.get_worksheet(7)
        write_sheet.update(f'{1}:{2}', [[leng + len(res)]])
        print("success!!!!!!!!!!!!!!!")

        return [Ignore_invoices, sales_import, Ignore_invoice_nums]
    
    def live_addition(self, Ignore_invoices, sales_import, invoice_nums):
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        worksheet = self.spreadsheet.get_worksheet(6)
        leng = int(self.spreadsheet.get_worksheet(7).get_values()[0][0])
        f = open(Path(__file__).resolve().parent / "config/fieldnames_SalesImport.json")
        updater = SalesImport_Updater()
        sales_import = updater.updater(sales_import)

        field_names = json.load(f)
        dt = worksheet.get_all_records()
        Inumbers = []

        for i, invoice in enumerate(dt):
            if invoice["InvoiceNumber*"] in invoice_nums:
                Inumbers.append(i)

        res = []
        for dic in Ignore_invoices:
            length = len(dic[list(dic.keys())[0]])
            keys = list(dic.keys())

            for i in range(length):
                temp = []

                for key in field_names:
                    if key in keys:
                        temp.append(str(dic[key][i]))
                    else:
                        temp.append("")
                
                res.append(temp)

        for i, liveline_num in enumerate(Inumbers):
            print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
            cells = worksheet.range(f"A{liveline_num + 2}:BG{liveline_num + 2}")
            for j, e in enumerate(cells):
                e.value = res[i][j]
            print("--------------------------------------------------------------")
            worksheet.update_cells(cells)
        # for invoice in res:
        #     for i, invoice_number in enumerate(Inumbers):
        #         print(i)
        #         if invoice[2] == invoice_number:
        #             cells = worksheet.range(f"A{i + 1}:BG{i + 1}")
        #             for j, e in enumerate(cells):
        #                 e.value = invoice[j]

        #             worksheet.update_cells(cells)

        # worksheet.update(f'{leng + 1}:{leng + len(res)}', res)

        # write_sheet = self.spreadsheet.get_worksheet(7)
        # write_sheet.update(f'{1}:{2}', [[leng + len(res)]])

        print("Success Live Addition!!!")