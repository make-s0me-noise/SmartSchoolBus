import requests
from json import loads, dumps
from urllib.parse import urlparse
import sys
from config import *
import pymysql

import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

import numpy as np
import geopandas as gpd
from shapely.geometry import Point, Polygon
import geog
import warnings
from shapely.errors import ShapelyDeprecationWarning
from haversine import haversine
warnings.filterwarnings("ignore", category=ShapelyDeprecationWarning) 

from setting import createContentInstance_

DATA = {}
deviceToken = ''
DEBUG = True
def appnotification(token,title,content):
    expoURL = "https://exp.host/--/api/v2/push/send"
    header = {
        'Content-Type': 'application/json'
    }
    notidata = {
        "to": token,
        "title":title,
        "body":content
    }
    requests.post(expoURL,headers=header,json=notidata)

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        full_query = parsed_path.query
        result = {}
        # print("deviceToken =",deviceToken)
        # appnotification(deviceToken,"제목입니다.","컨텐츠에요")
        
        if full_query != '':
            if DEBUG:
                print("[*] full_query : " + full_query)
            for query in full_query.split('&'):
                key, val = query.split('=')

                # 학생 id를 바탕으로, 실시간 버스 위치 조회 및 내 아이 도착 정보 조회
                if key == 'sid':
                    result['student'] = {}
                    try:
                        sql_query = "SELECT station_id FROM student WHERE id={}".format(val)
                        cursor.execute(sql_query)
                        station_id = cursor.fetchone()[0]
                    except TypeError:
                        if DEBUG:
                            print("[-] student doesn't exist :(\n")
                        result['student']['err_msg'] = 'student doesn\'t exist :('

                    else:
                        try:
                            sql_query = "SELECT pass_flag FROM station WHERE id={}".format(station_id)
                            cursor.execute(sql_query)
                            isArrived = cursor.fetchone()[0]
                        except TypeError:
                            if DEBUG:
                                print("[-] station doesn't exist :(\n")
                            result['student']['err_msg'] = 'station for student doesn\'t exist :('

                        else:
                            result['student']['bus_id'] = 1
                            result['student']['onair_flag'] = BUS['ONAIR']

                            if BUS['ONAIR'] == 1: # 버스 운행 중일 때,
                                result['student']['longitude'] = BUS['LON']
                                result['student']['latitude'] = BUS['LAT']
                                result['student']['bus_starttime'] = BUS['START_TIME']

                                if isArrived == 1: # 아이가 도착했을 때,
                                    result['student']['bus_arrival'] = 1
                                    result['student']['bus_howmanytime'] = 0
                                    
                                else: # 아이가 아직 도착하지 않았을 때,
                                    sql_query = "SELECT SUM(howmanytime) FROM station WHERE id<={} AND pass_flag=0".format(station_id)
                                    cursor.execute(sql_query)
                                    arrival_time = cursor.fetchone()[0]
                                    
                                    result['student']['bus_arrival'] = 0
                                    result['student']['bus_howmanytime'] = int(arrival_time)
                                    if DEBUG:
                                        print("[*] arrival time : {}".format(arrival_time))

                            else: # 버스가 운행 중이지 않을 때,
                                result['student']['err_msg'] = 'bus hasn\'t left yet'
                                result['student']['longitude'] = DEFAULT_LONGITUDE
                                result['student']['latitude'] = DEFAULT_LATITUDE    

                # 버스 id를 바탕으로, 동승자 및 운전자 정보 조회
                if key == 'bid':
                    result['bus'] = {} 

                    try:
                        sql_query = "SELECT id, fellow_flag, fellow_id, driver_id FROM bus WHERE id={}".format(val)
                        cursor.execute(sql_query)
                        bus_id, fellow_flag, fellow_id, driver_id = cursor.fetchone()
                    except TypeError:
                        if DEBUG:
                            print("[-] bus doesn't exist :(\n")
                        result['bus']['err_msg'] = 'bus doesn\'t exist :('

                    else:
                        result['bus']['id'] = bus_id
                        result['bus']['fellow_flag'] = fellow_flag
                        result['bus']['driver'] = {}
                        result['bus']['fellow'] = {}
                        
                        if fellow_flag == 0:
                            if DEBUG:
                                print("[-] identification for a passenger failed :(\n")
                            result['bus']['err_msg'] = 'identification for a passenger failed :(' 
                        elif fellow_flag == 2:
                            if DEBUG:
                                print("[-] identification for a passenger is ongoing ;)\n")
                            result['bus']['err_msg'] = 'identification for a passenger is ongoing ;)'
                        else:
                            try:
                                sql_query = "SELECT * FROM fellow_driver WHERE id={}".format(fellow_id)
                                cursor.execute(sql_query)
                                fellow_id, fellow_name, fellow_phonenum = cursor.fetchone()
                            except TypeError:
                                if DEBUG:
                                    print("[-] fellow doesn't exist :(\n")
                                result['bus']['err_msg'] = 'fellow doesn\'t exist :('

                            else:
                                result['bus']['fellow']['id'] = fellow_id
                                result['bus']['fellow']['name'] = fellow_name
                                result['bus']['fellow']['phonenum'] = fellow_phonenum

                                try:
                                    sql_query = "SELECT * FROM fellow_driver WHERE id={}".format(driver_id)
                                    cursor.execute(sql_query)
                                    driver_id, driver_name, driver_phonenum = cursor.fetchone()
                                except TypeError:
                                    if DEBUG:
                                        print("[-] driver doesn't exist :(\n")
                                    result['bus']['err_msg'] = 'driver doesn\'t exist :('

                                else:
                                    result['bus']['driver']['id'] = driver_id
                                    result['bus']['driver']['name'] = driver_name
                                    result['bus']['driver']['phonenum'] = driver_phonenum
        # else:
        #     print("parsed_path : {}".format(parsed_path))

        if DEBUG:
            print(result)
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(dumps(result).encode(encoding='utf-8'))


    def do_POST(self):
        length = int(self.headers['Content-Length'])
        contentType = self.headers['Content-Type']
        post_data = self.rfile.read(length)
        
        # print('\n### Notification')
        parsed_path = urlparse(self.path)
        full_query = parsed_path.query
        content_length = int(self.headers['Content-Length'])
        
        # 기기 토큰 받기
        print("[*] parsed_path : {}".format(parsed_path))
        if parsed_path.path == '/token':
            deviceToken = loads(post_data.decode('utf8'))['token']
            print("토큰 등록 완료 :", deviceToken)

            sql_query = "UPDATE student SET device_id='{}' WHERE id=3".format(deviceToken)
            cursor.execute(sql_query)
            conn.commit()
            
        else:
            r = loads(post_data.decode('utf8').replace("'", '"'))
            # if DEBUG:
            #     print(self.headers)
            #     print(r)
            #     print(r['m2m:sgn']['sur'].split('/'))
            
            path = r['m2m:sgn']['sur'].split('/')
            # if DEBUG:
            #     print(path)
        
            component = path[2]
            sensorType = path[3]
            fullPath = component + '/' + sensorType

        
            CIN = False
            SUB = False
            try:
                rn = r['m2m:sgn']['nev']['rep']['m2m:cin']['con']
                CIN = True
            except:
                rn = r['m2m:sgn']['nev']['rep']['m2m:sub']['rn']
                SUB = True


            if CIN:
                try:
                    sensorValue = int(r['m2m:sgn']['nev']['rep']['m2m:cin']['con'])
                except ValueError:
                    sensorValue = float(r['m2m:sgn']['nev']['rep']['m2m:cin']['con'])

                if sensorType.startswith("gps"):
                    if sensorType == 'gps_lon':
                        BUS['LON'] = sensorValue
                        sql_query = "UPDATE bus SET longitude={} WHERE id=1".format(sensorValue)
                        cursor.execute(sql_query)
                        conn.commit()

                    elif sensorType == 'gps_lat':
                        BUS['LAT'] = sensorValue
                        sql_query = "UPDATE bus SET latitude={} WHERE id=1".format(sensorValue)
                        cursor.execute(sql_query)
                        conn.commit()
                
                    CUR_GPS = Point([BUS['LON'], BUS['LAT']])
                    if BUS['ONAIR'] == 0: # 버스가 아직 출발하지 않았을 때,
                        if CUR_GPS.within(STATIONS[BUS['LOCATION']]) == False:
                            BUS['START_TIME'] = r['m2m:sgn']['nev']['rep']['m2m:cin']['ct']
                            BUS['ONAIR'] = 1

                            sql_query = "UPDATE bus SET onair_flag=1, start_time='{}', end_time=NULL WHERE id=1".format(BUS['START_TIME'])
                            cursor.execute(sql_query)

                            sql_query = "UPDATE station SET pass_flag=0"
                            cursor.execute(sql_query)
                            conn.commit()

                            createContentInstance_('bus/fellow', 'camera_comm', 1)
                            if DEBUG:
                                print("[*] Bus started driving :)\n")
                            
                            sql_query = "SELECT device_id FROM student"
                            cursor.execute(sql_query)
                            result = cursor.fetchall()
                            for data in result:
                                device_id = data[0]
                                appnotification(device_id, "Smart School Bus", "버스가 출발했습니다.")

                    elif BUS['ONAIR'] == 1: # 버스가 운행 중일 때,                    
                        if DEBUG:
                            print(CUR_GPS.within(STATIONS[(BUS['LOCATION'] + 1) % len(STATIONS)]))
                            print((BUS['LOCATION'] + 1))
                            print((BUS['LOCATION'] + 1) % len(STATIONS))
                            print(STATIONS[(BUS['LOCATION'] + 1) % len(STATIONS)].distance(CUR_GPS))

                        if CUR_GPS.within(STATIONS[(BUS['LOCATION'] + 1) % len(STATIONS)]): # 버스가 다음 정류장에 도착했을 때,
                            BUS['LOCATION'] = (BUS['LOCATION'] + 1) % len(STATIONS)
                            if BUS['LOCATION'] == 0: # 현재 정류장이 시작점이었을 경우
                                BUS['ONAIR'] = 2 # 버스 운행 종료
                                BUS['END_TIME'] = r['m2m:sgn']['nev']['rep']['m2m:cin']['ct']
                                sql_query = "UPDATE bus SET onair_flag=0, end_time='{}' WHERE id=1".format(BUS['END_TIME'])
                                cursor.execute(sql_query)
                                conn.commit()

                                # 슬리핑 차일드 체크 요청 전송
                                createContentInstance_('bus/rear', 'buzzer', 1)
                                if DEBUG:
                                    print("[*] Bus stopped driving :)\n")
                                    print(BUS)
                            else:
                                sql_query = "UPDATE station SET pass_flag=1 WHERE id={}".format(BUS['LOCATION'])
                                cursor.execute(sql_query)
                                conn.commit()

                                sql_query = "SELECT device_id FROM student WHERE station_id={}".format(BUS['LOCATION'] + 1)
                                cursor.execute(sql_query)
                                result = cursor.fetchall()
                                for data in result:
                                    device_id = data[0]
                                    appnotification(device_id, "Smart School Bus", "곧 도착합니다.")

                                if DEBUG:
                                    print("[*] Bus arrived at station({}) :>\n".format(BUS['LOCATION']))

                elif sensorType == 'camera_data':
                    if sensorValue == 0:
                        createContentInstance_('bus/fellow', 'camera_comm', 1)
                        if DEBUG:
                            print("[*] Camera re-shoot please :)\n")
                            print(BUS)
                            
                elif component == 'seats':
                    WEIGHT[sensorType] = sensorValue
                    sql_query = "UPDATE weight SET value={} WHERE id={}".format(sensorValue, sensorType[4:5])
                    cursor.execute(sql_query)
                    conn.commit()

                    sql_query = "SELECT SUM(value) FROM weight WHERE id<5"
                    cursor.execute(sql_query)
                    NUMOFSTU = cursor.fetchone()[0]
                    WEIGHT['NUMOFSTU'] = NUMOFSTU
                    if DEBUG:
                        print("[*] weight! {}\n".format(fullPath))
                    
                    if BUS['ONAIR'] == 2 and sensorValue == 1:
                        if DEBUG:
                            print("[*] Sleeping Child is exist!")
                        sql_query = "SELECT device_id FROM student"
                        cursor.execute(sql_query)
                        result = cursor.fetchall()
                        for data in result:
                            device_id = data[0]
                            appnotification(device_id, "Smart School Bus", "슬리핑 차일드가 존재합니다!")

                elif component == 'board':
                    if WEIGHT[sensorType] != sensorValue and sensorValue == 1: # 발판에 사람이 감지되었을 때,
                        WEIGHT['ONBOARD'] = True
                        # board_weight
                        createContentInstance_('bus/board', 'board_weight', sensorValue)
                        if DEBUG:
                            print("[*] Child is detected on board :(\n")
                    elif sensorValue == 0: # 발판에 사람이 더 이상 감지되지 않을 때,
                        WEIGHT['ONBOARD'] = False
                        createContentInstance_('bus/board', 'board_weight', sensorValue)
                        if DEBUG:
                            print("[*] Child isn't detected now :)\n")

                    WEIGHT[sensorType] = sensorValue
                    sql_query = "UPDATE weight SET value={} WHERE id=5".format(sensorValue)
                    cursor.execute(sql_query)
                    conn.commit()
                    if DEBUG:
                        print("[*] weight! {}\n".format(fullPath))
                else:
                    print(fullPath)

                # if fullPath in DATA:
                #     DATA[fullPath].append(sensorValue)

                # if DEBUG:
                #     print(DATA) 

            elif SUB:
                if not fullPath in DATA:
                    DATA[fullPath] = []
            
            else:
                print("Other")
                print(r)

            self.send_response(200)
            self.send_header('X-M2M-RSC', '2000')
            self.end_headers()

def run_http_server():
    httpd = HTTPServer(('', 5000), SimpleHTTPRequestHandler)
    print('***starting server & waiting for notifications***')
    httpd.serve_forever()

if __name__ == "__main__":
    try:
        conn = pymysql.connect(user=DB['user'], passwd=DB['password'], host=DB['host'], db=DB['database'], charset='utf8')
        cursor = conn.cursor()

        sql_query = "SELECT onair_flag, longitude, latitude, start_time, end_time FROM bus WHERE id=1"
        cursor.execute(sql_query)
        onair_flag, longitude, latitude, start_time, end_time = cursor.fetchone()
        BUS['ONAIR'] = 1 if onair_flag == 1 else 0
        BUS['LON'] = longitude
        BUS['LAT'] = latitude
        BUS['START_TIME'] = start_time
        BUS['END_TIME'] = end_time
        if BUS['ONAIR'] == 1:
            sql_query = "SELECT id FROM station WHERE pass_flag=1 ORDER BY id DESC"
            cursor.execute(sql_query)
            sid = cursor.fetchone()[0]
            BUS['LOCATION'] = sid
        
        if DEBUG:
            print(BUS)

        sql_query = "SELECT longitude, latitude FROM station"
        cursor.execute(sql_query)
        result = cursor.fetchall()

        for data in result:
            STATIONS.append([data[0], data[1]])

        print(STATIONS)
        for i in range(len(STATIONS)):
            point = Point([STATIONS[i][0], STATIONS[i][1]]) # 경도, 위도
            num_point = 10
            radius = 70
            angles = np.linspace(0, 360, num_point)
            circle = Polygon(geog.propagate(point, angles, radius))
            STATIONS[i] = circle
        
        print(len(STATIONS))
            
        
    except:
        print("[-] mysql connection error :(\n")
        sys.exit(1)

    run_http_server()
