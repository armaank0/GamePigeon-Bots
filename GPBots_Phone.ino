// Upload to Arduino Micro Attached to Phone

// Calibrate for centering mouse on screen at startup
const int deviceWidth = 200;
const int deviceHeight = 600;

#include <nRF24L01.h>
#include <RF24.h>
#include <SPI.h>
#include <Mouse.h>
#include <Keyboard.h>

RF24 radio(5, 7);
const byte address[6] = "0001";

char command = ' ';
bool l_down = false;
bool r_down = false;

void setup() {
  radio.begin();
  radio.openReadingPipe(0, address);
  radio.setPALevel(RF24_PA_MIN);
  radio.startListening();
  Mouse.begin();
  Keyboard.begin();
  Serial.begin(115200);
  delay(2000);

  //Move the mouse to top left of screen
  for (int i = 0; i < (int) (deviceWidth / 127) + 1; i++) {
    delay(100);
    Mouse.move(-127, 0, 0);
  }
  for (int i = 0; i < (int) (deviceHeight / 127) + 1; i++) {
    delay(100);
    Mouse.move(0, -127, 0);
  }
  //Move the mouse to the center of the screen
  int remainderX = deviceWidth / 2;
  for (int i = 0; i < (int) (deviceWidth / 2 / 127); i++) {
    delay(100);
    Mouse.move(127, 0, 0);
    remainderX -= 127;
  }
  remainderX = (signed char) remainderX;
  delay(100);
  Mouse.move(remainderX, 0, 0);
  int remainderY = deviceHeight / 2;
  for (int i = 0; i < (int) (deviceHeight / 2 / 127); i++) {
    delay(100);
    Mouse.move(0, 127, 0);
    remainderY -= 127;
  }
  delay(100);
  remainderY = (signed char) remainderY;
  Mouse.move(0, remainderY, 0);

}

void loop() {
  if (radio.available()) {
    char text[20] = "";
    radio.read(&text, sizeof(text));

    command = text[0];

    if (command == 'm') {
      String x_str = String(text).substring(2, String(text).indexOf('/'));
      String y_str = String(text).substring(String(text).indexOf('/') + 1);
      int x = x_str.toInt();
      int y = y_str.toInt();

      Mouse.move(x, y, 0);
      Serial.print(x);
      Serial.print("  ");
      Serial.println(y);
    } else if (command == 'l') {
      Mouse.press(MOUSE_LEFT);

    } else if (command == 'n') {
      Mouse.release(MOUSE_LEFT);

    } else if (command == 'r') {
      Mouse.press(MOUSE_RIGHT);

    } else if (command == 'f') {
      Mouse.release(MOUSE_RIGHT);

    } else if (command == 'd') {
      Mouse.move(0, 0, 1);

    } else if (command == 'u') {
      Mouse.move(0, 0, -1);

    } else if (command == 'w') {
      String x_str = String(text).substring(2, String(text).indexOf('/'));
      String y_str = String(text).substring(String(text).indexOf('/') + 1);
      int x = x_str.toInt();
      int y = y_str.toInt();

      //Move the mouse to top left of screen
      for (int i = 0; i < (int) (deviceWidth / 127) + 1; i++) {
        delay(100);
        Mouse.move(-127, 0, 0);
      }
      for (int i = 0; i < (int) (deviceHeight / 127) + 1; i++) {
        delay(100);
        Mouse.move(0, -127, 0);
      }

      Mouse.move(x, 127, 0);
      delay(100);
      Mouse.move(0, 127, 0);
      delay(100);
      Mouse.move(0, 127, 0);
      delay(100);
      Mouse.move(0, y, 0);
    } else if (command == 'k') {
      String key_str = String(text).substring(2, String(text).indexOf('/'));
      int key = key_str.toInt();
      Keyboard.press(key);

    } else if (command == 'j') {
      String key_str = String(text).substring(2, String(text).indexOf('/'));
      int key = key_str.toInt();
      Keyboard.release(key);

    } else if (command == 'c') {
      String x_str = String(text).substring(2, String(text).indexOf('/'));
      String y_str = String(text).substring(String(text).indexOf('/') + 1);
      int x = x_str.toInt();
      int y = y_str.toInt();
      //Move the mouse to top left of screen
      for (int i = 0; i < (int) (deviceWidth / 127) + 1; i++) {
        delay(100);
        Mouse.move(-127, 0, 0);
      }
      for (int i = 0; i < (int) (deviceHeight / 127) + 1; i++) {
        delay(100);
        Mouse.move(0, -127, 0);
      }

      Mouse.move(127, 127, 0);
      delay(100);
      Mouse.move(x, 127, 0);
      delay(100);
      Mouse.move(0, 127, 0);
      delay(100);
      Mouse.move(0, 127, 0);
      delay(100);
      Mouse.move(0, y, 0);
    }
  }
}
