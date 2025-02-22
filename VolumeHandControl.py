import cv2
import time
import numpy as np
import HandTrackingModule as htm
import mediapipe as mp
import math
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

#####
wCam, hCam = 640, 480
#####

cap = cv2.VideoCapture(0)

cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0

detector = htm.handDetector(detectionCon=0.7)


devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)
# volume.GetMute()
# volume.GetMasterVolumeLevel()

# Digunakan untuk mendapatkan range volume
volRange = volume.GetVolumeRange()

# Batasan volume
minVol = volRange[0]
maxVol = volRange[1]

# Nilai awal
vol = 0
volBar = 400 # Karena pada bar atau kotak angka terendahnya adalah 400 maka nilai awal itu 400 = 0
volPer = 0

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    # Mendapatkan data nomor 4 (untuk ujung jempol) dan 8 (untuk ujung telunjuk)
    if len(lmList) != 0:
        #print(lmList[4], lmList[8])

        x1, y1 =lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        cx, cy = (x1+x2)//2, (y1+y2)//2

        # Digunakan untuk menandai ujung jempol dan telunjuk dengan bulatan
        cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (x2, y2), 15, (255, 0, 255), cv2.FILLED)

        # Digunakan untuk membuat garis yang menghubungkan antara ujung jempol dan telunjuk
        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)

        # Digunakan untuk mendapatkan lingkaran atau circle di antara dua circle yang berada di jempol dan telunjuk
        cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)

        # Digunakan untuk mengetahui selisih jarak antara ujung jempol dan ujung telunjuk
        length = math.hypot(x2 - x1, y2 - y1)
        # print(length)

        # Hand range dari 50 to 300
        # Konversi hand range ke volume range
        # Volume range -65 to 0
        vol = np.interp(length, [50, 300], [minVol, maxVol])
        volBar = np.interp(length, [50, 300], [400, 150])
        volPer = np.interp(length, [50, 300], [0, 100])
        print(int(length), vol)
        volume.SetMasterVolumeLevel(vol, None)

        # Ketika ujung telunjuk didekatkan dengan ujung jempol maka volume akan berkurang begitu juga sebaliknya
        # Min length = -65,...
        # Max length = 0.00

        # Apabila panjang atau length kurang dari 50 maka akan muncul lingkaran dengan warna hijau
        if length < 50:
            cv2.circle(img, (cx, cy), 15, (0, 255, 0), cv2.FILLED)

    # Digunakan untuk menampilkan bar warna biru dan angka dalam %
    cv2.rectangle(img, (50, 150), (85, 480), (255, 0, 0), 3)
    cv2.rectangle(img, (50, int(volBar)), (85, 480), (255, 0, 0), cv2.FILLED)
    cv2.putText(img, f'FPS: {int(volPer)} %', (40, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 3)

    cTime = time.time()
    fps = 1 / (cTime-pTime)
    pTime = cTime

    cv2.putText(img, f'FPS: {int(fps)}', (40, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 3)

    cv2.imshow("Img", img)
    cv2.waitKey(1)
