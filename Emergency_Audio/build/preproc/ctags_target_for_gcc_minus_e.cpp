# 1 "c:\\Users\\Owner\\OneDrive\\Desktop\\Emergency_Audio\\sketch.ino"
# 1 "c:\\Users\\Owner\\OneDrive\\Desktop\\Emergency_Audio\\sketch.ino"
# 2 "c:\\Users\\Owner\\OneDrive\\Desktop\\Emergency_Audio\\sketch.ino" 2

ezButton toggleSwitch(7);

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
 if (state == 0x1)
  Serial.println("Switch: OFF");
 else
  Serial.println("Switch: ON");
}
