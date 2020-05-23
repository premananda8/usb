import serial

ser = serial.Serial()
ser.baudrate = 19200
ser.port = "COM1"#
ser.open()
