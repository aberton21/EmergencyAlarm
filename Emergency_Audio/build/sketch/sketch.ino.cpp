#include <Arduino.h>
#line 1 "c:\\Users\\Owner\\OneDrive\\Desktop\\Emergency_Audio\\sketch.ino"
#line 1 "c:\\Users\\Owner\\OneDrive\\Desktop\\Emergency_Audio\\sketch.ino"
#include <ezButton.h>

ezButton toggleSwitch(7);

#line 5 "c:\\Users\\Owner\\OneDrive\\Desktop\\Emergency_Audio\\sketch.ino"
void setup();
#line 10 "c:\\Users\\Owner\\OneDrive\\Desktop\\Emergency_Audio\\sketch.ino"
void loop();
#line 5 "c:\\Users\\Owner\\OneDrive\\Desktop\\Emergency_Audio\\sketch.ino"
void setup()
{
	Serial.begin(9600);
	toggleSwitch.setDebounceTime(50);
}
void loop()
{
	toggleSwitch.loop();
	
	if (toggleSwitch.isPressed())
		Serial.println("Switch: OFF -> ON");
	
	if(toggleSwitch.isReleased())
		Serial.println("Switch: ON -> OFF");
	
	int state = toggleSwitch.getState();
	if (state == HIGH)
		Serial.println("Switch: OFF");
	else
		Serial.println("Switch: ON");
}

