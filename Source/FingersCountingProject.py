import cv2
import time
import os
import HandTrackingModule as htm


wCam, hCam = 640, 480

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

# digunakan untuk mengakses gambar yang ada dalam folder ImageFingers
folderPath = "ImageFingers"
myList = os.listdir(folderPath)
print(myList)

overlayList = []
for imPath in myList:
    image = cv2.imread(f'{folderPath}/{imPath}')
    # print(image)
    overlayList.append(image)

# Cek jumlah image yang berhasil di import
print(len(overlayList))
pTime = 0

detector = htm.handDetector(detectionCon=0.75)

# Angka ujung jari sesuai dengan ketentuan mediapipe
tipIds = [4, 8, 12, 16, 20]

# Digunakan untuk tangan kanan
while True:
    # Digunakan untuk mendeteksi tangan melalui kamera
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    print(lmList)

    if len(lmList) != 0:
        fingers = []

        # Digunakan untuk jempol karena ketika menutup tangan angka dari jempol tetap terdeteksi
        if lmList[tipIds[0]][1] > lmList[tipIds[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        # digunakan untuk range 1 sampai 5 --> jari telunjuk hingga jari kelingking
        for id in range(1, 5):
            if lmList[tipIds[id]][2] < lmList[tipIds[id]-2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        # Angka 1 = open dan angka 0 = close
        # 1. Ketika kita menutup tangan maka nilai nya adalah [0, 0, 0, 0, 0]
        # 2. Tangan membentuk angka 1 --> [1, 0, 0, 0, 0]
        # 3. Tangan membentuk angka 2 --> [0, 1, 0, 0, 0]
        # 4. Tangan membentuk angka 3 --> [0, 0, 1, 0, 0]
        # 5. Tangan membentuk angka 4 --> [0, 0, 0, 1, 0]
        # 6. Tangan membentuk angka 5 --> [0, 0, 0, 0, 1]
        # 7. Tangan membuka --> [1, 1, 1, 1, 1]
        # print(fingers)

        # Digunakan untuk menampilkan gambar yang sesuai dengan angka yang dibentuk oleh jari
        # Dihitung seberapa banyak jari yang terbuka
        totalFIngers = fingers.count(1)
        print(totalFIngers)

        # Display the frame
        # Menampilkan gambar angka 1-5
        h, w, c = overlayList[totalFIngers-1].shape
        img[0:218, 0:177] = overlayList[totalFIngers-1]

        # Ketika tangan kita terdeteksi maka akan muncul gambar dan kotak berwarna hijau yang berisi angka sesuai dengan angka yang dibentuk oleh jari tangan
        cv2.rectangle(img, (20, 255), (170, 425), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, str(totalFIngers), (45, 375), cv2.FONT_HERSHEY_PLAIN, 10, (255, 0, 0), 25)


    cTime = time.time()
    fps = 1/(cTime - pTime)
    # Update
    pTime = cTime

    cv2.putText(img, f'FPS: {int(fps)}', (400, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

    cv2.imshow('Image', img)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()