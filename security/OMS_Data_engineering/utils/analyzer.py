

def Input_analyzer(file_contents):
    pass

def Output_analyzer(file_contents):

    user_names = []
    po_dates = []
    for file_content in file_contents:
        file_content = str(file_content)
        temp = file_content

        locs = []
        while temp.find('"') + 1:
            locs.append(temp.find('"'))
            temp = temp[locs[-1] + 1:]

        if len(locs) != 0:
            po_date = file_content[locs[0] + locs[1] + 1:].split(",")[23]

            str_date = []
            if po_date:
                po_date = str(int(float(po_date)))
                str_date = [po_date[4:6], po_date[6:], po_date[:4]]

                if str_date[0][0] == "0":
                    str_date[0] = str_date[0][1]

                if str_date[1][0] == "0":
                    str_date[1] = str_date[1][1]

                po_dates.append("/".join(str_date))
        
        else:
            po_dates.append("")
        temp_name = str(file_content).split("\\r\\n")[1]
        temp_name = temp_name.split(",")[1]
        temp_name = temp_name.replace("\\", "")
        user_names.append(temp_name)
        
    return [user_names, po_dates]