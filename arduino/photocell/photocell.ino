/*****************************************************************************
 * photocell.ino - Arduino sensor control                                    *
 * uses built-in LED on pin 13 to indicate an open door                      *
 * uses a photoresistor connected to pin A0 to sense the state of the door   *
 *                                                                           *
 * Copyright (c) 2014 Nathanael A. Smith                                     *
 * License: MIT (see http://opensource.org/licenses/MIT)                     *
 *****************************************************************************/

// used to hold the photocell voltage reading
int photocellReading;
// the analogRead() value to indicate an open door
int THRESHHOLD_HIGH = 100;
// the analogRead() value to indicate a closed door
int THRESHHOLD_LOW = 95;

void setup() {
  // the LED pin
  pinMode(13, OUTPUT);
  // initialize serial and send default state
  Serial.begin(9600);
  Serial.write('0');
  // the photocell pin
  pinMode(A0, INPUT);
}

void loop() {
  // is the door open?
  if (analogRead(A0)>THRESHHOLD_HIGH) {
    // check to see if just random flutter; helps to debounce electronics
    delay(500);
    if (analogRead(A0)<=THRESHHOLD_LOW) {
      exit(0);
    }
    
    // the door is open
    // send message
    Serial.write('1');
    
    //set LED pin to high
    digitalWrite(13, HIGH);
    delay(1000);
    
    // wait for door to close
    while (analogRead(A0)>THRESHHOLD_LOW) {
      delay(100);
    }
    delay(1000);

    // write closed state to serial
    digitalWrite(13, LOW);
    Serial.write('0');
  }
}
