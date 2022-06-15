#include <SoftwareSerial.h>
#include <Servo.h>


SoftwareSerial HC05(5, 6);
Servo myservo;

int m_r = 13;
int m_r_plus = 11;
int m_r_minus = 12;
int m_l = 10;
int m_l_plus = 8;
int m_l_minus = 9;

int pisk = 7;

int serv = 4;

int pos = 0;

int t_ok = 1000;
int t_err = 500;

void setup() {
  HC05.begin(9600);
  
  pinMode(m_r, OUTPUT);
  pinMode(m_r_minus, OUTPUT);
  pinMode(m_r_plus, OUTPUT);
  pinMode(m_l, OUTPUT);
  pinMode(m_l_minus, OUTPUT);
  pinMode(m_l_plus, OUTPUT);

  myservo.attach(serv);
}

void servo_up() {
  for(pos = 0; pos < 180; pos += 1) {
    myservo.write(pos);
    delay(15);
  }
}

void servo_down() {
  for(pos = 0; pos >= 180; pos -= 1) {
    myservo.write(pos);
    delay(15);
  }
}

void pisk_signal(taimer) {
  digitalWrite(pisk, HIGH);
  delay(taimer);
  digitalWrite(pisk, LOW);
}

void go(taimer){
  digitalWrite(m_r, HIGH);
  digitalWrite(m_r_plus, HIGH);
  digitalWrite(m_l, HIGH);
  digitalWrite(m_l_plus, HIGH);
  delay(taimer);
  digitalWrite(m_r, LOW);
  digitalWrite(m_r_plus, LOW);
  digitalWrite(m_l, LOW);
  digitalWrite(m_l_plus, LOW);
}

void back(taimer) {
  digitalWrite(m_r_minus, HIGH);
  digitalWrite(m_l_minus, HIGH);
  delay(taimer);
  digitalWrite(m_r_minus, LOW);
  digitalWrite(m_l_minus, LOW);
}

void left(taimer) {
  digitalWrite(m_r_plus, HIGH);
  digitalWrite(m_l_minus, HIGH);
  delay(taimer);
  digitalWrite(m_r_plus, LOW);
  digitalWrite(m_l_minus, LOW);
}

void right(taimer) {
  digitalWrite(m_l_plus, HIGH);
  digitalWrite(m_r_minus, HIGH);
  delay(taimer);
  digitalWrite(m_l_plus, LOW);
  digitalWrite(m_r_minus, LOW);
}

void loop() {
  if(HC05.available() > 0) {
    char receive = HC05.read(); //Read from Serial Communication
    if(receive == '5')
    {
      pisk_signal(t_ok);
      servo_up();
      delay(500);
      servo_down();
    }
    if(receive == '2')
    {
      pisk_signal(t_ok);
      back(t_ok);
    }
    if(receive == '4')
    {
      pisk_signal(t_ok);
      left(t_ok);
    }
    if(receive == '6')
    {
      pisk_signal(t_ok);
      right(t_ok);
    }
    if(receive == '8')
    {
      pisk_signal(t_ok);
      go(t_ok);
    }
    else {
      pisk_signal(t_err);
      delay(t_err);
      pisk_signal(t_err);
    }
  }
}
