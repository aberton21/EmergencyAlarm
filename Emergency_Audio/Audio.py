from inspect import modulesbyfile
from playsound import playsound
from ctypes import cast, POINTER
import serial
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from subprocess import PIPE
import psutil
import os
import subprocess

alarm_sound = "emergency-alarm-with-reverb-29431.mp3"

arduinoSerialData = serial.Serial('com3', 9600)

alarm_playing = False

while True:
    myData = ''
    if arduinoSerialData.inWaiting() > 0:
        myData = arduinoSerialData.readline()
        myData = str(myData,'utf-8')
        myData = myData.strip('\r\n')            
        print(myData)
            
        if myData == 'Switch: ON':
            
            isOpen = "chrome.exe" in (i.name() for i in psutil.process_iter())
            if (isOpen):
                subprocess.Popen("TASKKILL /F /IM chrome.exe 2> nul", shell=True)
                    
            # Get default audio device using pycaw
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            volume = cast(interface, POINTER(IAudioEndpointVolume))

            # Get current volume
            currentVolumeDb = volume.GetMasterVolumeLevel()
            volume.SetMasterVolumeLevel(-0.0, None)

            # Check if the alarm is already playing
            if not alarm_playing:
                playsound(alarm_sound)
                alarm_playing = True
                
        elif myData == 'Switch: OFF':
            # Check if the alarm is currently playing
            if alarm_playing:
                alarm_playing = False
                subprocess.Popen("TASKKILL /F /IM wmplayer.exe 2> nul", shell=True)
