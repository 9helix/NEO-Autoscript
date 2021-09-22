import pickle, math
from builtins import open # Keep in context
from pathlib import Path
from neo_autoscript.config import DATA_FILE


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
    jd = float(jd)
    jd_frac = math.modf(jd)[0] + 0.5
    ms, h = math.modf(jd_frac * 24)
    s, m = math.modf(ms * 60)
    return f'{h:02.0f}{m:02.0f}{s*60:02.0f}'
