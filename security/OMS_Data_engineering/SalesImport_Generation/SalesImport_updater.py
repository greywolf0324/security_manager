from pathlib import Path
import json

class SalesImport_Updater:
    def __init__(self) -> None:
        f = open(Path(__file__).resolve().parent.parent / "config/fieldnames_SalesImport.json")
        self.field_names = json.load(f)

        pass

    def updater(self, sales_import):
        updated_salesimport = []

        for invoice_num, invoice in enumerate(sales_import):
            

            if len(set(invoice["StockLocation"][1:])) == 1:
                updated_salesimport.append({})
                for key in self.field_names:
                    updated_salesimport[-1].update({
                        key:[]
                    })

                for key in self.field_names:
                    if key == "StockLocation":
                        updated_salesimport[-1][key].append(invoice[key][1])
                    
                    else:
                        try:
                            updated_salesimport[-1][key].append(invoice[key][0])
                        except:
                            updated_salesimport[-1][key].append("")

                for i in range(1, len(invoice[list(invoice.keys())[0]])):
                    for key in self.field_names:
                        if key == "StockLocation":
                            updated_salesimport[-1][key].append("")

                        else:
                            try:
                                updated_salesimport[-1][key].append(invoice[key][i])
                            except:
                                updated_salesimport[-1][key].append("")

                updated_salesimport[-1] = invoice
                updated_salesimport[-1]["StockLocation"][0] = updated_salesimport[-1]["StockLocation"][1]

                for i in range(1, len(invoice[list(invoice.keys())[0]])):
                    updated_salesimport[-1]["StockLocation"][i] = ""

                continue

            else:
                location_list = list(set(invoice["StockLocation"][1:]))

                updated_num = 0
                for location in location_list:
                    updated_salesimport.append({})
                    updated_num = updated_num + 1

                    for key in self.field_names:
                        updated_salesimport[-1].update({
                            key: []
                        })
                        
                    for key in self.field_names:
                        if key == "InvoiceNumber*":
                            updated_salesimport[-1][key].append(str(invoice[key][0]) + f"-{updated_num}")    
                        
                        elif key == "StockLocation":
                            updated_salesimport[-1][key].append(location)    
                    
                        else:
                            try:
                                updated_salesimport[-1][key].append(invoice[key][0])
                            except:
                                updated_salesimport[-1][key].append("")
                    
                    for i in range(1, len(invoice[list(invoice.keys())[0]])):
                        if invoice["StockLocation"][i] == location:
                            for key in self.field_names:
                                if key == "StockLocation":
                                    updated_salesimport[-1][key].append("")

                                elif key == "InvoiceNumber*":
                                    updated_salesimport[-1][key].append(str(invoice[key][0]) + f"-{updated_num}") 

                                else:
                                    try:
                                        updated_salesimport[-1][key].append(invoice[key][i])
                                    except:
                                        updated_salesimport[-1][key].append("")

        return updated_salesimport
