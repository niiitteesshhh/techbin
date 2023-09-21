#include <Arduino.h>
#include <ESP32Servo.h>

Servo myservo;
int servoPin = 19;  
int trigPin = 2;    // Ultrasonic sensor trigger pin
int echoPin = 4;    // Ultrasonic sensor echo pin

void setup() {
  myservo.attach(servoPin);
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  Serial.begin(115200);
}

void loop() {
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  unsigned long duration = pulseIn(echoPin, HIGH);
  float distance_cm = (duration / 2.0) * 0.0343;

  Serial.print("Distance: ");
  Serial.print(distance_cm);
  Serial.println(" cm");

  if (distance_cm < 7.0) {
    // Open the lid (move servo to 90 degrees)
    myservo.write(160);
    delay(1000);  // Adjust delay to control how long the lid stays open
  } else {
    // Close the lid (move servo back to 0 degrees)
    myservo.write(0);
    delay(1000);  // Adjust delay to control how long the lid stays closed
  }
}
