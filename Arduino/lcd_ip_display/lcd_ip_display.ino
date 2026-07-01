/*
  lcd_ip_display.ino
  ---------------------------------------------------
  Arduino Uno + JHD629-204A 20x4 LCD via HW-61 (PCF8574) I2C backpack.

  Wiring:
    LCD/HW-61 VCC -> Arduino 5V
    LCD/HW-61 GND -> Arduino GND
    LCD/HW-61 SDA -> Arduino A4
    LCD/HW-61 SCL -> Arduino A5

  Behavior:
    - Waits for serial commands from the Python script (9600 baud).
    - "IP:<address>\n"  -> stores the IP string (does not display yet)
    - "SHOW\n"          -> displays the stored IP on the LCD
    - "CLEAR\n"         -> clears the LCD
    - Sends back a short "OK:..." acknowledgement after each command,
      which the Python script prints for confirmation.

  Library required (install via Arduino IDE Library Manager):
    "LiquidCrystal I2C" by Frank de Brabander (or the John Rickman fork).
    Search "LiquidCrystal I2C" in Tools > Manage Libraries.
*/

#include <Wire.h>
#include <LiquidCrystal_I2C.h>

// If your LCD text looks garbled or blank, your backpack may be at
// 0x3F instead of 0x27 -- run an I2C scanner sketch to confirm.
LiquidCrystal_I2C lcd(0x27, 20, 4);

String inputBuffer = "";
String currentIP = "";

void setup() {
  Serial.begin(9600);

  lcd.init();
  lcd.backlight();
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Ready.");
  lcd.setCursor(0, 1);
  lcd.print("Waiting for IP...");

  Serial.println("OK:ARDUINO_READY");
}

void loop() {
  while (Serial.available()) {
    char c = Serial.read();
    if (c == '\n') {
      processCommand(inputBuffer);
      inputBuffer = "";
    } else if (c != '\r') {
      inputBuffer += c;
    }
  }
}

void processCommand(String cmd) {
  cmd.trim();

  if (cmd.startsWith("IP:")) {
    currentIP = cmd.substring(3);
    Serial.println("OK:IP_STORED:" + currentIP);

  } else if (cmd == "SHOW") {
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("Device IP Address:");
    lcd.setCursor(0, 1);
    if (currentIP.length() > 0) {
      lcd.print(currentIP);
    } else {
      lcd.print("No IP received");
    }
    Serial.println("OK:SHOWN");

  } else if (cmd == "CLEAR") {
    lcd.clear();
    Serial.println("OK:CLEARED");

  } else if (cmd.length() > 0) {
    Serial.println("ERR:UNKNOWN_CMD:" + cmd);
  }
}
