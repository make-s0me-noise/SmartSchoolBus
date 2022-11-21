DB = {
    'user'     : 'root',
    'password' : 'pass',
    'host'     : '127.0.0.1',
    'port'     : '3306',
    'database' : 'python_backend'
}

DB_URL = f"mysql+mysqlconnector://{DB['user']}:{DB['password']}@{DB['host']}:{DB['port']}/{DB['database']}?charset=utf8" 
DEFAULT_LONGITUDE = 127.07333331532686
DEFAULT_LATITUDE = 37.552369388104445
BUS = {}
BUS['LON'] = DEFAULT_LONGITUDE
BUS['LAT'] = DEFAULT_LATITUDE
BUS['LOCATION'] = 0
BUS['ONAIR'] = False
WEIGHT = {}
WEIGHT['board_weight'] = 0
WEIGHT['seat1'] = 0
WEIGHT['seat2'] = 0
WEIGHT['seat3'] = 0
WEIGHT['seat4'] = 0
WEIGHT['ONBOARD'] = False
WEIGHT['NUMOFSTU'] = 0

STATIONS = [[DEFAULT_LONGITUDE, DEFAULT_LATITUDE]]