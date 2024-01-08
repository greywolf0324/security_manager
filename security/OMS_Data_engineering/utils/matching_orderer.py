from ...models import Osalesimport_fields
from collections import OrderedDict

osales_fields = [item.field_name for item in Osalesimport_fields.objects.all()]

def Orderer(matching_input):
    matching_res = []

    for matching in matching_input:
        d = OrderedDict(matching)

        for key in osales_fields:
            d.move_to_end(key)
        
        matching_res.append(d)

    return matching_res