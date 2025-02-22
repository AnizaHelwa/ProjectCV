import cv2

face_ref = cv2.CascadeClassifier("face_ref.xml")
camera = cv2.VideoCapture(0)

def face_detection(frame):
    optimized_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_ref.detectMultiScale(optimized_frame, scaleFactor=1.1, minNeighbors=5)
    return faces

def drawer_box(frame):
    for x, y, w, h in face_detection(frame):
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 4)
    
def close_window():
    camera.release()q
    cv2.destroyAllWindows()
    # exit()
    
def main():
    while True:
        ret, frame = camera.read()
        if not ret:
            print("Error: Kamera tidak dapat diakses!")
            break
        # _, frame = camera.read()
        drawer_box(frame)
        cv2.imshow("Helwa OpenCV", frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            close_window()
            break
    
if __name__ == "__main__":
    main()