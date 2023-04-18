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


arduinoSerialData = serial.Serial('com3', 9600)

audio = None

audio_file = "emergency-alarm-with-reverb-29431.mp3"

def switch_on():
    global audio
    print("Alarm activated")

    # Get default audio device using pycaw
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))

    # Get current volume
    currentVolumeDb = volume.GetMasterVolumeLevel()
    volume.SetMasterVolumeLevel(-48.0, None)

    # Kill all running applications
    os.system("pkill -f")
    # subprocess.Popen("TASKKILL /F /IM chrome.exe 2> nul", shell=True)

    # Play audio
    audio = subprocess.Popen(["wmplayer.exe", audio_file])

def switch_off():
    print("Alarm deactivated")

while True:
    myData = ''
    if (arduinoSerialData.inWaiting()>0):
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
            
        i = 0
        while i < 112:
            playsound('emergency-alarm-with-reverb-29431.mp3')
            i += 1
        break
