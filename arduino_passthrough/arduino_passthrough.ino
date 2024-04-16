#include <Keyboard.h>

int startChar = 251; //KEY_F24
int seperatorChar = 250; //KEY_F23
int endChar = 247; //KEY_F20
int releaseDec = 249; //KEY_F22
int holdDec = 248; //KEY_F21 
int currentKey;
int currentDelay;

void setup() {
  Serial.begin(115200);
  Serial.setTimeout(1);

  Keyboard.begin();
}

void loop() {
  while (!Serial.available());
  if(!hasStartCommand()){
    return;
  }

  while (Serial.available()){
    if(!setCurrentCommand()){
      return;
    }
    if(!setCurrentDelay()){
      return;
    }

    if(currentDelay == holdDec){
      Keyboard.press(currentKey);
      delay(100);
    }else if(currentDelay == releaseDec){
      Keyboard.release(currentKey);
      delay(100);
    }else{
      delay(currentDelay);
      Keyboard.press(currentKey);
      delay(currentDelay);
      Keyboard.release(currentKey);
    }

    if(Serial.peek() == endChar){
      return;
    }
  }

  delay(750);
}

boolean hasStartCommand(){
  int in;
  while(Serial.available()){
    in = (int) Serial.read();
    if (in == startChar){
      return true;
    }
  }
  return false;
}

boolean setCurrentCommand(){
  int in;
  while(Serial.available()){
    if (Serial.peek() != seperatorChar){
      in = Serial.read();
    }else{
      Serial.read();
      currentKey = in;
      return true;
    }
  }
  return false;
}

boolean setCurrentDelay(){
  int in;
  while(Serial.available()){
    if (Serial.peek() != seperatorChar){
      in = Serial.read();
    }else{
      Serial.read();
      currentDelay = in;
      return true;
    }
  }
  return false;
}