from decimal import Decimal


def dec2(input):
    return Decimal(str(input)).quantize(Decimal('.01'))