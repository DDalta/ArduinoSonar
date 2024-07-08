import serial
import time

if __name__ == "__main__":
   
   arduino = serial.Serial("COM3", 9600, timeout=.1)

   while True:
      read = arduino.readline().decode("utf-8")

      print(read)