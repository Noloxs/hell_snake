#include <Keyboard.h>

char ctrlKey = KEY_LEFT_CTRL;
int pressDelay = 80;
int keyDelay = 50;
char command[] = "kkil"; //down,down,up,right

void setup() {
  // make pin 2 an input and turn on the
  // pullup resistor so it goes high unless
  // connected to ground:

command[0] = KEY_DOWN_ARROW;
command[1] = KEY_DOWN_ARROW;
command[2] = KEY_UP_ARROW;
command[3] = KEY_RIGHT_ARROW;

  pinMode(2, INPUT_PULLUP);
  Keyboard.begin();
}

void loop() {
  //if the button is pressed
  if (digitalRead(2) == LOW) {
    Keyboard.press(ctrlKey);
    delay(pressDelay);
    for (byte i = 0; i < sizeof(command) - 1; i++) {
      Keyboard.press(command[i]);
      delay(keyDelay);
      Keyboard.release(command[i]);
      delay(keyDelay);
    }
    Keyboard.release(ctrlKey);
    delay(750);
  }
}