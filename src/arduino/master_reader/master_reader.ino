// Reader used to test the prototype I2C Keypad device

// Adapted from Wire Master Reader
// by Nicholas Zambetti <http://www.zambetti.com>

// This example code is in the public domain.


#include <Wire.h>

void setup() {
  Wire.begin();        // join i2c bus
  Serial.begin(9600);  // start serial for output
}

void loop() {
  Wire.requestFrom(8, 1);    // request 6 bytes from slave device #8

  while (Wire.available()) {
    char c = Wire.read(); // receive a byte as character
    if (c) {
    Serial.print(c);         // print the character
    }
  }

  delay(100); // check every 0.1 seconds
}
