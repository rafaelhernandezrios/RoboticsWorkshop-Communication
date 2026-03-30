/*
 * Workshop: pyserial + Arduino
 * Commands (ASCII, newline-terminated):
 *   L1  -> LED on (built-in)
 *   L0  -> LED off
 *   S<angle> -> servo 0-180 (e.g. S90)
 */

#include <Servo.h>

Servo servo;
const int LED_PIN = LED_BUILTIN;
// Change if your board uses a different pin for the servo signal
const int SERVO_PIN = 9;

void setup() {
  Serial.begin(9600);
  while (!Serial) {
    ;  // native USB boards (Leonardo, Micro, etc.)
  }
  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN, LOW);
  servo.attach(SERVO_PIN);
  servo.write(90);
}

void loop() {
  if (Serial.available() <= 0) {
    return;
  }

  String line = Serial.readStringUntil('\n');
  line.trim();
  if (line.length() == 0) {
    return;
  }

  char c = line.charAt(0);
  if (c == 'L' || c == 'l') {
    int v = line.substring(1).toInt();
    digitalWrite(LED_PIN, v ? HIGH : LOW);
    Serial.println(F("OK LED"));
  } else if (c == 'S' || c == 's') {
    int angle = line.substring(1).toInt();
    angle = constrain(angle, 0, 180);
    servo.write(angle);
    Serial.println(F("OK SERVO"));
  } else {
    Serial.println(F("ERR unknown"));
  }
}
