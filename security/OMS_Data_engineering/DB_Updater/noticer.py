import pandas as pd
from pathlib import Path
from google.oauth2 import service_account
import gspread
from ..sheet_reader import frame_converter
import json

class NOTICER:
  def __init__(self) -> None:
    f = open(Path(__file__).resolve().parent.parent / "config/django-connection-1008-5f931d8f4038.json")
    google_json = json.load(f)
    credentials = service_account.Credentials.from_service_account_info(google_json)
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    creds_with_scope = credentials.with_scopes(scope)
    client = gspread.authorize(creds_with_scope)
    spreadsheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1CDnIivm8hatRQjG7nvbMxG-AuP19T-W2bNAhbFwEuE0")
      
    self.additional_uom = pd.read_csv(Path(__file__).resolve().parent.parent / "config/uom_sku.csv")
    # self.paymentterms = pd.read_csv(Path(__file__).resolve().parent.parent / "config/OMS_DB/OMS_PaymentTerm.csv")
    self.paymentterms = frame_converter(spreadsheet.get_worksheet(2).get_all_records())
    
    self.length = 0
    self.new_additional_uom = set()
    self.new_paymentterm = set()
    self.new_InventoryList = set()

  def getter(self, matching_res):
    # print(type(matching_res))
    for i, element in enumerate(matching_res):
      self.length = len(element[list(element.keys())[0]])

      for k in range(1, self.length):
        if (element["Vendor Style"][k] not in self.additional_uom.keys()) and (element["Vendor Style"][k] not in self.new_additional_uom):
          self.new_additional_uom.add(element["Vendor Style"][k])
      
      if element["Frt Terms"][0] == "":
        self.new_paymentterm.add(element["Frt Terms"][0])
      
      else:
        if element["Frt Terms"][0] not in list(self.paymentterms["Name"]):
          self.new_paymentterm.add(element["Frt Terms"][0])
    
    self.new_InventoryList = self.new_additional_uom

    return [list(self.new_additional_uom), list(self.new_paymentterm), list(self.new_InventoryList)]