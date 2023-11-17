import pandas as pd
from pathlib import Path


UOM = pd.read_csv(Path(__file__).resolve().parent.parent / "config/OMS_DB/OMS_AdditionalUOM.csv", index_col = False)
uom = UOM[["BaseSKU", "AdditionalUnitsOfMeasureSKU", "NumberOfBaseUnitsInAdditionalUnit"]]
# uom = UOM[["BaseSKU"]]
keys = list(uom["BaseSKU"])

dic = {}

for i, key in enumerate(keys):
  print(uom["BaseSKU"], uom["NumberOfBaseUnitsInAdditionalUnit"])
  dic.update({key: [uom["AdditionalUnitsOfMeasureSKU"][i], uom["NumberOfBaseUnitsInAdditionalUnit"][i]]})

temp_df = pd.DataFrame(dic)
temp_df.to_csv(Path(__file__).resolve().parent.parent / "config/uom_sku.csv", index = False, lineterminator = "\n")