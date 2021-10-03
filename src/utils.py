import pickle
from builtins import open  # Keep in context
from pathlib import Path
from config import DATA_FILE


@type.__call__
class PersistentData:

    def __init__(self):
        if Path(DATA_FILE).exists():
            ns = pickle.load(open(Path(DATA_FILE), 'rb'))
            self.__dict__.update(ns)

    def __del__(self):
        ns = self.__dict__
        pickle.dump(ns, open(Path(DATA_FILE), 'wb'))


def jd_to_hhmmss(jd):
    JDtime = str(jd)
    decimal_part = JDtime[JDtime.find('.')+1:]
    decimal_part = float(decimal_part)/(10**len(decimal_part))+0.5
    day_decimal = str(decimal_part*24)
    hr_decimal = day_decimal[:day_decimal.find('.')]

    min_decimal = str(round(float(day_decimal.replace(hr_decimal, ''))*60))
    #min_decimal = min_decimal[:min_decimal.find('.')]
    hr_decimal = int(hr_decimal)
    min_decimal = int(min_decimal)
    if hr_decimal >= 24:
        hr_decimal -= 24
    if min_decimal >= 60:
        hr_decimal += 1
        min_decimal -= 60
    if hr_decimal >= 24:
        hr_decimal -= 24
    hr_decimal = str(hr_decimal)
    min_decimal = str(min_decimal)
    if len(hr_decimal) == 1:
        hr_decimal = '0'+hr_decimal
    if len(min_decimal) == 1:
        min_decimal = '0'+min_decimal
    time = hr_decimal+min_decimal
    return time
