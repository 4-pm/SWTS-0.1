#include <Servo.h>
//импорт билиотеки серво для управления сервоприводами

#include <SoftwareSerial.h>
//импорт библиотеки для работы с модулем Bluetooth HC-05

SoftwareSerial mySerial(2, 3); // указываем пины rx и tx соответственно

// Motor shield использует четыре контакта 4, 5, 6, 7 для управления моторами 
// 4 и 7 — для направления, 5 и 6 — для скорости
#define SPEED_1      5 
#define DIR_1        4 //левый мотор
 
#define SPEED_2      6
#define DIR_2        7 //правый мотор

Servo servo_right;
Servo servo_left;

int pos = 0;

void setup() {
  pinMode(2,INPUT);
  //порт для чтения информации с bluetooth модуля
  pinMode(3,OUTPUT);
  //порт для отправки информации с bluetooth модуля
  Serial.begin(9600);
  //порт принятия информации в компиляторе Arduino IDE
  mySerial.begin(9600);
  //порт для работы с модулем HC-05
  Serial.println("SWTS welcome you");
  delay(500);
  Serial.println("The machine starts working");

  // подключаем сервоприводы к выводам 11 и 12
  servo_right.attach(11);
  servo_right.write(0);
  servo_left.attach(12);
  servo_left.write(180);
  
  // настраиваем выводы платы 4, 5, 6, 7 на вывод сигналов 
  for (int i = 4; i < 8; i++) {     
    pinMode(i, OUTPUT);
  }
} 

void move_forward(int speed_1, int speed_2, int timer_1, int timer_2) {
  // устанавливаем направление моторов «M1», «M2» в одну сторону
  digitalWrite(DIR_1, HIGH);
  digitalWrite(DIR_2, HIGH);
  // включаем моторы на максимальной скорости
  analogWrite(SPEED_1, speed_1);
  analogWrite(SPEED_2, speed_2);
  // ждём
  delay(timer_1);

  // отключаем мотор 2
  analogWrite(SPEED_2, 0);

  delay(timer_2);

  // отключаем мотор 1
  analogWrite(SPEED_1, 0);

  // ждём одну секунду
  delay(1000);
}

void move_back(int speed_1, int speed_2, int timer_1, int timer_2) {
  // устанавливаем направление моторов «M1», «M2» в одну сторону
  digitalWrite(DIR_1, LOW);
  digitalWrite(DIR_2, LOW);
  // включаем моторы на максимальной скорости
  analogWrite(SPEED_1, speed_1);
  analogWrite(SPEED_2, speed_2);
  // ждём
  delay(timer_1);

  // отключаем мотор 2
  analogWrite(SPEED_2, 0);

  delay(timer_2);

  // отключаем мотор 1
  analogWrite(SPEED_1, 0);
  
  // ждём одну секунду
  delay(1000);
}

void move_left(int speed_1, int speed_2, int timer_1, int timer_2) {
  // устанавливаем направление моторов «M1», «M2» в разные стороны
  digitalWrite(DIR_1, LOW);
  digitalWrite(DIR_2, HIGH);
  // включаем моторы на максимальной скорости
  analogWrite(SPEED_1, speed_1);
  analogWrite(SPEED_2, speed_2);
  // ждём
  delay(timer_1);

  // отключаем мотор 2
  analogWrite(SPEED_2, 0);

  delay(timer_2);

  // отключаем мотор 1
  analogWrite(SPEED_1, 0);
  
  // ждём одну секунду
  delay(1000);
}

void move_right(int speed_1, int speed_2, int timer_1, int timer_2) {
  // устанавливаем направление моторов «M1», «M2» в разные стороны
  digitalWrite(DIR_1, HIGH);
  digitalWrite(DIR_2, LOW);
  // включаем моторы на максимальной скорости
  analogWrite(SPEED_1, speed_1);
  analogWrite(SPEED_2, speed_2);
  // ждём
  delay(timer_1);

  // отключаем мотор 2
  analogWrite(SPEED_2, 0);

  delay(timer_2);

  // отключаем мотор 1
  analogWrite(SPEED_1, 0);
  
  // ждём одну секунду
  delay(1000);
}

void rake() {
  for (pos = 0; pos < 180; pos += 1) {
   servo_right.write(pos);
   servo_left.write(180 - pos);
   delay(15); 
  }

  //поднимаем для сброса мусора
  
  delay(1000);
  
  for (pos = 180; pos >= 0; pos -= 1) {
   servo_right.write(pos);
   servo_left.write(180 - pos);
   delay(15); 
  }

  //возвращаем в исходное положение
  
  delay(1000);
}

void loop() {
  if (mySerial.available() > 0){
    char b_com = mySerial.read();
    Serial.println("Using the command  ");
    Serial.println(b_com); //вывод значения с bluetooth
    if (b_com == '5') {
      Serial.println("SWTS picks up the rake");
      rake(); //подъём грабель
    }
    if (b_com == '8'){
      Serial.println("SWTS are moving forward");
      int c_t = mySerial.read(); //время движения
      int c_t_2 = 50; //дополнительное время движения мотора 1
      move_forward(255, 220, c_t, c_t_2); //параметры: скорость мотора 1, скорость мотора 2, время движения, дополнительное время движения мотора 1
    }
    if (b_com == '2'){
      Serial.println("SWTS are moving back");
      int c_t = mySerial.read(); //время движения
      int c_t_2 = 50; //дополнительное время движения мотора 1
      move_back(255, 220, c_t, c_t_2); //параметры: скорость мотора 1, скорость мотора 2, время движения, дополнительное время движения мотора 1
    }
    if (b_com == '4'){
      Serial.println("SWTS are rotating left");
      int c_t = mySerial.read(); //время движения
      int c_t_2 = 50; //дополнительное время движения мотора 1
      move_left(255, 220, c_t, c_t_2); //параметры: скорость мотора 1, скорость мотора 2, время движения, дополнительное время движения мотора 1
    }
    if (b_com == '6'){
      Serial.println("SWTS are rotating right");
      int c_t = mySerial.read(); //время движения
      int c_t_2 = 50; //дополнительное время движения мотора 1
      move_right(255, 220, c_t, c_t_2); //параметры: скорость мотора 1, скорость мотора 2, время движения, дополнительное время движения мотора 1
    }
  }
  delay(1000); //задержка 1 секунда
}
