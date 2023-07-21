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
import time
import threading


arduinoSerialData = serial.Serial('com4', 9600)

audio_file = "emergency-alarm-with-reverb-29431.mp3"
file_path = r"C:\cniapserv\ID Badge Computer\Desktop\emergency-alarm-with-reverb-29431"

alarm_playing = False

while True:
    myData = ''
    if (arduinoSerialData.inWaiting()>0):
        myData = arduinoSerialData.readline()
        myData = str(myData,'utf-8')
        myData = myData.strip('\r\n')
        print(myData)
        
    if myData == 'Switch: ON':

        edgeOpen = "msedge.exe" in (i.name() for i in psutil.process_iter())
        if (edgeOpen):
            subprocess.Popen("TASKKILL /F /IM msedge.exe 2> nul", shell=True)
        
        chromeOpen = "chrome.exe" in (i.name() for i in psutil.process_iter())
        if (chromeOpen):
            subprocess.Popen("TASKKILL /F /IM chrome.exe 2> nul", shell=True)
 
                
        # Get default audio device using pycaw
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))

        # Get current volume
        currentVolumeDb = volume.GetMasterVolumeLevel()
        volume.SetMasterVolumeLevel(-50.0, None)

        if not alarm_playing:
            alarm_playing = True
            playsound(audio_file) 
    
    elif myData == 'Switch: OFF':
        if alarm_playing:
            alarm_playing = False
            subprocess.Popen("TASKKILL /F /IM wmplayer.exe 2> nul", shell=True)
