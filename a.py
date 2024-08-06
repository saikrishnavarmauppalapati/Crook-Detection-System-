from tkinter import messagebox
import subprocess
import cv2
import face_recognition

# XML container for front faces detection algorithm
faceClassif = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

contadorDesconocidos = 0  # To monitor alerts

# Set of images for detection
image_paths = [rf'C:\Users\manid\OneDrive\Desktop\Face_recognition_With_WhatsApp_Alert-master\set\one{i}.JPG' for i in range(1, 13)]
images = [face_recognition.load_image_file(image_path) for image_path in image_paths]

encodings_personal = [face_recognition.face_encodings(image)[0] for image in images]

encoding_conocidos = encodings_personal
nombres_encoding = ["IGNACIO"] * len(encodings_personal)

# OpenCV video capture
cam = cv2.VideoCapture(1)

texto = cv2.FONT_HERSHEY_COMPLEX
reduc = 5

countR = 0

while True:
    ubi_rostro = []
    encoding_rostros = []
    nombres_rostros = []
    nom = ""
    
    ret_val, img = cam.read()
    if not ret_val:
        break

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    img_rgb = cv2.resize(img[:, :, ::-1], (0, 0), fx=1.0/reduc, fy=1.0/reduc)
    ubi_rostro = face_recognition.face_locations(img_rgb)
    encodings_rostros = face_recognition.face_encodings(img_rgb, ubi_rostro)

    faces = faceClassif.detectMultiScale(gray, 
                                         scaleFactor=1.1,
                                         minNeighbors=22,
                                         minSize=(10, 10),
                                         maxSize=(200, 200))

    for (x, y, w, h) in faces:
        for encoding in encodings_rostros:
            coincidencias = face_recognition.compare_faces(encoding_conocidos, encoding)

            if True in coincidencias:
                nom = nombres_encoding[coincidencias.index(True)]
                contadorDesconocidos = 0
            else:
                nom = "STRANGER"
                contadorDesconocidos += 1

            nombres_rostros.append(nom)

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
