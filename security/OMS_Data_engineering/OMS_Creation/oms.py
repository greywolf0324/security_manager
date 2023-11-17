import pandas as pd
from pathlib import Path

class OMS_Creation:
  def __init__(self) -> None:
    self.uom = pd.read_csv(Path(__file__).resolve().parent.parent / "config/OMS_DB/OMS_UOM.csv")
    self.inventory = pd.read_csv(Path(__file__).resolve().parent.parent / "config/OMS_DB/OMS_InventoryList.csv")
    self.length = 0

  def UOM_Addition(self, input):
     for page in input:
      for product in page["Product*"][1:]:
          if product.split("-")[1] not in self.uom["Name"]:
              #Add uom to UOM
              pass
          
  def InventoryList_Addition(self, input):
     for page in input:
        self.length = len(page[list(page.keys())[0]])

        for product in page["Product*"][1:]:
           if product.split("-")[0] not in self.inventory["ProductCode"]:
              #Add production to Inventory_List
              pass

  def OMS_generator(self, SalesImport):

    #OMS_UOM
    self.UOM_Addition(SalesImport)
    
    #OMS_InventoryList
    self.InventoryList_Addition(SalesImport)