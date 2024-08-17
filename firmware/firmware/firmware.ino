#include <EEPROM.h>

#include <EEPROM.h>
#include <string.h>
#include <SoftwareSerial.h>

#define in1 A3        //left_input1
#define in2 9         //left_input1
#define EN 3       //enable for both pins
#define TRIG_PIN1 6   //left_trig
#define ECHO_PIN1 5  //left_echo 
//-----------------------------------------

#define in3 2         //right_input2
#define in4 4         //right_input2
#define TRIG_PIN2 10  //right_trig
#define ECHO_PIN2 A2  //right_echo
//-----------------------------------------

#define red A1       //red_RGB_led
#define blue 8       //blue_RGB_led
#define green 7      //green_RGB_led
//-----------------------------------------



//*****************************************
// Bluetooth Module Connection
//*****************************************


SoftwareSerial BluetoothSerial(0, 1); // RX, TX


//*****************************************
// Current and Voltage Sensor Pins
//*****************************************


#define CURRENT_SENSOR_PIN A4   
#define VOLTAGE_SENSOR_PIN A5   

//*****************************************
// Variable Declaration
//*****************************************
long duration1;   //duration for left sensor
long duration2;   //duration for right sensor
String Mode;      //variable to select mode
int button;       // variable to control direction manually
String speed;     // variable takes speed as string from user
int sp;           //variable controls speed level
int safe_distance; // fixed distance from wall 

float kp = 1.0;  // Proportional gain
float ki = 0.5;  // Integral gain
float kd = 0.1;  // Derivative gain

float right_previous_error = 0; //intialization of right wall ditance error
float left_previous_error = 0;   //intialization of left wall ditance error

float integral_right = 0; //intilization of right integral variable
float integral_left = 0;  //intilization of left integral variable

void setup() {
  Serial.begin(9600);  // Baud rate for Serial Monitor
  BluetoothSerial.begin(9600);  // Baud rate for Bluetooth Module

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
  // Read current and voltage values
  float current = readCurrent();
  float voltage = readVoltage();
  Serial.print("Current: ");
  Serial.println(current);
  Serial.println(" A");

  Serial.print("Voltage: ");
  Serial.print(voltage);
  Serial.println(" V");


  
  // Display current and voltage values via Bluetooth
  BluetoothSerial.print("Current: ");
  BluetoothSerial.print(current);
  BluetoothSerial.println(" A");
  
  BluetoothSerial.print("Voltage: ");
  BluetoothSerial.print(voltage);
  BluetoothSerial.println(" V");

  BluetoothSerial.println("Choose Car Speed: low, medium, high");

  while (!BluetoothSerial.available()) {
    // Wait for user input via Bluetooth
  }
  
  if (BluetoothSerial.available()) { 
    speed = BluetoothSerial.readString();
    BluetoothSerial.println(speed);
    speed.toUpperCase();
    if (speed.equals("LOW")) {
      sp = 25;
      digitalWrite(green, LOW);
      digitalWrite(blue, LOW);
      digitalWrite(red, HIGH);
      delay(1000);
    } else if (speed.equals("MEDIUM")) {
      sp = 127;
      digitalWrite(green, LOW);
      digitalWrite(red, LOW);
      digitalWrite(blue, HIGH);
      delay(1000);
    } else if (speed.equals("HIGH")) {
      sp = 255;
      digitalWrite(red, LOW);
      digitalWrite(blue, LOW);
      digitalWrite(green, HIGH);
      delay(1000);
    } 
  }
  
  BluetoothSerial.println("Choose Car Mode: manual or auto");

  while (!BluetoothSerial.available()) {
    // Wait for user input via Bluetooth
  }
  
  if (BluetoothSerial.available()) {
    Mode = BluetoothSerial.readString();
    BluetoothSerial.println(Mode);
    Mode.toUpperCase();

    if (Mode.equals("MANUAL")) {
      Manual();
    } else if (Mode.equals("AUTO")) {
      Autonomous();
    } 
  }  
}

//****************************************
// Define functions for Current and Voltage Reading
//****************************************

float readCurrent() {
  int sensorValue = analogRead(CURRENT_SENSOR_PIN);
  float voltage = (sensorValue / 1023.0) * 5.0; // Convert to voltage
  float current = (voltage - 2.5) / 0.185; // Convert voltage to current 
  return current;
}

float readVoltage() {
  int sensorValue = analogRead(VOLTAGE_SENSOR_PIN);
  float voltage = (sensorValue / 1023.0) * 5.0; // Convert to voltage
  return voltage; // Adjust with your voltage divider ratio
}

//****************************************
// define functions for motor control
//****************************************

void Forward() {
  analogWrite(EN, sp);   
  digitalWrite(in1, HIGH);   //left wheel moves forward
  digitalWrite(in2, LOW);
  digitalWrite(in3, HIGH);   // Right wheel moves forward
  digitalWrite(in4, LOW);  
  delay(1000); //1 second
}

void Backward() {
  analogWrite(EN, sp);   
  digitalWrite(in1, LOW);   //left wheel moves Backward
  digitalWrite(in2, HIGH);
  digitalWrite(in3, LOW);   // Right wheel moves Backward
  digitalWrite(in4, HIGH);  
  delay(1000);   //1 second
}

void Right() {
  analogWrite(EN, sp);   
  digitalWrite(in1, HIGH);   //left wheel moves Forward
  digitalWrite(in2, LOW);
  digitalWrite(in3, LOW);   //Right wheel moves Backward
  digitalWrite(in4, HIGH);  
  delay(1000);   //1 second
}

void Left() {
  analogWrite(EN, sp);   
  digitalWrite(in1, LOW);   //left wheel moves Backward
  digitalWrite(in2, HIGH);
  digitalWrite(in3, HIGH);   // Right wheel moves Forward
  digitalWrite(in4, LOW);  
  delay(1000);  //1 second
}

void Stop() {
  analogWrite(EN, 0);   // when sending to ENABLE 0 it stops moving 
  digitalWrite(in1, LOW);  
  digitalWrite(in2, LOW);
  digitalWrite(in3, LOW);   
  digitalWrite(in4, LOW);
  delay(500);   //0.5 second
}

void Manual() {
  while (true) {
    BluetoothSerial.println("Choose Car Position: 1: forward, 2: backward, 3: right, 4: left, 0: exit");
    
    while (!BluetoothSerial.available()) {
      // Wait for user input via Bluetooth
    }
    
    if (BluetoothSerial.available()) {
      String b;  // button as string
      b = BluetoothSerial.readString();
      button = b.toInt();
      
      switch (button) {
        case 1: // forward 
          Forward();
          break;
          
        case 2: // backward
          Backward();
          break;
          
        case 3: // right
          Right();
          break;
          
        case 4: // left           
          Left();
          break;
      }
      
      if (button == 0) {
        Stop();
        break;
      }
    }
  } 
}  

void Autonomous() {
  String d;
  BluetoothSerial.println("Enter safe distance");
  
  while (!BluetoothSerial.available()) {
    // Wait for user input via Bluetooth
  }
  
  if (BluetoothSerial.available()) {
    d = BluetoothSerial.readString();
    BluetoothSerial.println(d);
    safe_distance = d.toInt();
  }

  while (true) {
    // Measure the distance from the left ultrasonic sensor
    digitalWrite(TRIG_PIN1, LOW);
    delayMicroseconds(2);
    digitalWrite(TRIG_PIN1, HIGH);
    delayMicroseconds(10);
    digitalWrite(TRIG_PIN1, LOW);
    duration1 = pulseIn(ECHO_PIN1, HIGH);
    float distance_left = duration1 * 0.034 / 2;

    // Measure the distance from the right ultrasonic sensor
    digitalWrite(TRIG_PIN2, LOW);
    delayMicroseconds(2);
    digitalWrite(TRIG_PIN2, HIGH);
    delayMicroseconds(10);
    digitalWrite(TRIG_PIN2, LOW);
    duration2 = pulseIn(ECHO_PIN2, HIGH);
    float distance_right = duration2 * 0.034 / 2;

    // Print the distance on the right side
    BluetoothSerial.print("Distance_right: ");
    BluetoothSerial.print(distance_right);
    BluetoothSerial.println(" cm");

    // Print the distance on the left side
    BluetoothSerial.print("Distance_left: ");
    BluetoothSerial.print(distance_left);
    BluetoothSerial.println(" cm");
   if (distance_right < safe_distance || distance_left < safe_distance) {
      Stop();

      // Calculate errors
      float error_left = safe_distance - distance_left;   //error is difference between safe ditance and left distance
      float error_right = safe_distance - distance_right;

      // PID control for left wall
      integral_left += error_left;
      float derivative_left = error_left - left_previous_error;
      float correction_left = kp * error_left + ki * integral_left + kd * derivative_left;
      left_previous_error = error_left;    //update left previous error

      // PID control for right wall
      integral_right += error_right;
      float derivative_right = error_right - right_previous_error;
      float correction_right = kp * error_right + ki * integral_right + kd * derivative_right;
      right_previous_error = error_right;     //update right previous error
      float abs_correction_left = abs(correction_left); //positive value only allowed
      float abs_correction_right = abs(correction_right); //positive value only allowed

      // Adjust the car's direction based on the corrections
      if (abs_correction_left > abs_correction_right) {
        Right();
        delay(300); // Adjust this delay for tuning
        Stop();
        Forward();
        delay(300); // Ensure it aligns parallel again
        Stop();
        

      } else if (abs_correction_right > abs_correction_left) {
        Left();
        delay(300); // Adjust this delay for fine-tuning
        Stop();
        Forward();
        delay(300); // Ensure it aligns parallel again
        Stop();
      
      }
    } else {
      // If the distances are balanced, move straight forward
      Forward();
      delay(600); // Adjust this delay for the duration of the forward movement
    }

    delay(300);
  }
}




