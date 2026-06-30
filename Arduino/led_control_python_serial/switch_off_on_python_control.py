import serial
import time

# --- SETUP ---
# Configured for your specific Arduino UNO port
arduino_port = 'COM7' 
baud_rate = 9600

try:
    print(f"Connecting to Arduino on {arduino_port}...")
    # Open the serial port
    ser = serial.Serial(arduino_port, baud_rate, timeout=1)
    
    # The Arduino resets when a serial connection opens. 
    # We must wait 2 seconds for it to wake back up before sending commands.
    time.sleep(2) 
    print("Connected successfully!")
    
except Exception as e:
    print(f"Failed to connect: {e}")
    print("Check your COM port and make sure the Arduino IDE Serial Monitor is closed.")
    exit()

# --- MAIN PROGRAM ---
print("\n--- Built-in LED Controller ---")
print("Type '1' -> Turn LED ON")
print("Type '2' -> Turn LED OFF")
print("Type 'q' -> Quit")

while True:
    user_input = input("\nEnter command (1/2/q): ")

    if user_input == '1':
        ser.write(b'1') # Sends the byte '1' to Arduino
        print("-> Light is now ON.")
        
    elif user_input == '2':
        ser.write(b'2') # Sends the byte '2' to Arduino
        print("-> Light is now OFF.")
        
    elif user_input.lower() == 'q':
        print("Closing connection...")
        break
        
    else:
        print("Invalid command. Please type 1, 2, or q.")

# Safely close the USB connection when you quit
ser.close()