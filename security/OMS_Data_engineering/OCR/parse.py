import pdfplumber
import re
import pandas as pd
from openpyxl import load_workbook
import xlsxwriter
import os
import numpy as np
import math


# PDF Parsing for Bucee's
class BUCEE_Parsing_PDF:
    def __init__(self) -> None:
        self.keys = ['LINE', 'SKU', 'VENDOR PN', 'UPC/GTIN', 'DESCRIPTIONLINE ITEM COMMENTS', 'MARKS AND NUMBERS', 'UNIT COST/RETAIL PRICE', 'QTY', 'UOM', 'ITEMTOTAL', 'PO Date:', 'Requested Delivery Date:', 'Requested Ship Date:', 'Cancel Date:', 'Delivery Window:', 'Shipping Window:', 'Vendor #:', 'Department #:', 'Freight Terms:', 'Preferred Carrier:', 'Terms Type', 'Terms Basis:', 'Terms Disc\n%:', 'Disc. Due Date:', 'Disc. Days:', 'Net Due Date:', 'Net Days:', 'Description:', 'TYPE', 'SERVICE TYPE', 'PERCENT', 'RATE', 'QTY_', 'UOM_', 'DESCRIPTION', 'AMOUNT', 'Total Qty:', 'Weight:', 'Volume:', 'Purchase Order Total:', '280.80', 'Order #', "PO_currency", "Ship To Name", "Ship To Address 1", "Ship To City", "Ship To State", "Ship to Zip", "Ship To Country", "Buying Party Name"]


    def re_fun(self, str_input: str) -> dict:
        if str_input == None:
            return None
        loc = str_input.rfind(":")
        left, right = str_input[:loc] + str_input[loc], (str_input[loc:])[1:]
        
        return {left: right}
    
    def PO_parser(self, paths: list, currency):
        #this function will generate PO table
        res = {}
        
        for k, path in enumerate(paths):
            res[f"PDF{k}"] = {}
            pdf = pdfplumber.open(path)

            for page_num, page in enumerate(pdf.pages):
                res[f"PDF{k}"][f"page{page_num}"] = {}

                for key in self.keys:
                    res[f"PDF{k}"][f"page{page_num}"].update({key: []})
                
                #non main table addition
                non_product_tables = []
                ## non table addition
                non_table_content = []
                non_table_str = page.extract_text_simple()
                non_table_lis = non_table_str.split("\n")
                non_product_tables.append({"Order #": non_table_lis[4]})
                non_product_tables.append({"Ship To Name": "Buc" + non_table_lis[18].split("Buc")[1]})
                non_product_tables.append({"Ship To Address 1": non_table_lis[19]})
                non_product_tables.append({"Ship To City": non_table_lis[20].split(",")[0]})
                non_product_tables.append({"Ship To State": non_table_lis[20].split(",")[1].split(" ")[1]})
                non_product_tables.append({"Ship to Zip": non_table_lis[20].split(",")[1].split(" ")[2]})
                non_product_tables.append({"Ship To Country": non_table_lis[20].split(",")[1].split(" ")[3]})
                non_product_tables.append({"Buying Party Name":("Buc" + non_table_lis[18].split("Buc")[2]).split("Creative ")[0]})

                for i, table in enumerate(page.extract_tables()):
                    if i == 2:
                        product_table = table
                    if i != 2:
                        items = [item for sublist in table for item in sublist]
                        for item in items: 
                            if self.re_fun(item) == None:
                                continue
                            else:
                                non_product_tables.append(self.re_fun(item))

                non_product_dic = {}
                for dic in non_product_tables:
                    non_product_dic.update(dic)
                
                non_blank_keys = list(non_product_dic.keys())

                for key in self.keys:
                    if key == "UOM_":
                        res[f"PDF{k}"][f"page{page_num}"][key].append(non_product_dic["UOM"])
                    elif key == "QTY_":
                        res[f"PDF{k}"][f"page{page_num}"][key].append(non_product_dic["QTY"])
                    elif key == "PO_currency":
                        res[f"PDF{k}"][f"page{page_num}"][key].append("USD")
                    else:
                        if key in non_blank_keys:
                            res[f"PDF{k}"][f"page{page_num}"][key].append(non_product_dic[key])
                        else:
                            res[f"PDF{k}"][f"page{page_num}"][key].append("")

                # main table addition
                
                # product_keys = product_table[0]
                product_table_ = product_table[1 : len(product_table) - 1]
                product_keys = ['LINE', 'SKU', 'VENDOR PN', 'UPC/GTIN', 'DESCRIPTIONLINE ITEM COMMENTS', 'MARKS AND NUMBERS', 'UNIT COST/RETAIL PRICE', 'QTY', 'UOM', 'ITEMTOTAL']
                product_dic = {}
                for key in product_keys:
                    product_dic.update({key:[]})

                for i, line in enumerate(product_table_):
                    for i, key in enumerate(product_keys):
                        product_dic[key].append(line[i])
                for i in range(len(product_table_)):
                    for key in self.keys:
                        if key in product_keys:
                            res[f"PDF{k}"][f"page{page_num}"][key].append(product_dic[key][i])
                        else:
                            res[f"PDF{k}"][f"page{page_num}"][key].append("")
                temp_total = [product_table[len(product_table) - 1][9]]
                for _ in range(len(product_table) - 2):
                    temp_total.append("")
                res[f"PDF{k}"][f"page{page_num}"].update({"total": temp_total})

        if os.path.isfile("OCR_res.xlsx"):
            os.remove("OCR_res.xlsx")
        book = xlsxwriter.Workbook("OCR_res.xlsx")
        sheet = book.add_worksheet("cont_excel")
        for idx, header in enumerate(self.keys):
            sheet.write(0, idx, header)
        sheet.write(0, len(self.keys), "total")
        book.close()

        book = load_workbook("OCR_res.xlsx")
        sheet = book.get_sheet_by_name("cont_excel")
        for dic in res:
            for di in res[dic]:
                for i in range(len(res[dic][di]["LINE"])):
                    temp = []

                    for key in res[dic][di].keys():
                        temp.append(res[dic][di][key][i])

                    sheet.append(temp)


        book.save(filename = "OCR_res.xlsx")

        return res
    
class BUCEE_Parsing:
    def __init__(self, customer_name) -> None:
        self.keys = ["PO Number", "Release Number", "PO Date", "Dept #", "Retailers PO", "Requested Delivery Date", "Delivery Dates", "Ship Dates", "Cancel Date", "Carrier", "Carrier Details", "Ship To Location", "PO Line #", "Qty Ordered", "Unit of Measure", "Unit Price", "Buyers Catalog or Stock Keeping #", "UPC/EAN", "Vendor Style", "Retail Price", "Product/Item Description", "Color", "Size", "Pack Size", "Pack Size UOM", "Number of Inner Packs", "Number of Pcs per Inner Pack", "Store #", "Qty per Store #", "Record Type", "PO purpose", "PO Type", "Contract Number", "Currency", "Ship Status", "Letter of Credit", "Vendor #", "Division #", "Cust Acct #", "Customer Order #", "Promo #", "Ticket Description", "Other Info / #s", "Frt Terms", "Carrier Service Level", "Payment Terms %", "Payment Terms Disc Due Date", "Payment Terms Disc Days Due", "Payment Terms Net Due Date", "Payment Terms Net Days", "Payment Terms Disc Amt", "Payment Terms Desc", "Contact Phone", "Contact Fax", "Contact Email", "Allow/Charge Type", "Allow/Charge Service", "Allow/Charge Amt", "Allow/Charge %", "Allow/Charge Rate", "Allow/Charge Qty", "Allow/Charge Desc", "Ship To Name", "Ship To Address 1", "Ship To Address 2", "Ship To City", "Ship To State", "Ship to Zip", "Ship To Country", "Ship To Contact", "Bill To Name", "Bill To Address 1", "Bill To Address 2", "Bill To City", "Bill To State", "Bill To Zip", "Bill To Country", "Bill To Contact", "Buying Party Name", "Buying Party Location", "Buying Party Address 1", "Buying Party Address 2", "Buying Party City", "Buying Party State", "Buying Party Zip", "Buying Party Country", "Buying Party Contact", "Ultimate Location", "Notes/Comments", "Ship To Additional Name", "Ship To Additional Name 2", "Bill To Additional Name", "Bill To Additional Name 2", "Buyer Additional Name", "Buyer Additional Name 2", "GTIN", "PO Total Amount", "PO Total Weight ", "PO Total UOM ", "Shipping account number", "Mark for Name", "Mark for Address 1", "Mark for Address 2", "Mark for City", "Mark for State", "Mark for Postal", "Mark for Country", "Shipping Container Code", "National Drug Code", "Expiration Date", "Dist", "Scheduled Quantity", "Scheduled Qty UOM", "Required By Date", "Must Arrive By", "Entire Shipment", "Agreement Number", "Additional Vendor Part #", "Buyer Part Number", "Carrier Details Special Handling", "Restrictions/Conditions"]
        
    def PO_parser(self, paths: list, currency):
        res = []

        for k, path in enumerate(paths):
            try:
                pdf = pd.read_csv(path, encoding='ISO-8859-1')
            except:
                pdf = pd.read_excel(path)
            res.append([])
            lis = list(pdf[list(pdf.keys())[0]])
            lens = []
            init = lis[0]
            length = 0

            for item in lis:
                if init == item:
                    length = length  + 1
                
                else:
                    lens.append(length)
                    init = item
                    length = 1

            lens.append(length)
            steper = 0

            for num, length in enumerate(lens):
                res[k].append({})

                for key in self.keys:
                    res[k][num].update({
                        key: []
                    })

                for i in range(length):
                    if type(pdf.iloc[i + steper]["Dept #"]) != float:
                        for key, item in zip(self.keys, list(pdf.iloc[i + steper])[:-1]):
                            
                            if type(item) == np.int64:
                                res[k][num][key].append(int(item))
                            
                            elif type(item) != str:
                                if math.isnan(item):
                                    res[k][num][key].append("")
                                else:
                                    if key in ["Unit Price", "PO Total Amount"]:
                                        res[k][num][key].append(float(item))
                                    else:
                                        res[k][num][key].append(int(item))
                            else:
                                res[k][num][key].append(item)
                        # res[k][num].append(list(pdf.iloc[i + steper])[:-1])
                
                steper = steper + i + 1
        
        return res
# PDF Parsing for Pepco
class PEPCO_Parsing:
    def __init__(self, customer_name) -> None:
        self.keys = ["Order - ID", "Pre Order -ID", "Item No", "Item classification", "Item name", "Item name English", "Promotional product", "Supplier product code", "Season", "Merch code", "Collection", "Pictogram no", "Style type", "Supplier name", "Supplier ID", "Terms of payments", "Date of order creation", "Booking date", "Handover date", "Port of shipment", "Destination port", "Destination DC", "Delivery terms", "Transport mode", "Time of delivery", "Purchase price", "Total", "ONE", "Pack multiplier", "Total qty in outer", "barcode", "PO_currency"]
        pass

    def PO_parser(self, paths: list, currency):
        #this function will generate PO table
        res = {}

        for k, path in enumerate(paths):
            res[f"PDF{k}"] = {}
            pdf = pdfplumber.open(path)

            for key in self.keys:
                res[f"PDF{k}"].update({key: []})

            for page_num, page in enumerate(pdf.pages):
                if page_num == 0:
                    

                    content = page.extract_text_simple().split("\n")
                    if currency == "eur":
                        #title - 1
                        for i in range(13):
                            res[f"PDF{k}"][self.keys[i]].append(content[i + 5].split(".")[-1][1:])

                        res[f"PDF{k}"][self.keys[0]].append(content[0 + 5].split(".")[-1][1:])
                        
                        for i in range(1, 13):
                            res[f"PDF{k}"][self.keys[i]].insert(0, "")

                        #title - 2
                        for i in range(4):
                            res[f"PDF{k}"][self.keys[i + 13]].append(content[i + 19].split(".")[-1][1:])

                        for i in range(3):
                            res[f"PDF{k}"][self.keys[i + 13]].insert(0, "")
                        res[f"PDF{k}"][self.keys[3 + 13]].insert(1, "")

                        #title - 3
                        for i in range(8):
                            res[f"PDF{k}"][self.keys[i + 17]].append(content[i + 24].split(".")[-1][1:])
                        
                        for i in range(8):
                            if i == 0:
                                res[f"PDF{k}"][self.keys[i + 17]].insert(1, "")
                            elif i == 1:
                                res[f"PDF{k}"][self.keys[i + 17]].insert(1, "")
                            else:
                                res[f"PDF{k}"][self.keys[i + 17]].insert(0, "")

                    if currency == "usd":
                        #title - 1
                        for i in range(13):
                            res[f"PDF{k}"][self.keys[i]].append(content[i + 4].split(".")[-1][1:])

                        res[f"PDF{k}"][self.keys[0]].append(content[0 + 4].split(".")[-1][1:])

                        for i in range(1, 13):
                            res[f"PDF{k}"][self.keys[i]].insert(0, "")

                        #title - 2
                        for i in range(3):
                            res[f"PDF{k}"][self.keys[i + 13]].append(content[i + 18].split(".")[-1][1:])

                        res[f"PDF{k}"][self.keys[3 + 13]].append(content[21].split(":")[1])

                        for i in range(3):
                            res[f"PDF{k}"][self.keys[i + 13]].insert(0, "")
                        res[f"PDF{k}"][self.keys[3 + 13]].insert(1, "")

                        #title - 3
                        for i in range(7):
                            res[f"PDF{k}"][self.keys[i + 17]].append(content[i + 23].split(":")[-1])

                        res[f"PDF{k}"][self.keys[24]].append(":".join(content[30].split(":")[-3:]))

                        for i in range(7):
                            if i == 0:
                                res[f"PDF{k}"][self.keys[i + 17]].insert(1, "")
                            elif i == 1:
                                res[f"PDF{k}"][self.keys[i + 17]].insert(1, "")
                            else:
                                res[f"PDF{k}"][self.keys[i + 17]].insert(0, "")
                        
                        res[f"PDF{k}"][self.keys[24]].insert(0, "")

                if page_num == 1:
                    content = page.extract_text_simple().split("\n")

                    if currency == "eur":
                        res[f"PDF{k}"][self.keys[25]].append(" ".join(content[6].split(" ")[3]))
                        res[f"PDF{k}"][self.keys[25]].insert(1, "")

                        res[f"PDF{k}"][self.keys[26]].append(content[8].split(".")[-1][1:])
                        res[f"PDF{k}"][self.keys[26]].insert(0, "")

                        res[f"PDF{k}"]["PO_currency"].append(content[6].split(" ")[4])
                        res[f"PDF{k}"]["PO_currency"].append("")

                    if currency == "usd":
                        res[f"PDF{k}"][self.keys[25]].append(" ".join(content[5].split(" ")[2].split("\xa0")[0]))
                        res[f"PDF{k}"][self.keys[25]].insert(1, "")

                        res[f"PDF{k}"][self.keys[26]].append(content[7].split(".")[-1].replace("\xa0", "").replace(": ", ""))
                        res[f"PDF{k}"][self.keys[26]].insert(0, "")

                        res[f"PDF{k}"]["PO_currency"].append(content[5].split(" ")[2].split("\xa0")[1])
                        res[f"PDF{k}"]["PO_currency"].append("")
                if page_num == 2:
                    content = page.extract_text_simple().split("\n")
                    if currency == "eur":
                        res[f"PDF{k}"][self.keys[27]].append(content[13].split(" ")[1])
                        res[f"PDF{k}"][self.keys[27]].insert(0, "")

                        res[f"PDF{k}"][self.keys[28]].append(content[13].split(" ")[3])
                        res[f"PDF{k}"][self.keys[28]].insert(0, "")

                        res[f"PDF{k}"][self.keys[29]].append(content[13].split(" ")[4])
                        res[f"PDF{k}"][self.keys[29]].insert(0, "")

                        res[f"PDF{k}"][self.keys[30]].append(content[6].split(";")[1].split(":")[1][1:])
                        res[f"PDF{k}"][self.keys[30]].insert(0, "")
                    #USD
                    if currency == "usd":
                        res[f"PDF{k}"][self.keys[27]].append(content[10].split(" ")[1])
                        res[f"PDF{k}"][self.keys[27]].insert(0, "")

                        res[f"PDF{k}"][self.keys[28]].append(content[10].split(" ")[3])
                        res[f"PDF{k}"][self.keys[28]].insert(0, "")

                        res[f"PDF{k}"][self.keys[29]].append(content[10].split(" ")[4])
                        res[f"PDF{k}"][self.keys[29]].insert(0, "")
                        
                        res[f"PDF{k}"][self.keys[30]].append(content[5].split(";")[1].split(":")[1].split("\xa0")[1])
                        res[f"PDF{k}"][self.keys[30]].insert(0, "")
            
            

        if os.path.isfile("OCR_res.xlsx"):
            os.remove("OCR_res.xlsx")
        book = xlsxwriter.Workbook("OCR_res.xlsx")
        sheet = book.add_worksheet("cont_excel")
        for idx, header in enumerate(self.keys):
            sheet.write(0, idx, header)
        sheet.write(0, len(self.keys), "total")
        book.close()

        book = load_workbook("OCR_res.xlsx")
        sheet = book.get_sheet_by_name("cont_excel")
        for dic in res:
            for i in range(2):
                temp = []
                for key in res[dic].keys():
                    temp.append(res[dic][key][i])

                sheet.append(temp)


        book.save(filename = "OCR_res.xlsx")

        return res
    
#PDF Parsing for Additional Pepco (poundland & dealz)
class PEPCO_Add_Parsing:
    def __init__(self, customer_name) -> None:
        self.keys = ["Order Number", "Invoice", "RegisteredAddress", "Supplier name", "Terms of payment", "Supplier number", "Method of payment", "Address", "Buyer", "Order Contact", "Deliver to", "Delivery Date", "Delivery Terms", "Date of order creation", "Handover date", "Sku", "Vendor Product No", "Product Description", "Department", "Cost price currency", "Unit Cost price", "Case Price", "Case Quantity", "Total Case Qty", "Total Unit Qty", "Total Order Value", "Comments"]

    def PO_parser(self, paths: list, currency):
        res = {}

        for k, path in enumerate(paths):
            
            res[f"PDF{k}"] = {}
            pdf = pdfplumber.open(path)
            page_num = 0
            res[f"PDF{k}"][f"page{page_num}"] = {}

            page = pdf.pages[0]

            invoice_page = page.within_bbox([page.search("Order Number")[0]['x0'], page.search("Order Number")[0]['bottom'], page.search("Registered")[0]['x0'], page.search("Supplier details")[0]['top']])
            PO_page = page.within_bbox([page.search("Order Number")[0]['x0'], page.search("Order Number")[0]['top'], page.width, page.search("Order Number")[0]['bottom']])
            contact_page = page.within_bbox([page.search("Terms of payment")[0]['x0'], page.search("Terms of payment")[0]['top'] - 3, page.width, page.search("Order Contact")[0]['bottom']])
            deliver_page = page.within_bbox([page.search("Deliver to")[0]['x0'], page.search("Deliver to")[0]['top'], page.search("Delivery Date")[0]['x0'], page.search("Delivery Terms")[0]['top'], ])
            date_page = page.within_bbox([page.search("Date of order")[0]['x0'], page.search("Date of order")[0]['top'] - 1, page.width, page.search("Handover date")[0]['bottom']])
            product_page = page.within_bbox([0, page.search("Purchased Price")[0]['bottom'], page.width, page.search("Total Order Value")[0]['top']])
            product_page_table = product_page.extract_tables(dict(
                explicit_vertical_lines = [page.search("Purchased Price")[0]['x0'], page.search("Product No")[0]['x0'], page.search("Product No")[0]['x1'], page.search("Department")[0]['x0'] - 5, page.search("Cost price")[0]['x0'], page.search("Cost price")[0]['x1'], page.search("Cost price")[0]['x1'] + 50, page.search("Cost price")[0]['x1'] + 100, page.search("Total Case")[0]['x0'], page.search("Total Unit")[0]['x0'], page.search("Total Unit")[0]['x1']],
                explicit_horizontal_lines = [0, page.search("Purchased Price")[0]['bottom'], page.width, page.search("Total Order Value")[0]['top']]
            ))

            res[f"PDF{k}"][f"page{page_num}"]["Order Number"] = PO_page.extract_text().split("Order Number ")[1]
            res[f"PDF{k}"][f"page{page_num}"]["Terms of payment"] = contact_page.extract_text().split("\n")[0].split("Terms of payment ")[1]
            res[f"PDF{k}"][f"page{page_num}"]["Buyer"] = contact_page.extract_text().split("\n")[2].split("Buyer ")[1]
            res[f"PDF{k}"][f"page{page_num}"]["order_contact"] = contact_page.extract_text().split("\n")[3].split("Order Contact ")[1]
            res[f"PDF{k}"][f"page{page_num}"]["Handover date"] = date_page.extract_text().split("\n")[2].split("Handover date ")[1]
            res[f"PDF{k}"][f"page{page_num}"]["Sku"] = product_page_table[0][1][0]
            res[f"PDF{k}"][f"page{page_num}"]["Cost price currency"] = product_page_table[0][1][4]
            res[f"PDF{k}"][f"page{page_num}"]["Unit Cost price"] = product_page_table[0][1][5]
            res[f"PDF{k}"][f"page{page_num}"]["Total Unit Qty"] = product_page_table[0][1][-1]
            # res[f"PDF{k}"][f"page{page_num}"]["Comments"]
            res[f"PDF{k}"][f"page{page_num}"]["Date of order creation"] = date_page.extract_text().split("\n")[0].split("Date of order ")[1]
            res[f"PDF{k}"][f"page{page_num}"]["invoice"] = invoice_page.extract_text().split("\n")[1:]
            res[f"PDF{k}"][f"page{page_num}"]["deliver_to"] = deliver_page.extract_text().split("Deliver to ")[1].replace("\n", " ")

        # res = {}

        # for k, path in enumerate(paths):
        #     res[f"PDF{k}"] = {}
        #     pdf = pdfplumber.open(path)

        #     for page_num, page in enumerate(pdf.pages):
        #         if page_num == 0:
        #             res[f"PDF{k}"] = {}

        #             for key in self.keys:
        #                 res[f"PDF{k}"].update({key: []})

                    

        #             content = (page.extract_text_simple()).split("\n")
        #             if "Supplier detail" in content[8]:
        #                 variable = 1
        #             elif "Supplier detail" in content[7]:
        #                 variable = 0
                        
        #             res[f"PDF{k}"]["Order Number"].append(content[1].split("Order Number")[1][1:])
        #             res[f"PDF{k}"]["Supplier name"].append(content[variable + 8].split("Supplier name")[1].split("Terms of payment")[0][1:])
        #             res[f"PDF{k}"]["Terms of payment"].append(content[variable + 8].split("Supplier name")[1].split("Terms of payment")[1][1:])
        #             res[f"PDF{k}"]["Supplier number"].append(content[variable + 9].split("Supplier number")[1].split("Method of payment")[0][1:])
        #             res[f"PDF{k}"]["Method of payment"].append(content[variable + 9].split("Supplier number")[1].split("Method of payment")[1][1:])
        #             add_1 = content[variable + 10].split("Address")[1].split("Buyer")[0][1:]
        #             add_2 = content[variable + 11]
        #             add_3 = content[variable + 13]
        #             res[f"PDF{k}"]["Address"].append("@".join([add_1, add_2, add_3]))
        #             res[f"PDF{k}"]["Buyer"].append(content[variable + 10].split("Address")[1].split("Buyer")[1][1:])
        #             res[f"PDF{k}"]["Order Contact"].append(content[variable + 12].split("Order Contact")[1][1:])
        #             deliver_to_1 = content[variable + 15].split("Deliver to")[1][1:].split("Delivery Date")[0]
        #             deliver_to_2 = content[variable + 16]
        #             res[f"PDF{k}"]["Deliver to"].append("@".join([deliver_to_1, deliver_to_2]))
        #             res[f"PDF{k}"]["Delivery Date"].append(content[variable + 15].split("Deliver to")[1][1:].split("Delivery Date")[1][1:])
        #             res[f"PDF{k}"]["Delivery Terms"].append(content[variable + 17].split("Delivery Terms")[1][1:])
        #             res[f"PDF{k}"]["Date of order creation"].append(content[variable + 18].split("Date of order")[1].replace(" ", ""))
        #             res[f"PDF{k}"]["Handover date"].append(content[variable + 20].split("Handover date")[1].replace(" ", ""))
                    
        #             temp = content[variable + 25].split(" ")

        #             for i, item in enumerate(temp):
        #                 if item == '':
        #                     temp.pop(i)

        #             res[f"PDF{k}"]["Total Unit Qty"].append(temp[10])
        #             res[f"PDF{k}"]["Total Case Qty"].append(temp[9])
        #             res[f"PDF{k}"]["Case Quantity"].append(temp[8])
        #             res[f"PDF{k}"]["Case Price"].append(temp[7])
        #             res[f"PDF{k}"]["Unit Cost price"].append(temp[6])
        #             res[f"PDF{k}"]["Cost price currency"].append(temp[5])
        #             res[f"PDF{k}"]["Sku"].append(temp[0])
        #             res[f"PDF{k}"]["Total Order Value"].append(content[30].replace(" ", ""))
        #             res[f"PDF{k}"]["Comments"].append(content[31].split("Comments:")[1])
        #             # res[f"PDF{k}"]["Vendor Product No"].append("")
        #             # res[f"PDF{k}"]["Product Description"].append("")
        #             # res[f"PDF{k}"]["Department"].append("")
        #             res[f"PDF{k}"]["Department"].append("TOYS (PEPCO)")
        #             product_desc_1 = temp[2]
        #             product_no_1 = temp[1]
        #             # product_desc_2 = 
        #             if "Purchased" in content[22]:
        #                 desc_var = 1
        #             elif "Purchased" in content[21]:
        #                 desc_var = 0
                    
        #             mixed_var = []
        #             for i in range(4 - desc_var - 1):
        #                 mixed_var.append(content[29 - i - 1])
        #             if desc_var == 0:
        #                 product_desc_4 = mixed_var[0]
        #                 product_desc_3 = mixed_var[1]
        #                 product_no_2 = re.findall(r"\d+", mixed_var[2])[0]
        #                 product_desc_2 = mixed_var[2].replace(product_no_2, "")
        #                 res[f"PDF{k}"]["Product Description"].append(" ".join([product_desc_1, product_desc_2, product_desc_3, product_desc_4]))
        #                 res[f"PDF{k}"]["Vendor Product No"].append(" ".join([product_no_1, product_no_2]))


        #             if desc_var == 1:
        #                 product_desc_3 = mixed_var[0]
        #                 try:
        #                     product_no_2 = re.findall(r"\d+", mixed_var[1])[0]
        #                 except:
        #                     product_no_2 = ""
        #                 product_desc_2 = mixed_var[1].replace(product_no_2, "")
        #                 res[f"PDF{k}"]["Product Description"].append(" ".join([product_desc_1, product_desc_2, product_desc_3]))
        #                 res[f"PDF{k}"]["Vendor Product No"].append(" ".join([product_no_1, product_no_2]))

        #             #problems
        #             invoice_1 = content[3].split("Poundland")[0]
        #             address_1 = "Poundland" + content[3].split("Poundland")[1]
        #             invoice_2 = content[4].split("Pattison")[0]
        #             address_2 = "Pattison" + content[4].split("Pattison")[1]
        #             invoice_3 = content[5].split("Walsall")[0]
        #             address_3 = "Walsall"
        #             address_4 = content[6]
        #             res[f"PDF{k}"]["Invoice"].append(" ".join([invoice_1, invoice_2, invoice_3]))
        #             res[f"PDF{k}"]["RegisteredAddress"].append(" ".join([address_1, address_2, address_3, address_4]))

        # if os.path.isfile("OCR_res.xlsx"):
        #     os.remove("OCR_res.xlsx")
        # book = xlsxwriter.Workbook("OCR_res.xlsx")
        # sheet = book.add_worksheet("cont_excel")
        # for idx, header in enumerate(self.keys):
        #     sheet.write(0, idx, header)
        # sheet.write(0, len(self.keys), "total")
        # book.close()

        # book = load_workbook("OCR_res.xlsx")
        # sheet = book.get_sheet_by_name("cont_excel")
        # for dic in res:
        #     for i in range(len(res[dic][list(res[dic].keys())[0]])):
        #         temp = []
        #         for key in res[dic].keys():
        #             temp.append(res[dic][key][i])

        #         sheet.append(temp)

        # book.save(filename = "OCR_res.xlsx")

        return res
    
class Walgreens_Parsing:
    def __init__(self, customer_name) -> None:
        self.keys = ["PO Number", "Release Number", "PO Date", "Dept #", "Retailers PO", "Requested Delivery Date", "Delivery Dates", "Ship Dates", "Cancel Date", "Carrier", "Carrier Details", "Ship To Location", "PO Line #", "Qty Ordered", "Unit of Measure", "Unit Price", "Buyers Catalog or Stock Keeping #", "UPC/EAN", "Vendor Style", "Retail Price", "Product/Item Description", "Color", "Size", "Pack Size", "Pack Size UOM", "Number of Inner Packs", "Number of Pcs per Inner Pack", "Store #", "Qty per Store #", "Record Type", "PO purpose", "PO Type", "Contract Number", "Currency", "Ship Status", "Letter of Credit", "Vendor #", "Division #", "Cust Acct #", "Customer Order #", "Promo #", "Ticket Description", "Other Info / #s", "Frt Terms", "Carrier Service Level", "Payment Terms %", "Payment Terms Disc Due Date", "Payment Terms Disc Days Due", "Payment Terms Net Due Date", "Payment Terms Net Days", "Payment Terms Disc Amt", "Payment Terms Desc", "Contact Phone", "Contact Fax", "Contact Email", "Allow/Charge Type", "Allow/Charge Service", "Allow/Charge Amt", "Allow/Charge %", "Allow/Charge Rate", "Allow/Charge Qty", "Allow/Charge Desc", "Ship To Name", "Ship To Address 1", "Ship To Address 2", "Ship To City", "Ship To State", "Ship to Zip", "Ship To Country", "Ship To Contact", "Bill To Name", "Bill To Address 1", "Bill To Address 2", "Bill To City", "Bill To State", "Bill To Zip", "Bill To Country", "Bill To Contact", "Buying Party Name", "Buying Party Location", "Buying Party Address 1", "Buying Party Address 2", "Buying Party City", "Buying Party State", "Buying Party Zip", "Buying Party Country", "Buying Party Contact", "Ultimate Location", "Notes/Comments", "Ship To Additional Name", "Ship To Additional Name 2", "Bill To Additional Name", "Bill To Additional Name 2", "Buyer Additional Name", "Buyer Additional Name 2", "GTIN", "PO Total Amount", "PO Total Weight ", "PO Total UOM ", "Shipping account number", "Mark for Name", "Mark for Address 1", "Mark for Address 2", "Mark for City", "Mark for State", "Mark for Postal", "Mark for Country", "Shipping Container Code", "National Drug Code", "Expiration Date", "Dist", "Scheduled Quantity", "Scheduled Qty UOM", "Required By Date", "Must Arrive By", "Entire Shipment", "Agreement Number", "Additional Vendor Part #", "Buyer Part Number", "Carrier Details Special Handling", "Restrictions/Conditions"]
        
        self.top_lis = ["PO Number", "PO Date", "Dept #", "Retailers PO", "Delivery Dates", "Ship Dates", "Ship To Location", "PO purpose", "PO Type", "Vendor #", "Payment Terms %", "Payment Terms Disc Days Due", "Payment Terms Desc", "Contact Phone", "Ship To Name", "Ship To Address 1", "Ship To City", "Ship To State", "Bill To Name", "Bill To Address 1", "Bill To City", "Bill To Country", "PO Total Amount", "PO Total Weight ", "PO Total UOM "]
        self.all_mid_lis = ["PO Number", "PO Line #", "Qty Ordered", "Unit of Measure", "Unit Price", "Buyers Catalog or Stock Keeping #", "Product/Item Description", "Pack Size", "Pack Size UOM", "Number of Inner Packs", "GTIN"]
    def PO_parser(self, paths: list, currency):
        res = []

        for k, path in enumerate(paths):
            pdf = pd.read_csv(path)
            res.append([])

            for i in range(int(len(pdf) / 6)):
                res[k].append({})

                for item in pdf:
                    res[k][i].update(
                        {
                            item: []
                        }
                    )
                    
                for key in self.top_lis:
                    if type(pdf.iloc[6 * i][key]) == np.int64:
                        res[k][i][key].append(int(pdf.iloc[6 * i][key]))
                    elif type(pdf.iloc[6 * i][key]) != str:
                        if math.isnan(pdf.iloc[6 * i][key]):
                            res[k][i][key].append("")
                        else:
                            res[k][i][key].append(pdf.iloc[6 * i][key])    
                    else:
                        res[k][i][key].append(pdf.iloc[6 * i][key])

                for key in pdf:
                    if key not in self.top_lis:
                        res[k][i][key].append("")

                for key in self.all_mid_lis:
                    if type(pdf.iloc[6 * i + 2][key]) == np.int64:
                        res[k][i][key].append(int(pdf.iloc[6 * i + 2][key]))
                    else:
                        res[k][i][key].append(pdf.iloc[6 * i + 2][key])

                for key in pdf:
                    if key not in self.all_mid_lis:
                        res[k][i][key].append("")

        # if os.path.isfile("OCR_res.xlsx"):
        #     os.remove("OCR_res.xlsx")
        # book = xlsxwriter.Workbook("OCR_res.xlsx")
        # sheet = book.add_worksheet("cont_excel")
        # for idx, header in enumerate(self.keys):
        #     sheet.write(0, idx, header)
        # sheet.write(0, len(self.keys), "total")
        # book.close()

        # book = load_workbook("OCR_res.xlsx")
        # sheet = book.get_sheet_by_name("cont_excel")
        # for dic in res:
        #     for i in range(len(res[dic][list(res[dic].keys())[0]])):
        #         temp = []
        #         for key in res[dic].keys():
        #             temp.append(res[dic][key][i])

        #         sheet.append(temp)

        # book.save(filename = "OCR_res.xlsx")
        
        return res
    
class Dollarama_Parsing:
    def __init__(self, customer_name) -> None:
        self.keys = ["Destination", "P/O #", "PO Dates", "Vendor", "Manuf", "Dollarama Item #", "Vendor Item #", "Inner Pack", "Carton Pack", "Carton Cu.Ft.", "Carton Weight", "Cost USD Each", "Item Description", "Item Colour", "Item Specification", "Ready Dates", "Quantity in Units", "Quantity in Cases", "Total Volume", "Total Weight", "Total USD Cost", "Total_Quantity in Units", "Total_Quantity in Cases", "Total_Total Volume", "Total_Total Weight", "Total_Total USD Cost", "Item Specification", "Packaging Details", "UPC Code", "Buyer", "Resp.", "Artwork Requirements", "Season", "Retail"]
        self.length = 1
        self.F_bbox = [615.7, 27.850000000000023, 728.14, 42.0]
        self.R_bbox = [18.05, 206.5, 524.08, 335.05]
        self.I_bbox = [529.2, 127.10000000000002, 728.14, 243.35000000000002]
        self.P_bbox = [529.2, 246.85000000000002, 728.14, 373.7]
        self.U_bbox = [529.2, 351.05, 728.14, 368.05]
        self.D_bbox = [529.2, 373.70000000000005, 728.14, 433.25]
    
    def PO_parser(self, paths: list, currency):
        res = {}

        for k, path in enumerate(paths):
            res[f"PDF{k}"] = {}
            pdf = pdfplumber.open(path)

            for page_num, page in enumerate(pdf.pages):
                res[f"PDF{k}"][f"page{page_num}"] = {}
                table_0 = page.extract_tables()
                table_1 = page.within_bbox(self.R_bbox).extract_table()
                F_page = page.within_bbox(self.F_bbox)
                I_page = page.within_bbox(self.I_bbox)
                P_page = page.within_bbox(self.P_bbox)
                U_page = page.within_bbox(self.U_bbox)
                D_page = page.within_bbox(self.D_bbox)

                self.length = len(table_1) - 2
                for key in self.keys:
                    res[f"PDF{k}"][f"page{page_num}"].update({key: []})

                res[f"PDF{k}"][f"page{page_num}"]["Destination"] = table_0[0][0][2].split("Destination: ")[1]
                res[f"PDF{k}"][f"page{page_num}"]["P/O #"] = page.extract_text_simple().split("\n")[0].split("P/O # ")[1]
                res[f"PDF{k}"][f"page{page_num}"]["PO Dates"] = F_page.extract_text()
                res[f"PDF{k}"][f"page{page_num}"]["Vendor"] = table_0[0][1][1]
                res[f"PDF{k}"][f"page{page_num}"]["Dollarama Item #"] = table_0[0][4][0]
                res[f"PDF{k}"][f"page{page_num}"]["Vendor Item #"] = table_0[0][4][4]
                res[f"PDF{k}"][f"page{page_num}"]["Inner Pack"] = table_0[0][4][6]
                res[f"PDF{k}"][f"page{page_num}"]["Carton Pack"] = table_0[0][4][7]
                res[f"PDF{k}"][f"page{page_num}"]["Carton Cu.Ft."] = table_0[0][4][8]
                res[f"PDF{k}"][f"page{page_num}"]["Carton Weight"] = table_0[0][4][10]
                res[f"PDF{k}"][f"page{page_num}"]["Cost USD Each"] = table_0[0][4][11]
                res[f"PDF{k}"][f"page{page_num}"]["Item Description"] = table_0[0][6][0]
                res[f"PDF{k}"][f"page{page_num}"]["Item Colour"] = table_0[0][6][5]
                res[f"PDF{k}"][f"page{page_num}"]["Item Specification"] = table_0[0][6][9]
                res[f"PDF{k}"][f"page{page_num}"]["Ready Dates"] = [table_1[i + 1][0] for i in range(self.length)]
                res[f"PDF{k}"][f"page{page_num}"]["Quantity in Units"] = [table_1[i + 1][1] for i in range(self.length)]
                res[f"PDF{k}"][f"page{page_num}"]["Quantity in Cases"] = [table_1[i + 1][2] for i in range(self.length)]
                res[f"PDF{k}"][f"page{page_num}"]["Total Volume"] = [table_1[i + 1][3] for i in range(self.length)]
                res[f"PDF{k}"][f"page{page_num}"]["Total Weight"] = [table_1[i + 1][4] for i in range(self.length)]
                res[f"PDF{k}"][f"page{page_num}"]["Total USD Cost"] = [table_1[i + 1][5] for i in range(self.length)]
                res[f"PDF{k}"][f"page{page_num}"]["Total_Quantity in Units"] = table_1[5][1]
                res[f"PDF{k}"][f"page{page_num}"]["Total_Quantity in Cases"] = table_1[5][2]
                res[f"PDF{k}"][f"page{page_num}"]["Total_Total Volume"] = table_1[5][3]
                res[f"PDF{k}"][f"page{page_num}"]["Total_Total Weight"] = table_1[5][4]
                res[f"PDF{k}"][f"page{page_num}"]["Total_Total USD Cost"] = table_1[5][5]
                res[f"PDF{k}"][f"page{page_num}"]["Item Specification"] = I_page.extract_text().split("\n")[1:]
                res[f"PDF{k}"][f"page{page_num}"]["Packaging Details"] = P_page.extract_text().split("\n")[1:]
                res[f"PDF{k}"][f"page{page_num}"]["UPC Code"] = U_page.extract_table()[0][1]
                res[f"PDF{k}"][f"page{page_num}"]["Buyer"] = D_page.extract_text().split("\n")[1].split("Resp")[0].split("Buyer")[1].replace(" ", "")
                res[f"PDF{k}"][f"page{page_num}"]["Resp."] = D_page.extract_text().split("\n")[1].split("Resp.")[1].replace(" ", "")
                res[f"PDF{k}"][f"page{page_num}"]["Artwork Requirements"] = "Dollarama"
                res[f"PDF{k}"][f"page{page_num}"]["Season"] = D_page.extract_text().split("\n")[3].split("Dollarama")[1][1:]
                res[f"PDF{k}"][f"page{page_num}"]["Retail"] = page.extract_text().split("\n")[35].split("> ")[1]

        return res
    
class Family_Dollar_Parsing:
    def __init__(self, customer_name) -> None:
        self.keys = ["Purchase Order", "PO First Ship Date", "PO Last Ship Date", "PO First DC Date", "PO Last DC Date", "Ship To", "Payment Terms", "Currencys", "Total PO Master Case Qty", "Total PO Case CFT", "Total PO Weight LBS", "Family Dollar SKU", "UPC", "VPN", "First Cost Eaches", "Total Eaches Ordered", "Total First Cost", "RMS Retail Price"]
        self.PO_coordinates = [15.108, 54.771999999999935, 131.572, 66.77199999999993]

    def PO_parser(self, paths: list, currency):
        res = {}

        for k, path in enumerate(paths):
            res[f"PDF{k}"] = {}
            pdf = pdfplumber.open(path)

            for page_num, page in enumerate(pdf.pages):
                res[f"PDF{k}"][f"page{page_num}"] = {}
                content = page.extract_tables()
                PO_page = page.within_bbox(self.PO_coordinates)
                
                res[f"PDF{k}"][f"page{page_num}"]["Purchase Order"] = PO_page.extract_text_simple().split("Purchase Order: ")[1]
                res[f"PDF{k}"][f"page{page_num}"]["PO First Ship Date"] = content[0][0][4]
                res[f"PDF{k}"][f"page{page_num}"]["PO Last Ship Date"] = content[0][1][4]
                res[f"PDF{k}"][f"page{page_num}"]["PO First DC Date"] = content[0][2][4]
                res[f"PDF{k}"][f"page{page_num}"]["PO Last DC Date"] = content[0][3][4]
                res[f"PDF{k}"][f"page{page_num}"]["Ship To"] = content[0][0][5]
                res[f"PDF{k}"][f"page{page_num}"]["Payment Terms"] = content[0][3][6]
                res[f"PDF{k}"][f"page{page_num}"]["Currencys"] = content[0][2][8]
                res[f"PDF{k}"][f"page{page_num}"]["Total PO Master Case Qty"] = content[0][3][8]
                res[f"PDF{k}"][f"page{page_num}"]["Total PO Case CFT"] = content[0][4][8]
                res[f"PDF{k}"][f"page{page_num}"]["Total PO Weight LBS"] = content[0][5][8]
                res[f"PDF{k}"][f"page{page_num}"]["Family Dollar SKU"] = content[3][1][0]
                res[f"PDF{k}"][f"page{page_num}"]["UPC"] = content[3][1][3]
                res[f"PDF{k}"][f"page{page_num}"]["VPN"] = content[3][1][4]
                res[f"PDF{k}"][f"page{page_num}"]["Inner Case Pack"] = content[3][1][7]
                res[f"PDF{k}"][f"page{page_num}"]["Master Case Pack"] = content[3][1][8]
                res[f"PDF{k}"][f"page{page_num}"]["First Cost Eaches"] = content[3][1][11]
                res[f"PDF{k}"][f"page{page_num}"]["Total Eaches Ordered"] = content[3][1][12]
                res[f"PDF{k}"][f"page{page_num}"]["Total Master Cases Ordered"] = content[3][1][13]
                res[f"PDF{k}"][f"page{page_num}"]["Total First Cost"] = content[3][1][14]
                res[f"PDF{k}"][f"page{page_num}"]["RMS Retail Price"] = content[3][1][15]
                
        return res

class Gabes_Parsing:
    def __init__(self, customer_name) -> None:
        self.O_coordinates = [261.0, 41, 362.51695, 55]
        self.S_coordinates = [256.0, 65, 366.0, 145]
        self.P_coordinates = [3.0, 181, 555.77734, 193]
        self.p_v_lines = [3.0, 55.57422, 242.89456, 371.7969, 555.77734]
        self.p_h_lines = [181, 193]

    def PO_parser(self, paths: list, currency):
        res = {}
        

        for k, path in enumerate(paths):
            res[f"PDF{k}"] = {}
            pdf = pdfplumber.open(path)

            for page_num, page in enumerate(pdf.pages):
                if page_num == 0:
                    O_page = page.within_bbox(self.O_coordinates)
                    S_page = page.within_bbox(self.S_coordinates)
                    P_page = page.within_bbox(self.P_coordinates)
                    P_content = P_page.extract_table(dict(
                                    explicit_vertical_lines = self.p_v_lines,
                                    explicit_horizontal_lines = self.p_h_lines 
                                ))

                    res[f"PDF{k}"][f"page{page_num}"] = {}

                    res[f"PDF{k}"][f"page{page_num}"]["Order Date"] =  page.extract_text_simple().split("Order Date ")[1]
                    res[f"PDF{k}"][f"page{page_num}"]["PO"] = page.extract_text_simple().split("\n")[0].split("Purchase Order ")[1]
                    res[f"PDF{k}"][f"page{page_num}"]["Ship To"] = S_page.extract_text_simple().replace("\xa0", "")
                    res[f"PDF{k}"][f"page{page_num}"]["Ship Date"] = P_content[0][1]
                    res[f"PDF{k}"][f"page{page_num}"]["Cancel Dates"] = P_content[0][2]
                    res[f"PDF{k}"][f"page{page_num}"]["Internal Item #"] = page.extract_tables()[0][6][0].split("\n")
                    res[f"PDF{k}"][f"page{page_num}"]["Ticket SKU"] = page.extract_tables()[0][6][1].split("\n")
                    res[f"PDF{k}"][f"page{page_num}"]["Total Qty"] = page.extract_tables()[0][6][3].split("\n")
                    res[f"PDF{k}"][f"page{page_num}"]["Style"] = page.extract_tables()[0][6][5].split("\n")
                    res[f"PDF{k}"][f"page{page_num}"]["Description"] = page.extract_tables()[0][6][7].split("\n")
                    res[f"PDF{k}"][f"page{page_num}"]["Unit Cost"] = page.extract_tables()[0][6][10].split("\n")
                    res[f"PDF{k}"][f"page{page_num}"]["Total Cost"] = page.extract_tables()[0][7][-1]
        
        return res
    
  
class TEDI_Parsing:
    def __init__(self, customer_name) -> None:
        pass

    def PO_parser(self, paths: list, currency):
        res = {}
        

        for k, path in enumerate(paths):
            res[f"PDF{k}"] = {}
            pdf = pdfplumber.open(path)

            for page_num, page in enumerate(pdf.pages):
                if page_num == 0:

                    tables = page.extract_tables()
                    
                    res[f"PDF{k}"][f"page{page_num}"] = {}

                    res[f"PDF{k}"][f"page{page_num}"]["Order number"] = tables[2][0][2]
                    res[f"PDF{k}"][f"page{page_num}"]["Shipping window"] = tables[2][0][6]
                    res[f"PDF{k}"][f"page{page_num}"]["Promotion date"] = tables[2][1][6]
                    
                    n_table = page.within_bbox([0, page.search("Artwork and samples")[0]['top'] - 5, page.width, page.search("Product weight in")[0]['bottom'] + 5]).extract_table()

                    res[f"PDF{k}"][f"page{page_num}"]["Artwork send until"] = n_table[1][18]
                    res[f"PDF{k}"][f"page{page_num}"]["Approval sample send until"] = n_table[2][18]
                    res[f"PDF{k}"][f"page{page_num}"]["Shipment sample send until"] = n_table[3][18]
                    res[f"PDF{k}"][f"page{page_num}"]["Description"] = n_table[8][7]

                    tt = page.within_bbox([0, page.search("Special requirements")[0]['top'] - 5, page.width, page.search("Product weight")[0]['bottom'] + 5]).extract_table()
                    res[f"PDF{k}"][f"page{page_num}"]["currencys"] = tt[4][0]
                    res[f"PDF{k}"][f"page{page_num}"]["price_unit"] = tt[4][2]
                    res[f"PDF{k}"][f"page{page_num}"]["total_cost"] = tt[5][2]
                    res[f"PDF{k}"][f"page{page_num}"]["Terms of payment"] = tt[4][13]
                    res[f"PDF{k}"][f"page{page_num}"]["total_quantity"] = tt[7][0]
                    res[f"PDF{k}"][f"page{page_num}"]["Supplier art.-no"] = tables[2][1][2].replace('"', "")

        return res

class Walmart_Parsing:
    def __init__(self, customer_name) -> None:
        self.keys = ["PO Number", "Release Number", "PO Date", "Dept #", "Retailers PO", "Requested Delivery Date", "Delivery Dates", "Ship Dates", "Cancel Date", "Carrier", "Carrier Details", "Ship To Location", "PO Line #", "Qty Ordered", "Unit of Measure", "Unit Price", "Buyers Catalog or Stock Keeping #", "UPC/EAN", "Vendor Style", "Retail Price", "Product/Item Description", "Color", "Size", "Pack Size", "Pack Size UOM", "Number of Inner Packs", "Number of Pcs per Inner Pack", "Store #", "Qty per Store #", "Record Type", "PO purpose", "PO Type", "Contract Number", "Currency", "Ship Status", "Letter of Credit", "Vendor #", "Division #", "Cust Acct #", "Customer Order #", "Promo #", "Ticket Description", "Other Info / #s", "Frt Terms", "Carrier Service Level", "Payment Terms %", "Payment Terms Disc Due Date", "Payment Terms Disc Days Due", "Payment Terms Net Due Date", "Payment Terms Net Days", "Payment Terms Disc Amt", "Payment Terms Desc", "Contact Phone", "Contact Fax", "Contact Email", "Allow/Charge Type", "Allow/Charge Service", "Allow/Charge Amt", "Allow/Charge %", "Allow/Charge Rate", "Allow/Charge Qty", "Allow/Charge Desc", "Ship To Name", "Ship To Address 1", "Ship To Address 2", "Ship To City", "Ship To State", "Ship to Zip", "Ship To Country", "Ship To Contact", "Bill To Name", "Bill To Address 1", "Bill To Address 2", "Bill To City", "Bill To State", "Bill To Zip", "Bill To Country", "Bill To Contact", "Buying Party Name", "Buying Party Location", "Buying Party Address 1", "Buying Party Address 2", "Buying Party City", "Buying Party State", "Buying Party Zip", "Buying Party Country", "Buying Party Contact", "Ultimate Location", "Notes/Comments", "Ship To Additional Name", "Ship To Additional Name 2", "Bill To Additional Name", "Bill To Additional Name 2", "Buyer Additional Name", "Buyer Additional Name 2", "GTIN", "PO Total Amount", "PO Total Weight ", "PO Total UOM ", "Shipping account number", "Mark for Name", "Mark for Address 1", "Mark for Address 2", "Mark for City", "Mark for State", "Mark for Postal", "Mark for Country", "Shipping Container Code", "National Drug Code", "Expiration Date", "Dist", "Scheduled Quantity", "Scheduled Qty UOM", "Required By Date", "Must Arrive By", "Entire Shipment", "Agreement Number", "Additional Vendor Part #", "Buyer Part Number", "Carrier Details Special Handling", "Restrictions/Conditions"]
        
        self.top_lis = ["PO Number", "PO Date", "Dept #", "Retailers PO", "Delivery Dates", "Ship Dates", "Ship To Location", "PO purpose", "PO Type", "Vendor #", "Payment Terms %", "Payment Terms Disc Days Due", "Payment Terms Desc", "Contact Phone", "Ship To Name", "Ship To Address 1", "Ship To City", "Ship To State", "Bill To Name", "Bill To Address 1", "Bill To City", "Bill To Country", "PO Total Amount", "PO Total Weight ", "PO Total UOM "]
        self.all_mid_lis = ["PO Number", "PO Line #", "Qty Ordered", "Unit of Measure", "Unit Price", "Buyers Catalog or Stock Keeping #", "Product/Item Description", "Pack Size", "Pack Size UOM", "Number of Inner Packs", "GTIN"]

    def PO_parser(self, paths: list, currency):
        res = []

        for k, path in enumerate(paths):
            pdf = pd.read_csv(path)
            res.append([])

            lis = list(pdf["PO Number"])
            lens = []
            init = lis[0]
            length = 0

            for item in lis:
                if init == item:
                    length = length  + 1
                
                else:
                    lens.append(length)
                    init = item
                    length = 1

            lens.append(length)
            steper = 0

            for num, length in enumerate(lens):
                res[k].append({})

                for key in self.keys:
                    res[k][num].update({
                        key: []
                    })

                for i in range(length):
                    if type(pdf.iloc[i + steper]["Unit of Measure"]) == str or i == 0:
                        for key, item in zip(self.keys, list(pdf.iloc[i + steper])[:-1]):
                            
                            if type(item) == np.int64:
                                res[k][num][key].append(int(item))
                            
                            elif type(item) != str:
                                if math.isnan(item):
                                    res[k][num][key].append("")
                                else:
                                    if key in ["Unit Price", "PO Total Amount"]:
                                        res[k][num][key].append(float(item))
                                    else:
                                        res[k][num][key].append(int(item))
                            else:
                                res[k][num][key].append(item)
                        # res[k][num].append(list(pdf.iloc[i + steper])[:-1])
                
                steper = steper + i + 1
        
        return res
    
class Ollies_Parsing:
    def __init__(self, customer_name) -> None:
        pass

    def PO_parser(self, paths: list, currency):
        res = {}

        for k, path in enumerate(paths):
            
            res[f"PDF{k}"] = {}
            pdf = pdfplumber.open(path)
            page_num = 0
            res[f"PDF{k}"][f"page{page_num}"] = {}

            cropped_page = pdf.pages[0].within_bbox([pdf.pages[0].search("PO#")[0]['x0'], pdf.pages[0].search("PO#")[0]['top'], pdf.pages[0].search("PO#")[0]['x0'] + 300, pdf.pages[0].search("Approved by")[0]['bottom']])
            crop = cropped_page.extract_text().split("\n")

            res[f"PDF{k}"][f"page{page_num}"]["PO#"] = crop[0].split("PO#: ")[1]
            res[f"PDF{k}"][f"page{page_num}"]["Vendor#"] = crop[5].split("Vendor#: ")[1]
            res[f"PDF{k}"][f"page{page_num}"]["Order Dt"] = crop[7].split("Order Dt: ")[1]
            res[f"PDF{k}"][f"page{page_num}"]["Start Ship Dt"] = crop[8].split("Start Ship Dt: ")[1]
            res[f"PDF{k}"][f"page{page_num}"]["End Ship Dt"] = crop[9].split("End Ship Dt: ")[1]
            res[f"PDF{k}"][f"page{page_num}"]["Exp Rec Dt"] = crop[10].split("Exp Rec Date: ")[1]
            res[f"PDF{k}"][f"page{page_num}"]["Terms"] = crop[11].split("Terms: ")[1]
            
            res[f"PDF{k}"][f"page{page_num}"]["Ln"] = []
            res[f"PDF{k}"][f"page{page_num}"]["sku"] = []
            res[f"PDF{k}"][f"page{page_num}"]["description"] = []
            res[f"PDF{k}"][f"page{page_num}"]["model#"] = []
            res[f"PDF{k}"][f"page{page_num}"]["cspk"] = []
            res[f"PDF{k}"][f"page{page_num}"]["unitsord"] = []
            res[f"PDF{k}"][f"page{page_num}"]["Cost"] = []
            res[f"PDF{k}"][f"page{page_num}"]["extcost"] = []

            page_flag = 0

            while len(pdf.pages[page_flag].search("Ext Cost")) != 0:
                try:
                    product_ending_y = pdf.pages[page_flag].search("Total -")[0]['bottom']
                except:
                    product_ending_y = pdf.pages[page_flag].height
                    
                ln_page = pdf.pages[page_flag].within_bbox([0, pdf.pages[page_flag].search("Ext Cost")[0]['top'], pdf.pages[page_flag].search("Ln")[0]['x1'], product_ending_y])
                sku_page = pdf.pages[page_flag].within_bbox([pdf.pages[page_flag].search("Ln")[0]['x1'], pdf.pages[page_flag].search("Ext Cost")[0]['top'], pdf.pages[page_flag].search("Description")[0]['x0'], product_ending_y])
                desc_page = pdf.pages[page_flag].within_bbox([pdf.pages[page_flag].search("Description")[0]['x0'], pdf.pages[page_flag].search("Ext Cost")[0]['top'], pdf.pages[page_flag].search("Model#")[0]['x0'], product_ending_y])
                model_page = pdf.pages[page_flag].within_bbox([pdf.pages[page_flag].search("Model#")[0]['x0'], pdf.pages[page_flag].search("Ext Cost")[0]['top'], pdf.pages[page_flag].search("Cs Pk")[0]['x0'], product_ending_y])
                cspack_page = pdf.pages[page_flag].within_bbox([pdf.pages[page_flag].search("Cs Pk")[0]['x0'], pdf.pages[page_flag].search("Ext Cost")[0]['top'], pdf.pages[page_flag].search("Units Ord")[0]['x0'], product_ending_y])
                unitsord_page = pdf.pages[page_flag].within_bbox([pdf.pages[page_flag].search("Units Ord")[0]['x0'], pdf.pages[page_flag].search("Ext Cost")[0]['top'], pdf.pages[page_flag].search("Cost")[0]['x0'] - 5, product_ending_y])
                cost_page = pdf.pages[page_flag].within_bbox([pdf.pages[page_flag].search("Cost")[0]['x0'] - 5, pdf.pages[page_flag].search("Ext Cost")[0]['top'], pdf.pages[page_flag].search("Ext Cost")[0]['x0'] - 10, product_ending_y])
                extcost_page = pdf.pages[page_flag].within_bbox([pdf.pages[page_flag].search("Ext Cost")[0]['x0'] - 10, pdf.pages[page_flag].search("Ext Cost")[0]['top'], pdf.pages[page_flag].search("Ext Cost")[0]['x1'] + 10, product_ending_y])

                res[f"PDF{k}"][f"page{page_num}"]["Ln"].extend(ln_page.extract_text().split("\n")[2:])
                res[f"PDF{k}"][f"page{page_num}"]["sku"].extend(sku_page.extract_text().split("\n")[2:])
                res[f"PDF{k}"][f"page{page_num}"]["description"].extend(desc_page.extract_text().split("\n")[2:])
                res[f"PDF{k}"][f"page{page_num}"]["model#"].extend(model_page.extract_text().split("\n")[2:])
                res[f"PDF{k}"][f"page{page_num}"]["cspk"].extend(cspack_page.extract_text().split("\n")[2:])
                res[f"PDF{k}"][f"page{page_num}"]["unitsord"].extend(unitsord_page.extract_text().split("\n")[2:])
                res[f"PDF{k}"][f"page{page_num}"]["Cost"].extend(cost_page.extract_text().split("\n")[2:])
                res[f"PDF{k}"][f"page{page_num}"]["extcost"].extend(extcost_page.extract_text().split("\n")[2:])

                page_flag = page_flag + 1

            res[f"PDF{k}"][f"page{page_num}"]["cspk"].pop(-1)
            
            res[f"PDF{k}"][f"page{page_num}"]["Total - unit"] = res[f"PDF{k}"][f"page{page_num}"]["unitsord"][-1]
            res[f"PDF{k}"][f"page{page_num}"]["unitsord"].pop(-1)
            res[f"PDF{k}"][f"page{page_num}"]["Total - cost"] = res[f"PDF{k}"][f"page{page_num}"]["extcost"][-1]
            res[f"PDF{k}"][f"page{page_num}"]["extcost"].pop(-1)
            
            
        return res

class ORBICO_Parsing:
    def __init__(self, customer_name) -> None:
        pass

    def PO_parser(self, paths: list, currency):
        res = {}

        for k, path in enumerate(paths):
            
            res[f"PDF{k}"] = {}
            pdf = pdfplumber.open(path)
            page_num = 0
            res[f"PDF{k}"][f"page{page_num}"] = {}

            page = pdf.pages[0]
            tables = page.extract_tables()

            res[f"PDF{k}"][f"page{page_num}"]["Date:"] = page.within_bbox([page.search("Date:")[0]['x0'], page.search("Date:")[0]['top'], page.width, page.search("No.:")[0]['bottom']]).extract_text().split("\n")[0].split("Date: ")[1]
            res[f"PDF{k}"][f"page{page_num}"]["No.:"] = page.within_bbox([page.search("Date:")[0]['x0'], page.search("Date:")[0]['top'], page.width, page.search("No.:")[0]['bottom']]).extract_text().split("\n")[1].split("No.: ")[1]
            res[f"PDF{k}"][f"page{page_num}"]["Shipped Date"] = tables[0][1][1]

            res[f"PDF{k}"][f"page{page_num}"]["Description"] = []
            res[f"PDF{k}"][f"page{page_num}"]["Item no."] = []
            res[f"PDF{k}"][f"page{page_num}"]["Qty pcs"] = []
            res[f"PDF{k}"][f"page{page_num}"]["Unit Prices"] = [] 
            res[f"PDF{k}"][f"page{page_num}"]["Total"] = []

            for i in range(1, len(tables[1])):
                res[f"PDF{k}"][f"page{page_num}"]["Description"].append(tables[1][i][1])
                res[f"PDF{k}"][f"page{page_num}"]["Item no."].append(tables[1][i][2])
                res[f"PDF{k}"][f"page{page_num}"]["Qty pcs"].append(tables[1][i][3])
                res[f"PDF{k}"][f"page{page_num}"]["Unit Prices"].append(tables[1][i][4])
                res[f"PDF{k}"][f"page{page_num}"]["Total"].append(tables[1][i][5])
            
            res[f"PDF{k}"][f"page{page_num}"]["Total:"] = tables[3][1][1]
            res[f"PDF{k}"][f"page{page_num}"]["Currencys"] = tables[3][2][1]
        
        return res
    
class EXCEL_Parsing:
    def __init__(self, customer_name) -> None:
        self.customer_name = customer_name

    def PO_parser(self, paths: list, currency):
        res = []

        for k, path in enumerate(paths):
            try:
                pdf = pd.read_csv(path, encoding='ISO-8859-1')
            except:
                pdf = pd.read_excel(path)

            cols = len(pdf.columns)
            res.append({})
            # this lines are to block excel inputs
            # if "PD MOLDIMALS SURPRISE" in list(pdf[list(pdf.keys())[20]]):
            #     continue
            i = 0
            num_po = -1
            while i < len(pdf[list(pdf.keys())[0]]):
                try:
                    a = (not math.isnan(pdf[list(pdf.keys())[2]][i]))
                except:
                    a = True
                
                try:
                    if cols == 122:
                        b = (not math.isnan(pdf[list(pdf.keys())[14]][i]))
                    else:
                        b = (not math.isnan(pdf[list(pdf.keys())[12]][i]))
                except:
                    b = True
                # print(a, b, i)
                
                if a ^ b:
                    if a:
                        res.append({})
                        num_po = num_po + 1

                        for key in list(pdf.keys())[:-1]:
                            try:
                                c = math.isnan(pdf[key][i])
                            except:
                                c = False

                            if c:
                                res[num_po][key] = [""]
                            else:
                                if key in ["Vendor Style", "Buyers Catalog or Stock Keeping #", "Payment Terms Net Days", "Ship To Location"]:
                                    try:
                                        res[num_po][key] = [str(int(pdf[key][i]))]
                                    except:
                                        res[num_po][key] = [str(pdf[key][i])]
                                else:
                                    res[num_po][key] = [str(pdf[key][i])]
                        # print(i)
                        # print(pdf["Notes/Comments"][i + 1])
                        # print(math.isnan(pdf["Notes/Comments"][i]))
                        try:
                            c = math.isnan(pdf["Notes/Comments"][i])
                        except:
                            c = False
                        if c:
                            res[num_po].update({
                                "Notes/Comments": [""]
                            })
                        else:
                            res[num_po].update({
                                "Notes/Comments": [pdf["Notes/Comments"][i + 1]]
                            })
                    else:
                        for key in list(pdf.keys())[:-1]:
                            try:
                                c = math.isnan(pdf[key][i])
                            except:
                                c = False

                            if c:
                                if self.customer_name == "Tar Heel Trading" and key in ["Unit Price", "UPC/EAN", "Product/Item Description"]:
                                    res[num_po][key].append(res[num_po][key][-1])
                                else:
                                    res[num_po][key].append("")
                            else:
                                if key in ["Vendor Style", "Buyers Catalog or Stock Keeping #", "Payment Terms Net Days", "UPC/EAN", "Retailers PO", "Ship To Location", "PO Line #", "Qty Ordered", "GTIN"]:
                                    try:
                                        res[num_po][key].append(str(int(pdf[key][i])))
                                    except:
                                        res[num_po][key].append(str(pdf[key][i]))
                                else:
                                    res[num_po][key].append(str(pdf[key][i]))
                # print(pdf["Notes/Comments"])
                
                i = i + 1
            
            res.pop(-1)
            temp = []
            temp_note = []
            i = 0
            if cols == 122:
                while i < len(pdf[list(pdf.keys())[0]]):
                    try:
                        # print(pdf[list(pdf.keys())[55]][i])
                        math.isnan(pdf[list(pdf.keys())[55]][i])
                    except:
                        # print("------------------------", [pdf[list(pdf.keys())[55]][i], pdf[list(pdf.keys())[56]][i], pdf[list(pdf.keys())[61]][i]])
                        temp.append([pdf[list(pdf.keys())[55]][i], pdf[list(pdf.keys())[56]][i], pdf[list(pdf.keys())[61]][i]])

                    try:
                        #Maijer
                        # print(pdf[list(pdf.keys())[57]][i], type(pdf[list(pdf.keys())[57]][i]), math.isnan(pdf[list(pdf.keys())[57]][i]))
                        if str(pdf[list(pdf.keys())[57]][i]) != "nan":
                            math.isnan(str(pdf[list(pdf.keys())[57]][i]))
                    except:
                        # print([pdf[list(pdf.keys())[57]][i], pdf[list(pdf.keys())[58]][i]])
                        temp[-1].extend([pdf[list(pdf.keys())[57]][i], pdf[list(pdf.keys())[58]][i]])
                    # print(temp)
                    # print("temp______")
                    try:
                        # print(pdf[list(pdf.keys())[88]][i], type(pdf[list(pdf.keys())[88]][i]))
                        math.isnan(pdf[list(pdf.keys())[88]][i])
                    except:
                        temp_note.append(pdf[list(pdf.keys())[88]][i])
                    # print(temp_note)
                    # print("temp_note______")
                    i = i + 1
                # print(temp)
                # print(len(res), len(temp))
                if len(temp) != 0:
                    for i, items in enumerate(temp):
                        # print(temp[-1 - i])
                        res[-1 - i][list(pdf.keys())[55]][0] = temp[-1 - i][0]
                        res[-1 - i][list(pdf.keys())[56]][0] = temp[-1 - i][1]
                        res[-1 - i][list(pdf.keys())[61]][0] = temp[-1 - i][2]
                        try:
                            res[-1 - i][list(pdf.keys())[57]][0] = temp[-1 - i][3]
                            res[-1 - i][list(pdf.keys())[58]][0] = temp[-1 - i][4]
                        except:
                            pass
                # print(len(temp_note))
                if len(temp_note) / 3 == len(temp) and len(temp) != 0:
                    for i in range(int(len(temp_note) / 3)):
                        res[-1 - i][list(pdf.keys())[88]][0] = ", ".join([temp_note[-1 - i * 3], temp_note[-1 - i * 3 - 1], temp_note[-1 - i * 3 - 2]])
                # elif len(temp_note) != 0:
                # elif len(pdf.columns) == 84:
                #     res.append({})

        # res.pop(-1)

        return res

class CVS_Parsing:
    def __init__(self, customer_name) -> None:
        pass

    def PO_parser(self, paths: list, currency):
        res = []

        for k, path in enumerate(paths):
            try:
                pdf = pd.read_csv(path, encoding='ISO-8859-1')
            except:
                pdf = pd.read_excel(path)
            # print(type(pdf["Release Number"][0]), pdf["Release Number"][0], math.isnan(pdf["Release Number"][0]), "______________")
            i = 0
            flag = 0
            po_num = pdf[list(pdf.keys())[0]][0]
            res.append({})

            for key in pdf.keys():
                try:
                    c = math.isnan(pdf[key][i])
                except:
                    c = False

                if c:
                    res[-1].update({
                        key: [""]
                    })
                else:
                    res[-1].update({
                        key: [pdf[key][0]]
                    })

            while i < len(pdf[list(pdf.keys())[0]]) - 1:
                i = i + 1

                while po_num == pdf[list(pdf.keys())[0]][i]:
                    for key in pdf.keys():
                        try:
                            c = math.isnan(pdf[key][i])
                        except:
                            c = False
                        # print(key, c, "___________")
                        if c:
                            res[-1][key].append("")
                            # print(key, res[-1][key])
                        else:
                            res[-1][key].append(pdf[key][i])
                    
                    po_num = pdf[list(pdf.keys())[0]][i]
                    
                    if i < len(pdf[list(pdf.keys())[0]]) - 1:
                        i = i + 1
                    else:
                        flag = 1
                        break
                
                if flag != 1:
                    res.append({})
                    for key in pdf.keys():
                        try:
                            c = math.isnan(pdf[key][i])
                        except:
                            c = False

                        if c:
                            res[-1].update({
                                key: [""]
                            })
                        else:
                            res[-1].update({
                                key: [pdf[key][i]]
                            })

                    po_num = pdf[list(pdf.keys())[0]][i]
                
        return res

class GiantTiger_Parsing:
    def __init__(self, customer_name) -> None:
        pass

    def PO_parser(self, paths: list, currency):
        res = {}

        for k, path in enumerate(paths):
            
            res[f"PDF{k}"] = {}
            pdf = pdfplumber.open(path)
            page_num = 0
            res[f"PDF{k}"][f"page{page_num}"] = {}
            page = pdf.pages[0]
            tables = page.extract_tables()

            res[f"PDF{k}"][f"page{page_num}"]["Purchase Order #"] = page.within_bbox([page.search("##")[0]['x1'], 0, page.search("GGG")[0]['x0'], page.search("GGG")[0]['bottom']]).extract_text()
            res[f"PDF{k}"][f"page{page_num}"]["Order Date"] = tables[0][1][4].split("\n")[0].split("OOrrddeerr DDaattee ")[1]
            res[f"PDF{k}"][f"page{page_num}"]["Original Delivery to CFS"] = tables[0][1][4].split("\n")[1].split("OOrriiggiinnaall DDeelliivveerryy ttoo CCFFSS//CCaarrrriieerr ")[1]
            res[f"PDF{k}"][f"page{page_num}"]["Cancel date"] = tables[0][1][4].split("\n")[3].split("CCaanncceell DDaattee ")[1]

            product_page = page.within_bbox([0, page.search("MST Total")[0]["top"], page.width, page.search("MST Total")[0]["top"] + 100])
            product_table = product_page.extract_table(dict(
                explicit_vertical_lines = [0, page.search("VPN#")[0]["x1"] + 5, page.search("Material Content")[0]["x0"], page.search("Material Content")[0]["x1"] + 20, page.search("UPC Code")[0]["x1"], page.search("G.T. SKU")[0]['x1'], page.search("Order Qty")[0]["x0"], page.search("Order Qty")[0]["x0"] + 20, page.search("Order Qty")[0]["x1"] + 14, page.search("Mastr")[0]["x1"], page.search("G.T. FOB")[0]["x0"], page.search("G.T. FOB")[0]["x0"] + 30, page.search("G.T. FOB")[0]["x1"] + 5, page.search("FOB Amount")[0]['x1'] + 5, page.width],
                explicit_horizontal_lines = [page.search("MST Total")[0]["top"], page.search("VPN#")[0]['bottom'], page.search("MST Total")[0]["top"] + 100]
            ))

            res[f"PDF{k}"][f"page{page_num}"]["UPC Code"] = product_table[1][3]
            res[f"PDF{k}"][f"page{page_num}"]["G.T. SKU"] = product_table[1][4]
            res[f"PDF{k}"][f"page{page_num}"]["Order Qty"] = product_table[1][6]
            res[f"PDF{k}"][f"page{page_num}"]["Mastr Pack"] = product_table[1][8]
            res[f"PDF{k}"][f"page{page_num}"]["G.T. Retail"] = product_table[1][10]
            res[f"PDF{k}"][f"page{page_num}"]["FOB(USD)"] = product_table[1][11]
            res[f"PDF{k}"][f"page{page_num}"]["Total Amount"] = product_table[1][12]

        return res
    
class HOBBYlobby_Parsing:
    def __init__(self, customer_name) -> None:
        pass

    def PO_parser(self, paths: list, currency):
        res = {}

        for k, path in enumerate(paths):
            
            res[f"PDF{k}"] = {}
            pdf = pdfplumber.open(path)
            page_num = 0
            res[f"PDF{k}"][f"page{page_num}"] = {}
            po_page = pdf.pages[0]
            for i, page in enumerate(pdf.pages):
                if len(page.search("SKU # DESC")) == 1:
                    product_page = page
                    break

            po_cont = po_page.extract_text().split("\n")

            for line in po_cont:
                if "Our Purchase Order#: " in line:
                    res[f"PDF{k}"][f"page{page_num}"]["Our Purchase Order#: "] = line.split("Our Purchase Order#: ")[1].replace(" ", "")
                    continue

                if "Ship Date: " in line:
                    res[f"PDF{k}"][f"page{page_num}"]["Ship Date: "] = line.split("Ship Date: ")[1].replace(" ", "")
                    continue
                
                if "Cancel Date: " in line:
                    res[f"PDF{k}"][f"page{page_num}"]["Cancel Date: "] = line.split("Cancel Date: ")[1].replace(" ", "")
                    continue
                
                if "Payment Terms: " in line:
                    res[f"PDF{k}"][f"page{page_num}"]["Payment Terms: "] = line.split("Payment Terms: ")[1].replace(" ", "")
                    continue
            
            for i, line in enumerate(product_page.extract_text().split("\n")):
                if "VENDOR#: " in line:
                    line_v = line
                
                if "QTY: " in line:
                    line_q = line

                if "SKU # DESC" in line:
                    line_num_s = i
            
            res[f"PDF{k}"][f"page{page_num}"]["SKU"] = product_page.extract_text().split("\n")[line_num_s + 1]
            res[f"PDF{k}"][f"page{page_num}"]["VENDOR#: "] = line_v.split("1ST COST")[0].split("VENDOR#: ")[1].replace(" ", "")
            res[f"PDF{k}"][f"page{page_num}"]["1ST COST"] = line_v.split("EXT COST")[0].split("1ST COST: ")[1].replace(" ", "")
            # print(line_v.split("PRE-PRICE")[0])
            res[f"PDF{k}"][f"page{page_num}"]["EXT COST"] = line_v.split("PRE-PRICE")[0].split("EXT COST:")[1].replace(" ", "")
            res[f"PDF{k}"][f"page{page_num}"]["PRE-PRICE"] = line_v.split("PRE-PRICE: ")[1].replace(" ", "")
            res[f"PDF{k}"][f"page{page_num}"]["QTY"] = line_q.split("U/M")[0].split("QTY: ")[1].replace(" ", "")

        return res
    
class Lekia_Parsing:
    def __init__(self, customer_name) -> None:
        pass

    def hline_extractor(self, page):
        cont = page.extract_text().split("\n")
        
        coordinate_lis = []

        pattern_lis = []
        for line in cont:
            if len(re.findall(r"\[ \d+\-\d+ \]", line)) == 1:
                pattern_lis.append(re.findall(r"\[ \d+\-\d+ \]", line)[0])
        
        for pattern in pattern_lis:
            coordinate_lis.append(page.search(pattern[2:-2])[0]['bottom'])

        return coordinate_lis

    def PO_parser(self, paths: list, currency):
        res = {}

        for k, path in enumerate(paths):
            
            res[f"PDF{k}"] = {}
            pdf = pdfplumber.open(path)
            page_num = 0
            res[f"PDF{k}"][f"page{page_num}"] = {}

            po_table = pdf.pages[0].within_bbox([pdf.pages[0].search("Purchase No.")[0]['x0'], pdf.pages[0].search("Purchase No.")[0]['top'], pdf.pages[0].width, pdf.pages[0].search("Purchase No.")[0]['x0'] + 30]).extract_table(dict(
                explicit_vertical_lines = [pdf.pages[0].search("Purchase No.")[0]['x0'], pdf.pages[0].search("Purchase date")[0]['x0'], pdf.pages[0].search("Supplier No.")[0]['x0'], pdf.pages[0].search("Supplier No.")[0]['x1']],
                explicit_horizontal_lines = [pdf.pages[0].search("Purchase No.")[0]['top'], pdf.pages[0].search("Purchase No.")[0]['bottom'], pdf.pages[0].search("Purchase No.")[0]['bottom'] + 20]
            ))
            res[f"PDF{k}"][f"page{page_num}"]["Purchase No."] = po_table[1][0]
            res[f"PDF{k}"][f"page{page_num}"]["Purchase date"] = po_table[1][1]
            res[f"PDF{k}"][f"page{page_num}"]["Supplier No."] = po_table[1][2]

            res[f"PDF{k}"][f"page{page_num}"]["Payment terms"] = pdf.pages[0].within_bbox([pdf.pages[0].search("Payment terms")[0]["x0"], pdf.pages[0].search("Payment terms")[0]["bottom"], pdf.pages[0].search("Payment terms")[0]["x0"] + 150, pdf.pages[0].search("Payment terms")[0]["bottom"] + 15]).extract_text()
            res[f"PDF{k}"][f"page{page_num}"]["Requested Delivery Date"] = pdf.pages[0].within_bbox([pdf.pages[0].search("Requested Delivery Date")[0]["x0"], pdf.pages[0].search("Payment terms")[0]["bottom"], pdf.pages[0].search("Requested Delivery Date")[0]["x1"], pdf.pages[0].search("Payment terms")[0]["bottom"] + 15]).extract_text()
            
            res[f"PDF{k}"][f"page{page_num}"]["Item"] = []
            res[f"PDF{k}"][f"page{page_num}"]["RDD"] = []
            res[f"PDF{k}"][f"page{page_num}"]["Quantity Unit"] = []
            res[f"PDF{k}"][f"page{page_num}"]["Price/unit"] = []
            res[f"PDF{k}"][f"page{page_num}"]["Value"] = []

            for i, page in enumerate(pdf.pages):
                temp = [page.search("Item RDD")[0]['bottom']]
                temp.extend(self.hline_extractor(page))
                production_table = page.within_bbox([page.search("Item RDD")[0]['x0'], page.search("Item RDD")[0]['bottom'], page.width - 25, temp[-1]]).extract_table(dict(
                    explicit_vertical_lines = [page.search("Item RDD")[0]['x0'], page.search("RDD")[0]['x0'], page.search("Quantity Unit")[0]['x0'], page.search("Price/unit")[0]['x0'], page.search("Price/unit")[0]['x1'] + 5, page.width - 25],
                    explicit_horizontal_lines = temp
                ))

                for line in production_table:
                    res[f"PDF{k}"][f"page{page_num}"]["Item"].append(line[0].split("\n")[0])
                    res[f"PDF{k}"][f"page{page_num}"]["RDD"].append(line[1])
                    res[f"PDF{k}"][f"page{page_num}"]["Quantity Unit"].append(line[2])
                    res[f"PDF{k}"][f"page{page_num}"]["Price/unit"].append(line[3])
                    res[f"PDF{k}"][f"page{page_num}"]["Value"].append(line[4])

        return res