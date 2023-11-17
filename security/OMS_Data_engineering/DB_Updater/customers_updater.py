import pandas as pd
from pathlib import Path
from ..sheet_reader import frame_converter
from google.oauth2 import service_account
import gspread
import json

def customer_fields_updater():
    f = open(Path(__file__).resolve().parent.parent / "config/django-connection-1008-5f931d8f4038.json")
    google_json = json.load(f)
    credentials = service_account.Credentials.from_service_account_info(google_json)
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    creds_with_scope = credentials.with_scopes(scope)
    client = gspread.authorize(creds_with_scope)
    spreadsheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1CDnIivm8hatRQjG7nvbMxG-AuP19T-W2bNAhbFwEuE0")
        
    # data = pd.read_csv(Path(__file__).resolve().parent.parent / "config/OMS_DB/OMS_Customers.csv", index_col = False)
    data = frame_converter(spreadsheet.get_worksheet(0).get_all_records())
    OMS_Customer_Sales_Import = {
        "TaxRule*": "TaxRule",
        "Account": "SaleAccount",
        "PriceTier": "PriceTier",
        "Discount": "Discount",
        "SalesRepresentative*": "SalesRepresentative",
        "StockLocation": "Location",
        "CustomerContact": "ContactComment",
        "CustomerPhone": "Phone",
        "CustomerEmail": "Email",
        "Terms": "PaymentTerm"
    }

    res = {}

    keys = list(data["Name"])

    values = []

    for key in OMS_Customer_Sales_Import:
        values.append(list(data[OMS_Customer_Sales_Import[key]]))

    for i, key in enumerate(keys):
        temp = []

        for j in range(len(OMS_Customer_Sales_Import)):
            temp.append(values[j][i])
        # print(key)
        res.update(
            {
                key: temp
            }
        )
    # print(res)
    df = pd.DataFrame(res)
    # print(df.head())
    df.to_csv(Path(__file__).resolve().parent.parent / "config/customer_fields.csv")

customer_fields_updater()