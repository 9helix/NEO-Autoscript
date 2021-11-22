from enum import Enum


NEOCONFIRM_URL = 'https://www.minorplanetcenter.net/iau/NEO/toconfirm_tabular.html'
NEOCONFIRM_CGI = 'https://cgi.minorplanetcenter.net/cgi-bin/confirmeph2.cgi'

DATA_FILE = './output/NEO_data.pkl'
DATA_DIR = './output'


class EphemInterval(int, Enum):

    MINUTES_60 = 0
    MINUTES_30 = 1
    MINUTES_10 = 2
    MINUTES_01 = 3


class Settings:

    def __init__(self, **kwargs):
        type(self).__dict__.update(kwargs)

    obs_code = 'L01'
    obs_start = None
    obs_interval = 5
    ephem_interval = EphemInterval.MINUTES_10
    max_mag = 22
    min_alt = 20
    min_speed = 10
    post_open_script = True  
    post_open_excluded = True  
