from inspect import modulesbyfile
from playsound import playsound
from ctypes import cast, POINTER
import serial
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import psutil
import subprocess
import time

arduinoSerialData = serial.Serial('com3', 9600)
time.sleep(1)
isOpen = "chrome.exe" in (i.name() for i in psutil.process_iter())

while True:
    if (arduinoSerialData.inWaiting()>0):
        myData = arduinoSerialData.readline()
        myData = str(myData,'utf-8')
        myData = myData.strip('\r\n')
        print(myData)
        
        if myData == 'Switch: ON':
            if ("chrome.exe" in (i.name() for i in psutil.process_iter())):
                subprocess.call("TASKKILL /F /IM chrome.exe 2> nul", shell=True)

            # Get default audio device using pycaw
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            volume = cast(interface, POINTER(IAudioEndpointVolume))

            # Get current volume
            currentVolumeDb = volume.GetMasterVolumeLevel()
            volume.SetMasterVolumeLevel(-25.0, None)

            i = 0
            while i < 113:
                playsound('emergency-alarm-with-reverb-29431.mp3')
                i += 1
            
            quit()