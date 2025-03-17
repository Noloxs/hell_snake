#include <Keyboard.h>

const int resetPin = 2;  // Pin used to trigger the reset mode

unsigned long lastKeyPressTime = 0;  // Track when the key was last pressed
unsigned long keyTimeout = 5000;  // Timeout to release the key if something goes wrong (in milliseconds)


void setup() {
  // Initialize Serial and Keyboard
  Serial.begin(115200);
  Serial.setTimeout(1);
  Keyboard.begin();

  // Initialize the reset pin as input
  pinMode(resetPin, INPUT_PULLUP);  // Assuming HIGH means reset mode
  
  // Check if reset pin is in the correct state (HIGH or LOW as per your requirement)
  if (digitalRead(resetPin) == LOW) {
    // Enter a safe mode: infinite loop to prevent any further execution
    while (true) {
      digitalWrite(LED_BUILTIN, HIGH);  // Turn on built-in LED (optional)
      delay(250);  // Delay for a visible blink
      digitalWrite(LED_BUILTIN, LOW);   // Turn off LED
      delay(250);
      digitalWrite(LED_BUILTIN, HIGH);  // Turn on built-in LED (optional)
      delay(250);  // Delay for a visible blink
      digitalWrite(LED_BUILTIN, LOW);   // Turn off LED
      delay(1250);
    }
  }
  // Normal program setup continues...
}

void loop() {
  // Your normal keyboard emulation code goes here.
  if (Serial.available() >= 3) {
    char key = Serial.read(); // Read the key character

    // Read the next two bytes (delay time)
    int16_t delayTime = (Serial.read() << 8) | Serial.read(); // Combine the two bytes to form the delay time

    // Press the key
    Keyboard.press(key);
    delay(abs(delayTime));
    
    // Wait for the specified delay
    if (delayTime >= 0) {
      Keyboard.release(key);
      delay(abs(delayTime));
    }
  }
  // If no data is available, allow the CPU to rest briefly
  else {
    delay(10);  // Small delay to allow at least one byte to arrive before checking again
  }

  // Safety check to make sure keys are always released after a certain timeout
  if (millis() - lastKeyPressTime > keyTimeout) {
    // If key has been pressed for too long and release was missed, forcibly release it
    Keyboard.releaseAll();
    lastKeyPressTime = millis();  // Reset last press time to avoid repeated releases
  }
}
