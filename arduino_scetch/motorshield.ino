#include <Servo.h>
#include <SoftwareSerial.h>

SoftwareSerial mySerial(2, 3);

int mL_plus = 13;
int mLb_plus = 11;
int mLb_minus = 10;

int mR_plus = 12;
int mRb_plus = 9;
int mRb_minus = 8;

int pisk = 6;

int pos1 = 0;

int x_pisk = 0;

Servo myservo;

void setup() {
  pinMode(2, INPUT);
  pinMode(3, OUTPUT);
  
  pinMode(pisk, OUTPUT);
  
  Serial.begin(9600);
  mySerial.begin(38400);
  Serial.println("Hello world!");
  
  pinMode(mL_plus, OUTPUT);
  pinMode(mLb_plus, OUTPUT);
  pinMode(mLb_minus, OUTPUT);
  
  pinMode(mR_plus, OUTPUT);
  pinMode(mRb_plus, OUTPUT);
  pinMode(mRb_minus, OUTPUT);

  myservo.attach(5);
}

void vpered(int timer) {
  digitalWrite(mL_plus, HIGH);
  digitalWrite(mLb_plus, HIGH);
  digitalWrite(mR_plus, HIGH);
  digitalWrite(mRb_plus, HIGH);
  
  delay(timer);
  
  digitalWrite(mL_plus, LOW);
  digitalWrite(mLb_plus, LOW);
  digitalWrite(mR_plus, LOW);
  digitalWrite(mRb_plus, LOW);
}

void back(int timer) {
  digitalWrite(mLb_minus, HIGH);
  digitalWrite(mRb_minus, HIGH);
  
  delay(timer);
  
  digitalWrite(mLb_minus, LOW);
  digitalWrite(mRb_minus, LOW);
}

void left(int timer) {
  digitalWrite(mLb_minus, HIGH);
  digitalWrite(mRb_plus, HIGH);
  
  delay(timer);
  
  digitalWrite(mLb_minus, LOW);
  digitalWrite(mRb_plus, LOW);
}

void right(int timer) {
  digitalWrite(mRb_minus, HIGH);
  digitalWrite(mLb_plus, HIGH);
  
  delay(timer);
  
  digitalWrite(mRb_minus, LOW);
  digitalWrite(mLb_plus, LOW);
}

void charge_signal(int timer) {
  for (x_pisk = 0; x_pisk < timer; x_pisk += 1) {
    digitalWrite(pisk, HIGH);
    delay(1);
    digitalWrite(pisk, LOW);
  }
}

void servo_up(int values) {
  for (pos1 = 0; pos1 < values; pos1 += 1) {
    myservo.write(pos1);
    delay(15);
  }
}

void servo_down(int values) {
  for (pos1 = 0; pos1 < values; pos1 -= 1) {
    myservo.write(pos1);
    delay(15);
  }
}

void loop() {
  vpered(5000);

  delay(2000);
  
  back(5000);

  delay(2000);
  
  left(5000);

  delay(2000);
  
  right(5000);

  delay(2000);

  charge_signal(3000);

  delay(2000);

  servo_up(90);

  delay(2000);

  servo_down(90);

  delay(2000);

  if (mySerial.available()) {
    char c = mySerial.read();
    Serial.print(c);
  }
  if (Serial.available()) {
    char c = Serial.read();
    mySerial.write(c);
  }
}
