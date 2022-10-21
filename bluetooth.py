import serial

s = serial.Serial(port='COM8', baudrate=9600, timeout=1)
s.write(b'8')
s.close()