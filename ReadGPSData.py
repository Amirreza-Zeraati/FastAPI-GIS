import serial
import pynmea2

ser = serial.Serial('COM7', baudrate=9600, timeout=1)
while True:
    data = ser.readline()
    if data.startswith(b'$GPGGA'):
        msg = pynmea2.parse(data.decode('utf-8'))
        print(msg.latitude, msg.longitude)