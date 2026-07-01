"""
lcd_ip_control.py
-------------------------------------------------------------
Listens for global keypresses on the Mac:
    '1' -> tells the Arduino to display this machine's IP address
    '2' -> tells the Arduino to clear the LCD
    ESC -> quits the script

Requires:
    pip3 install pyserial pynput

macOS note:
    pynput's global key listener needs "Input Monitoring" permission.
    See the setup notes at the bottom of this file / the chat reply.
"""

import serial
import socket
import time
from pynput import keyboard

# ---- EDIT THIS to match your Arduino's serial port ----
# Find it by running in Terminal (with Arduino plugged in):
#   ls /dev/cu.*
# It will look like /dev/cu.usbmodemXXXX (genuine Uno / 16U2)
# or /dev/cu.wchusbserialXXXX (CH340 clone).
SERIAL_PORT = "/dev/cu.usbmodem11201"
BAUD_RATE = 9600
# ---------------------------------------------------------


def get_local_ip():
    """Get this Mac's LAN IP address (doesn't actually send traffic)."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip


def read_ack(ser, timeout=1.0):
    """Read one line back from Arduino and print it, if available."""
    ser.timeout = timeout
    line = ser.readline().decode(errors="ignore").strip()
    if line:
        print("Arduino:", line)


def main():
    print(f"Opening serial port {SERIAL_PORT} ...")
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=2)
    time.sleep(2.2)  # Arduino resets when serial opens; give it time to boot

    # Drain any startup message (e.g. "OK:ARDUINO_READY")
    read_ack(ser, timeout=1.0)

    ip = get_local_ip()
    print(f"Detected local IP: {ip}")
    ser.write(f"IP:{ip}\n".encode())
    read_ack(ser)

    print("\nReady. Press '1' to show the IP on the LCD, '2' to clear it, ESC to quit.\n")

    def on_press(key):
        try:
            if key.char == "1":
                ser.write(b"SHOW\n")
                read_ack(ser)
            elif key.char == "2":
                ser.write(b"CLEAR\n")
                read_ack(ser)
        except AttributeError:
            if key == keyboard.Key.esc:
                print("Exiting.")
                return False  # stops the listener

    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

    ser.close()


if __name__ == "__main__":
    main()