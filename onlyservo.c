#include <ESP32Servo.h>

Servo myservo;

void setup() {
  myservo.attach(19);
  myservo.write(0);  // Set the initial position to 0 degrees (lid closed)
  delay(1000);       // Wait for the lid to close completely (adjust delay if needed)
}

void loop() {
  // Open the lid (move servo to 90 degrees)
  myservo.write(90);
  delay(1000);  // Adjust delay to control how long the lid stays open

  // Close the lid (move servo back to 0 degrees)
  myservo.write(0);
  delay(1000);  // Adjust delay to control how long the lid stays closed
}
