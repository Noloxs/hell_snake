#include <Keyboard.h>

void setup() {
  Serial.begin(115200);
  Serial.setTimeout(1);

  Keyboard.begin();
}

void loop() {
  if (Serial.available() > 0) {
    char key = Serial.read(); // Read the hex character

    // Read the next two bytes which represent the delay time
    while (Serial.available() < 2) {
      // Wait for the two bytes to be available
    }
    int16_t delayTime = (Serial.read() << 8) | Serial.read(); // Combine the two bytes

    // Press the key
    Keyboard.press(key);
    delay(abs(delayTime));

    // Release the key if delayTime is non-negative
    if (delayTime >= 0) {
      Keyboard.release(key);
      delay(abs(delayTime));
    }
  }
}