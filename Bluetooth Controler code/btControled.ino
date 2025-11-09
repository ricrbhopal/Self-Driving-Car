#include <AFMotor.h>
#include <SoftwareSerial.h>

// Bluetooth on pins 10 (RX), 11 (TX)
SoftwareSerial BT(10, 11);

// Define motors
AF_DCMotor leftMotor(3);   // Left motor on M3
AF_DCMotor rightMotor(2);  // Right motor on M2

int motorSpeed = 200; // Speed (0–255)

void setup() 
{
  Serial.begin(9600);    // For debugging via USB
  BT.begin(38400);        // For Bluetooth HC-05/HC-04 communication

  Serial.println("✅ Bluetooth Robot Ready!");

  // Initialize motors
  leftMotor.setSpeed(motorSpeed);
  rightMotor.setSpeed(motorSpeed);

  // Stop motors initially
  leftMotor.run(RELEASE);
  rightMotor.run(RELEASE);
}

void loop() {
  // Read from Bluetooth (mobile/PC)
  if (BT.available()) 
  {
    char command = BT.read();

    // Ignore newline characters
    if (command == '\n' || command == '\r') return;
    Serial.print("BT Command: ");
    Serial.println(command);
    moveRobot(command);
  }

  // Optional: Also accept commands from Serial Monitor
  // if (Serial.available()) {
  //   char command = Serial.read();
  //   if (command == '\n' || command == '\r') return;

  //   Serial.print("Serial Command: ");
  //   Serial.println(command);
  //   moveRobot(command);
  // }
}

// Function for robot movement
void moveRobot(char cmd) 
{
  switch (cmd) 
  {
    case 'f':   // Forward
      Serial.println("🚙 Forward");
      leftMotor.run(FORWARD);
      rightMotor.run(FORWARD);
      break;

    case 'b':   // Backward
      Serial.println("⬅️ Backward");
      leftMotor.run(BACKWARD);
      rightMotor.run(BACKWARD);
      break;

    case 'l':   // Left
      Serial.println("↩️ Left");
      leftMotor.run(RELEASE);
      rightMotor.run(FORWARD);
      break;

    case 'r':   // Right
      Serial.println("↪️ Right");
      rightMotor.run(RELEASE);
      leftMotor.run(FORWARD);
      break;

    case 's':   // Stop
      Serial.println("🛑 Stop");
      leftMotor.run(RELEASE);
      rightMotor.run(RELEASE);
      break;

    default:
      Serial.println("⚠️ Invalid Command");
      leftMotor.run(RELEASE);
      rightMotor.run(RELEASE);
      break;
  }
}
