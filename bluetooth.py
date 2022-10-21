import serial

s = serial.Serial(port='COM8', baudrate=9600, timeout=1)
s.write(b'6')
s.write(b'0650')
s.write(b'4')
s.write(b'0650')
s.close()

# 6 = 600 mc
# 4 = 0900 mc

# !!!!!!!!!!650