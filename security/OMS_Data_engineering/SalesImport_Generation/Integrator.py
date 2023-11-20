import json
import pandas as pd
from csv import writer
from pathlib import Path
import re
from google.oauth2 import service_account
import gspread
from ..sheet_reader import frame_converter
import datetime
from currency_converter import CurrencyConverter

class Integrate_All:
    def __init__(self, customer_name) -> None:
        # Initialize productLib and UOM
        # f = open(Path(__file__).resolve().parent.parent / "config/django-connection-1008-5f931d8f4038.json")
        # google_json = json.load(f)
        # credentials = service_account.Credentials.from_service_account_info(google_json)
        # scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
        # creds_with_scope = credentials.with_scopes(scope)
        # client = gspread.authorize(creds_with_scope)
        # spreadsheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1CDnIivm8hatRQjG7nvbMxG-AuP19T-W2bNAhbFwEuE0")

        self.additional_uom = pd.read_csv(Path(__file__).resolve().parent.parent / "config/uom_sku.csv")
        # self.inventory_list = pd.read_csv(Path(__file__).resolve().parent.parent / "config/OMS_DB/OMS_InventoryList.csv", index_col = False)
        # self.inventory_list = frame_converter(spreadsheet.get_worksheet(1).get_all_records())
        self.inventory_list = None
        self.currency_matcher = {}
        self.length = 0
        self.currency = ""
        self.terms = []
        # self.uom = pd.read_csv(Path(__file__).resolve().parent.parent / "config/OMS_DB/OMS_UOM.csv")
        # self.uom = frame_converter(spreadsheet.get_worksheet(4).get_all_records())

        # self.paymentterms = pd.read_csv(Path(__file__).resolve().parent.parent / "config/OMS_DB/OMS_PaymentTerm.csv")
        # self.paymentterms = frame_converter(spreadsheet.get_worksheet(2).get_all_records())

        self.OMS_Customer_Sales_Import = {
            "TaxRule*": "TaxRule",#Tax Exempt
            "Account": "SaleAccount",#4000
            "PriceTier": "PriceTier",#Tier 1 - Retail Pricing
            "Discount": "Discount",#0
            "SalesRepresentative*": "SalesRepresentative",#Jodie Pederson
            "StockLocation": "Location",#Houston Warehouse
            "CustomerContact": "ContactComment",#
            "CustomerPhone": "Phone",#
            "CustomerEmail": "Email",#
            "Terms": "PaymentTerm"#?    90 Days
        }
        self.add_match = {
            "ShippingAddressLine1*": "Ship To Address 1",
            "ShippingAddressLine2": "Ship To Address 2",
            "ShippingCity*": "Ship To City",
            "ShippingProvince*": "Ship To State",
            "ShippingPostcode*": "Ship to Zip",
            "ShippingCountry*": "Ship To Country",
            "ShipToCompany*": "Ship To Name",
            "BillingAddressLine1*": "Bill To Address 1",
            "BillingAddressLine2": "Bill To Address 2",
            "BillingCity*": "Bill To City",
            "BillingProvince*": "Bill To State",
            "BillingPostcode*": "Bill To Zip",
            "BillingCountry*": "Bill To Country",
        }
        self.customer_name = customer_name
        self.customer_name_init = customer_name
        self.customers = None
        self.non_blank_list = ["ShippingNotes", "InvoiceDate*/ExpireDate", "YourBaseCurrency*", "CustomerCurrency*", "ShippingAddressLine1*", "ShippingCity*", "ShippingProvince*", "ShippingPostcode*", "ShippingCountry*", "BillingAddressLine1*", "CustomerName*", "InvoiceNumber*", "Product*", "Quantity*", "Price/Amount*", "CurrencyConversionRate", "RecordType*", "Account", "TaxRule*", "Discount"]
        self.available_currencies = ['DKK', 'JPY', 'RON', 'AUD', 'TRY', 'GBP', 'MXN', 'RUB', 'LVL', 'BGN', 'SEK', 'ILS', 'MYR', 'CYP', 'CHF', 'NOK', 'SKK', 'EUR', 'EEK', 'PHP', 'BRL', 'HRK', 'IDR', 'CNY', 'MTL', 'KRW', 'INR', 'CAD', 'NZD', 'HUF', 'HKD', 'SGD', 'ZAR', 'ROL', 'THB', 'CZK', 'ISK', 'USD', 'PLN', 'LTL', 'TRL', 'SIT']

    def auto_fun(self, customer_name):
        customer_match = pd.read_csv(Path(__file__).resolve().parent.parent / "config/customer_fields.csv")
        
        values = list(customer_match[customer_name])
        auto_dic = {}

        # Account
        auto_dic.update({"Account": self.fun_iter_all(values[1])})

        #TaxRule*
        temp = []
        for _ in range(self.length):
            temp.append(values[0])
        
        auto_dic.update({"TaxRule*": self.fun_iter_all(values[0])})

        #Discount
        auto_dic.update({"Discount": self.fun_iter_line(values[3])})

        #rest [0, 3, 5, 6, 7, 8, 9]
        rest = [2, 4, 5, 6, 7, 8, 9]
        for i, field in enumerate(self.OMS_Customer_Sales_Import):
            if i in rest:
                temp = []
                temp.append(values[i])
                for _ in range(self.length - 1):
                    temp.append("")
                auto_dic.update({field: temp})
        
        # auto_dic.update({"Terms": self.fun_iter_top(self.terms[0])})
            
        return auto_dic
    
    def fun_iter_all(self, input):
        temp = []
        
        for _ in range(self.length):
            temp.append(input)
        
        return temp
    
    def fun_iter_top_currency(self, input):
        if self.customer_name in ["Walmart US", "Buc-ee's"]:
            temp = ["USD"]
        else: 
            temp = [input]

        for _ in range(self.length - 1):
            temp.append("")

        return temp
    
    def fun_iter_top_currency_customer(self):
        temp = [self.currency_matcher[self.customer_name]]

        for _ in range(self.length - 1):
            temp.append("")

        return temp
    
    def fun_iter_top(self, input):
        temp = [input]

        for _ in range(self.length - 1):
            temp.append("")

        return temp
    
    def fun_iter_topp(self, input):
        # if input == "":
        #     temp = ["NO"]
        # else:
        temp = [input]

        for _ in range(self.length - 1):
            temp.append("")

        return temp
    
    def fun_date_top(self, input):
        temp = [input.replace("-", "")]

        for _ in range(self.length - 1):
            temp.append("")

        return temp
    
    def fun_iter_line(self, input):
        temp = []
        temp.append("")

        for _ in range(self.length - 1):
            temp.append(input)
        
        return temp
    
    def fun_shippingnotes(self, m_shipdates: str, m_canceldates: str):
        shippingnotes = [m_shipdates[0] + "-" + m_canceldates[0]]
        for _ in range(1, self.length):
            shippingnotes.append("")

        return shippingnotes
    
    def fun_invoicedata_expiredate(self, m_shipdates: str):
        temp = []
        
        # if self.customer_name == "Walgreens":
        #     temp.append("".join([m_shipdates[0].split(" - ")[1].split("/")[i] for i in [2, 0, 1]]).replace("\n", ""))
        # else:
        if m_shipdates[0] != "":
            if self.customer_name in ["Family Dollar", "Walmart US", "Ollies", "Giant Tiger", "CVS", "Hobby Lobby", "Lekia", "Big Lots Stores", "Meijers", "MICHAELS", "Fred Meyer", "Tar Heel Trading"]:
                tem = m_shipdates[0].split("/")
                temp.append("".join([tem[i] for i in [2, 0, 1]]).replace("\n", ""))

            elif self.currency == "USD" and self.customer_name != "Buc-ee's":
                temp.append("".join(m_shipdates[0].split(".")[::-1]).replace("\n", ""))
            
            elif self.customer_name == "Gabe's":
                temp.append("".join(m_shipdates[0].split("/")[::-1]).replace("\n", ""))
                temp[0] = "20" + temp[0]
            elif self.customer_name in ["TEDI"]:
                temp.append("".join(m_shipdates[0].split(".")[::-1]).replace("\n", ""))
            elif self.customer_name in ["Walgreens", "TARGET"]:
                temp.append("".join([m_shipdates[0].split(" - ")[0].split("/")[i] for i in [2, 0, 1]]).replace("\n", ""))
            else:
                temp.append("".join(m_shipdates[0].split("/")[::-1]).replace("\n", ""))
        else:
            temp = [""]
        for _ in range(self.length - 1):
            temp.append("")

        return temp

    def fun_total(self, quantity, price_amount):
        total = [""]

        for i in range(1, self.length):
            total.append(quantity[i] * price_amount[i])

        return {"Total*": total}

    def fun_invoice(self):
        temp = []
        temp.append("invoice")
        for _ in range(self.length - 1):
            temp.append("invoicelines")

        return {"RecordType*": temp}
    
    def fun_remove_space(self, st):
        st = str(st)
        st = st.replace(" ", "")

        return st

    def re_init(self):
        self.additional_uom = pd.read_csv("config/uom_sku.csv")

    
        
    #Define several Integrate_funs that is needed for SalesImport
    def fun_Price_Amount(self, m_qty_ordered, m_unit_price):
        price_amount = []
        
        for i in range(1, self.length):
            if m_qty_ordered[i] == '': m_qty_ordered[i] = '0'
            if m_unit_price[i] == '': m_unit_price[i] = '0'
            price_amount.append(float(m_qty_ordered[i]) * (float(m_unit_price[i])))
        
        price_amount.insert(0, "")
        
        return price_amount
    
    def fun_invoicenumber(self, m_po_number):
        return m_po_number
    
    def fun_SKU_converter(self, input, uom):
        if uom == "Case":
            return 1
        else:
            temp = list(self.inventory_list[self.inventory_list["ProductCode"] == input]["DefaultUnitOfMeasure"])[0]
            if temp == "Unit":
                return 1
            else:
                # extract number from pattern "Case Pack 12 PD6 ..." (example, it is representative pattern)
                return re.findall("\d+", temp.split("Case Pack")[1])[0]

    def Integrate_final(self, matching_res, customer_name, terms, spreadsheet):
        # self.customer_name = customer_name
        self.inventory_list = frame_converter(spreadsheet.get_worksheet(1).get_all_records())
        c = CurrencyConverter()

        for name, Currency in zip(list(frame_converter(spreadsheet.get_worksheet(0).get_all_records())["Name"]), list(frame_converter(spreadsheet.get_worksheet(0).get_all_records())["Currency"])):
            self.currency_matcher.update({
                name: Currency
            })

        if terms[0] == "select":
            self.terms.append()
        for term in terms:
            self.terms.append(term)

        SalesImport = []
        for i in range(len(matching_res)):
            SalesImport.append({})

        for i,  element in enumerate(matching_res):
            #everything will be done here
            self.length = len(element[list(element.keys())[0]])

            # Create formula fields
            # # Initialize Customer_Name
            self.customer_name = self.customer_name_init
            if (self.customer_name in ["Pepco", "Poundland"]) and element["Currency"][0] == "CNY":
                self.customer_name = self.customer_name + " - RMB"
            
            else:
                if self.customer_name == "Pepco":
                    self.customer_name = self.customer_name + " - " + element["Currency"][0]
                
                elif self.customer_name == "Walmart":
                    if matching_res[0]["Currency"][0] == "US Dollar":
                        self.customer_name = self.customer_name + " US"

            self.currency = element["Currency"][0]
            
            # if "Pepco" not in self.customer_name:
            #     SalesImport[i].update(
            #         {
            #             "ShippingNotes": self.fun_shippingnotes(element["Ship Dates"], element["Cancel Date"]),
            #             "InvoiceDate*/ExpireDate": self.fun_invoicedata_expiredate(element["Ship Dates"]),
            #             "YourBaseCurrency*": self.fun_iter_top_currency(element["Currency"][0]),
            #             "CustomerCurrency*": self.fun_iter_top_currency(element["Currency"][0]),
                        
            #         }
            #     )
            # else:
            SalesImport[i].update(
                {
                    "ShippingNotes": self.fun_shippingnotes(element["Ship Dates"], element["Cancel Date"]),
                    "ShipmentRequiredByDate": self.fun_invoicedata_expiredate(element["Ship Dates"]),
                    "InvoiceDate*/ExpireDate": self.fun_invoicedata_expiredate(element["PO Date"]),
                    "YourBaseCurrency*": self.fun_iter_top_currency("USD"),
                    "CustomerCurrency*": self.fun_iter_top_currency_customer(),
                    "ShipToOther*": self.fun_iter_topp("NO")
                }
            )
            
            
            if self.customer_name in ["Buc-ee's", "CVS"]:
                SalesImport[i].update(
                    {
                        "BillingAddressLine1*": element["Ship To Address 1"],
                        # "BillingAddressLine2": element["Buying Party Address 2"],
                        "BillingCity*": element["Ship To City"],
                        "BillingProvince*": element["Ship To State"],
                        "BillingPostcode*": element["Ship to Zip"],
                        "BillingCountry*": element["Ship To Country"],
                        "ShippingAddressLine1*": element["Ship To Address 1"],
                        # "ShippingAddressLine2":element["Buying Party Address 2"],
                        "ShippingCity*": element["Ship To City"],
                        "ShippingProvince*": element["Ship To State"],
                        "ShippingPostcode*": element["Ship to Zip"],
                        "ShippingCountry*": element["Ship To Country"],
                    }
                )
            elif self.customer_name == "Poundland":
                SalesImport[i].update(
                    {
                        "CustomerEmail": element["Contact Email"],

                        "BillingAddressLine1*": element["Buying Party Address 1"],
                        # "BillingAddressLine2": element["Buying Party Address 2"],
                        "BillingCity*": element["Buying Party City"],
                        # "BillingProvince*": element["Buying Party State"],
                        # "BillingPostcode*": element["Buying Party Zip"],
                        # "BillingCountry*": element["Buying Party Country"],
                        "ShippingAddressLine1*":element["Buying Party Address 1"],
                        "ShippingAddressLine2":element["Buying Party Address 2"],
                        "ShippingCity*":element["Buying Party City"],
                        # "ShippingProvince*":element["Buying Party State"],
                        # "ShippingPostcode*":element["Buying Party Zip"],
                        # "ShippingCountry*":element["Buying Party Country"],
                    }
                )

            elif self.customer_name in ["Walmart US", "TARGET"]:
                SalesImport[i].update(
                    {
                        "BillingAddressLine1*": element["Buying Party Address 1"],
                        "BillingAddressLine2": element["Buying Party Address 2"],
                        "BillingCity*": element["Buying Party City"],
                        "BillingProvince*": element["Buying Party State"],
                        "BillingPostcode*": element["Buying Party Zip"],
                        "BillingCountry*": element["Buying Party Country"],
                        "ShippingAddressLine1*":element["Buying Party Address 1"],
                        "ShippingAddressLine2":element["Buying Party Address 2"],
                        "ShippingCity*":element["Buying Party City"],
                        "ShippingProvince*":element["Buying Party State"],
                        "ShippingPostcode*":element["Buying Party Zip"],
                        "ShippingCountry*":element["Buying Party Country"],
                    }
                )
                if self.customer_name == "TARGET":
                    SalesImport[i].update({
                        "ShipToCompany*": element["Buying Party Name"]
                    })

            elif self.customer_name in ["Big Lots Stores", "TARGET", "Walgreens", "Meijers", "MICHAELS", "Fred Meyer", "Tar Heel Trading"]:
        
                for key in self.add_match:
                    SalesImport[i].update({
                        key: element[self.add_match[key]]
                    })
            #customername
            #Add OMS_CustomerName addition functionality
            #frontend input here
            # lis_customer = [i for i in range(49)] 
            # with open("config/OMS_DB/OMS_Customers.csv", "a") as f:
            #     writer_object = writer(f)

            #     writer_object.writerow(lis_customer)
            #     f.close()

            
            
            
            SalesImport[i].update(
                {
                    "CustomerName*": self.fun_iter_all(self.customer_name),
                }
            )

            # Add InvoiceNumber*
            SalesImport[i].update(
                {
                    "InvoiceNumber*": self.fun_iter_all(element["PO Number"][0])
                }
            )

            # Add customername inherited fields
            SalesImport[i].update(self.auto_fun(self.customer_name))
            
            # Add RecordType
            SalesImport[i].update(self.fun_invoice())

            # Add [Product*, quantity*, Price/Amount], Total*
            product = {"Product*": [""]}
            quantity = {"Quantity*": [""]}
            price = {"Price/Amount*": [""]}

            def vendor_addition(input, num):
                temp = self.fun_SKU_converter(element["Vendor Style"][k], element["Unit of Measure"][1])

                product["Product*"].append(element["Vendor Style"][k])
                quantity["Quantity*"].append(int(float(input["Qty Ordered"][num])) / int(float(temp)))
                price["Price/Amount*"].append(float(self.fun_remove_space(input["Unit Price"][num])) * int(float(temp)))

            for k in range(1, self.length):
                vendor_addition(element, k)

            SalesImport[i].update(product)
            SalesImport[i].update(quantity)
            SalesImport[i].update(price)
            SalesImport[i].update(self.fun_total(quantity["Quantity*"], price["Price/Amount*"]))

            temp = [c.convert(1, SalesImport[i]["CustomerCurrency*"][0], "USD")]

            for _ in range(self.length - 1):
                temp.append("")

            SalesImport[i].update(
                {
                    "CurrencyConversionRate": temp
                }
            )

            SalesImport[i].update(
                {
                    "StockLocation": element["StockLocation"]
                }
            )

            #################################################################### Order Notes Addition ###################################################################
            temp_comment = []

            # PO Date
            if customer_name in ["Big Lots Stores", "Buc-ee's", "Five Below", "TARGET", "Walmart", "CVS", "Walgreens", "Meijers", "MICHAELS", "Fred Meyer", "Tar Heel Trading"]:
                temp_comment = ["PO Date: " + str(element["PO Date"][0])]
            
            # Dept #
            if customer_name in ["Big Lots Stores", "Buc-ee's", "Five Below", "TARGET", "Walmart", "CVS", "Walgreens", "Meijers", "Fred Meyer", "Tar Heel Trading"]:
                temp_comment[0] = temp_comment[0] + "\n"
                temp_comment[0] = temp_comment[0] + "Dept #: " + str(element["Dept #"][0])
            
            # Buyers Catalog or Stock Keeping #
            if customer_name in ["Big Lots Stores", "Buc-ee's", "TARGET", "Walmart", "Meijers", "MICHAELS", "Fred Meyer"]:
                temp_comment[0] = temp_comment[0] + "\n"
                temp_comment[0] = temp_comment[0] + "Buyers Catalog or Stock Keeping #: "
                for item in element["Buyers Catalog or Stock Keeping #"][1:]:
                    temp_comment[0] = temp_comment[0] + str(item) + "; "
                temp_comment[0] = temp_comment[0][:-2]
            
            # UPC/EAN
            if customer_name in ["Big Lots Stores", "Buc-ee's", "TARGET", "Walmart", "CVS", "Meijers", "Fred Meyer", "Tar Heel Trading"]:
                temp_comment[0] = temp_comment[0] + "\n"
                temp_comment[0] = temp_comment[0] + "UPC/EAN: "

                for item in element["UPC/EAN"][1:]:
                    try:
                        temp_comment[0] = temp_comment[0] + str(int(float(item))) + "; "
                    except:
                        temp_comment[0] = temp_comment[0] + str(item) + "; "
                temp_comment[0] = temp_comment[0][:-2]
            
            # Product/Item Description
            if customer_name in ["Big Lots Stores", "Buc-ee's", "Five Below", "TARGET", "CVS", "Walgreens", "Meijers", "MICHAELS", "Fred Meyer", "Tar Heel Trading"]:
                temp_comment[0] = temp_comment[0] + "\n"
                temp_comment[0] = temp_comment[0] + "Product/Item Description: "
                for item in element["Product/Item Description"][1:]:
                    temp_comment[0] = temp_comment[0] + str(item) + "; "
                temp_comment[0] = temp_comment[0][:-2]
            
            if customer_name in ["Big Lots Stores", "Buc-ee's", "Five Below", "TARGET", "Walmart", "CVS", "Walgreens", "Meijers", "MICHAELS", "Fred Meyer", "Tar Heel Trading"]:
                for _ in range(self.length - 1):
                    temp_comment.append("")
                SalesImport[i].update(
                    {
                        "Reference/Comment/Note": temp_comment
                    }
                )

            ################################################################### Shipping Notes Addition ###################################################################
            temp_ = []

            # Ship Dates
            if customer_name in ["Big Lots Stores", "Buc-ee's", "Five Below", "TARGET", "Walmart", "CVS", "Five Below", "Walgreens", "Meijers", "MICHAELS", "Fred Meyer", "Tar Heel Trading"]:
                temp_shippingnotes = ["Ship Dates: " + str(element["Ship Dates"][0])]
            
            # Cancel Date
            if customer_name in ["Buc-ee's", "TARGET", "Five Below", "Meijers", "MICHAELS", "Fred Meyer", "Tar Heel Trading"]:
                temp_shippingnotes[0] = temp_shippingnotes[0] + "\n"
                temp_shippingnotes[0] = temp_shippingnotes[0] + "Cancel Date: " + str(element["Cancel Date"][0])

            # Frt Terms
            if customer_name in ["Big Lots Stores", "TARGET", "Walmart", "Five Below", "Meijers", "MICHAELS", "Fred Meyer"]:
                temp_shippingnotes[0] = temp_shippingnotes[0] + "\n"
                temp_shippingnotes[0] = temp_shippingnotes[0] + "Frt Terms: " + str(element["Frt Terms"][0])

            # Other Info / #s
            if customer_name in ["Big Lots Stores", "Walmart", "Tar Heel Trading"]:
                temp_shippingnotes[0] = temp_shippingnotes[0] + "\n"
                temp_shippingnotes[0] = temp_shippingnotes[0] + "Other Info / #s: " + str(element["Other Info / #s"][0])

            # Carrier Details
            if customer_name in ["Walmart", "Meijers", "MICHAELS"]:
                temp_shippingnotes[0] = temp_shippingnotes[0] + "\n"
                temp_shippingnotes[0] = temp_shippingnotes[0] + "Carrier Details: " + str(element["Carrier Details"][0])

            # Ticket Description
            if customer_name in ["Five Below"]:
                temp_shippingnotes[0] = temp_shippingnotes[0] + "\n"
                temp_shippingnotes[0] = temp_shippingnotes[0] + "Ticket Description: " + str(element["Ticket Description"][0])

            # Notes/Comments
            if customer_name in ["Walmart", "Walgreens", "Five Below"]:
                temp_shippingnotes[0] = temp_shippingnotes[0] + "\n"
                temp_shippingnotes[0] = temp_shippingnotes[0] + "Notes/Comments: " + str(element["Notes/Comments"][0])
            
            # Ship To Name
            if customer_name in ["CVS", "MICHAELS"]:
                temp_shippingnotes[0] = temp_shippingnotes[0] + "\n"
                temp_shippingnotes[0] = temp_shippingnotes[0] + "Ship to location: " + str(element["Ship To Name"][0])

            # Ship To Location
            if customer_name in ["Fred Meyer", "Tar Heel Trading"]:
                temp_shippingnotes[0] = temp_shippingnotes[0] + "\n"
                temp_shippingnotes[0] = temp_shippingnotes[0] + "Ship to location: " + str(element["Ship To Location"][0])

            # Allow/Charge Type
            if customer_name in ["Walgreens"]:
                temp_shippingnotes[0] = temp_shippingnotes[0] + "\n"
                temp_shippingnotes[0] = temp_shippingnotes[0] + "Allow/Charge Type: " + str(element["Allow/Charge Type"][0])
            
            # Allow/Charge Service
            if customer_name in ["Walgreens"]:
                temp_shippingnotes[0] = temp_shippingnotes[0] + "\n"
                temp_shippingnotes[0] = temp_shippingnotes[0] + "Allow/Charge Service: " + str(element["Allow/Charge Service"][0])
            
            # Allow/Charge Desc
            if customer_name in ["Walgreens"]:
                temp_shippingnotes[0] = temp_shippingnotes[0] + "\n"
                temp_shippingnotes[0] = temp_shippingnotes[0] + "Allow/Charge Desc: " + str(element["Allow/Charge Desc"][0])

            # GTIN
            if customer_name in ["MICHAELS"]:
                temp_shippingnotes[0] = temp_shippingnotes[0] + "\n"
                temp_shippingnotes[0] = temp_shippingnotes[0] + "GTIN: "
                for item in element["GTIN"][1:]:
                    temp_shippingnotes[0] = temp_shippingnotes[0] + str(item) + "; "
                temp_shippingnotes[0] = temp_shippingnotes[0][:-2]

            if customer_name in ["Big Lots Stores", "Buc-ee's", "Five Below", "TARGET", "Walmart", "CVS", "Five Below", "Walgreens", "Meijers", "MICHAELS", "Fred Meyer", "Tar Heel Trading"]:
                for _ in range(self.length - 1):
                    temp_shippingnotes.append("")
                
                SalesImport[i].update(
                    {
                        "ShippingNotes": temp_shippingnotes
                    }
                )

            ################################################################### MemoOnInvoice ###################################################################
            temp_memo = []
            # Allow/Charge Type
            if customer_name in ["Meijers"]:
                temp_memo = ["Allow/Charge Type: " + str(element["Allow/Charge Type"][0])]
            
            # Allow/Charge Service
            if customer_name in ["Meijers"]:
                temp_memo[0] = temp_memo[0] + "\n"
                temp_memo[0] = temp_memo[0] + "Allow/Charge Service: " + str(element["Allow/Charge Service"][0])
            
            # Allow/Charge Desc
            if customer_name in ["Meijers"]:
                temp_memo[0] = temp_memo[0] + "\n"
                temp_memo[0] = temp_memo[0] + "Allow/Charge Desc: " + str(element["Allow/Charge Desc"][0])
            
            # Allow/Charge Amt
            if customer_name in ["Meijers"]:
                temp_memo[0] = temp_memo[0] + "\n"
                temp_memo[0] = temp_memo[0] + "Allow/Charge Amt: " + str(element["Allow/Charge Amt"][0])
            
            # Allow/Charge %
            if customer_name in ["Meijers"]:
                temp_memo[0] = temp_memo[0] + "\n"
                temp_memo[0] = temp_memo[0] + "Allow/Charge %: " + str(element["Allow/Charge %"][0])
            
            if customer_name in ["Meijers"]:
                for _ in range(self.length - 1):
                    temp_memo.append("")
                SalesImport[i].update(
                    {
                        "MemoOnInvoice": temp_memo
                    }
                )
        return SalesImport
