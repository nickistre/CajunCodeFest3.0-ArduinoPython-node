// receiver.pde
//
// Simple example of how to use VirtualWire to receive messages
// Implements a simplex (one-way) receiver with an Rx-B1 module
//
// See VirtualWire.h for detailed API docs
// Author: Mike McCauley (mikem@airspayce.com)
// Copyright (C) 2008 Mike McCauley
// $Id: receiver.pde,v 1.3 2009/03/30 00:07:24 mikem Exp $

#include <VirtualWire.h>

#include <DeviceSerial.h>

DeviceSerial deviceSerial = DeviceSerial(1);

void setup()
{
    deviceSerial.init();

    // Initialise the IO and ISR
    vw_set_ptt_inverted(true); // Required for DR3100
    
    vw_set_rx_pin(12);
    vw_setup(2000);	 // Bits per sec

    vw_rx_start();       // Start the receiver PLL running
    
    deviceSerial.send(String("Max Buffer Len: ") + VW_MAX_MESSAGE_LEN, "log");
}

void loop()
{
    uint8_t buf[VW_MAX_MESSAGE_LEN];
    uint8_t buflen = VW_MAX_MESSAGE_LEN;

    if (vw_get_message(buf, &buflen)) // Non-blocking
    {
	int i;

        digitalWrite(13, true); // Flash a light to show received good message
	// Message with a good checksum received, dump it.
	
        
        String data = String("dataType: ") + buf[0] + ", data: [";
        char delim[2] = " ";	

	for (i = 1; i < buflen; i++)
	{
          char bufVal[2];
          data += delim;
          data += buf[i];
          delim[0] = ',';
	}
        data.concat(" ]");
        
	deviceSerial.send(data, "data");
        digitalWrite(13, false);
    }
}
