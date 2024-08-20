#include <EEPROM.h>
#include <string.h>
#include <SoftwareSerial.h>


#define in1 A3       //left_input1
#define in2 9        //left_input1
#define EN 3         //enable for both motors
#define TRIG_PIN1 6  //left_trig
#define ECHO_PIN1 5  //left_echo
//-----------------------------------------


#define in3 2         //right_input2
#define in4 4         //right_input2
#define TRIG_PIN2 10  //right_trig
#define ECHO_PIN2 A2  //right_echo
//-----------------------------------------

#define red A1   //red_RGB_led
#define blue 8   //blue_RGB_led
#define green 7  //green_RGB_led
//-----------------------------------------


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

float kp = 1.0;   // Proportional gain
float ki = 0.5;   // Integral gain
float kd = 0.1;   // Derivative gain

float right_previous_error = 0; //initialization of right wall distance error
float left_previous_error = 0;  //initialization of left wall distance error

float right_integral = 0;       //initialization of right integral variable
float left_integral = 0;        //initialization of left integral variable

float distance_right;           //read from right ultrasonic
float distance_left;            //read from left ultrasonic

void setup() {
  Serial.begin(9600);  //baud rate

  //define the inputs and outputs 
  pinMode(in1, OUTPUT);
  pinMode(in2, OUTPUT);
  pinMode(in3, OUTPUT);
  pinMode(in4, OUTPUT);
  pinMode(EN, OUTPUT);
  pinMode(TRIG_PIN1, OUTPUT);
  pinMode(ECHO_PIN1, INPUT);
  pinMode(TRIG_PIN2, OUTPUT);
  pinMode(ECHO_PIN2, INPUT);
}

void loop() {
  Serial.println("Choose Car Speed: low, medium, high");

  while (!Serial.available()) {
    // Wait for user input
  }
  if (Serial.available()) { 
    speed = Serial.readStringUntil('\n');
    speed.trim(); // Remove any whitespace
    Serial.println(speed);
    speed.toUpperCase();

    if (speed.equals("LOW")) {
      sp = 65;
      digitalWrite(green, LOW);
      digitalWrite(blue, LOW);
      digitalWrite(red, HIGH);
      delay(1000); // 1 sec
    } 
    else if (speed.equals("MEDIUM")) {
      sp = 130;
      digitalWrite(green, LOW);
      digitalWrite(red, LOW);
      digitalWrite(blue, HIGH);
      delay(1000);
    } 
    else if (speed.equals("HIGH")) {
      sp = 255;
      digitalWrite(red, LOW);
      digitalWrite(blue, LOW);
      digitalWrite(green, HIGH);
      delay(1000);
    } 
    
  }

  Serial.println("Choose Car Mode: manual or auto");
  while (!Serial.available()) {
    // Wait for user input
  }
  if (Serial.available()) {
    Mode = Serial.readStringUntil('\n'); // read until newline
    Mode.trim(); // Remove any whitespace
    Serial.println(Mode);
    Mode.toUpperCase();

    if (Mode.equals("MANUAL")) {
      Manual();    
    } else if (Mode.equals("AUTO")) {
      Autonomous();   
    } 
  }  
}

//****************************************
// Function Definitions
//****************************************

// Function to make the car move forward
void Forward() {
  analogWrite(EN, sp);   
  digitalWrite(in1, HIGH);   //left wheel moves forward
  digitalWrite(in2, LOW);
  digitalWrite(in3, HIGH);   // Right wheel moves forward
  digitalWrite(in4, LOW);  
  delay(1000); //1 second
}

// Function to make the car move backward
void Backward() {
  analogWrite(EN, sp);   
  digitalWrite(in1, LOW);   //left wheel moves backward
  digitalWrite(in2, HIGH);
  digitalWrite(in3, LOW);   // Right wheel moves backward
  digitalWrite(in4, HIGH);  
  delay(1000);   //1 second
}

// Function to make the car turn right
void Right() {
  analogWrite(EN, sp);   
  digitalWrite(in1, HIGH);   //left wheel moves forward
  digitalWrite(in2, LOW);
  digitalWrite(in3, LOW);   //Right wheel moves backward
  digitalWrite(in4, HIGH);  
  delay(1000);   //1 second
}

// Function to make the car turn left
void Left() {
  analogWrite(EN, sp);   
  digitalWrite(in1, LOW);   //left wheel moves backward
  digitalWrite(in2, HIGH);
  digitalWrite(in3, HIGH);   // Right wheel moves forward
  digitalWrite(in4, LOW);  
  delay(1000);  //1 second
}

// Function to stop the car
void Stop() {
  analogWrite(EN, 0);   // when sending to ENABLE 0 it stops moving 
  digitalWrite(in1, LOW);  
  digitalWrite(in2, LOW);
  digitalWrite(in3, LOW);   
  digitalWrite(in4, LOW);
  delay(500);   //0.5 second
}

// PID control function
void PID() {
  // Calculate errors
  float error_left = safe_distance - distance_left;   //error is difference between safe distance and left distance
  float error_right = safe_distance - distance_right;

  // PID control for left wall
  left_integral += error_left;     //accumalte errors
  float left_derivative = error_left - left_previous_error; //predict future
  float correction_left = kp * error_left + ki * left_integral + kd * left_derivative;
  left_previous_error = error_left;    //update left previous error

  // PID control for right wall
  right_integral += error_right;
  float right_derivative = error_right - right_previous_error;
  float correction_right = kp * error_right + ki * right_integral + kd * right_derivative;
  right_previous_error = error_right;     //update right previous error
  

  if (correction_left > correction_right) {
    // Turn right to correct left side distance
    Right();
    delay(300); // Adjust this delay for tuning
    Stop();
    Forward(); // Move forward to create some space
    delay(200); 
    Stop();
    Left(); // Compensate with a left turn
    delay(150); 
    Stop();
  } else if (correction_right > correction_left) {
    // Turn left to correct right side distance
    Left();
    delay(300); // Adjust this delay for fine-tuning
    Stop();
    Forward(); // Move forward to create some space
    delay(200); 
    Stop();
    Right();  // Compensate with a right turn
    delay(150); 
    Stop();
  }
}

// Function to read ultrasonic sensors
void read_ultrasonic() {
  // Measure the distance from the left ultrasonic sensor
  digitalWrite(TRIG_PIN1, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN1, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN1, LOW);
  duration1 = pulseIn(ECHO_PIN1, HIGH);
  distance_left = duration1 * 0.034 / 2;

  // Measure the distance from the right ultrasonic sensor
  digitalWrite(TRIG_PIN2, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN2, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN2, LOW);
  duration2 = pulseIn(ECHO_PIN2, HIGH);
  distance_right = duration2 * 0.034 / 2;

  Serial.print("Distance_right: ");
  Serial.print(distance_right);
  Serial.println(" cm");

  Serial.print("Distance_left: ");
  Serial.print(distance_left);
  Serial.println(" cm");
}

// Function to control car manually
void Manual() {
  while (true) {
    Serial.println("Choose Car Position: 1:forward, 2:backward, 3:right, 4:left, 0:exit");
    while (!Serial.available()) {
      // Wait for user input
    }
    if (Serial.available()) {
      String b;        // button as string
      b = Serial.readStringUntil('\n');
      b.trim(); 
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

// Function for autonomous mode
void Autonomous() {
  String d;
  Serial.println("Enter safe distance");
  while (!Serial.available()) {
    // Wait for user input
  }
  if (Serial.available()) {
    d = Serial.readStringUntil('\n');
    d.trim(); 
    Serial.println(d);
    safe_distance = d.toInt();
  }

  while (true) {
    read_ultrasonic();
    
    if (distance_right < safe_distance || distance_left < safe_distance) {
      Stop();
      PID();
    }
    else {
      // If the distances are balanced, move straight forward
      Forward();
      delay(600); // Adjust this delay for the duration of the forward movement
    }

    delay(300);
  }
}

