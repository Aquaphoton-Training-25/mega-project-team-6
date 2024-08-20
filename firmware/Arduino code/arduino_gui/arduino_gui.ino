#include <EEPROM.h>
#include <string.h>
#include <SoftwareSerial.h>

#define in1 A3       // left_input1
#define in2 9        // left_input2
#define EN 3         // enable for both motors
#define TRIG_PIN1 6  // left_trig
#define ECHO_PIN1 5  // left_echo

#define in3 2        // right_input1
#define in4 4        // right_input2
#define TRIG_PIN2 10 // right_trig
#define ECHO_PIN2 A2 // right_echo

#define red A1   // red_RGB_led
#define blue 8   // blue_RGB_led
#define green 7  // green_RGB_led

#define CURRENT_SENSOR_PIN A4   
#define VOLTAGE_SENSOR_PIN A5 

long duration1;      // duration for left sensor
long duration2;      // duration for right sensor
String Mode;      // Variable to select mode
String speed; 
int sp;              // variable controls speed level
int safe_distance;   // fixed distance from wall 

float kp = 1.0;      // Proportional gain
float ki = 0.5;      // Integral gain
float kd = 0.1;      // Derivative gain

float right_previous_error = 0; // initialization of right wall distance error
float left_previous_error = 0;  // initialization of left wall distance error

float right_integral = 0;       // initialization of right integral variable
float left_integral = 0;        // initialization of left integral variable

float distance_right;           // read from right ultrasonic
float distance_left;            // read from left ultrasonic

void setup() {
  Serial.begin(9600);  // baud rate

  // Define the inputs and outputs 
  pinMode(in1, OUTPUT);
  pinMode(in2, OUTPUT);
  pinMode(in3, OUTPUT);
  pinMode(in4, OUTPUT);
  pinMode(EN, OUTPUT);
  pinMode(TRIG_PIN1, OUTPUT);
  pinMode(ECHO_PIN1, INPUT);
  pinMode(TRIG_PIN2, OUTPUT);
  pinMode(ECHO_PIN2, INPUT);
  pinMode(red, OUTPUT);
  pinMode(blue, OUTPUT);
  pinMode(green, OUTPUT);
}

void loop() {
  // Check if data is available on Serial
  if (Serial.available()) {
    String command = Serial.readStringUntil('\n');
    command.trim();

    if (command.equals("LOW")) {
      sp = 70;
      digitalWrite(green, LOW);
      digitalWrite(blue, LOW);
      digitalWrite(red, HIGH);
    } else if (command.equals("MEDIUM")) {
      sp = 150;
      digitalWrite(green, LOW);
      digitalWrite(red, LOW);
      digitalWrite(blue, HIGH);
    } else if (command.equals("HIGH")) {
      sp = 255;
      digitalWrite(red, LOW);
      digitalWrite(blue, LOW);
      digitalWrite(green, HIGH);
    } else if (command.equals("MANUAL")) {
      Mode = "MANUAL";
      Manual();
    } else if (command.equals("AUTO")) {
      Mode = "AUTO";
      Serial.println("Enter safe distance:");
    } else if (command.startsWith("S")) {
      safe_distance = command.substring(1).toInt();
    } else if (command.equals("1")) {
      Forward();
    } else if (command.equals("2")) {
      Backward();
    } else if (command.equals("3")) {
      Right();
    } else if (command.equals("4")) {
      Left();
    } else if (command.equals("0")) {
      Stop();
    }
  }

  // If in AUTO mode, handle autonomous driving
  if (Mode.equals("AUTO")) {
    Autonomous();
  }

  // Read and send current and voltage values
  float current = readCurrent();
  float voltage = readVoltage();
  Serial.print("Current: ");
  Serial.print(current);
  Serial.println(" A");
  Serial.print("Voltage: ");
  Serial.print(voltage);
  Serial.println(" V");
  delay(5000);

  
  // Read distances and send them
  if (Mode.equals("AUTO")) {
    digitalWrite(TRIG_PIN1, LOW);
    delayMicroseconds(2);
    digitalWrite(TRIG_PIN1, HIGH);
    delayMicroseconds(10);
    digitalWrite(TRIG_PIN1, LOW);
    duration1 = pulseIn(ECHO_PIN1, HIGH);
    float distance_left = duration1 * 0.034 / 2;
    
    digitalWrite(TRIG_PIN2, LOW);
    delayMicroseconds(2);
    digitalWrite(TRIG_PIN2, HIGH);
    delayMicroseconds(10);
    digitalWrite(TRIG_PIN2, LOW);
    duration2 = pulseIn(ECHO_PIN2, HIGH);
    float distance_right = duration2 * 0.034 / 2;
    
    Serial.print("Distance_left: ");
    Serial.print(distance_left);
    Serial.println(" cm");
    Serial.print("Distance_right: ");
    Serial.print(distance_right);
    Serial.println(" cm");
    delay(2000);
  }
}

void setLED(int onLED, int offLED1, int offLED2) {
  digitalWrite(onLED, HIGH);
  digitalWrite(offLED1, LOW);
  digitalWrite(offLED2, LOW);
  delay(1000); // 1 sec
}

void sendSensorValues() {
  float current = readCurrent();
  float voltage = readVoltage();
  Serial.print("Current: ");
  Serial.print(current);
  Serial.println(" A");
  Serial.print("Voltage: ");
  Serial.print(voltage);
  Serial.println(" V");
  delay(5000);
}

// Function to move the car forward
void Forward() {
  analogWrite(EN, sp);   
  digitalWrite(in1, HIGH);   // left wheel moves forward
  digitalWrite(in2, LOW);
  digitalWrite(in3, HIGH);   // right wheel moves forward
  digitalWrite(in4, LOW);  
  delay(1000); // 1 second
}

// Function to move the car backward
void Backward() {
  analogWrite(EN, sp);   
  digitalWrite(in1, LOW);    // left wheel moves backward
  digitalWrite(in2, HIGH);
  digitalWrite(in3, LOW);    // right wheel moves backward
  digitalWrite(in4, HIGH);  
  delay(1000);   // 1 second
}

// Function to turn the car right
void Right() {
  analogWrite(EN, sp);   
  digitalWrite(in1, HIGH);   // left wheel moves forward
  digitalWrite(in2, LOW);
  digitalWrite(in3, LOW);    // right wheel moves backward
  digitalWrite(in4, HIGH);  
  delay(1000);   // 1 second
}

// Function to turn the car left
void Left() {
  analogWrite(EN, sp);   
  digitalWrite(in1, LOW);    // left wheel moves backward
  digitalWrite(in2, HIGH);
  digitalWrite(in3, HIGH);   // right wheel moves forward
  digitalWrite(in4, LOW);  
  delay(1000);  // 1 second
}

// Function to stop the car
void Stop() {
  analogWrite(EN, 0);        // stops movement
  digitalWrite(in1, LOW);  
  digitalWrite(in2, LOW);
  digitalWrite(in3, LOW);   
  digitalWrite(in4, LOW);
  delay(500);   // 0.5 second
}

// PID control function
void PID() {
  // Calculate errors
  float error_left = safe_distance - distance_left;
  float error_right = safe_distance - distance_right;

  // PID control for left wall
  left_integral += error_left;
  float left_derivative = error_left - left_previous_error;
  float correction_left = kp * error_left + ki * left_integral + kd * left_derivative;
  left_previous_error = error_left;

  // PID control for right wall
  right_integral += error_right;
  float right_derivative = error_right - right_previous_error;
  float correction_right = kp * error_right + ki * right_integral + kd * right_derivative;
  right_previous_error = error_right;
  
  // Adjust movement based on PID corrections
  if (correction_left > correction_right) {
    adjustDirection(Right, Left);
  } 
  else if (correction_right > correction_left) {
    adjustDirection(Left, Right);
  }
}

void adjustDirection(void (*firstTurn)(), void (*secondTurn)()) {
  firstTurn();
  delay(300);
  Stop();
  Forward();
  delay(200); 
  Stop();
  secondTurn();
  delay(150); 
  Stop();
}

float readCurrent() {
  int sensorValue = analogRead(CURRENT_SENSOR_PIN);
  float voltage = (sensorValue / 1023.0) * 5.0;
  float current = (voltage - 2.5) / 0.185;
  return current;
}

float readVoltage() {
  int sensorValue = analogRead(VOLTAGE_SENSOR_PIN);
  float voltage = (sensorValue / 1023.0) * 5.0;
  return voltage;
}

// Function to read ultrasonic sensors
void read_ultrasonic() {
  // Measure the distance from the left ultrasonic sensor
  distance_left = measureDistance(TRIG_PIN1, ECHO_PIN1);
  // Measure the distance from the right ultrasonic sensor
  distance_right = measureDistance(TRIG_PIN2, ECHO_PIN2);

  Serial.print("Distance_right: ");
  Serial.print(distance_right);
  Serial.println(" cm");

  Serial.print("Distance_left: ");
  Serial.print(distance_left);
  Serial.println(" cm");
}

float measureDistance(int trigPin, int echoPin) {
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  long duration = pulseIn(echoPin, HIGH);
  return duration * 0.034 / 2;
}

// Function to control the car manually
void Manual() {
  while (true) {
    Serial.println("Choose Car Position: 1: forward, 2: backward, 3: right, 4: left, 0: exit");
    
    while (!Serial.available()) {
      // Wait for user input via Serial
    }
    
    if (Serial.available()) {
      char command = Serial.read();
      switch (command) {
        case '1':
          Forward();
          break;
        case '2':
          Backward();
          break;
        case '3':
          Right();
          break;
        case '4':
          Left();
          break;
        default:
          Stop();
          break;
      }
    }
  }
}

// Function for autonomous mode
void Autonomous() {
  while (true) {
    if (Serial.available()) {
      String command = Serial.readStringUntil('\n');
      command.trim();
      
      if (command.startsWith("S")) {
        safe_distance = command.substring(1).toInt();
        Serial.print("Safe distance set to: ");
        Serial.println(safe_distance);
        break;  // Exit the loop once the distance is set
      }
    }
  }

  while (true) {
    read_ultrasonic();

    if (distance_right < safe_distance || distance_left < safe_distance) {
      Stop();
      PID();
    } else {
      Forward();
      delay(600);  // Adjust this delay for the duration of the forward movement
    }

    delay(300);
  }
}


