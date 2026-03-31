/*
 * Practice 4 — expects lines:  servoid,position
 * Servo IDs 1..4 map to pins D9..D12 (edit pins[] if needed).
 * Position: 0..180
 *
 * Hardware: powering several servos from the Arduino 5V (USB) rail often
 * browns out the MCU — you get resets and no serial output. Use a separate
 * 5V supply for servo + and tie GND to Arduino GND; signal wires stay on D9–D12.
 */

#include <Servo.h>

Servo servos[4];
const int PINS[4] = {9, 10, 11, 12};

void setup() {
  Serial.begin(9600);
  // Native USB boards (Leonardo, Micro, etc.): wait until USB serial is ready.
  while (!Serial) {
    ;
  }
  // Let USB CDC settle; avoids garbage / missed first bytes after host opens port.
  delay(200);

  // Stagger attach + move to reduce peak current (four servos at once can reset the board).
  for (int i = 0; i < 4; i++) {
    servos[i].attach(PINS[i]);
    servos[i].write(90);
    delay(120);
  }

  Serial.setTimeout(200);
  Serial.println(F("READY"));
}

void loop() {
  if (Serial.available() <= 0) {
    return;
  }
  String line = Serial.readStringUntil('\n');
  line.trim();
  int comma = line.indexOf(',');
  if (comma <= 0) {
    Serial.println(F("ERR format (use id,pos)"));
    return;
  }
  int id = line.substring(0, comma).toInt();
  int pos = line.substring(comma + 1).toInt();
  if (id < 1 || id > 4) {
    Serial.println(F("ERR id"));
    return;
  }
  pos = constrain(pos, 0, 180);
  servos[id - 1].write(pos);
  Serial.println(F("OK"));
}
