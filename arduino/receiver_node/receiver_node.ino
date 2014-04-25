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
#include <DeviceMessage.h>

#define DEVICE_ID 1

DeviceSerial deviceSerial = DeviceSerial(DEVICE_ID);

unsigned int messageCount = 0;

void setup()
{
    deviceSerial.init();

    // Initialise the IO and ISR
    vw_set_ptt_inverted(true); // Required for DR3100
    
    vw_set_rx_pin(12);
    vw_setup(2000);	 // Bits per sec

    vw_rx_start();       // Start the receiver PLL running
    
    deviceSerial.send("ready", "device");
}

void loop()
{
    checkRF();
    checkSerialMessages();
}

void checkRF()
{
    uint8_t buf[VW_MAX_MESSAGE_LEN];
    uint8_t buflen = VW_MAX_MESSAGE_LEN;

    if (vw_get_message(buf, &buflen)) // Non-blocking
    {
	int i;

        digitalWrite(13, true); // Flash a light to show received good message
	// Message with a good checksum received, dump it.
	
        DeviceMessage deviceMessage = DeviceMessage();
        
        deviceMessage.deviceId = buf[0];
        deviceMessage.messageId = messageCount;
        messageCount++;
        
        deviceMessage.type = String("data");
        
        String data = String("[");
        char delim[2] = " ";	

	for (i = 1; i < buflen; i++)
	{
          data += delim;
          data += buf[i];
          delim[0] = ',';
	}
        data.concat(" ]");
        
        deviceMessage.data =data;
        
	deviceSerial.sendMessage(deviceMessage);
        digitalWrite(13, false);
    }
}

void checkSerialMessages()
{
    if (deviceSerial.available()) {
    DeviceMessage message;
    deviceSerial.receiveMessage(message);
    
    
    if (message.type == "do-echo") {
      deviceSerial.send(message.data, "echo");
    }
    else if(message.type == "device" && message.data == "ready?")
    {
      deviceSerial.send("ready", "device");
    }
    else {
      deviceSerial.send(String("Received Unknown Type: "+message.type +" from device id: "+message.deviceId), "log");
    }
  }
}
