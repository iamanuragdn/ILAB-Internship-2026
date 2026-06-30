#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <WiFi.h>

LiquidCrystal_I2C lcd(0x27, 20, 4);

const char* ssid = "Bill Wi the Science Fi";
const char* password = "qzaz4468shusbs";

void setup() {
  Serial.begin(115200);
  lcd.init();
  lcd.backlight();
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Connecting WiFi...");

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("\nConnected!");
  Serial.print("IP Address: ");
  Serial.println(WiFi.localIP());

  lcd.clear();
  lcd.print("Ready. Press 1/2");
  Serial.println("Type 1 to show IP, 2 to clear display");
}

void loop() {
  if (Serial.available()) {
    char key = Serial.read();

    if (key == '1') {
      lcd.clear();
      lcd.setCursor(0, 0);
      lcd.print("Device IP:");
      lcd.setCursor(0, 1);
      lcd.print(WiFi.localIP());
      Serial.println("Showing IP on LCD");
    }
    else if (key == '2') {
      lcd.clear();
      Serial.println("Display cleared");
    }
  }
}