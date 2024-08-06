from tkinter import messagebox
import subprocess
import cv2
import dlib
import numpy as np

# Load the detector
detector = dlib.get_frontal_face_detector()
# Load the predictor with the full path
predictor = dlib.shape_predictor(r'C:\Users\manid\OneDrive\Desktop\Face_recognition_With_WhatsApp_Alert-master\shape_predictor_68_face_landmarks.dat')
# Load the face recognition model with the full path
face_rec_model = dlib.face_recognition_model_v1(r'C:\Users\manid\OneDrive\Desktop\Face_recognition_With_WhatsApp_Alert-master\dlib_face_recognition_resnet_model_v1.dat')

contadorDesconocidos = 0  # To monitor alerts

# Helper function to get face encodings
def get_face_encodings(image):
    detections = detector(image, 1)
    shapes = [predictor(image, det) for det in detections]
    return [np.array(face_rec_model.compute_face_descriptor(image, shape)) for shape in shapes]

# Load known images and get encodings
known_images = [
    cv2.imread(r'C:\Users\manid\OneDrive\Desktop\Face_recognition_With_WhatsApp_Alert-master\set\one.JPG'),
    cv2.imread(r'C:\Users\manid\OneDrive\Desktop\Face_recognition_With_WhatsApp_Alert-master\set\one2.JPG'),
    cv2.imread(r'C:\Users\manid\OneDrive\Desktop\Face_recognition_With_WhatsApp_Alert-master\set\one3.JPG'),
    cv2.imread(r'C:\Users\manid\OneDrive\Desktop\Face_recognition_With_WhatsApp_Alert-master\set\one4.JPG'),
    cv2.imread(r'C:\Users\manid\OneDrive\Desktop\Face_recognition_With_WhatsApp_Alert-master\set\one5.JPG'),
    cv2.imread(r'C:\Users\manid\OneDrive\Desktop\Face_recognition_With_WhatsApp_Alert-master\set\one6.JPG'),
    cv2.imread(r'C:\Users\manid\OneDrive\Desktop\Face_recognition_With_WhatsApp_Alert-master\set\one7.JPG'),
    cv2.imread(r'C:\Users\manid\OneDrive\Desktop\Face_recognition_With_WhatsApp_Alert-master\set\one8.JPG'),
    cv2.imread(r'C:\Users\manid\OneDrive\Desktop\Face_recognition_With_WhatsApp_Alert-master\set\one9.JPG'),
    cv2.imread(r'C:\Users\manid\OneDrive\Desktop\Face_recognition_With_WhatsApp_Alert-master\set\one10.JPG'),
    cv2.imread(r'C:\Users\manid\OneDrive\Desktop\Face_recognition_With_WhatsApp_Alert-master\set\one11.JPG'),
    cv2.imread(r'C:\Users\manid\OneDrive\Desktop\Face_recognition_With_WhatsApp_Alert-master\set\one12.JPG')
]
known_encodings = [get_face_encodings(img)[0] for img in known_images]

nombres_encoding = ["IGNACIO"] * len(known_encodings)

# OpenCV video capture
cam = cv2.VideoCapture(1)

texto = cv2.FONT_HERSHEY_COMPLEX
reduc = 5

countR = 0

while True:
    ret_val, img = cam.read()
    if not ret_val:
        break

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_rgb = cv2.resize(img[:, :, ::-1], (0, 0), fx=1.0/reduc, fy=1.0/reduc)
    detections = detector(img_rgb, 1)
    encodings_rostros = get_face_encodings(img_rgb)

    for (i, det) in enumerate(detections):
        x, y, w, h = det.left(), det.top(), det.width(), det.height()
        nom = ""
        for encoding in encodings_rostros:
            coincidencias = [np.linalg.norm(encoding - known_encoding) < 0.6 for known_encoding in known_encodings]

            if True in coincidencias:
                nom = nombres_encoding[coincidencias.index(True)]
                contadorDesconocidos = 0
            else:
                nom = "STRANGER"
                contadorDesconocidos += 1

        if contadorDesconocidos > 5:
            subprocess.run('python WhatsappMessage.py', shell=True)
            messagebox.showinfo('ALERT', 'UNKNOWN IDENTIFIED')
            contadorDesconocidos = 0
            cv2.imwrite(f'stranger_{countR}.jpg', img)
            countR += 1
            cv2.destroyAllWindows()

        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(img, nom, (x, y - 6), texto, 0.6, (255, 255, 255), 1)

    cv2.imshow('live camera', img)   

    if cv2.waitKey(1) == 27:  # Esc to quit
        break

cv2.destroyAllWindows()
