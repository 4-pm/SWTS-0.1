import serial

s = serial.Serial(port='COM9', baudrate=9600, timeout=10)

s.write(5)
