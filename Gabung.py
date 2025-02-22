import cv2
import time
import numpy as np
import HandTrackingModule as htm
import mediapipe as mp
import math
import os
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# Menginisialisasi Face Detection
face_ref = cv2.CascadeClassifier("face_ref.xml")

# Camera settings
# Mengaatur ukuran camera
wCam, hCam = 640, 480

# Inisialisasi kamera
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

# Initialize hand detector --> mendeteksi tangan
detector = htm.handDetector(detectionCon=0.7)

# Mengakses pengaturan audio
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)
volRange = volume.GetVolumeRange()

# Batasan Volume
minVol = volRange[0]
maxVol = volRange[1]

# Nilai awal volume
# Karena pada bar atau kotak angka terendahnya adalah 400 maka nilai awal itu 400 = 0
vol, volBar, volPer = 0, 400, 0

# digunakan untuk mengakses gambar yang ada dalam folder ImageFingers
folderPath = "ImageFingers"
myList = os.listdir(folderPath)
overlayList = [cv2.imread(f'{folderPath}/{imPath}') for imPath in myList]

# Kode atau angka untuk tiap ujung jari
tipIds = [4, 8, 12, 16, 20]
pTime = 0

def face_detection(frame):
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_ref.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5)
    return faces

def draw_face_box(frame):
    for x, y, w, h in face_detection(frame):
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 4)

def control_volume(img, lmList):
    global vol, volBar, volPer
    if len(lmList) != 0:
        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

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
        cv2.putText(img, f'Volume: {int(volPer)}%', (40, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 3)

def count_fingers(img, lmList):
    if len(lmList) != 0:
        fingers = []
        # Digunakan untuk jempol karena ketika menutup tangan angka dari jempol tetap terdeteksi
        if lmList[tipIds[0]][1] > lmList[tipIds[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)
        # fingers.append(1 if lmList[tipIds[0]][1] > lmList[tipIds[0] - 1][1] else 0)

        # digunakan untuk range 1 sampai 5 --> jari telunjuk hingga jari kelingking
        for id in range(1, 5):
            if lmList[tipIds[id]][2] < lmList[tipIds[id]-2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        # for id in range(1, 5):
        #     fingers.append(1 if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2] else 0)


        # Angka 1 = open dan angka 0 = close
        # 1. Ketika kita menutup tangan maka nilai nya adalah [0, 0, 0, 0, 0]
        # 2. Tangan membentuk angka 1 --> [1, 0, 0, 0, 0]
        # 3. Tangan membentuk angka 2 --> [0, 1, 0, 0, 0]
        # 4. Tangan membentuk angka 3 --> [0, 0, 1, 0, 0]
        # 5. Tangan membentuk angka 4 --> [0, 0, 0, 1, 0]
        # 6. Tangan membentuk angka 5 --> [0, 0, 0, 0, 1]
        # 7. Tangan membuka --> [1, 1, 1, 1, 1]

        # Digunakan untuk menampilkan gambar yang sesuai dengan angka yang dibentuk oleh jari
        # Dihitung seberapa banyak jari yang terbuka
        totalFingers = fingers.count(1)

        # Display the frame
        # Menampilkan gambar angka 1-5
        h, w, c = overlayList[totalFingers - 1].shape
        img[0:218, 0:177] = overlayList[totalFingers - 1]

        # Ketika tangan kita terdeteksi maka akan muncul gambar dan kotak berwarna hijau yang berisi angka sesuai dengan angka yang dibentuk oleh jari tangan
        cv2.rectangle(img, (20, 255), (170, 425), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, str(totalFingers), (45, 375), cv2.FONT_HERSHEY_PLAIN, 10, (255, 0, 0), 25)

def main():
    global pTime
    while True:
        ret, img = cap.read()
        if not ret:
            print("Error: Kamera tidak dapat diakses!")
            break
        img = detector.findHands(img)
        lmList = detector.findPosition(img, draw=False)
        draw_face_box(img)
        control_volume(img, lmList)
        count_fingers(img, lmList)
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img, f'FPS: {int(fps)}', (40, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 3)
        cv2.imshow("Img", img)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            cap.release()
            cv2.destroyAllWindows()
            break

if __name__ == "__main__":
    main()
