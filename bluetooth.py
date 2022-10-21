import serial

s = serial.Serial(port='COM8', baudrate=9600, timeout=1)
s.write(b'4')
s.write(b'0600')
s.close()

# 6 = 500 mc
# 4 = 600 mc