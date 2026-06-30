// Pin 13 is connected to the built-in "L" LED on the Arduino Uno
const int ledPin = 13; 

void setup() {
  // Start the serial connection so the Arduino can talk to Python
  Serial.begin(9600);
  
  // Set the built-in LED pin as an output
  pinMode(ledPin, OUTPUT);
  
  // Ensure the LED is off when the board starts
  digitalWrite(ledPin, LOW); 
}

void loop() {
  // Check if Python has sent any data
  if (Serial.available() > 0) {
    
    // Read the number sent from Python
    char incomingByte = Serial.read();
    
    // If Python sends '1', turn the built-in LED ON
    if (incomingByte == '1') {
      digitalWrite(ledPin, HIGH);
    } 
    // If Python sends '2', turn the built-in LED OFF
    else if (incomingByte == '2') {
      digitalWrite(ledPin, LOW);
    }
  }
}