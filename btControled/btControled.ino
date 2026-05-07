#include <AFMotor.h>
#include <SoftwareSerial.h>

// Bluetooth HC-05
SoftwareSerial BT(10, 11);  // RX, TX

// Motors (M3 = left, M2 = right)
AF_DCMotor leftMotor(3);
AF_DCMotor rightMotor(2);

// Speed (increase for torque)
int baseSpeed = 160;
int turnSpeed = 80;

void setup() 
{
  Serial.begin(9600);
  BT.begin(38400);

  Serial.println("System Ready");

  // Ensure motors are stopped initially
  leftMotor.setSpeed(0);
  rightMotor.setSpeed(0);
  leftMotor.run(RELEASE);
  rightMotor.run(RELEASE);
}

void loop() 
{
  // Check Bluetooth
  if (BT.available()) 
  {
    char cmd = BT.read();

    // Ignore garbage
    if (cmd == '\n' || cmd == '\r') return;

    Serial.print("Received: ");
    Serial.println(cmd);

    moveRobot(cmd);
  }
}

// ---------------- MOTOR CONTROL ---------------- //
void moveRobot(char cmd) 
{
  switch (cmd) 
  {
    case 'f':   // Forward
      Serial.println("Forward");

      leftMotor.setSpeed(baseSpeed);
      rightMotor.setSpeed(baseSpeed);

      leftMotor.run(FORWARD);
      rightMotor.run(FORWARD);
      break;

    case 'b':   // Backward
      Serial.println("Backward");

      leftMotor.setSpeed(baseSpeed);
      rightMotor.setSpeed(baseSpeed);

      leftMotor.run(BACKWARD);
      rightMotor.run(BACKWARD);
      break;

    case 'l':   // STRONG LEFT TURN
      Serial.println("Left");

      leftMotor.setSpeed(turnSpeed);
      rightMotor.setSpeed(baseSpeed);

      leftMotor.run(BACKWARD);   // reverse left
      rightMotor.run(FORWARD);   // forward right
      break;

    case 'r':   // STRONG RIGHT TURN
      Serial.println("Right");

      leftMotor.setSpeed(baseSpeed);
      rightMotor.setSpeed(turnSpeed);

      leftMotor.run(FORWARD);
      rightMotor.run(BACKWARD);  // reverse right
      break;

    case 's':   // Stop
      Serial.println("Stop");

      leftMotor.setSpeed(0);
      rightMotor.setSpeed(0);

      leftMotor.run(RELEASE);
      rightMotor.run(RELEASE);
      break;

    default:
      Serial.println("Invalid Command");

      leftMotor.run(RELEASE);
      rightMotor.run(RELEASE);
      break;
  }
}