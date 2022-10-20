#include <SoftwareSerial.h>

SoftwareSerial mySerial(2, 3);

int gLed = 13;


void setup() {
  // put your setup code here, to run once:
  pinMode(2, INPUT);
  pinMode(3, OUTPUT);
  pinMode(gLed, OUTPUT);
  digitalWrite(gLed,LOW);
  Serial.begin(9600);
  mySerial.begin(9600);
  Serial.println("start prg");
}

void loop() {
  int buf_size = mySerial.available();
  if (buf_size == 1) {
      digitalWrite(gLed, HIGH);
      delay(1000);
      digitalWrite(gLed, LOW);
      delay(1000);
      int but_size = 0;
    }
}
