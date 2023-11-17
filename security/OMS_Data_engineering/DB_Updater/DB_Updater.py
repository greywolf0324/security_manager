import pandas as pd
from csv import writer
from pathlib import Path

class Udpater:
    def __init__(self) -> None:
        pass
    
    def elaborator(self, file_path):
        temp_df = pd.read_csv(file_path, encoding = "latin-1")
        f = open(file_path, "w+")
        temp_df.to_csv(f, lineterminator = "\n", encoding = "utf-8")
        f.close()

    def updater(self, new_DB: list):
        #OMS udpate
        ## OMS_AditionalUOM: updating and elaborating
        with open(Path(__file__).resolve().parent.parent / "config/OMS_DB/OMS_AdditionalUOM.csv", "a") as f:
            for line in new_DB[0]:
                writer_object = writer(f)
                writer_object.writerow(line)
                f.close()
        
        # self.elaborator(Path(__file__).resolve().parent.parent / "config/OMS_DB/OMS_AdditionalUOM.csv")

        ## OMS_PaymentTerm: updating and elaborating
        with open(Path(__file__).resolve().parent.parent / "config/OMS_DB/OMS_PaymentTerm.csv", "a") as f:
            for line in new_DB[1]:
                writer_object = writer(f)

                writer_object.writerow(line)
                f.close()
        
        # self.elaborator(Path(__file__).resolve().parent.parent / "config/OMS_DB/OMS_PaymentTerm.csv")

        ## OMS_InventoryList: updating and elaborating
        with open(Path(__file__).resolve().parent.parent / "config/OMS_DB/OMS_InventoryList.csv", "a") as f:
            for line in new_DB[2]:
                writer_object = writer(f)

                writer_object.writerow(line)
                f.close()
        
        # self.elaborator(Path(__file__).resolve().parent.parent / "config/OMS_DB/OMS_InventoryList.csv")

        ## OMS_UOM: updating and elaborating
        with open(Path(__file__).resolve().parent.parent / "config/OMS_DB/OMS_UOM.csv", "a") as f:
            df_uom = pd.read_csv(Path(__file__).resolve().parent.parent / "config/OMS_DB/OMS_UOM.csv")
            writer_object = writer(f)
            df = pd.read_csv(Path(__file__).resolve().parent.parent / "config/OMS_DB/OMS_AdditionalUOM.csv")
            lis = df["AdditionalUnitsOfMeasureName"]

            temp_set = set(lis)

            for item in temp_set:
                if item not in list(df_uom["Name"]):
                    writer_object.writerow([item])

        # self.elaborator(Path(__file__).resolve().parent.parent / "config/OMS_DB/OMS_UOM.csv")

        #uom_sku udpate
        UOM = pd.read_csv(Path(__file__).resolve().parent.parent / "config/OMS_DB/OMS_AdditionalUOM.csv")
        uom = UOM[["BaseSKU", "AdditionalUnitsOfMeasureSKU", "NumberOfBaseUnitsInAdditionalUnit"]]
        # uom = UOM[["BaseSKU"]]
        keys = list(uom["BaseSKU"])

        dic = {}

        for i, key in enumerate(keys):
          dic.update({key: [uom["AdditionalUnitsOfMeasureSKU"][i], uom["NumberOfBaseUnitsInAdditionalUnit"][i]]})

        temp_df = pd.DataFrame(dic)
        temp_df.to_csv(Path(__file__).resolve().parent.parent / "config/uom_sku.csv", index = False, lineterminator = "\n")