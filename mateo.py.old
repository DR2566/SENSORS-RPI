import time
from bme280 import BME280
from smbus import SMBus

bus = SMBus(1)
bme280 = BME280(i2c_dev=bus)


while True:
    temperature = bme280.get_temperature()
    pressure = bme280.get_pressure()
    format_temp = "{:.2f}".format(temperature)
    print('Temperature = ' + format_temp + ' C ')
    format_press = "{:.2f}".format(pressure)
    print('Pressure = ' + format_press + ' hPa \n')
    format_time = time.strftime("%d.%b.%Y-%H:%M:%S", time.localtime()) 
    log_file = open("/home/raspberry/LetkaGML-Mateo/rpi-firmware/web/data/data.txt", "at")
    actual = open("/home/raspberry/LetkaGML-Mateo/rpi-firmware/web/data/actual.txt", "wt")
    log_file.write(format_time + ';' + format_temp + ';' + format_press + "\n")
    actual.write(format_time + "\n")
    actual.write(format_temp + "\n")
    actual.write(format_press + "\n")
    log_file.close()
    actual.close()
    # time.sleep() for testing
    time.sleep(300)

