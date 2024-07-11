// Upload to Arduino Micro Attached to Computer

#include <nRF24L01.h>
#include <RF24.h>
#include <SPI.h>
#include <Mouse.h>

RF24 radio(5, 7);
const byte address[6] = "0001";
char buf[20];

const int deviceWidth = 1320;
const int deviceHeight = 848;

void setup() {
  SerialUSB.begin(115200);

  radio.begin();
  radio.openWritingPipe(address);
  radio.setPALevel(RF24_PA_MIN);
  radio.stopListening();
  Serial.begin(115200);
  Mouse.begin();
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
  if (readline(SerialUSB.read(), buf, 20) > 0) {
    radio.write(buf, sizeof(buf));
  }
}

int readline(int readch, char *buffer, int len) {
  static int pos = 0;
  int rpos;

  if (readch > 0) {
    switch (readch) {
      case '\r': // Ignore CR
        break;
      case '\n': // Return on new-line
        rpos = pos;
        pos = 0;  // Reset position index ready for next time
        return rpos;
      default:
        if (pos < len - 1) {
          buffer[pos++] = readch;
          buffer[pos] = 0;
        }
    }
  }
  return 0;
}
