import requests
import json
import configparser
import threading
import uuid
import random
import time

# Parameters
config = configparser.ConfigParser()
with open('default.json', 'r') as f:
    config = json.load(f)

# CSE Params
csePoA = "http://" + config["cse"]["ip"] + ":" + str(config["cse"]["port"])                              #모비우스 url
cseName = config["cse"]["name"]                                                                          #Mobius
cseRelease = config["cse"]["release"]                                                                    #3                           

# AE Params
aePoA = "http://" + config["monitor"]["ip"] + ":" + str(config["monitor"]["port"])                       #파이썬 서버 url       
requestNr = random.randint(0,10000)

def createAE(name):
    global requestNr, cseRelease
    print("\n[Create AE REQUEST]") 
    url = csePoA + '/' + cseName
    representation = {
        'm2m:ae': {
            'rn': name,
            'api': 'app.company.com',
            'rr': False,
            'srv': ['2a']
        }
    }
    headers = {
        'Content-Type': 'application/vnd.onem2m-res+json;ty=2',
        'X-M2M-RI': 'req' + str(requestNr),
        'X-M2M-RVI': cseRelease,
        'X-M2M-Origin': "Cae-" + name
    }

    print(representation)
    res = requests.post(url,
        json = representation,
        headers = headers
    )

    requestNr += 1
    print("\n[RESPONSE]")
    if res.status_code == 409:
        # print("AE Creation error : ", res.text)
        res = json.loads(res.text)['m2m:dbg']
        if res == 'resource is already exist':
            print("AE is already presents!")
        #    resetAE(name, rr)
    elif res.status_code == 201:
        print("AE Creation : ", res.status_code)
    else:
        print("AE Creation Error!")
        print(res.text)

def resetAE(name, rr):
    global requestNr, cseRelease

    print("\n[Reset AE REQUEST]")
    url = csePoA + '/' + cseName + '/' + name
    hdrs = {
        'X-M2M-RVI': cseRelease,
        'X-M2M-RI': 'req' + str(requestNr),
        'X-M2M-Origin': "Cae-" + name,
        }
    print(hdrs)

    r = requests.delete(url, headers=hdrs)
    print("\n[RESPONSE]")
    print("{} : {}".format(r.status_code, r.text))
    if r.status_code == 200:
        createAE(name, rr)
    else:
        print("AE deletion error!")

def createContainer(path, name):
    global requestNr, cseRelease

    print("\n[Create Container REQUEST]")

    url = csePoA + '/' + cseName + '/' + path
    headers = {
        'Content-Type': 'application/json;ty=3',
        'X-M2M-RI': 'req' + str(requestNr),
        'X-M2M-RVI': cseRelease,
        'X-M2M-Origin': "Cae-" + name
    }
    representation = {
        'm2m:cnt': {
            'rn': name,
            'mni': 10
        }
    }
    res = requests.post(url,
        json = representation,
        headers = headers
    )

    requestNr += 1
    print("\n[RESPONSE]")
    print(res.text)
    print(res.status_code)

def createDataContainer(path, name):
    global requestNr, cseRelease

    print("\n[Create Container REQUEST]")

    url = csePoA + '/' + cseName + '/' + path + '/' + name
    headers = {
        'Content-Type': 'application/json;ty=3',
        'X-M2M-RI': 'req' + str(requestNr),
        'X-M2M-RVI': cseRelease,
        'X-M2M-Origin': "Cae-" + name
    }
    representation = {
        'm2m:cnt': {
            'rn': "DATA",
            'mni': 10
        }
    }
    res = requests.post(url,
        json = representation,
        headers = headers
    )

    requestNr += 1
    print("\n[RESPONSE]")
    print(res.text)
    print(res.status_code)

def createSubscription(path, name):
    global requestNr, cseRelease
    print("\n[Create Subscription REQUEST]")
    url = csePoA + '/' + cseName + '/' + path + '/' + name
    print(url)

    representation = {
        'm2m:sub': {
            'rn': 'sub',
            'nu': [aePoA + '/'],
            "nct": 1,
            "enc": {
                "net": [3]
            }
        }
    }
    headers = {
        'Content-Type': 'application/json;ty=23',
        'X-M2M-Origin': 'Cae-' + name,
        'X-M2M-RI': 'req' + str(requestNr),
        'X-M2M-RVI': cseRelease
    }
    print(representation)
    print(headers)

    res = requests.post(url,
        json = representation,
        headers = headers
    )

    requestNr += 1
    print("\n[RESPONSE]")
    if res.status_code != 201:
        print("{} : {}".format(res.status_code, res.text))
        res = json.loads(res.text)['m2m:dbg']
    else:
        print("Sub Creation : ", res.status_code)

def createContentInstance(path, name, content):
    global requestNr, cseRelease
    print("\n[Create ContentInstance REQUEST]")
    url = csePoA + '/' + cseName + '/' + path + '/' + name
    print(url)

    representation = {
        'm2m:cin': {
            'cnf': 'application/text:0',
            'con': content
        }
    }
    headers = {
        'Content-Type': 'application/json;ty=4',
        'X-M2M-Origin': 'Cae-' + name,
        'X-M2M-RI': 'req' + str(requestNr),
        'X-M2M-RVI': cseRelease
    }
    print(representation)
    print(headers)

    while True:
        try:
            res = requests.post(url,
                json = representation,
                headers = headers,
                timeout=3
            )
        except requests.exceptions.ReadTimeout:
            print("[*] createContentInstance: timeout!")
        else:
            break

    requestNr += 1
    print("\n[RESPONSE]")
    if res.status_code != 201:
        print("{} : {}".format(res.status_code, res.text))
        res = json.loads(res.text)['m2m:dbg']
    else:
        print("Cin Creation : ", res.status_code)


def createSensorType(ae, sensorType):
    createContainer(ae, sensorType)

def createConSub(ae, sensorType, sensorName):
    createContainer(ae+'/'+sensorType, sensorName)
    createSubscription(ae+'/'+sensorType, sensorName)

def createContentInstance_(path, name, content):
    createContentInstance(path, name, content)
    createContentInstance(path, name, content)

if __name__ == "__main__":
    # createAE('bus')
    # createContainer('bus', 'driver')
    # createContainer('bus/driver', 'driver_led')
    # createConSub('bus', 'driver', 'gps_lon')
    # createConSub('bus', 'driver', 'gps_lat')

    # createContainer('bus', 'fellow')
    # createContainer('bus/fellow', 'fellow_led')
    # createConSub('bus', 'fellow', 'camera_data')
    # createConSub('bus', 'fellow', 'camera_comm')

    # createContainer('bus', 'app')
    
    # createContainer('bus', 'rear') 
    # createConSub('bus', 'rear', 'button')
    # createConSub('bus', 'rear', 'buzzer') # 실제 서비스에서는 sub일 필요가 없음. 디버깅용

    # createContainer('bus', 'seats')
    # createContainer('bus/seats', 'seat1_weight')
    # createContainer('bus/seats', 'seat2_weight')
    # createContainer('bus/seats', 'seat3_weight')
    # createContainer('bus/seats', 'seat4_weight')
    # createConSub('bus', 'seats', 'seat1_weight')
    # createConSub('bus', 'seats', 'seat2_weight')
    # createConSub('bus', 'seats', 'seat3_weight')
    # createConSub('bus', 'seats', 'seat4_weight')

    # createContainer('bus', 'board')
    # createConSub('bus', 'board', 'weight')

    # # 영실관
    # createContentInstance_('bus/driver', 'gps_lon', 127.07333331532686)
    # createContentInstance_('bus/driver', 'gps_lat', 37.552369388104445)

    # # 후문
    # time.sleep(2)
    # createContentInstance_('bus/driver', 'gps_lon', 127.0725)
    # createContentInstance_('bus/driver', 'gps_lat', 37.5529)

    # # 후문
    # time.sleep(2)
    # createContentInstance_('bus/driver', 'gps_lon', 127.0725)
    # createContentInstance_('bus/driver', 'gps_lat', 37.5529)

    # # 학술정보원 앞
    # time.sleep(2)
    # createContentInstance_('bus/driver', 'gps_lon', 127.07303331532686)
    # createContentInstance_('bus/driver', 'gps_lat', 37.5535)

    # # 대양AI센터
    # time.sleep(2)
    # createContentInstance_('bus/driver', 'gps_lon', 127.0758)
    # createContentInstance_('bus/driver', 'gps_lat', 37.5510)

    # 세종대학교 정문
    time.sleep(2)
    createContentInstance_('bus/driver', 'gps_lon', 127.0751)
    createContentInstance_('bus/driver', 'gps_lat', 37.5491)

    # # 광개토관 앞
    # time.sleep(2)
    # createContentInstance_('bus/driver', 'gps_lon', 127.0735)
    # createContentInstance_('bus/driver', 'gps_lat', 37.5503)

    # # 영실관
    # createContentInstance_('bus/driver', 'gps_lon', 127.07333331532686)
    # createContentInstance_('bus/driver', 'gps_lat', 37.552369388104445)


    # while True:
    #     createContentInstance('bus/weight', 'seat1', random.randint(  0, 60))
    #     createContentInstance('bus/weight', 'seat2', random.randint(0, 60))
    #     createContentInstance('bus/weight', 'seat3', random.randint(0, 60))
    #     createContentInstance('bus/weight', 'seat4', random.randint(0, 60))
    #     createContentInstance('bus/weight', 'board', random.randint(0, 60))
    #     time.sleep(1)
    
