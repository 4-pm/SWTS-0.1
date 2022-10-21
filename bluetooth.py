import serial

s = serial.Serial(port='COM9', baudrate=9600, timeout=1)
s.write(b'8')
#s.write(b'0475')
s.close()

# 6 = 600 mc
# 4 = 0900 mc

# !!!!!!!!!!650
