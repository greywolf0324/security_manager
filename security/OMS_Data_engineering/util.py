from collections import OrderedDict

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
        print("=-=-", field_len)
        for field in fields:
            if field not in po.keys():
                po.update({
                    field: [''] * field_len
                })

    return input