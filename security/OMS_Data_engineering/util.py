# from monday import MondayClient
import requests
import json
from collections import OrderedDict
import pandas as pd
from ..models import OMS_Customers, OMS_Locations, OMS_Inventory_List
import time

def orderer(input, fields, customer_name):
    matching_res = []

    for matching in input:
        d = OrderedDict(matching)

        # if customer_name == "MICHAELS":
        #     for key in fields[:-1]:
        #         d.move_to_end(key)
        # else:
        for key in fields:
            d.move_to_end(key)
        
        matching_res.append(d)

    return matching_res

def field_adder(input: list, fields):
    field_len = len(input[0][list(input[0].keys())[0]])
    
    for po in input:
        field_len = len(po[list(po.keys())[0]])
        for field in fields:
            if field not in po.keys():
                po.update({
                    field: [''] * field_len
                })

    return input

def monday_pagefetcher():
    Customers_boardID = 5790363144
    Inventory_boardID = 5829229370
    StockLocation_boardID = 5751350023
    
    def customer_writer(database):
        for customer in database:
            input = OMS_Customers(
                Name = customer["name"],
                Status = customer["column_values"][9]["text"],
                Currency = customer["column_values"][10]["text"],
                PaymentTerm = customer["column_values"][11]["text"],
                TaxRule = customer["column_values"][12]["text"],
                PriceTier = customer["column_values"][13]["text"],
                Discount = customer["column_values"][14]["text"],
                CreditLimit = customer["column_values"][15]["text"],
                Carrier = customer["column_values"][17]["text"],
                SalesRepresentative = customer["column_values"][18]["text"],
                Location = customer["column_values"][19]["text"],
                TaxNumber = customer["column_values"][20]["text"],
                Tags = customer["column_values"][22]["text"],
            )
            input.save()
    
    def inventory_writer(database):
        for inventory in database:
            input = OMS_Inventory_List(
                ProductCode = inventory["name"],
                Name = inventory["column_values"][1]["text"],
                Type = inventory["column_values"][2]["text"],
                # Brand = inventory["column_values"][3]["text"],
                CostingMethod = inventory["column_values"][5]["text"],
                DefaultUnitOfMeasure = inventory["column_values"][6]["text"],
                PurchaseTaxRule = inventory["column_values"][11]["text"],
                SaleTaxRule = inventory["column_values"][12]["text"],
                Status = inventory["column_values"][18]["text"],
                DefaultLocation = inventory["column_values"][19]["text"],
                Length = inventory["column_values"][41]["text"],
                Width = inventory["column_values"][42]["text"],
                Height = inventory["column_values"][43]["text"],
                Weight = inventory["column_values"][44]["text"],
                WeightUnits = inventory["column_values"][45]["text"],
            )
            input.save()

    def location_writer(database):
        for location in database:
            input = OMS_Locations(
                Location = location["name"]
            )
            input.save()

    def db_clearer(OMS):
        x = OMS.objects.all()
        x.delete()

    def init_querier(board_id):
        init_query = f'{{boards (ids: {board_id}) {{name items_count description items_page(limit: 50) {{cursor items{{name column_values{{id value text type}}}}}}}} }}'
        data = {'query': init_query}

        r = requests.post(url=apiUrl, headers=header, json=data)
        res = json.loads(r.text)

        return res
    
    def querier(cursor_key):
        query = """query {
                            next_items_page (limit: 50, cursor: "%s") {
                                cursor
                                items {
                                id
                                name
                                column_values{
                                    id
                                    value
                                    type
                                    text
                                }
                                }
                            }
                            }""" % cursor_key

        data = {'query' : query}

        r = requests.post(url=apiUrl, json=data, headers=header)

        res = json.loads(r.text)

        return res

    page_count = 50    
    apiUrl = "https://api.monday.com/v2"
    apiKey = "eyJhbGciOiJIUzI1NiJ9.eyJ0aWQiOjMxNTY0MDE4NiwiYWFpIjoxMSwidWlkIjo1MzU2MTE3OSwiaWFkIjoiMjAyNC0wMS0zMFQxMzowMToyOC4wMDBaIiwicGVyIjoibWU6d3JpdGUiLCJhY3RpZCI6MTQwOTEyNjQsInJnbiI6InVzZTEifQ.8C67Rzk5p64CozxxpGB-bbTn5BPv27TwF7dQ-3bTTuk"
    header = {"Authorization": apiKey}
    
    # monday = MondayClient(token = apiKey)


    db_clearer(OMS_Customers)
    # db_clearer(OMS_Inventory_List)
    # db_clearer(OMS_Locations)

    res = init_querier(Customers_boardID)
    cursor_key = res['data']['boards'][0]['items_page']['cursor']
    items = res['data']['boards'][0]['items_page']['items']
    customer_writer(items)

    count = len(items)
    while count == page_count:
        print("writing...")
        res = querier(cursor_key)
        cursor_key = res['data']['next_items_page']['cursor']
        items = res['data']['next_items_page']['items']
        count = len(items)
        customer_writer(items)

    # num = 1
    # arr = monday.boards.fetch_items_by_board_id(board_ids = Customers_boardID, limit = 100, page=num)
    # db = [item for item in [item for item in arr['data']['boards'][0]['items']]]
    # print(0, "==========")
    # print(db[0])
    # customer_writer(db)

    # while len([item for item in [item for item in arr['data']['boards'][0]['items']]]) == 100:
    #     print(num, "==========")
    #     num += 1
    #     arr = monday.boards.fetch_items_by_board_id(board_ids = Customers_boardID, limit = 100, page=num)
    #     db = [item for item in [item for item in arr['data']['boards'][0]['items']]]
        
    #     customer_writer(db)

    # ==================================================================================================================================
    
    # res = init_querier(Inventory_boardID)
    # cursor_key = res['data']['boards'][0]['items_page']['cursor']
    # items = res['data']['boards'][0]['items_page']['items']
    # inventory_writer(items)

    # count = len(items)
    # while count == page_count:
    #     print("writing...")
    #     res = querier(cursor_key)
    #     cursor_key = res['data']['next_items_page']['cursor']
    #     items = res['data']['next_items_page']['items']
    #     count = len(items)
    #     inventory_writer(items)

    # ==================================================================================================================================
    # num = 1
    # arr = monday.boards.fetch_items_by_board_id(board_ids = StockLocation_boardID, limit = 100, page=num)
    # db = [item for item in [item for item in arr['data']['boards'][0]['items']]]
    
    # location_writer(db)

    # while len([item for item in [item for item in arr['data']['boards'][0]['items']]]) == 100:
    #     print(num, "==========")
    #     num += 1
    #     arr = monday.boards.fetch_items_by_board_id(board_ids = StockLocation_boardID, limit = 100, page=num)
    #     db = [item for item in [item for item in arr['data']['boards'][0]['items']]]
        
    #     location_writer(db)

def modelto_dataframe(DB_model, Fields_model):
    DB = DB_model.objects.all()
    Fields = Fields_model.objects.all()
    DB_fields = [f.name for f in DB_model._meta.get_fields()]
    
    dic = {}
    for field in Fields:
        dic.update({
            field.field_name: []
        })

    for invent in DB:
        for field_name, field in zip(Fields, DB_fields[1:]):
            dic[field_name.field_name].append(DB_model._meta.get_field(field).value_from_object(invent))

    df = pd.DataFrame(dic)

    return df