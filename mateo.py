import time, datetime
from bme280 import BME280
from smbus import SMBus
import requests
import board
import busio
import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

good_time = True

class API:
    def __init__(self, url):
        self.url = url

    def get_url(self, name):
        url_sensor = self.url + name + '/post'
        return url_sensor

    def get_json(self, value):
        json = {'value' : str(value)}
        return json

    def upload_data(self, name, value):
        my_obj = self.get_json(value)
        url_sensor = self.get_url(name)
        #print(my_obj, url_sensor)
        print(url_sensor, my_obj)
        post_response = requests.post(url_sensor, json = my_obj)
        print(post_response.text)

class METEO:
    def __init__(self):
        self.bus = SMBus(1)
        self.i2c = busio.I2C(board.SCL, board.SDA)   # Create the I2C bus for UV
        self.bme = BME280(i2c_dev=self.bus)
        self.ads = ADS.ADS1015(self.i2c)             # variable to access ads1115
        self.ads_val = AnalogIn(self.ads, ADS.P0)    # variable for output channel of uv sensor
        self.ads_ref = AnalogIn(self.ads, ADS.P1)    # variable for reference channel of UV sensor
        self.iter_num = 5
        self.current_temp = None
        self.current_press = None
        self.current_humid = None
        self.current_uv = None
        # Constants for UV sensor:
        self.UV_IN_MIN = 0.96
        self.UV_IN_MAX = 2.8
        self.UV_OUT_MIN = 0.0
        self.UV_OUT_MAX = 15.0



    def get_temp(self):
        temps_list = []
        for i in range(self.iter_num):
            temp = self.bme.get_temperature()
            if i != 0:
                temps_list.append(temp)
            time.sleep(1)
        self.current_temp = round(get_avg(temps_list),2)
        
    def get_press(self):
        press_list = []
        for i in range(self.iter_num):
            press = self.bme.get_pressure()
            if i != 0:
                press_list.append(press)
            time.sleep(1)
        self.current_press = round(get_avg(press_list),2)

    def get_humid(self):
        humid_list = []
        for i in range(self.iter_num):
            humid = self.bme.get_humidity()
            if i != 0:
                humid_list.append(humid)
            time.sleep(1)
        self.current_humid = round(get_avg(humid_list),2)
    
    def get_uv(self):
        uv_list = []
        for i in range(self.iter_num):
            uv = self.v2mw()
            if i !=0:
                uv_list.append(uv)
            time.sleep(1)
        self.current_uv = round(get_avg(uv_list),2)
        #print(self.current_uv)
    
    def v2mw(self): 
        # get intensity from output voltage
        #print(self.ads_val)
        #print(self.ads_ref)
        return (self.ads_val.voltage*3.3/self.ads_ref.voltage - self.UV_IN_MIN) * (self.UV_OUT_MAX - self.UV_OUT_MIN) / (self.UV_IN_MAX - self.UV_IN_MIN) + self.UV_OUT_MIN

    def write_data(self):
        file_data = open('/home/raspberry/LetkaGML-Mateo/rpi-firmware/web/graph/datas.txt', "a")
        actual = open("/home/raspberry/LetkaGML-Mateo/rpi-firmware/web/data/actual.txt", "wt")
        time = get_right_time(str(datetime.datetime.now()))
        #print(time)
        file_data.write(time+';'+str(self.current_temp)+';'+str(self.current_press)+';'+str(self.current_humid)+';'+str(self.current_uv)+'\n')
        file_data.close()
        actual.write(time+'\n')
        actual.write(str(self.current_temp)+'\n')
        actual.write(str(self.current_press)+'\n')
        actual.write(str(self.current_humid)+'\n')
        actual.write(str(self.current_uv)+'\n')
        actual.close()
        restAPI.upload_data('humidity', self.current_humid)
        restAPI.upload_data('temperature', self.current_temp)
        restAPI.upload_data('pressure', self.current_press)
        restAPI.upload_data('uv', self.current_uv)

def get_avg(list_num):
    return sum(list_num) / len(list_num)
def convert_float(float_num): # we want to change "." separator substitude to "," for excel
    int_str = str(float_num)
    new_int = ""
    for letter in int_str:
        if letter == ".":
            new_int += ","
        else:
            new_int += letter
    return new_int
def get_right_time(time_bad): # the input is the bad setted time on the system, this function it converts to a right current time
    date_code = ''
    for letter in time_bad:
        try:
            integer = int(letter)
            date_code += letter
        except:
            pass
    day = date_code[6:8]
    month = date_code[4:6]
    year = date_code[0:4]
    hour = date_code[8:10]
    minute = date_code[10:12]
    second = date_code[12:14]
    if good_time == 0:
        time_bad = datetime.datetime(int(year),int(month),int(day),int(hour),int(minute),int(second))
        time_shift = datetime.timedelta(hours=0,minutes=0,seconds=0)
        right_time = str(time_bad + time_shift)
    else:
        right_time = day+'.'+month+'.'+year+';'+hour+':'+minute+':'+second
    #print(day,month,year,hour,minute,second)
    return right_time

restAPI = API('http://172.20.1.18:3333/')
meteo = METEO()

meteo.get_uv()
meteo.get_temp()
meteo.get_press()
meteo.get_humid()

meteo.write_data()


