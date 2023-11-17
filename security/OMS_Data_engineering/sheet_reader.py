import pandas as pd

def frame_converter(data):
    keys = list(data[0].keys())
    
    dic = {}
    for key in keys:
        dic.update(
            {
                key: []
            }
        )
    
    for element in data:
        for key in element:
            dic[key].append(str(element[key]))

    return pd.DataFrame(dic)