from os.path import exists
import pandas as pd
from pathlib import Path
from ..utils.strings import string_converter

class AutoDB:
    def __init__(self) -> None:
        self.auto_dic = {}
        self.length = 0
        self.customer_name = ""
        self.SKU_list = ["Buc-ee's", "Dollarama", "Gabe's", "Family Dollar", "Walmart", "Big Lots Stores", "TARGET", "Five Below", "Lekia", "Meijers", "MICHAELS", "Fred Meyer"]
        self.customer_list = ["Pepco", "Poundland", "Walgreens", "Ollies", "TEDI", "CVS", "Giant Tiger", "Hobby Lobby"]

    def DB_tester(self, customer_name, matching_res):
        self.length = len(matching_res[0][list(matching_res[0].keys())[0]])
        self.customer_name = customer_name
        
        if not exists(Path(__file__).resolve().parent.parent / f"config/AutoFill_DB/{customer_name}.csv"):
            dic = {
                "PO":[],
                "Unit of Measure": [],
                "StockLocation": [],
                "Vendor Style from OMS_equal": [],
            }

            df = pd.DataFrame(dic)

            df.to_csv(Path(__file__).resolve().parent.parent / f"config/AutoFill_DB/{customer_name}.csv", index = False)
        
        else:
            self.auto_dic = {}
            auto_df = pd.read_csv(Path(__file__).resolve().parent.parent / f"config/AutoFill_DB/{customer_name}.csv", index_col = False)
            # print(auto_df["PO"], "***********")
            for item in string_converter(list(auto_df["PO"])):
                print(type(item), item, "__")

            print(type(string_converter(list(auto_df["PO"]))))
            print("______________________________________")
            if customer_name in self.SKU_list:
                for po in matching_res: 
                    # print(list(po["Vendor Style"])[1:])
                    for sku in list(po["Vendor Style"])[1:]:
                        # print("Printing autoFill_DB PO types...")
                        # if len(list(auto_df["PO"])) != 0:
                        #     print(type(list(auto_df["PO"])[0]))
                        # else:
                        #     print("DB is empty... :)")
                        
                        try:
                            sku_con = int(float(sku))
                        except:
                            sku_con = str(sku)

                        if sku_con in list(auto_df["PO"]):
                            self.auto_dic.update(
                                {
                                    sku_con: [list(auto_df[auto_df["PO"] == sku_con]["Unit of Measure"])[0], list(auto_df[auto_df["PO"] == sku_con]["StockLocation"])[0], list(auto_df[auto_df["PO"] == sku_con]["Vendor Style from OMS_equal"])[0]]
                                }
                            )
            
            else:
                # for item in list(auto_df["PO"]):
                #     print(type(item), item)
                for po in matching_res: 
                    
                    for sku in list(po["Buyers Catalog or Stock Keeping #"])[1:]:
                        # for sku in list(po["Buyers Catalog or Stock Keeping #"])[1:]:
                        #     print(type(sku), sku, "__")
                        # print(str(sku))
                        # if str(sku) == "724510":
                        #     print("same_____")
                        if str(sku) in string_converter(list(auto_df["PO"])):
                            # print("+++++++++++++++++++++++++++++++++++++++++++++++")
                            self.auto_dic.update(
                                {
                                    int(sku): [list(auto_df[auto_df["PO"] == int(float(sku))]["Unit of Measure"])[0], list(auto_df[auto_df["PO"] == int(float(sku))]["StockLocation"])[0], list(auto_df[auto_df["PO"] == int(float(sku))]["Vendor Style from OMS_equal"])[0]]
                                }
                            )
                        # else:
                        #     print(str(sku), "++++++++")
        return self.auto_dic

    def auto_DB_updater(self, sku_match, customer_name):
        db = pd.read_csv(Path(__file__).resolve().parent.parent / f"config/AutoFill_DB/{customer_name}.csv")

        POs = []
        UOMs = []
        LOCATIONs = []
        TARGETs = []
        po_list = []

        for item in list(db["PO"]):
            po_list.append(str(item))

        for key in sku_match:
            if str(key) not in po_list:
                POs.append(str(key))
                UOMs.append(sku_match[key][0])
                LOCATIONs.append(sku_match[key][1])
                TARGETs.append(sku_match[key][2])
        
        df = pd.DataFrame(
            {
                "PO": POs,
                "Unit of Measure": UOMs,
                "StockLocation": LOCATIONs,
                "Vendor Style from OMS_equal": TARGETs,
            }
        )

        df.to_csv(Path(__file__).resolve().parent.parent / f"config/AutoFill_DB/{customer_name}.csv", header = False, mode = "a", index = False)