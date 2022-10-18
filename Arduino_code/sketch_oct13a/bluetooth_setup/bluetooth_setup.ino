#include <SoftwareSerial.h>

SoftwareSerial mySerial(2, 3);


void setup() {
  // put your setup code here, to run once:
  pinMode(2, INPUT);
  pinMode(2, OUTPUT);
  Serial.begin(9600);
  mySerial.begin(38400);
  Serial.println("start prg");
}

void loop() {
  if (mySerial.available()){
    char c = mySerial.read();
    Serial.print(c);
  }
  if (Serial.available()){
    char c = Serial.read();
    mySerial.write(c);
  }
}
