from collections import OrderedDict
import pandas as pd

def orderer(input, fields):
    matching_res = []

    for matching in input:
        d = OrderedDict(matching)

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