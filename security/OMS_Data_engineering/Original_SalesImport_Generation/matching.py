# "PO Number": "",
# "PO Date": "",
# "Ship Dates": "",
# "Cancel Date": "",
# "Qty Ordered": "",
# "Unit of Measure": "",
# "Unit Price": "",
# "Buyers Catalog or Stock Keeping #": "",
# "UPC/EAN": "",
# "Vendor Style": "",
# "Product/Item Description": "",
# "PO Total Amount": "",
# "PO Total Weight": "",
                                                                                                                                                                                                                                                                                                                                                                                                                                                                    
                                                                                                                                                                                                                                                                                                                                                                                                                                                                    
import json
import re
import pandas as pd
from pathlib import Path
import numpy as np
import math

class PO_Match:
    def match_formula(self, input):
        temp_key = input.keys()

        for item in self.field_names:
            if item not in temp_key:
                temp = []
                
                for _ in range(self.length):
                    temp.append("")
                
                input.update({item: temp})
            
        return input
    
    def initial_part_init(self):
        self.initial_part = {}
        # self.initial_part = self.pair
        for key in self.pair:
            self.initial_part.update({key:""})

class PO_Match_BUCEE_PDF(PO_Match):
    def __init__(self) -> None:
        # parse_res: OCR parsed result for PO
        
        self.PO_keys = []
        self.variables = {}
        self.data = []
        self.length = 0
        self.pair = {
            'PO Line #': "LINE",
            'Vendor Style': "VENDOR PN",
            'UPC/EAN': "UPC/GTIN",
            'Product/Item Description': "DESCRIPTIONLINE ITEM COMMENTS",
            "Dept #": "DESCRIPTIONLINE ITEM COMMENTS",
            'Unit Price': "UNIT COST/RETAIL PRICE",
            'Qty Ordered': "QTY",
            "Unit of Measure": "UOM",
            "PO Date": "PO Date:",
            "Requested Delivery Date": "Requested Delivery Date:",
            "Ship Dates": "Requested Ship Date:",
            "Cancel Date": "Cancel Date:",
            "Vendor #": "Vendor #:",
            "Frt Terms": "Freight Terms:",
            "Payment Terms Disc Due Date": "Disc. Due Date:",
            "Payment Terms Net Days": "Disc. Days:",
            "Payment Terms Net Due Date": "Net Due Date:",
            "Payment Terms Net Days": "Net Days:",
            "Buyers Catalog or Stock Keeping #": "SKU",
            "PO Total Amount": "total",
            "PO Total Weight": "Weight:",
            "PO Number": "Order #",
            "Retailers PO": "Order #",
            "Currency": "PO_currency",
            "Ship To Name": "Ship To Name",
            "Ship To Address 1": "Ship To Address 1",
            "Ship To City": "Ship To City",
            "Ship To State": "Ship To State",
            "Ship to Zip": "Ship to Zip",
            "Ship To Country": "Ship To Country",
            "Buying Party Name": "Buying Party Name",
        }
        
        self.initial_part = {
            "PO Line #": "",
            'Vendor Style': "",
            "UPC/EAN": "",
            "Product/Item Description": "",
            "Dept #": "",
            'Unit Price': "",
            'Qty Ordered': "",
            "Unit of Measure": "",
            "PO Date": "",
            "Requested Delivery Date": "",
            "Ship Dates": "",
            "Cancel Date": "",
            "Vendor #": "",
            "Frt Terms": "",
            "Payment Terms Disc Due Date": "",
            "Payment Terms Net Days": "",
            "Payment Terms Net Due Date": "",
            "Payment Terms Net Days": "",
            "Buyers Catalog or Stock Keeping #": "",
            "PO Total Amount": "",
            "PO Total Weight": "",
            "PO Number": "",
            "Retailers PO": "",
            "Currency": "",
            "Ship To Name": "",
            "Ship To Address 1": "",
            "Ship To City": "",
            "Ship To State": "",
            "Ship to Zip": "",
            "Ship To Country": "",
            "Buying Party Name": "",
        }
        
        f = open(Path(__file__).resolve().parent.parent / "config/field_names_SalesImport_original.json")
        self.field_names = json.load(f)
        self.field_names_temp = []
        for item in self.field_names:
            self.field_names_temp.append(item) 
        for item in self.field_names_temp:
            a = list(self.pair.keys())
            if item in list(self.pair.keys()):
                (self.field_names).remove(item)
    
    def variable_init(self):
        self.variables = {}
        for key in self.field_names:
            self.variables[key] = ""
    
    def match_plain(self, input):
        res = []

        for i, _ in enumerate(input):
            pdf = input[f"PDF{i}"]

            for j, _ in enumerate(pdf):
                res.append(pdf[f"page{j}"])

        return res
    
    def match_divide(self, input):

        input = list(input)
        input.remove("\n")
        input = "".join(input)
        input_ = input.split("Department Number")
        temp = []

        for i, element in enumerate(input_):
            if ":" in element: temp.append(i)

            # f_th = input_[0:temp[1]]
            # s_nd = input_[temp[1]:]
        return [input_[0:temp[1]], input_[temp[1]:]]
    
    def order_extract(self, input):
        temp = []
        temp.append(re.findall(r"\d+", input[0])[0][2:])
        for i in range(1, self.length):
            temp.append("")
            

        return temp
    
    def match_same(self, input):
        self.initial_part_init()
        
        for key in self.pair:
            if key == "Product/Item Description":
                input[key] = []
                input["Dept #"] = []

                for i in range(1, self.length):
                    input[key].append(self.match_divide(input[self.pair[key]][i])[0][0].split(":")[1])
                    input["Dept #"].append(self.match_divide(input[self.pair[key]][i])[1][0].split(":")[1])

                input[key].insert(0, "")
                input["Dept #"].insert(0, "")
                del input[self.pair[key]]
                
            elif key == "Dept #": continue
            
            elif key == "Unit Price":
                input[key] = []

                for i in range(1, self.length):
                    temp = re.findall(r'\d\.\d+', input[self.pair[key]][i])
                    input[key].append("".join(temp))
                
                input[key].insert(0, "")

                del input[self.pair[key]]
            
            elif key == 'Vendor Style':
                input[key] = []
                
                for i in range(1, self.length):
                    temp = re.findall(r'\d', input[self.pair[key]][i])
                    input[key].append("".join(temp))
                
                input[key].insert(0, "")
                del input[self.pair[key]]

            elif key == "PO Number":
                input[key] = self.order_extract(input[self.pair[key]])
                del input[self.pair[key]]
            
            elif key == "Retailers PO":
                input[key] = input["PO Number"]

            elif key in ["Ship To Name", "Ship To Address 1", "Ship To City", "Ship To State", "Ship to Zip", "Ship To Country", "Buying Party Name"]:
                input[key] = input[self.pair[key]]

            else:
                input[key] = input[self.pair[key]]
                del input[self.pair[key]]

        return input
    
    def match_final(self, PO_res):
        # return final result
        output = self.match_plain(PO_res)
        
        # get PO_res keys
        self.PO_keys = list(output[0].keys())
        self.PO_inherited = []
        for key in self.pair:
            self.PO_inherited.append(self.pair[key])

        #register un-inherited keys
        
        
        for content in output:
            self.length = len(content["LINE"])
            item = self.match_same(content)
            item = self.match_formula(item)
            # output.pop(i)
            # output.insert(i, item)
            for key in self.PO_keys:
                if key not in self.PO_inherited:
                    del item[key]

        df = pd.DataFrame(output[0])
        df.to_excel("sales_origin.xlsx")
        
        return output
    
class PO_Match_BUCEE(PO_Match):
    def __init__(self) -> None:
        pass
    
    def match_plain(self, input):
        res = []

        for pdf in input:
            for page in pdf:
                res.append(page)

        return res
    
    def match_final(self, PO_res):
        output = self.match_plain(PO_res)
        
        return output

class PO_Match_PEPCO(PO_Match):
    def __init__(self) -> None:
        # parse_res: OCR parsed result for PO
        
        self.PO_keys = []
        # self.variables = {}
        # self.data = []
        self.length = 0
        self.pair = {
            "PO Number": "Order - ID",
            "PO Date": "Date of order creation",
            "Ship Dates": "Booking date",
            "Cancel Date": "Handover date",
            "Qty Ordered": "Total",
            "Unit Price": "Purchase price",
            "Buyers Catalog or Stock Keeping #": "Item No",
            "UPC/EAN": "barcode",
            "Currency": "PO_currency",
            "Payment Terms Net Days": "Terms of payments",
            "Number of Inner Packs": "Pack multiplier",
            "Number of Pcs per Inner Pack": "ONE",
        }
        self.initial_part = {
            "PO Number": "",
            "PO Date": "",
            "Ship Dates": "",
            "Cancel Date": "",
            "Qty Ordered": "",
            "Unit Price": "",
            "Buyers Catalog or Stock Keeping #": "",
            "UPC/EAN": "",
            "Currency": "",
            "Payment Terms Net Days": "",
            "Number of Inner Packs": "",
            "Number of Pcs per Inner Pack": "",
        }

        f = open(Path(__file__).resolve().parent.parent / "config/field_names_SalesImport_original.json")
        self.field_names = json.load(f)
        self.field_names_temp = []

        for item in self.field_names:
            self.field_names_temp.append(item)

        for item in self.field_names_temp:
            if item in list(self.pair.keys()):
                (self.field_names).remove(item)
    
    def match_numdivide(self, num):
        return num.replace(",", ".").replace(" ", "")
    
    def match_remove_space(self, st):
        st = st.replace(" ", "")

        return st
    
    def match_plain(self, input):
        res = []

        for i, _ in enumerate(input):
            pdf = input[f"PDF{i}"]
            res.append(pdf)
        
        return res
    
    def match_same(self, input):
        self.initial_part_init()

        for key in self.pair:
            if key == "Unit Price":
                input[key] = []
                input[key].append("")
                input[key].append(self.match_numdivide(input[self.pair[key]][0]))
                del input[self.pair[key]]
            
            elif key == "PO Number":
                input[key] = input[self.pair[key]]
                input["Retailers PO"] = input[self.pair[key]]
                del input[self.pair[key]]
                
            elif key == "Buyers Catalog or Stock Keeping #":
                input[key] = [""]
                input[key].append(input[self.pair[key]][1].replace(" ", ""))

                del input[self.pair[key]]
            elif key == "Payment Terms Net Days":
                input[key] = [input[self.pair[key]][1]]
                input[key].append("")

                del input[self.pair[key]]

            else:
                input[key] = input[self.pair[key]]
                del input[self.pair[key]]

        return input
    
    def match_fun(self, input):
        #PO Line #
        input["PO Line #"] = []
        input["PO Line #"].append("")
        for i in range(self.length - 1):
            input["PO Line #"].append(i + 1)
        
        #PO Total Amount
        input["PO Total Amount"] = []
        input["PO Total Amount"].append(float(self.match_remove_space(input["Unit Price"][1])) * float(self.match_remove_space(input["Qty Ordered"][1])))
        input["PO Total Amount"].append("")

        ##remove fields
        # (self.field_names).remove("PO Line #")
        # (self.field_names).remove("PO Total Amount")

        return input

    def match_final(self, PO_res):
        output = self.match_plain(PO_res)

        self.PO_keys = list(output[0].keys())
        self.PO_inherited = []
        for key in self.pair:
            self.PO_inherited.append(self.pair[key])

        for content in output:
            self.field_names = self.field_names_temp
            self.length = len(content[list(content.keys())[0]])
            item = self.match_same(content)
            item = self.match_fun(item)
            item = self.match_formula(item)

            for key in self.PO_keys:
                if key not in self.PO_inherited:
                    del item[key]

        df = pd.DataFrame(output[0])
        df.to_excel("sales_origin.xlsx")

        return output
    
class PO_Match_PEPCO_Add(PO_Match):
    def __init__(self) -> None:
        self.PO_keys = []
        self.length = 2
        self.pair = {
            "PO Number": "Order Number",
            "Payment Terms Net Days": "Terms of payment",
            "Ship Dates": "Handover date",#0
            "Buyers Catalog or Stock Keeping #": "Sku",#1
            "Currency": "Cost price currency",#0
            "Unit Price": "Unit Cost price",#1
            "Qty Ordered": "Total Unit Qty",#1
            # "Notes/Comments": "Comments",#1
            "PO Date": "Date of order creation",#0
            "Contact Email": "Buyer",
            # "": "order_contact",
            "Buying Party Name": "invoice",
            "Buying Party Location": "invoice",
            "Buying Party Address 1": "invoice",
            # "Buying Party Address 2"
            "Buying Party City": "invoice",
            # "Buying Party State"
            # "Buying Party Zip"
            # "Buying Party Country"
            # "Buying Party Contact"
            "Bill To Address 1": "deliver_to",
            "Bill To Address 2": "deliver_to",
            "Bill To City": "deliver_to",
            # "Bill To State"
            # "Bill To Zip"
            # "Bill To Country"
            # "Bill To Contact"
        }

        f = open(Path(__file__).resolve().parent.parent / "config/field_names_SalesImport_original.json")
        self.field_names = json.load(f)
        self.field_names_temp = []

        for item in self.field_names:
            self.field_names_temp.append(item) 

        for item in self.field_names_temp:
            if item in list(self.pair.keys()):
                (self.field_names).remove(item)

    def match_plain(self, input):
        res = []

        for i, _ in enumerate(input):
            pdf = input[f"PDF{i}"]

            for j, _ in enumerate(pdf):
                res.append(pdf[f"page{j}"])

        return res

    def match_same(self, input):
        self.initial_part_init()

        for key in self.pair:
            if key == "PO Number":
                temp = re.findall(r'\d+', input[self.pair[key]])
                input[key] = [temp[0]]
                input[key].append(temp[0])
                input["Retailers PO"] = [""]
                input["Retailers PO"].append(temp[0])

                del input[self.pair[key]]
            
            elif key == "Payment Terms Net Days":
                input[key] = [input[self.pair[key]]]
                input[key].append("")

                del input[self.pair[key]]
            
            elif key == "Ship Dates":
                input[key] = [input[self.pair[key]]]
                input[key].append("")

                del input[self.pair[key]]

            elif key == "Buyers Catalog or Stock Keeping #":
                input[key] = [""]
                input[key].append(input[self.pair[key]])

                del input[self.pair[key]]

            elif key == "Currency":
                input[key] = [input[self.pair[key]]]
                input[key].append("")

                del input[self.pair[key]]

            elif key == "Unit Price":
                input[key] = [""]
                input[key].append(input[self.pair[key]])

                del input[self.pair[key]]

            elif key == "Qty Ordered":
                input[key] = [""]
                input[key].append(int(float(input[self.pair[key]])))

                del input[self.pair[key]]

            elif key == "PO Date":
                input[key] = [input[self.pair[key]]]
                input[key].append("")

                del input[self.pair[key]]

            elif key == "Contact Email":
                input[key] = [input[self.pair[key]]]
                input[key].append("")

                del input[self.pair[key]]

            elif key == "Buying Party Name":
                input[key] = [input[self.pair[key]][0]]
                input[key].append("")

                # del input[self.pair[key]]

            elif key == "Buying Party Location":
                input[key] = [input[self.pair[key]][1]]
                input[key].append("")

                # del input[self.pair[key]]

            elif key == "Buying Party Address 1":
                input[key] = [input[self.pair[key]][2]]
                input[key].append("")

                # del input[self.pair[key]]

            elif key == "Buying Party City":
                input[key] = [input[self.pair[key]][3]]
                input[key].append("")

                del input[self.pair[key]]

            elif key == "Bill To Address 1":
                input[key] = [input[self.pair[key]].split(",")[0]]
                input[key].append("")

                # del input[self.pair[key]]

            elif key == "Bill To Address 2":
                input[key] = [input[self.pair[key]].split(",")[1]]
                input[key].append("")

                # del input[self.pair[key]]

            elif key == "Bill To City":
                input[key] = [input[self.pair[key]].split(",")[2]]
                input[key].append("")

                del input[self.pair[key]]
            # elif key == "Ship Dates":
            # else:
            #     input[key] = [input[self.pair[key]][0]]
            #     input[key].append("")

            #     del input[self.pair[key]]
        
        return input

    def match_final(self, PO_res):
        output = self.match_plain(PO_res)
        self.PO_keys = list(output[0].keys())
        self.PO_inherited = []
        for key in self.pair:
            self.PO_inherited.append(self.pair[key])

        for content in output:
            self.field_names = self.field_names_temp
            
            item = self.match_same(content)
            item = self.match_formula(item)
            
            for key in self.PO_keys:
                if key not in self.PO_inherited:
                    del item[key]

        df = pd.DataFrame(output[0])
        df.to_excel("sales_origin.xlsx")
        return output
    
class PO_Match_Walgreens:
    def __init__(self) -> None:
        self.length = 2

    def match_plain(self, input):
        res = []

        for pdf in input:
            for page in pdf:
                res.append(page)

        return res
    
    def match_date(self, input):
        temp = []
        temp.append(input[0].split(" - "))
    
        for _ in range(self.length - 1):
            temp.append(["", ""])
        
        return temp
    
    def match_list(self, input):
        temp_1 = []
        temp_2 = []

        for lis in input:
            temp_1.append(lis[0])
            temp_2.append(lis[1])
        
        return [temp_1, temp_2]

    def match_final(self, PO_res):
        output = self.match_plain(PO_res)
        for content in output:
            self.length = len(content[list(content.keys())[0]])
            dates = self.match_list(self.match_date(content["Ship Dates"]))

            for key in content:
                if key == "Ship Dates":
                    content[key] = dates[0]
                
                elif key == "Cancel Date":
                    content[key] = dates[1]
                    
        df = pd.DataFrame(output[0])
        df.to_excel("sales_origin.xlsx")

        return output
    
class PO_Match_Dollarama(PO_Match):
    def __init__(self) -> None:
        self.PO_keys = []
        self.length = 1
        self.pair = {
            "PO Number": "P/O #",
            "PO Date": "PO Dates",
            "Ship Dates": "Ready Dates",
            "Qty Ordered": "Quantity in Units",
            "Unit of Measure": "",
            "Unit Price": "Cost USD Each",
            "Buyers Catalog or Stock Keeping #": "Dollarama Item #",
            "UPC/EAN": "UPC Code",
            "Retail Price": "Retail",
            "Product/Item Description": "Item Description",
            "PO Total Amount": "Total_Total USD Cost",
            "PO Total Weight": "Total_Total Weight",
            "Vendor Style": "Vendor",
        }

        self.month_match = {
            "January": 1,
            "February":2,
            "March": 3,
            "April": 4,
            "May": 5,
            "June": 6,
            "July": 7,
            "August": 8,
            "September": 9,
            "October": 10,
            "November": 11,
            "December": 12,
        }

        f = open(Path(__file__).resolve().parent.parent / "config/field_names_SalesImport_original.json")
        self.field_names = json.load(f)
        self.field_names_temp = []

        for item in self.field_names:
            self.field_names_temp.append(item) 

        for item in self.field_names_temp:
            if item in list(self.pair.keys()):
                (self.field_names).remove(item)

    def match_plain(self, input):
        res = []

        for i, _ in enumerate(input):
            pdf = input[f"PDF{i}"]

            for j, _ in enumerate(pdf):
                res.append(pdf[f"page{j}"])

        return res
    
    def length_gain(self, input):
        length = 0

        for item in input:
            if item == '':
                break

            length = length + 1

        return length
    
    def product_updater(self, input):
        output = []

        for item in input:
            temp = []
            for i in range(self.length):
                temp.append(item[i])
            
            output.append(temp)
        
        return output
    
    def date_converter_1(self, input: str):
        for key in self.month_match:
            if key in input:
                return input.replace(key, str(self.month_match[key]) + ",").replace(",", "/").replace(" ", "")
            
    def date_converter_2(self, input: str):
        for key in self.month_match:
            if key in input:
                temp = input.replace(key, str(self.month_match[key])).replace("-", "/").split("/")
                break
        
        return "/".join([temp[i] for i in [1, 0, 2]])
    
    def match_same(self, input):
        self.initial_part_init()

        for key in self.pair:
            if key == "PO Number":
                input[key] = [input[self.pair[key]]]

                for _ in range(self.length - 1): 
                    input[key].append(input[self.pair[key]])

                input["Retailers PO"] = [input[self.pair[key]]]

                for _ in range(self.length - 1): 
                    input["Retailers PO"].append("")

                del input[self.pair[key]]
                
            elif key == "PO Date":
                input[key] = [self.date_converter_1(input[self.pair[key]])]

                for _ in range(self.length - 1):
                    input[key].append("")

                del input[self.pair[key]]
            
            elif key == "Ship Dates":
                input[key] = [self.date_converter_2(input[self.pair[key]][0])]

                for _ in range(self.length - 1):
                    input[key].append("")

                del input[self.pair[key]]
            
            elif key == "Qty Ordered":
                input[key] = [""]

                for i in range(self.length - 1):
                    input[key].append(re.sub('[^0-9]+', '', input[self.pair[key]][i]))

                del input[self.pair[key]]
            
            elif key == "Unit of Measure":
                input[key] = [""]

                for _ in range(self.length - 1):
                    input[key].append("Each")
            
                #There is non-key to delete
            
            elif key == "Unit Price":
                input[key] = [""]

                for _ in range(self.length - 1):
                    input[key].append(float(input[self.pair[key]]))

                del input[self.pair[key]]
            
            elif key == "Buyers Catalog or Stock Keeping #":
                input[key] = [""]

                for _ in range(self.length - 1):
                    input[key].append(input[self.pair[key]])
                
                del input[self.pair[key]]

            elif key == "UPC/EAN":
                input[key] = [""]

                for _ in range(self.length - 1):
                    input[key].append(input[self.pair[key]])
                
                del input[self.pair[key]]
            
            elif key == "Retail Price":
                input[key] = [input[self.pair[key]]]

                for _ in range(self.length - 1):
                    input[key].append("")

                del input[self.pair[key]]

            elif key == "Product/Item Description":
                input[key] = [""]

                for _ in range(self.length - 1):
                    input[key].append(input[self.pair[key]])

                del input[self.pair[key]]

            elif key == "PO Total Amount":
                input[key] = [float(input[self.pair[key]].replace(",", ""))]

                for _ in range(self.length - 1):
                    input[key].append("")

                del input[self.pair[key]]

            elif key == "PO Total Weight":
                input[key] = [float(re.sub('[^0-9]+', '', input[self.pair[key]]))]

                for _ in range(self.length - 1):
                    input[key].append("")

                del input[self.pair[key]]
            
            elif key == "Vendor Style":
                input[key] = [""]

                for _ in range(self.length - 1):
                    input[key].append(input[self.pair[key]])

                del input[self.pair[key]]
        
        return input

    def match_final(self, PO_res):
        output = self.match_plain(PO_res)

        self.PO_keys = list(output[0].keys())
        self.PO_inherited = []

        for key in self.pair:
            self.PO_inherited.append(self.pair[key])

        for content in output:
            self.length = self.length_gain(content["Ready Dates"]) + 1

            [content["Ready Dates"], content["Quantity in Units"], content["Quantity in Cases"], content["Total Volume"], content["Total Weight"], content["Total USD Cost"]] = self.product_updater([content["Ready Dates"], content["Quantity in Units"], content["Quantity in Cases"], content["Total Volume"], content["Total Weight"], content["Total USD Cost"]])

            item = self.match_same(content)
            item = self.match_formula(item)

            for key in self.PO_keys:
                if key not in self.PO_inherited:
                    del item[key]

        df = pd.DataFrame(output[0])
        df.to_excel("sales_origin.xlsx")

        return output
    
class PO_Match_Family_Dollar(PO_Match):
    def __init__(self) -> None:
        self.PO_keys = []
        self.variables = {}
        self.data = []
        self.length = 2
        self.pair = {
            "PO Number": "Purchase Order", 
            "Ship Dates": "PO First Ship Date", 
            "Cancel Date": "PO Last Ship Date", 
            # : "PO First DC Date",
            # : "PO Last DC Date", 
            "Payment Terms Net Days": "Payment Terms", 
            "Currency": "Currencys", 
            "PO Total Weight": "Total PO Weight LBS", 
            "Buyers Catalog or Stock Keeping #": "Family Dollar SKU", 
            "UPC/EAN": "UPC", 
            "Vendor Style": "VPN", 
            "Unit Price": "First Cost Eaches", 
            "Number of Pcs per Inner Pack": "Inner Case Pack",
            "Pack Size UOM": "Master Case Pack",
            "Number of Inner Packs": "",
            "Qty Ordered": "Total Eaches Ordered", 
            "PO Total Amount": "Total First Cost", 
            # : "RMS Retail Price"
        }

        f = open(Path(__file__).resolve().parent.parent / "config/field_names_SalesImport_original.json")
        self.field_names = json.load(f)
        self.field_names_temp = []
        for item in self.field_names:
            self.field_names_temp.append(item) 
        for item in self.field_names_temp:
            a = list(self.pair.keys())
            if item in list(self.pair.keys()):
                (self.field_names).remove(item)

    def match_plain(self, input):
        res = []

        for i, _ in enumerate(input):
            pdf = input[f"PDF{i}"]

            for j, _ in enumerate(pdf):
                res.append(pdf[f"page{j}"])

        return res
    
    def match_same(self, input):
        self.initial_part_init()
        
        for key in self.pair:
            if key == "PO Number":
                input[key] = [input[self.pair[key]]]

                for _ in range(self.length - 1): 
                    input[key].append(input[self.pair[key]])

                input["Retailers PO"] = [input[self.pair[key]]]

                for _ in range(self.length - 1): 
                    input["Retailers PO"].append("")

                del input[self.pair[key]]

            elif key == "Ship Dates":
                input[key] = [input[self.pair[key]]]

                for _ in range(self.length - 1): 
                    input[key].append("")
                
                del [input[self.pair[key]]]

            elif key == "Cancel Date":
                input[key] = [input[self.pair[key]]]

                for _ in range(self.length - 1): 
                    input[key].append("")
                
                del [input[self.pair[key]]]

            elif key == "Payment Terms Net Days":
                input[key] = [input[self.pair[key]]]

                for _ in range(self.length - 1): 
                    input[key].append("")
                
                del [input[self.pair[key]]]

            elif key == "Currency":
                input[key] = [input[self.pair[key]]]

                for _ in range(self.length - 1): 
                    input[key].append("")
                
                del [input[self.pair[key]]]

            elif key == "PO Total Weight":
                input[key] = [float(re.sub('[^0-9]+', '', input[self.pair[key]]))]

                for _ in range(self.length - 1): 
                    input[key].append("")
                
                del [input[self.pair[key]]]

            elif key == "Buyers Catalog or Stock Keeping #":
                input[key] = [""]

                for _ in range(self.length - 1):
                    input[key].append(input[self.pair[key]])

                del input[self.pair[key]]

            elif key == "UPC/EAN":
                input[key] = [""]

                for _ in range(self.length - 1):
                    input[key].append(input[self.pair[key]])

                del input[self.pair[key]]

            elif key == "Vendor Style":
                input[key] = [""]

                for _ in range(self.length - 1):
                    input[key].append(input[self.pair[key]])

                del input[self.pair[key]]

            elif key == "Unit Price":
                input[key] = [""]

                for _ in range(self.length - 1):
                    input[key].append(input[self.pair[key]])

                del input[self.pair[key]]

            elif key == "Qty Ordered":
                input[key] = [""]

                for _ in range(self.length - 1):
                    input[key].append(int(re.sub('[^0-9]+', '', input[self.pair[key]])))

                del input[self.pair[key]]

            elif key == "PO Total Amount":
                input[key] = [input[self.pair[key]].replace(",", "")]

                for _ in range(self.length - 1): 
                    input[key].append("")
                
                del input[self.pair[key]]

            elif key in ["Number of Pcs per Inner Pack", "Pack Size UOM"]:
                input[key] = [""]
                
                for i in range(self.length - 1): 
                    input[key].append(input[self.pair[key]])
                
                del input[self.pair[key]]
            
            elif key == "Number of Inner Packs":
                input[key] = [""]

                for i in range(self.length - 1): 
                    input[key].append(int(int(input["Pack Size UOM"][1]) / int(input["Number of Pcs per Inner Pack"][1])))
                
        
        return input



    def match_final(self, PO_res):
        # return final result
        output = self.match_plain(PO_res)
        
        # get PO_res keys
        self.PO_keys = list(output[0].keys())
        self.PO_inherited = []
        for key in self.pair:
            self.PO_inherited.append(self.pair[key])

        #register un-inherited keys
        
        
        for content in output:
            item = self.match_same(content)
            item = self.match_formula(item)
            # output.pop(i)
            # output.insert(i, item)
            for key in self.PO_keys:
                if key not in self.PO_inherited:
                    del item[key]

        return output

class PO_Match_Gabes(PO_Match):
    def __init__(self) -> None:
        self.PO_keys = []
        self.length = 1
        self.pair = {
            "PO Number": "PO",
            "PO Date": "Order Date",
            "Ship Dates": "Ship Date",
            "Cancel Date": "Cancel Dates",
            "Qty Ordered": "Total Qty",
            "Unit of Measure": "",
            "Unit Price": "Unit Cost",
            "Buyers Catalog or Stock Keeping #": "Internal Item #",
            "UPC/EAN": "Ticket SKU",
            "Vendor Style": "Style",
            "Product/Item Description": "Description",
            "PO Total Amount": "Total Cost",
        }
        f = open(Path(__file__).resolve().parent.parent / "config/field_names_SalesImport_original.json")
        self.field_names = json.load(f)
        self.field_names_temp = []

        for item in self.field_names:
            self.field_names_temp.append(item) 

        for item in self.field_names_temp:
            if item in list(self.pair.keys()):
                (self.field_names).remove(item)

    def match_plain(self, input):
        res = []

        for i, _ in enumerate(input):
            pdf = input[f"PDF{i}"]

            for j, _ in enumerate(pdf):
                res.append(pdf[f"page{j}"])

        return res

    def match_same(self, input):
        self.initial_part_init()

        for key in self.pair:
            if key == "PO Number":
                input[key] = [input[self.pair[key]]]

                for _ in range(self.length - 1): 
                    input[key].append(input[self.pair[key]])

                input["Retailers PO"] = [input[self.pair[key]]]

                for _ in range(self.length - 1): 
                    input["Retailers PO"].append("")

                del input[self.pair[key]]

            elif key == "PO Date":
                temp = [input[self.pair[key]].split('/')[i] for i in [2, 0, 1]]
                temp[0] = '20' + str(temp[0])
                date = '\\'.join(temp)
                input[key] = [date]

                for _ in range(self.length - 1):
                    input[key].append("")

                del input[self.pair[key]]

            elif key == "Ship Dates":
                input[key] = [input[self.pair[key]]]

                for _ in range(self.length - 1):
                    input[key].append("")

                del input[self.pair[key]]

            elif key == "Cancel Date":
                input[key] = [input[self.pair[key]]]

                for _ in range(self.length - 1):
                    input[key].append("")

                del input[self.pair[key]]

            elif key == "Qty Ordered":
                input[key] = [""]

                for i in range(self.length - 1):
                    input[key].append(re.sub('[^0-9]+', '', input[self.pair[key]][i]))

                del input[self.pair[key]]
                
            elif key == "Unit of Measure":
                input[key] = [""]

                for _ in range(self.length - 1):
                    input[key].append("Each")
            
                #There is non-key to delete

            elif key == "Unit Price":
                input[key] = [""]

                for i in range(self.length - 1):
                    input[key].append(float(input[self.pair[key]][i].replace("$", "")))

                del input[self.pair[key]]
            
            elif key == "PO Total Amount":
                input[key] = [input[self.pair[key]].replace("$", "").replace(",", "")]

                for i in range(self.length - 1):
                    input[key].append("")
                
                del input[self.pair[key]]
            
            else:
                input[key] = [""]

                for i in range(self.length - 1):
                    input[key].append(input[self.pair[key]][i])

                del input[self.pair[key]]
        
        return input

    def match_final(self, PO_res):
        # return final result
        output = self.match_plain(PO_res)
        
        # get PO_res keys
        self.PO_keys = list(output[0].keys())
        self.PO_inherited = []

        for key in self.pair:
            self.PO_inherited.append(self.pair[key])

        for content in output:
            self.length = len(content["Unit Cost"]) + 1

            item = self.match_same(content)
            item = self.match_formula(item)

            for key in self.PO_keys:
                if key not in self.PO_inherited:
                    del item[key]

        df = pd.DataFrame(output[0])
        df.to_excel("sales_origin.xlsx")

        return output

class PO_Match_TEDI(PO_Match):
    def __init__(self) -> None:
        self.PO_keys = []
        self.length = 2
        self.pair = {
            "PO Number": "Order number",
            # "PO Date": "Order Date",
            "Ship Dates": "Shipping window",
            "Cancel Date": "Shipping window",
            "Qty Ordered": "total_quantity",
            "Unit of Measure": "",
            "Unit Price": "price_unit",
            "Buyers Catalog or Stock Keeping #": "Supplier art.-no",
            # "UPC/EAN": "Ticket SKU",
            # "Vendor Style": "",
            "Product/Item Description": "Description",
            "PO Total Amount": "total_cost",
        }
        f = open(Path(__file__).resolve().parent.parent / "config/field_names_SalesImport_original.json")
        self.field_names = json.load(f)
        self.field_names_temp = []

        for item in self.field_names:
            self.field_names_temp.append(item) 

        for item in self.field_names_temp:
            if item in list(self.pair.keys()):
                (self.field_names).remove(item)
    
    def match_plain(self, input):
        res = []

        for i, _ in enumerate(input):
            pdf = input[f"PDF{i}"]

            for j, _ in enumerate(pdf):
                res.append(pdf[f"page{j}"])

        return res
    
    def match_same(self, input):
        self.initial_part_init()

        for key in self.pair:
            if key == "PO Number":
                input[key] = [input[self.pair[key]]]

                for _ in range(self.length - 1): 
                    input[key].append(input[self.pair[key]])

                input["Retailers PO"] = [input[self.pair[key]]]

                for _ in range(self.length - 1): 
                    input["Retailers PO"].append("")

                del input[self.pair[key]]
            
            elif key == "Ship Dates":
                input[key] = [input[self.pair[key]].split(" - ")[0]]

                for _ in range(self.length - 1): 
                    input[key].append("")
            
            elif key == "Cancel Date":
                input[key] = [input[self.pair[key]].split(" - ")[1]]

                for _ in range(self.length - 1): 
                    input[key].append("")
                
                del input[self.pair[key]]
            
            elif key == "Qty Ordered":
                input[key] = [""]

                for _ in range(self.length - 1): 
                    input[key].append(input[self.pair[key]])
                
                del input[self.pair[key]]

            elif key == "Unit of Measure":
                input[key] = [""]

                for _ in range(self.length - 1):
                    input[key].append("Each")
            
                #There is non-key to delete
            
            elif key == "Unit Price":
                input[key] = [""]

                for _ in range(self.length - 1):
                    input[key].append(re.sub(r'\s*[A-Za-z]+\b', '', input[self.pair[key]]))

                del input[self.pair[key]]
            
            elif key == "Product/Item Description":
                input[key] = [""]

                for i in range(self.length - 1):
                    input[key].append(input[self.pair[key]])
                
                del input[self.pair[key]]
            
            elif key == "PO Total Amount":
                input[key] = [re.sub(r'\s*[A-Za-z]+\b', '', input[self.pair[key]]).replace(",", "")]

                for i in range(self.length - 1):
                    input[key].append("")

                del input[self.pair[key]]

            elif key == "Buyers Catalog or Stock Keeping #":
                input[key] = [""]
                input[key].append(input[self.pair[key]])

                del input[self.pair[key]]

        return input
                
    def match_final(self, PO_res):
        # return final result
        output = self.match_plain(PO_res)

        # get PO_res keys
        self.PO_keys = list(output[0].keys())
        self.PO_inherited = []

        for key in self.pair:
            self.PO_inherited.append(self.pair[key])

        for content in output:
            item = self.match_same(content)
            item = self.match_formula(item)

            for key in self.PO_keys:
                if key not in self.PO_inherited:
                    del item[key]

        df = pd.DataFrame(output[0])
        df.to_excel("sales_origin.xlsx")

        return output

class PO_Match_Walmart(PO_Match):
    def __init__(self) -> None:
        pass
    
    def match_plain(self, input):
        res = []

        for pdf in input:
            for page in pdf:
                res.append(page)

        return res
    def match_same(self, input):
        for key in input:
            if key == "Ship Dates":
                input[key][0] = input[key][0].split(" - ")[0]
    def match_final(self, PO_res):
        output = self.match_plain(PO_res)
        
        for input in output:
            self.match_same(input)
        return output
    
class PO_Match_Ollies(PO_Match):
    def __init__(self) -> None:
        self.PO_keys = []
        self.length = 2
        self.pair = {
            "PO Number": "PO#",
            "PO Date": "Order Dt",
            "Ship Dates": "Start Ship Dt",
            "Cancel Date": "Exp Rec Dt",
            "Qty Ordered": "unitsord",
            "Unit of Measure": "",
            "Unit Price": "Cost",
            "Buyers Catalog or Stock Keeping #": "sku",
            # "UPC/EAN": "",
            "Vendor Style": "model#",
            "Product/Item Description": "description",
            "PO Total Amount": "Total - unit",
            # "PO Total Weight": "",
        }

        f = open(Path(__file__).resolve().parent.parent / "config/field_names_SalesImport_original.json")
        self.field_names = json.load(f)
        self.field_names_temp = []

        for item in self.field_names:
            self.field_names_temp.append(item) 

        for item in self.field_names_temp:
            if item in list(self.pair.keys()):
                (self.field_names).remove(item)

    def match_plain(self, input):
        res = []

        for i, _ in enumerate(input):
            pdf = input[f"PDF{i}"]

            for j, _ in enumerate(pdf):
                res.append(pdf[f"page{j}"])

        return res
    
    def match_date(self, input: str):
        temp = input.split("/")
        if temp[0] in "123456789":
            temp[0] = "0" + temp[0]
        temp[2] = "20" + temp[2]

        return "/".join(temp)
    
    def match_same(self, input):
        self.initial_part_init()

        for key in self.pair:
            if key == "PO Number":
                input[key] = [input[self.pair[key]]]

                for _ in range(self.length - 1): 
                    input[key].append(input[self.pair[key]])

                input["Retailers PO"] = [input[self.pair[key]]]

                for _ in range(self.length - 1): 
                    input["Retailers PO"].append("")

                del input[self.pair[key]]

            elif key == "PO Date":
                input[key] = [self.match_date(input[self.pair[key]])]

                for _ in range(self.length - 1):
                    input[key].append("")

                del input[self.pair[key]]

            elif key == "Ship Dates":
                input[key] = [self.match_date(input[self.pair[key]])]

                for _ in range(self.length - 1):
                    input[key].append("")

                del input[self.pair[key]]

            elif key == "Cancel Date":
                input[key] = [self.match_date(input[self.pair[key]])]

                for _ in range(self.length - 1):
                    input[key].append("")

                del input[self.pair[key]]

            elif key == "Qty Ordered":
                input[key] = [""]

                input[key].extend(input[self.pair[key]])
                
                del input[self.pair[key]]
            
            elif key == "Unit of Measure":
                input[key] = [""]

                for _ in range(self.length - 1):
                    input[key].append("Each")

                #There is non-key to delete

            elif key == "Unit Price":
                input[key] = [""]

                input[key].extend(input[self.pair[key]])
                # for _ in range(self.length - 1):
                #     input[key].append(input[self.pair[key]])

                del input[self.pair[key]]
            
            elif key == "Buyers Catalog or Stock Keeping #":
                input[key] = [""]

                input[key].extend(input[self.pair[key]])
                # for _ in range(self.length - 1):
                #     input[key].append(input[self.pair[key]])

                del input[self.pair[key]]

            elif key == "Vendor Style":
                input[key] = [""]

                input[key].extend(input[self.pair[key]])
                # for _ in range(self.length - 1):
                #     input[key].append(input[self.pair[key]])

                del input[self.pair[key]]
            elif key == "Product/Item Description":
                input[key] = [""]

                input[key].extend(input[self.pair[key]])
                # for _ in range(self.length - 1):
                #     input[key].append(input[self.pair[key]])

                del input[self.pair[key]]
            
            elif key == "PO Total Amount":
                input[key] = [input[self.pair[key]]]

                for _ in range(self.length - 1):
                    input[key].append(input[self.pair[key]])

                del input[self.pair[key]]

        return input
        
    def match_final(self, PO_res):
        # return final result
        output = self.match_plain(PO_res)
        
        # get PO_res keys
        self.PO_keys = list(output[0].keys())
        self.PO_inherited = []

        for key in self.pair:
            self.PO_inherited.append(self.pair[key])

        for content in output:
            self.length = len(content["Ln"]) + 1

            item = self.match_same(content)
            item = self.match_formula(item)
            
            for key in self.PO_keys:
                if key not in self.PO_inherited:
                    del item[key]

        df = pd.DataFrame(output[0])
        df.to_excel("sales_origin.xlsx")

        return output
    
class PO_Match_ORBICO(PO_Match):
    def __init__(self) -> None:
        self.PO_keys = []
        self.length = 2
        self.pair = {
            "PO Number": "No.:",
            "PO Date": "Date:",
            # "Ship Dates": "",
            # "Cancel Date": "",
            "Qty Ordered": "Qty pcs",
            "Unit of Measure": "",
            "Unit Price": "Unit Prices",
            "Buyers Catalog or Stock Keeping #": "Item no.",
            # "UPC/EAN": "",
            # "Vendor Style": "",
            "Product/Item Description": "Description",
            "PO Total Amount": "Total:",
            # "PO Total Weight": "",
        }

        f = open(Path(__file__).resolve().parent.parent / "config/field_names_SalesImport_original.json")
        self.field_names = json.load(f)
        self.field_names_temp = []

        for item in self.field_names:
            self.field_names_temp.append(item) 

        for item in self.field_names_temp:
            if item in list(self.pair.keys()):
                (self.field_names).remove(item)
    
    def match_spaceremover(self, input):
        for i, _ in enumerate(input):
            input[i] = input[i].replace(" ", "")
        
        return input

    def match_chRemover(self, input):
        for i, _ in enumerate(input):
            input[i] = input[i].replace(",", ".").replace("$", "")

        return input

    def match_plain(self, input):
        res = []

        for i, _ in enumerate(input):
            pdf = input[f"PDF{i}"]

            for j, _ in enumerate(pdf):
                res.append(pdf[f"page{j}"])

        return res
    
    def match_same(self, input):
        self.initial_part_init()

        for key in self.pair:
            if key == "PO Number":
                input[key] = [input[self.pair[key]]]

                for _ in range(self.length - 1): 
                    input[key].append(input[self.pair[key]])

                input["Retailers PO"] = [input[self.pair[key]]]

                for _ in range(self.length - 1): 
                    input["Retailers PO"].append("")

                del input[self.pair[key]]

            elif key == "PO Date":
                input[key] = [input[self.pair[key]]]

                for _ in range(self.length - 1):
                    input[key].append("")

                del input[self.pair[key]]

            elif key == "Qty Ordered":
                input[key] = [""]

                input[key].extend(self.match_spaceremover(input[self.pair[key]]))
                
                del input[self.pair[key]]

            elif key == "Unit of Measure":
                input[key] = [""]

                for _ in range(self.length - 1):
                    input[key].append("Each")

                #There is non-key to delete

            elif key == "Unit Price":
                input[key] = [""]

                input[key].extend(self.match_chRemover(input[self.pair[key]]))
                # for _ in range(self.length - 1):
                #     input[key].append(input[self.pair[key]])

                del input[self.pair[key]]

            elif key == "Buyers Catalog or Stock Keeping #":
                input[key] = [""]

                input[key].extend(input[self.pair[key]])
                # for _ in range(self.length - 1):
                #     input[key].append(input[self.pair[key]])

                del input[self.pair[key]]
                
            elif key == "Product/Item Description":
                input[key] = [""]

                input[key].extend(input[self.pair[key]])
                # for _ in range(self.length - 1):
                #     input[key].append(input[self.pair[key]])

                del input[self.pair[key]]

            elif key == "PO Total Amount":
                input[key] = [input[self.pair[key]]]

                for _ in range(self.length - 1):
                    input[key].append(input[self.pair[key]])

                del input[self.pair[key]]

        return input
    
    def match_final(self, PO_res):
        # return final result
        output = self.match_plain(PO_res)
        
        # get PO_res keys
        self.PO_keys = list(output[0].keys())
        self.PO_inherited = []

        for key in self.pair:
            self.PO_inherited.append(self.pair[key])

        for content in output:
            self.length = len(content["Description"]) + 1

            item = self.match_same(content)
            item = self.match_formula(item)
            
            for key in self.PO_keys:
                if key not in self.PO_inherited:
                    del item[key]

        df = pd.DataFrame(output[0])
        df.to_excel("sales_origin.xlsx")

        return output

class PO_Match_EXCEL(PO_Match):
    def __init__(self) -> None:
        self.PO_keys = []
        self.length = 2
        self.pair = {
            "PO Number": "Invoice Number",
            "PO Date": "PO Date",
            "Ship Dates": "Requested Ship / Delivery Date",
            # "Cancel Date": "",
            "Qty Ordered": "Qty Ordered",
            "Unit of Measure": "Unit of Measure",
            "Unit Price": "Unit Price",
            "Buyers Catalog or Stock Keeping #": "Buyer's Catalog or Stock Keeping #",
            "UPC/EAN": "UPC/EAN",
            "Vendor Style": "Vendor Style",
            "Product/Item Description": "Product/Item Description",
            "PO Total Amount": "Invoice Total",
            # "PO Total Weight": "",
            "Ship To Location": "Ship To Location",
            "Payment Terms Net Days": "Payment Terms Net Days",
            "Ship To Name": "Ship To Name",
            "Ship To Address 1": "Ship To Address 1",
            "Ship To Address 2": "Ship to address 2",				
            "Ship To City":	"Ship to City",			
            "Ship To State": "Ship To State",
            "Ship to Zip": "Ship to Zip",
            "Ship To Country": "Ship To ctry"
        }
        f = open(Path(__file__).resolve().parent.parent / "config/field_names_SalesImport_original.json")
        self.field_names = json.load(f)
        self.field_names_temp = []
        for item in self.field_names:
            self.field_names_temp.append(item) 
        for item in self.field_names_temp:
            a = list(self.pair.keys())
            if item in list(self.pair.keys()):
                (self.field_names).remove(item)
                
    def match_convTstr(self, input: list):
        temp = []

        for item in input:
            try:
                c = math.isnan(item)
            except:
                c = False
            
            if c:
                temp.append("")
            else:
                temp.append(str(item))

        return temp
    
    def match_same(self, input):
        self.initial_part_init()

        for key in self.pair:
            if key == "PO Number":
                input[key] = input[self.pair[key]]

                input["Retailers PO"] = [input[self.pair[key]][0]]

                for _ in range(self.length - 1): 
                    input["Retailers PO"].append("")

                del input[self.pair[key]]

            elif key in ["PO Date", "Ship Dates", "PO Total Amount", "Ship To Location", "Payment Terms Net Days", "Ship To Name", "Ship To Address 1", "Ship To Address 2", "Ship To City", "Ship To State", "Ship to Zip", "Ship To Country"]:
                input[key] = [input[self.pair[key]][0]]

                for _ in range(self.length - 1):
                    input[key].append("")

                if key not in ["PO Date", "Ship To Location", "Payment Terms Net Days", "Ship To Name", "Ship To Address 1", "Ship To State", "Ship to Zip"]:
                    del input[self.pair[key]]
            
            elif key in ["Qty Ordered", "Unit of Measure", "Unit Price", "Buyers Catalog or Stock Keeping #", "UPC/EAN", "Vendor Style", "Product/Item Description"]:
                if key in ["Buyers Catalog or Stock Keeping #"]:
                    temp = []
                    for value in input[self.pair[key]]:
                        try:
                            temp.append(int(float(value)))
                        except:
                            temp.append("")
                    input[key] = temp
                else:
                    input[key] = input[self.pair[key]]

                if key in ["Buyers Catalog or Stock Keeping #"]:
                    del input[self.pair[key]]

        # for key in input.keys():
        #     if key not in list(self.pair.keys()) and key in self.field_names:
        #         input[key] = self.match_convTstr(input[key])
        #         input[key].insert(0, "")

        return input
    
    def match_formula(self, input):
        temp_key = input.keys()

        for item in self.field_names:
            if item not in temp_key or item not in self.PO_inherited:
                temp = []
                
                for _ in range(self.length):
                    temp.append("")
                
                try:
                    del input[item]
                except:
                    pass

                input.update({item: temp})
            
        return input
    
    def __init__(self) -> None:
        self.PO_keys = []
        self.length = 2
        self.pair = {
            "PO Number": "Invoice Number",
            "PO Date": "PO Date",
            "Ship Dates": "Requested Ship / Delivery Date",
            # "Cancel Date": "",
            "Qty Ordered": "Qty Ordered",
            "Unit of Measure": "Unit of Measure",
            "Unit Price": "Unit Price",
            "Buyers Catalog or Stock Keeping #": "Buyer's Catalog or Stock Keeping #",
            "UPC/EAN": "UPC/EAN",
            "Vendor Style": "Vendor Style",
            "Product/Item Description": "Product/Item Description",
            "PO Total Amount": "Invoice Total",
            # "PO Total Weight": "",
            "Ship To Location": "Ship To Location",
            "Payment Terms Net Days": "Payment Terms Net Days",
            "Ship To Name": "Ship To Name",
            "Ship To Address 1": "Ship To Address 1",
            "Ship To Address 2": "Ship to address 2",				
            "Ship To City":	"Ship to City",			
            "Ship To State": "Ship To State",
            "Ship to Zip": "Ship to Zip",
            "Ship To Country": "Ship To ctry"
        }
        f = open(Path(__file__).resolve().parent.parent / "config/field_names_SalesImport_original.json")
        self.field_names = json.load(f)
        self.field_names_temp = []
        for item in self.field_names:
            self.field_names_temp.append(item) 
        for item in self.field_names_temp:
            a = list(self.pair.keys())
            if item in list(self.pair.keys()):
                (self.field_names).remove(item)
                
    def match_convTstr(self, input: list):
        temp = []

        for item in input:
            try:
                c = math.isnan(item)
            except:
                c = False
            
            if c:
                temp.append("")
            else:
                temp.append(str(item))

        return temp
    
    def match_same(self, input):
        self.initial_part_init()

        for key in self.pair:
            if key == "PO Number":
                input[key] = input[self.pair[key]]

                input["Retailers PO"] = [input[self.pair[key]][0]]

                for _ in range(self.length - 1): 
                    input["Retailers PO"].append("")

                del input[self.pair[key]]

            elif key in ["PO Date", "Ship Dates", "PO Total Amount", "Ship To Location", "Payment Terms Net Days", "Ship To Name", "Ship To Address 1", "Ship To Address 2", "Ship To City", "Ship To State", "Ship to Zip", "Ship To Country"]:
                input[key] = [input[self.pair[key]][0]]

                for _ in range(self.length - 1):
                    input[key].append("")

                if key not in ["PO Date", "Ship To Location", "Payment Terms Net Days", "Ship To Name", "Ship To Address 1", "Ship To State", "Ship to Zip"]:
                    del input[self.pair[key]]
            
            elif key in ["Qty Ordered", "Unit of Measure", "Unit Price", "Buyers Catalog or Stock Keeping #", "UPC/EAN", "Vendor Style", "Product/Item Description"]:
                if key in ["Buyers Catalog or Stock Keeping #"]:
                    temp = []
                    for value in input[self.pair[key]]:
                        try:
                            temp.append(int(float(value)))
                        except:
                            temp.append("")
                    input[key] = temp
                else:
                    input[key] = input[self.pair[key]]

                if key in ["Buyers Catalog or Stock Keeping #"]:
                    del input[self.pair[key]]

        # for key in input.keys():
        #     if key not in list(self.pair.keys()) and key in self.field_names:
        #         input[key] = self.match_convTstr(input[key])
        #         input[key].insert(0, "")

        return input
    
    def match_formula(self, input):
        temp_key = input.keys()

        for item in self.field_names:
            if item not in temp_key or item not in self.PO_inherited:
                temp = []
                
                for _ in range(self.length):
                    temp.append("")
                
                try:
                    del input[item]
                except:
                    pass

                input.update({item: temp})
            
        return input
    
    def match_final(self, PO_res):
        print(PO_res)
        if len(PO_res[0].keys()) > 100:
            print(len(PO_res[0].keys()), "=======================")
            df = pd.DataFrame(PO_res[0])
            df.to_excel("sales_origin.xlsx")
            return PO_res
        else:
            # get PO_res keys
            self.PO_keys = list(PO_res[0].keys())
            self.PO_inherited = []

            for key in self.pair:
                self.PO_inherited.append(self.pair[key])

            temp = []
            for key in self.PO_keys:
                if key not in self.PO_inherited and key in self.field_names:
                    temp.append(key)
            
            self.PO_inherited.extend(temp)

            for content in PO_res:
                self.length = len(content[list(content.keys())[0]])

                item = self.match_same(content)
                item = self.match_formula(item)

                for key in self.PO_keys:
                    if key not in self.PO_inherited:
                        del item[key]

            print(len(PO_res[0].keys()))
            print("*****************************")
            for key, item in PO_res[0].items():
                print(key, ": ", len(item))
            df = pd.DataFrame(PO_res[0])
            df.to_excel("sales_origin.xlsx")

            return PO_res
class PO_Match_CVS(PO_Match):
    def __init__(self) -> None:
        self.PO_keys = []
        self.length = 2
        self.pair = {
            "PO Number": "PO Number",
            "PO Date": "PO Date",
            "Ship Dates": "Requested Ship / Delivery Date",
            "Cancel Date": "Cancel Date",
            "Qty Ordered": "Qty Ordered",
            "Unit of Measure": "Unit of Measure",
            "Unit Price": "Unit Price",
            "Buyers Catalog or Stock Keeping #": "Purchasers Item Code",
            "UPC/EAN": "GTIN/UPC/EAN",
            # "Vendor Style": "",
            "Product/Item Description": "Product/Item Description",
            "PO Total Amount": "Total Amount Due",
            # "PO Total Weight": "",
            "Dept #": "Dept #",
            "Ship To Name": "Ship To Location",
            "Payment Terms %": "Payment Terms %",
            "Payment Terms Net Days": "Payment Terms Net Days",
            "Payment Terms Net Days": "Payment Terms Net Days",
            "Payment Terms Disc Amt": "Payment Terms Disc Amt",
            "Ship To Address 1": "Ship To Address",
            "Ship To City": "Ship To City",
            "Ship To State": "Ship To State",
            "Ship to Zip": "Ship to Zip",
        }

        f = open(Path(__file__).resolve().parent.parent / "config/field_names_SalesImport_original.json")
        self.field_names = json.load(f)
        self.field_names_temp = []

        for item in self.field_names:
            self.field_names_temp.append(item) 

        for item in self.field_names_temp:
            if item in list(self.pair.keys()):
                (self.field_names).remove(item)

    def match_convTstr(self, input: list):
        temp = []

        for item in input:
            try:
                c = math.isnan(item)
            except:
                c = False
            
            if c:
                temp.append("")
            else:
                temp.append(str(item))

        return temp
    
    def match_same(self, input):
        self.initial_part_init()

        for key in self.pair:
            if key == "Ship Dates":
                input[key] = [str(input[self.pair[key]][0])]
                input["Retailers PO"] = [str(input[self.pair[key]][0])]

                for _ in range(self.length):
                    input[key].append(str(input[self.pair[key]][0]))
                    input["Retailers PO"].append("")
                
                del input[self.pair[key]]

            elif key == "UPC/EAN":
                input[key] = [""]

                for i in range(self.length):
                    input[key].append(str(input[self.pair[key]][i]))

                del input[self.pair[key]]
            
            elif key in ["PO Total Amount", "Ship To Address 1"]:
                input[key] = [str(input[self.pair[key]][0])]

                for _ in range(self.length):
                    input[key].append("")

                del input[self.pair[key]]
            
            elif key in ["PO Number", "Dept #"]:
                temp = input[key]
                input[key] = [str(temp[0])]

                for _ in range(self.length):
                    input[key].append(str(temp[0]))

            elif key in ["PO Date", "Cancel Date", "Ship To Name", "Payment Terms %", "Payment Terms Net Days", "Payment Terms Net Days", "Payment Terms Disc Amt", "Ship To City", "Ship To State", "Ship to Zip"]:
                if key == "Ship To Name":
                    temp = "CVS - " + str(input[self.pair[key]][0])
                else:
                    temp = str(input[self.pair[key]][0])
                input[key] = [temp]

                for _ in range(self.length):
                    input[key].append("")
                
            elif key == "Buyers Catalog or Stock Keeping #":
                input[key] = [""]

                input[key].extend(self.match_convTstr(input[self.pair[key]]))

                del input[self.pair[key]]

            elif key in ["Qty Ordered", "Unit of Measure", "Unit Price", "Product/Item Description"]:
                temp = []
                for item in input[key]:
                    temp.append(str(item))
                input[key] = [""]
                input[key].extend(temp)
        
        for key in input.keys():
            if key not in list(self.pair.keys()) and key in self.field_names:
                input[key] = self.match_convTstr(input[key])
                input[key].insert(0, "")

        return [input, temp]
    
    def match_formula(self, input):
        temp_key = input.keys()

        for item in self.field_names:
            if item not in temp_key or item not in self.PO_inherited:
                temp = []
                
                for _ in range(self.length + 1):
                    temp.append("")
                
                try:
                    del input[item]
                except:
                    pass

                input.update({item: temp})
            
        return input
    
    def match_final(self, PO_res):
        # get PO_res keys
        self.PO_keys = list(PO_res[0].keys())
        self.PO_inherited = []

        for key in self.pair:
            self.PO_inherited.append(self.pair[key])

        temp = []
        for key in self.PO_keys:
            if key not in self.PO_inherited and key in self.field_names:
                temp.append(key)
        
        self.PO_inherited.extend(temp)

        for content in PO_res:
            self.length = len(content[list(content.keys())[0]])
            item = self.match_same(content)[0]
            item = self.match_formula(item)

            for key in self.PO_keys:
                if key not in self.PO_inherited:
                    del item[key]
        
        df = pd.DataFrame(PO_res[0])
        df.to_excel("sales_origin.xlsx")

        return PO_res
    
class PO_Match_GiantTiger(PO_Match):
    def __init__(self) -> None:
        self.PO_keys = []
        self.length = 2
        self.pair = {
            "PO Number": "Purchase Order #",
            "PO Date": "Order Date",
            "Ship Dates": "Original Delivery to CFS",
            "Cancel Date": "Cancel date",
            "Qty Ordered": "Order Qty",
            "Unit of Measure": "",
            "Unit Price": "FOB(USD)",
            "Buyers Catalog or Stock Keeping #": "G.T. SKU",
            "UPC/EAN": "UPC Code",
            # "Vendor Style": "",
            # "Product/Item Description": "Description",
            "PO Total Amount": "Total Amount",
            # "PO Total Weight": "",
        }

        f = open(Path(__file__).resolve().parent.parent / "config/field_names_SalesImport_original.json")
        self.field_names = json.load(f)
        self.field_names_temp = []

        for item in self.field_names:
            self.field_names_temp.append(item) 

        for item in self.field_names_temp:
            if item in list(self.pair.keys()):
                (self.field_names).remove(item)

    def match_plain(self, input):
        res = []

        for i, _ in enumerate(input):
            pdf = input[f"PDF{i}"]

            for j, _ in enumerate(pdf):
                res.append(pdf[f"page{j}"])

        return res
    
    def match_same(self, input):
        self.initial_part_init()

        for key in self.pair:
            if key == "PO Number":
                input[key] = [input[self.pair[key]]]

                for _ in range(self.length - 1): 
                    input[key].append(input[self.pair[key]])

                input["Retailers PO"] = [input[self.pair[key]]]

                for _ in range(self.length - 1): 
                    input["Retailers PO"].append("")

                del input[self.pair[key]]

            elif key == "PO Date":
                temp = [input[self.pair[key]].split('/')[i] for i in [0, 1, 2]]
                temp[2] = '20' + str(temp[2])
                if int(temp[0]) in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
                    temp[0] = '0' + str(temp[0])
                date = '/'.join(temp)
                input[key] = [date]

                for _ in range(self.length - 1):
                    input[key].append("")

                del input[self.pair[key]]
            
            elif key == "Ship Dates":
                temp = [input[self.pair[key]].split('/')[i] for i in [0, 1, 2]]
                temp[2] = '20' + str(temp[2])
                if int(temp[0]) in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
                    temp[0] = '0' + str(temp[0])
                date = '/'.join(temp)
                input[key] = [date]

                for _ in range(self.length - 1):
                    input[key].append("")

                del input[self.pair[key]]

            elif key == "Cancel Date":
                temp = [input[self.pair[key]].split('/')[i] for i in [0, 1, 2]]
                temp[2] = '20' + str(temp[2])
                if int(temp[0]) in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
                    temp[0] = '0' + str(temp[0])
                date = '/'.join(temp)
                input[key] = [date]

                for _ in range(self.length - 1):
                    input[key].append("")

                del input[self.pair[key]]

            elif key == "Qty Ordered":
                input[key] = [""]

                input[key].append(input[self.pair[key]])
                
                del input[self.pair[key]]

            elif key == "Unit of Measure":
                input[key] = [""]

                for _ in range(self.length - 1):
                    input[key].append("Each")

                #There is non-key to delete

            elif key == "Unit Price":
                input[key] = [""]

                input[key].append(input[self.pair[key]])
                # for _ in range(self.length - 1):
                #     input[key].append(input[self.pair[key]])

                del input[self.pair[key]]

            elif key == "Buyers Catalog or Stock Keeping #":
                input[key] = [""]

                input[key].append(input[self.pair[key]])
                # for _ in range(self.length - 1):
                #     input[key].append(input[self.pair[key]])

                del input[self.pair[key]]

            elif key == "Qty Ordered":
                input[key] = [""]

                input[key].append(input[self.pair[key]])
                
                del input[self.pair[key]]

            elif key == "PO Total Amount":
                input[key] = [input[self.pair[key]]]

                for _ in range(self.length - 1):
                    input[key].append(input[self.pair[key]])

                del input[self.pair[key]]

            elif key == "UPC/EAN":
                input[key] = [""]
                for _ in range(self.length - 1):
                    input[key].append(input[self.pair[key]])

                del input[self.pair[key]]

        return input

    def match_final(self, PO_res):
        # return final result
        output = self.match_plain(PO_res)
        
        # get PO_res keys
        self.PO_keys = list(output[0].keys())
        self.PO_inherited = []

        for key in self.pair:
            self.PO_inherited.append(self.pair[key])

        for content in output:
            item = self.match_same(content)
            item = self.match_formula(item)
            
            for key in self.PO_keys:
                if key not in self.PO_inherited:
                    del item[key]

        df = pd.DataFrame(output[0])
        df.to_excel("sales_origin.xlsx")

        return output
    
class PO_Match_HOBBYlobby(PO_Match):
    def __init__(self) -> None:
        self.PO_keys = []
        self.length = 2
        self.pair = {
            "PO Number": "Our Purchase Order#: ",
            # "PO Date": "Order Date",
            "Ship Dates": "Ship Date: ",
            "Cancel Date": "Cancel Date: ",
            "Qty Ordered": "QTY",
            "Unit of Measure": "",
            "Unit Price": "1ST COST",
            "Buyers Catalog or Stock Keeping #": "SKU",
            # "UPC/EAN": "UPC Code",
            # "Vendor Style": "",
            # "Product/Item Description": "Description",
            "PO Total Amount": "EXT COST",
            # "PO Total Weight": "",
        }

        f = open(Path(__file__).resolve().parent.parent / "config/field_names_SalesImport_original.json")
        self.field_names = json.load(f)
        self.field_names_temp = []

        for item in self.field_names:
            self.field_names_temp.append(item) 

        for item in self.field_names_temp:
            if item in list(self.pair.keys()):
                (self.field_names).remove(item)

    def match_plain(self, input):
        res = []

        for i, _ in enumerate(input):
            pdf = input[f"PDF{i}"]

            for j, _ in enumerate(pdf):
                res.append(pdf[f"page{j}"])

        return res
    
    def match_date(self, input: str):
        return "/".join([input.split("-")[i] for i in [1, 2, 0]])
    
    def match_same(self, input):
        self.initial_part_init()

        for key in self.pair:
            if key == "PO Number":
                input[key] = [input[self.pair[key]]]

                for _ in range(self.length - 1): 
                    input[key].append(input[self.pair[key]])

                input["Retailers PO"] = [input[self.pair[key]]]

                for _ in range(self.length - 1): 
                    input["Retailers PO"].append("")

                del input[self.pair[key]]
            
            elif key in ["Ship Dates", "Cancel Date"]:
                input[key] = [self.match_date(input[self.pair[key]])]

                for _ in range(self.length - 1):
                    input[key].append("")

                del input[self.pair[key]]
            
            elif key in ["Qty Ordered", "Buyers Catalog or Stock Keeping #"]:
                input[key] = [""]

                for _ in range(self.length - 1):
                    if key == "Buyers Catalog or Stock Keeping #":
                        input[key].append(re.findall(r'\d+', input[self.pair[key]])[0])
                    else:
                        input[key].append(input[self.pair[key]])

                del input[self.pair[key]]

            elif key == "Unit Price":
                input[key] = [""]

                for _ in range(self.length - 1):
                    input[key].append(input[self.pair[key]].replace("$", ""))

                del input[self.pair[key]]

            elif key == "PO Total Amount":
                input[key] = [re.sub('[$,]', '', input[self.pair[key]])]

                for _ in range(self.length - 1):
                    input[key].append("")

                del input[self.pair[key]]

        return input


    def match_final(self, PO_res):
        # return final result
        output = self.match_plain(PO_res)
        
        # get PO_res keys
        self.PO_keys = list(output[0].keys())
        self.PO_inherited = []

        for key in self.pair:
            self.PO_inherited.append(self.pair[key])

        for content in output:
            item = self.match_same(content)
            item = self.match_formula(item)
            
            for key in self.PO_keys:
                if key not in self.PO_inherited:
                    del item[key]

        df = pd.DataFrame(output[0])
        df.to_excel("sales_origin.xlsx")

        return output
    
class PO_Match_Lekia(PO_Match):
    def __init__(self) -> None:
        self.PO_keys = []
        self.length = 2
        self.pair = {
            "PO Number": "Purchase No.",
            "PO Date": "Purchase date",
            "Ship Dates": "Requested Delivery Date",
            # "Cancel Date": "Cancel Date: ",
            "Qty Ordered": "Quantity Unit",
            "Unit of Measure": "",
            "Unit Price": "Price/unit",
            # "Buyers Catalog or Stock Keeping #": "SKU",
            "Payment Terms Net Days": "Payment terms",
            # "UPC/EAN": "UPC Code",
            "Vendor Style": "Item",
            # "Product/Item Description": "Description",
            # "PO Total Amount": "EXT COST",
            # "PO Total Weight": "",
        }

        f = open(Path(__file__).resolve().parent.parent / "config/field_names_SalesImport_original.json")
        self.field_names = json.load(f)
        self.field_names_temp = []

        for item in self.field_names:
            self.field_names_temp.append(item) 

        for item in self.field_names_temp:
            if item in list(self.pair.keys()):
                (self.field_names).remove(item)

    def match_plain(self, input):
        res = []

        for i, _ in enumerate(input):
            pdf = input[f"PDF{i}"]

            for j, _ in enumerate(pdf):
                res.append(pdf[f"page{j}"])

        return res
    
    def match_date(self, input: str):
        return "/".join([input.split("-")[i] for i in [1, 2, 0]])
    
    def match_same(self, input):
        self.initial_part_init()

        for key in self.pair:
            if key == "PO Number":
                input[key] = [input[self.pair[key]]]

                for _ in range(self.length - 1): 
                    input[key].append(input[self.pair[key]])

                input["Retailers PO"] = [input[self.pair[key]]]

                for _ in range(self.length - 1): 
                    input["Retailers PO"].append("")

                del input[self.pair[key]]
            
            elif key in ["Ship Dates", "PO Date", "Payment Terms Net Days"]:
                if key in ["Ship Dates", "PO Date"]:
                    input[key] = [self.match_date(input[self.pair[key]])]
                
                else:
                    input[key] = [input[self.pair[key]]]

                for _ in range(self.length - 1):
                    input[key].append("")

                del input[self.pair[key]]

            elif key in ["Unit Price", "Qty Ordered", "Vendor Style"]:
                input[key] = [""]

                if key == "Unit Price":
                    for i in range(self.length - 1):
                        input[key].append(input[self.pair[key]][i].replace(",", "."))

                elif key == "Qty Ordered":
                    for i in range(self.length - 1):
                        input[key].append(input[self.pair[key]][i].replace("pcs", ""))

                elif key == "Vendor Style":
                    for i in range(self.length - 1):
                        # if input[self.pair[key]][i][0] == '0':
                        #     input[key].append(input[self.pair[key]][i][1:])
                        # else:
                            input[key].append(input[self.pair[key]][i])

                del input[self.pair[key]]

            elif key == "Unit of Measure":
                input[key] = [""]

                for _ in range(self.length - 1):
                    input[key].append("Each")

                #There is non-key to delete

        return input
    
    def match_final(self, PO_res):
        # return final result
        output = self.match_plain(PO_res)
        
        # get PO_res keys
        self.PO_keys = list(output[0].keys())
        self.PO_inherited = []

        for key in self.pair:
            self.PO_inherited.append(self.pair[key])

        for content in output:
            self.length = len(content[list(content.keys())[5]]) + 1

            item = self.match_same(content)
            item = self.match_formula(item)
            
            for key in self.PO_keys:
                if key not in self.PO_inherited:
                    del item[key]

        df = pd.DataFrame(output[0])
        df.to_excel("sales_origin.xlsx")

        return output