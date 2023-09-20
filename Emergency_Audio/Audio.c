#include <stdio.h>
#include <string.h>
#include <windows.h>
#include <mmsystem.h> 
#include <mmdeviceapi.h>
#include <audioclient.h>
#include <playsoundapi.h>
#include <psapi.h>
#include <tlhelp32.h>

#define MAX_BUFFER_SIZE 255

char* alarm_sound = "emergency-alarm-with-reverb-29431.mp3";

void stopChrome() {
    HWND h = FindWindow(NULL, "Google Chrome");
    if (h) {
        PostMessage(h, WM_CLOSE, 0, 0);
    }
}

void setMasterVolume(float level) {
    IMMDeviceEnumerator* enumerator = NULL;
    IMMDevice* speakers = NULL;
    IAudioEndpointVolume* endpointVolume = NULL;

    CoInitialize(NULL);
    CoCreateInstance(&CLSID_MMDeviceEnumerator, NULL, CLSCTX_ALL, &IID_IMMDeviceEnumerator, (void**)&enumerator);
    enumerator->lpVtbl->GetDefaultAudioEndpoint(enumerator, eRender, eMultimedia, &speakers);
    speakers->lpVtbl->Activate(speakers, &IID_IAudioEndpointVolume, CLSCTX_ALL, NULL, (void**)&endpointVolume);
    endpointVolume->lpVtbl->SetMasterVolumeLevelScalar(endpointVolume, level, NULL);
    endpointVolume->lpVtbl->Release(endpointVolume);
    speakers->lpVtbl->Release(speakers);
    enumerator->lpVtbl->Release(enumerator);
    CoUninitialize();
}

int isChromeOpen() {
    HANDLE hSnapshot;
    PROCESSENTRY32 pe;
    int found = 0;

    hSnapshot = CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0);
    pe.dwSize = sizeof(PROCESSENTRY32);
    if (Process32First(hSnapshot, &pe)) {
        do {
            if (strcmp(pe.szExeFile, "chrome.exe") == 0) {
                found = 1;
                break;
            }
        } while (Process32Next(hSnapshot, &pe));
    }
    CloseHandle(hSnapshot);
    return found;
}

int main() {
    HANDLE arduinoSerialData = CreateFile("COM3", GENERIC_READ | GENERIC_WRITE, 0, NULL, OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, NULL);

    if (arduinoSerialData == INVALID_HANDLE_VALUE) {
        printf("Error opening COM port\n");
        return 1;
    }

    DCB serialParams = { 0 };
    serialParams.DCBlength = sizeof(DCB);

    if (!GetCommState(arduinoSerialData, &serialParams)) {
        printf("Error getting COM port state\n");
        CloseHandle(arduinoSerialData);
        return 1;
    }

    serialParams.BaudRate = 9600;

    if (!SetCommState(arduinoSerialData, &serialParams)) {
        printf("Error setting COM port state\n");
        CloseHandle(arduinoSerialData);
        return 1;
    }

    BOOL alarm_playing = FALSE;
    char myData[MAX_BUFFER_SIZE];

    while (1) {
        DWORD bytesRead;
        if (ReadFile(arduinoSerialData, myData, sizeof(myData), &bytesRead, NULL) && bytesRead > 0) {
            myData[bytesRead] = '\0';
            printf("%s", myData);

            if (strcmp(myData, "Switch: ON\r\n") == 0) {
                int isOpen = isChromeOpen();
                if (isOpen) {
                    stopChrome();
                }

                setMasterVolume(0.0f);

                if (!alarm_playing) {
                    PlaySound(alarm_sound, NULL, SND_FILENAME | SND_ASYNC);
                    alarm_playing = TRUE;
                }
            }
            else if (strcmp(myData, "Switch: OFF\r\n") == 0) {
                if (alarm_playing) {
                    alarm_playing = FALSE;
                    PlaySound(NULL, 0, 0);
                }
            }
        }
    }

    CloseHandle(arduinoSerialData);
    return 0;
}   