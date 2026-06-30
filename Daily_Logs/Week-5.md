# Internship Weekly Log: Week 5

**Developer:** Abhilash Ghosh and Anurag Debnath\
**Date:** June 30, 2026  

---

## Day 1: June 30, 2026

### Part 1: Hardware-Software Interfacing — Arduino LED Control via Python Serial  
**Hardware:** Arduino Uno, USB A-to-B Cable  
**Environment:** Windows PC, Arduino IDE 2.3.10, VS Code, Python 3.12

#### ✅ What I Did
1. **Hardware Connection:** Connected the Arduino Uno to the PC via USB and identified the correct communication port (COM7).
2. **Microcontroller Setup:** Wrote and uploaded C++ code to the Arduino to initialize a 9600 baud serial connection and set the built-in LED (Pin 13) as an output.
3. **Environment Configuration:** Resolved a Python environment mismatch in VS Code by forcing the installation of the `pyserial` library directly into the specific Python 3.12 executable path used by the debugger.
4. **Code Development:** Wrote a Python script to establish a serial connection with the Arduino over COM7. 
5. **Command Integration:** Implemented a continuous `while True` loop in Python to capture keyboard input and transmit corresponding byte commands (`b'1'` for ON, `b'2'` for OFF) to the Arduino.
6. **Deployment:** Successfully achieved real-time hardware actuation (toggling the built-in LED) directly from the Python terminal interface.

#### 📸 Visual Evidence
<table>
  <tr>
    <td align="center"><b>1. Port Configuration</b></td>
    <td align="center"><b>2. Python Terminal Output</b></td>
  </tr>
  <tr>
    <td align="center"> <img src="./assets/week5_arduino_com7.png" width="500" alt="Arduino IDE showing board connected to COM7"></td>
    <td align="center"><img src="./assets/week5_python_terminal.png" width="500" alt="VS Code terminal showing successful connection and command execution"></td>
  </tr>
</table>

#### 📊 Results
| Metric | Value |
|--------|-------|
| **Target Hardware** | Arduino Uno (Built-in LED, Pin 13) |
| **Communication Protocol** | USB Serial |
| **Baud Rate** | 9600 bps |
| **Port Assignment** | COM7 |
| **Operation Status** | Successful real-time control via keyboard inputs |

#### 🧠 Key Learnings
- **Serial Port Exclusivity:** A single COM port can only be accessed by one application at a time. The Arduino IDE's Serial Monitor must be fully closed before a Python script can successfully connect to the microcontroller.
- **Hardware Reset Timing:** Opening a serial connection from Python automatically triggers a reset on the Arduino Uno. It is necessary to implement a delay (`time.sleep(2)`) in the Python script immediately after opening the port to allow the board to wake up before sending data.
- **Data Encoding:** Serial ports process raw bytes, not standard high-level strings. Commands sent via Python must be encoded as bytes (e.g., `b'1'`) for the Arduino to correctly read and process the incoming serial data.
- **Environment Management:** When working with VS Code debuggers, standard `pip install` commands might apply to a different global environment. Packages must be installed explicitly into the specific interpreter path executing the script.

#### ❌ Issues Faced & Solutions
| Issue | Cause | Solution |
|-------|-------|----------|
| `ModuleNotFoundError: No module named 'serial'` | The VS Code debugger was using a specific Python 3.12 executable that lacked the `pyserial` package. | Forced installation to the exact executable path: `& "...\python.exe" -m pip install pyserial` |
| `FileNotFoundError` for `COM3` | The Python script hardcoded `COM3`, but Windows assigned the Arduino to `COM7`. | Identified the correct port via Arduino IDE and updated the Python script variable to `arduino_port = 'COM7'` |

#### 📁 Files Created / Modified
- [serial_led_control.ino](../Arduino/led_control_python_serial/serial_led_control.ino) —  Arduino C++ script for initializing serial communication and listening for byte commands to toggle Pin 13.
- [switch_off_on_python_control.py](../Arduino/led_control_python_serial/switch_off_on_python_control.py) — Python controller script utilizing `pyserial` for user input routing and hardware communication.