#include <Keyboard.h>

const int resetPin = 2;  // Pin used to trigger the reset mode
const int ledPin = LED_BUILTIN; // LED pin for activity indication

unsigned long lastKeyPressTime = 0;  // Track when the key was last pressed
unsigned long keyTimeout = 5000;  // Timeout to release the key if something goes wrong (in milliseconds)
unsigned long inactivityThreshold = 120000;  // 120 seconds before entering idle state

// Initializes serial communication, keyboard, and checks reset pin
void setup() {
  Serial.begin(115200);
  Serial.setTimeout(1);
  Keyboard.begin();

  pinMode(resetPin, INPUT_PULLUP);  // Reset pin
  pinMode(ledPin, OUTPUT);  // LED indicator

  if (digitalRead(resetPin) == LOW) {
    while (true) {
      digitalWrite(ledPin, HIGH);
      delay(250);
      digitalWrite(ledPin, LOW);
      delay(250);
      digitalWrite(ledPin, HIGH);
      delay(250);
      digitalWrite(ledPin, LOW);
      delay(1250);
    }
  }
  // Initially active
  digitalWrite(ledPin, HIGH);
  lastKeyPressTime = millis();

}

// Handles LED and delays based on activity state
void handleIdleState() {
  if (millis() - lastKeyPressTime > inactivityThreshold) {
    digitalWrite(ledPin, LOW); // Turn off LED in idle state
    Keyboard.releaseAll();
    delay(5000); // Enter low-power idle state
  } else {
    delay(5); // Short delay during operation
  }
}

// Processes key press and release with a specified delay
void processKeyPress(char key, int16_t delayTime) {
  Keyboard.press(key);
  delay(abs(delayTime));

  if (delayTime >= 0) {
    Keyboard.release(key);
    delay(abs(delayTime));
  }
}

// Processes special commands received via serial
void processCommand(char command, char parameter) {
  switch (command) {
    case 0x01:  // Wakeup command
      lastKeyPressTime = millis(); // Refresh activity timer
      break;

    // Future commands can be added here with more cases
  }
}

// Reads and processes serial input, distinguishing between key presses and commands
void processSerialInput() {
  digitalWrite(ledPin, HIGH);
  lastKeyPressTime = millis(); // Update activity time

  char key = Serial.read();
  
  if (key == 0x00) {  // Special command mode
    char command = Serial.read();
    char parameter = Serial.read();
    processCommand(command, parameter);
  } else {
    int16_t delayTime = (Serial.read() << 8) | Serial.read();
    processKeyPress(key, delayTime);
  }
  
  delay(1);  // Maintain short delay during active operation
}

// Main loop, handling serial input and idle state
void loop() {
  if (Serial.available() >= 3) {
    processSerialInput();
  } else {
    handleIdleState();
  }
}
