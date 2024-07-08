#include <Servo.h>

const int servoPin = 9;

const int echoPin = 8;
const int trigPin = 7;

Servo myServo;

int angle = 0;
int direction = 1;
int distance;

void setup() {
  // put your setup code here, to run once:
  myServo.attach(servoPin);
  pinMode(echoPin, INPUT);
  pinMode(trigPin, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:

  myServo.write(angle);
  if (angle >= 180) {
    direction = -1;
  } else if (angle <= 0) {
    direction = 1;
  }

  distance = getDistanceFromSensor();
  Serial.print(distance);
  Serial.print(",");
  Serial.println(angle);

  angle += 1 * direction;
  delay(15);
}

int getDistanceFromSensor() {
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  float duration = pulseIn(echoPin, HIGH);

  float distance = (duration * .0343) / 2;
  return (int)distance;
}
