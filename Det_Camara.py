from tkinter import messagebox
import subprocess
import cv2
import face_recognition # type: ignore
#import pymysql

#______________XML CONTAINER FOR FRONT FACES DETECTION ALGORITHM________________
faceClassif = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
#_____________________________________________________________________________________

contadorDesconocidos = 0 #To monitor alerts

#___________________SET OF IMAGES FOR DETECTION__________________________________
imagen_yo = face_recognition.load_image_file(r'C:\Users\manid\OneDrive\Desktop\Face_recognition_With_WhatsApp_Alert-master\set\one.JPG')
imagen_yo2 = face_recognition.load_image_file(r'C:\Users\manid\OneDrive\Desktop\Face_recognition_With_WhatsApp_Alert-master\set\one2.JPG')
imagen_yo3 = face_recognition.load_image_file(r'C:\Users\manid\OneDrive\Desktop\Face_recognition_With_WhatsApp_Alert-master\set\one3.JPG')
imagen_yo4 = face_recognition.load_image_file(r'C:\Users\manid\OneDrive\Desktop\Face_recognition_With_WhatsApp_Alert-master\set\one4.JPG')

imagen_yo5 = face_recognition.load_image_file(r'C:\Users\manid\OneDrive\Desktop\Face_recognition_With_WhatsApp_Alert-master\set\one5.JPG')
imagen_yo6 = face_recognition.load_image_file(r'C:\Users\manid\OneDrive\Desktop\Face_recognition_With_WhatsApp_Alert-master\set\one6.JPG')
imagen_yo7 = face_recognition.load_image_file(r'C:\Users\manid\OneDrive\Desktop\Face_recognition_With_WhatsApp_Alert-master\set\one7.JPG')
imagen_yo8 = face_recognition.load_image_file(r'C:\Users\manid\OneDrive\Desktop\Face_recognition_With_WhatsApp_Alert-master\set\one8.JPG')
imagen_yo9 = face_recognition.load_image_file(r'C:\Users\manid\OneDrive\Desktop\Face_recognition_With_WhatsApp_Alert-master\set\one9.JPG')
imagen_yo10 = face_recognition.load_image_file(r'C:\Users\manid\OneDrive\Desktop\Face_recognition_With_WhatsApp_Alert-master\set\one10.JPG')
imagen_yo11 = face_recognition.load_image_file(r'C:\Users\manid\OneDrive\Desktop\Face_recognition_With_WhatsApp_Alert-master\set\one11.JPG')
imagen_yo12 = face_recognition.load_image_file(r'C:\Users\manid\OneDrive\Desktop\Face_recognition_With_WhatsApp_Alert-master\set\one12.JPG')

encoding_personal = face_recognition.face_encodings(imagen_yo)[0]
encoding_personal1 = face_recognition.face_encodings(imagen_yo2)[0]
encoding_personal2 = face_recognition.face_encodings(imagen_yo3)[0]
encoding_personal3 = face_recognition.face_encodings(imagen_yo4)[0]
encoding_personal4 = face_recognition.face_encodings(imagen_yo5)[0]
encoding_personal5 = face_recognition.face_encodings(imagen_yo6)[0]
encoding_personal6 = face_recognition.face_encodings(imagen_yo7)[0]
encoding_personal7 = face_recognition.face_encodings(imagen_yo8)[0]
encoding_personal8 = face_recognition.face_encodings(imagen_yo9)[0]
encoding_personal9 = face_recognition.face_encodings(imagen_yo10)[0]
encoding_personal10 = face_recognition.face_encodings(imagen_yo11)[0]
encoding_personal11 = face_recognition.face_encodings(imagen_yo12)[0]

encoding_conocidos = [
    encoding_personal,
    encoding_personal1,
    encoding_personal2,
    encoding_personal3,
    encoding_personal4,
    encoding_personal5,
    encoding_personal6,
    encoding_personal7,
    encoding_personal8,
    encoding_personal9,
    encoding_personal10,
    encoding_personal11,
]
nombres_encoding = [
    "IGNACIO",
    "IGNACIO",
    "IGNACIO",
    "IGNACIO",
    "IGNACIO",
    "IGNACIO",
    "IGNACIO",
    "IGNACIO",
    "IGNACIO",
    "IGNACIO",
    "IGNACIO",
    "IGNACIO"
]
#____________________________________________________________________

#_____________________CODE FOR MYSQL______________________________
#____________________________________________________________________



#_______________________OPENCV VIDEO CAPTURE_______________________
cam = cv2.VideoCapture(1)


texto = cv2.FONT_HERSHEY_COMPLEX
reduc = 5

countR = 0

while True:

    #__FOR FACE RECOGNITION____________________________________
    ubi_rostro = []
    encoding_rostros = []
    nombres_rostros = []
    nom = ""
    #_________________________________________________________________
    
    ret_val, img = cam.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    if ret_val:

        #_______________________HANDLING DOES NOT AFFECT DETECTION_______
        img_rgb = img[:, :, ::-1]
        img_rgb = cv2.resize(img_rgb, (0, 0), fx=1.0/reduc, fy=1.0/reduc)
        #________________________________________________________________

        ubi_rostro = face_recognition.face_locations(img_rgb)
        encodings_rostros = face_recognition.face_encodings(img_rgb, ubi_rostro)

        #______________________MANIPULATE THE QUALITY OF THE DETECTION________
        faces = faceClassif.detectMultiScale(gray, 
            scaleFactor=1.1,
            minNeighbors=22,
            minSize=(10,10),
            maxSize=(200,200))
        #___________________________________________________________________
        

        for (x,y,w,h) in faces:

            #___________________________KNOWN FACE FINDERS_______________
            for encoding in encodings_rostros:
                coincidencias = face_recognition.compare_faces(encoding_conocidos, encoding)

                if True in coincidencias:
                    nom = nombres_encoding[coincidencias.index(True)]

                    contadorDesconocidos = 0
                else:
                    nombre = "STRANGER"
                    contadorDesconocidos+=1
                nombres_rostros.append(nom)
            #_____________________INTRUDER ALERTS______________________________________
            if contadorDesconocidos>5:
                subprocess.run('python WhatsappMessage.py', shell=True)
                messagebox.showinfo('ALERT', 'UNKNOWN IDENTIFIED')
                contadorDesconocidos = 0
                cv2.imwrite('stranger_{}.jpg'.format(countR), img)
                countR+=1
                cv2.destroyAllWindows()

            #_______________________RECTANGLE AND NAME___________________________________
            cv2.rectangle(img,(x,y),(x+w,y+h),(0, 255, 0),2)
            cv2.putText(img, nom, (x, y - 6), texto, 0.6, (255,255,255), 1)

    cv2.imshow('live camera', img)   

    if cv2.waitKey(1) == 27:  
        break  # Esc to quit    
cv2.destroyAllWindows()