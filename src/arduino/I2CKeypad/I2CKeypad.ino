// I2C slave that reads a keypad

#include <Keypad.h>
#include <Wire.h>
const int BUFFER_SIZE = 16;

struct Buffer {
    uint8_t data[BUFFER_SIZE];
    uint8_t newest_index;
    uint8_t oldest_index;
};
volatile struct Buffer buffer = {{}, 0, 0};
enum BufferStatus {BUFFER_OK, BUFFER_EMPTY, BUFFER_FULL};

uint8_t byte_from_buffer;

const byte ROWS = 4; //four rows
const byte COLS = 4; //four columns
char keys[ROWS][COLS] = {
  {'1','2','3','A'},
  {'4','5','6','B'},
  {'7','8','9','C'},
  {'*','0','#','D'}
};
byte rowPins[ROWS] = {8, 7, 6, 5}; //connect to the row pinouts of the keypad
byte colPins[COLS] = {12, 11, 10, 9}; //connect to the column pinouts of the keypad

enum BufferStatus bufferRead(uint8_t *byte){
    if (buffer.newest_index == buffer.oldest_index){
        return BUFFER_EMPTY;
    }
    *byte = buffer.data[buffer.oldest_index];
    buffer.oldest_index = (buffer.oldest_index+1) % BUFFER_SIZE;
    return BUFFER_OK;
}

enum BufferStatus bufferWrite(uint8_t byte){
    uint8_t next_index = (buffer.newest_index+1) % BUFFER_SIZE;
 
    if (next_index == buffer.oldest_index){
        return BUFFER_FULL;
    }
    buffer.data[buffer.newest_index] = byte;
    buffer.newest_index = next_index;
    return BUFFER_OK;
}



Keypad keypad = Keypad( makeKeymap(keys), rowPins, colPins, ROWS, COLS );

void setup(){
  Serial.begin(9600);
  Wire.begin(8);                // join i2c bus with address #8
  Wire.onRequest(requestEvent); // register event
}
  
void loop() {
   char key = keypad.getKey();
   if (key) {
    bufferWrite(key);
   }
}

void requestEvent() {
  enum BufferStatus status;
  uint8_t char_from_buffer;
  status = bufferRead(&char_from_buffer);
  if (status == BUFFER_OK) {
    Wire.write(char_from_buffer);
  } 
  else {
   Wire.write(0x00);
  }
}
  
  // as expected by master
