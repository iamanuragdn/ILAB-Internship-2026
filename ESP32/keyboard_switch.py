import serial
import time

# Change this to your ESP32's COM port (Windows: COMx, Mac/Linux: /dev/ttyUSB0 or /dev/cu.usbserial-xxxx)
PORT = "COM5"
BAUD = 115200

ser = serial.Serial(PORT, BAUD, timeout=1)
time.sleep(2)  # wait for ESP32 to reset after serial connect

print("Connected to ESP32 on", PORT)
print("Press 1 to show IP, 2 to clear display, q to quit")

while True:
    key = input("Enter command (1/2/q): ").strip()

    if key == "1":
        ser.write(b'1')
        print("Sent: show IP")
    elif key == "2":
        ser.write(b'2')
        print("Sent: clear display")
    elif key == "q":
        break
    else:
        print("Invalid input, use 1, 2, or q")

    time.sleep(0.1)
    # print any response from ESP32
    while ser.in_waiting:
        print("ESP32:", ser.readline().decode(errors='ignore').strip())

ser.close()