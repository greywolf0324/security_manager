

def space_remover(input: str):
    return input.replace(" ", "")

def string_converter(input: list):
    temp = []

    for item in input:
        temp.append(str(item))

    return temp