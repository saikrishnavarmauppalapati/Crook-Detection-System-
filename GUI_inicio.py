from tkinter import *
import subprocess

#_____________________CAMERA START FUNCTION____________________________________
def onclick():
    subprocess.run(r'python C:\Users\manid\OneDrive\Desktop\Face_recognition_With_WhatsApp_Alert-master\Det_Camara.py', shell=True)

window=Tk()

#_____________________GUI________________________________________________________
btn=Button(window, text="Face recognition", fg='blue', command=onclick)
btn.place(x=80, y=100)
lbl=Label(window, text="Administrador", fg='red', font=("Helvetica", 16))
lbl.place(x=80, y=50)
window.title('Image')
window.geometry("300x200+600+100")
window.mainloop()