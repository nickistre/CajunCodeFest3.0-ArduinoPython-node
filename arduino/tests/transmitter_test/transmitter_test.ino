// transmitter.pde
//
// Simple example of how to use VirtualWire to transmit messages
// Implements a simplex (one-way) transmitter with an TX-C1 module
//
// See VirtualWire.h for detailed API docs
// Author: Mike McCauley (mikem@airspayce.com)
// Copyright (C) 2008 Mike McCauley
// $Id: transmitter.pde,v 1.3 2009/03/30 00:07:24 mikem Exp $

#include <VirtualWire.h>

unsigned long int count = 0;

void setup()
{
    Serial.begin(9600);	  // Debugging only
    Serial.println("setup");

    // Initialise the IO and ISR
    vw_set_ptt_inverted(true); // Required for DR3100
    vw_set_tx_pin(12);
    vw_setup(2000);	 // Bits per sec
    
    

  // if analog input pin 0 is unconnected, random analog
  // noise will cause the call to randomSeed() to generate
  // different seed numbers each time the sketch runs.
  // randomSeed() will then shuffle the random function.
  randomSeed(analogRead(0));
}

void loop()
{
    char msg[VW_MAX_MESSAGE_LEN] = "01234";
    
    
    Serial.print("Currentt count: ");
    Serial.println(count);
    
    unsigned long int data = random(60000);
    
    Serial.print("Data to send: ");
    Serial.println(data);
    
    // Set deviceId
    msg[0] = 1;
    
    // Convert timer into a byte array.
    unsigned char byteArrayCount[sizeof(unsigned long int)];
    memcpy(&msg[1], &data, sizeof(unsigned long int));
    
    msg[sizeof(unsigned long int)+2] = char(0);
    
    Serial.print("Sending: ");
    for (int i = 0; i < strlen(msg); i++) {
      Serial.print(byte(msg[i]));
      Serial.print(".");
    }
    Serial.println("");
    digitalWrite(13, true); // Flash a light to show transmitting
    vw_send((uint8_t *)msg, strlen(msg));
    vw_wait_tx(); // Wait until the whole message is gone
    digitalWrite(13, false);
    
    count++;
    delay(1000);
}
