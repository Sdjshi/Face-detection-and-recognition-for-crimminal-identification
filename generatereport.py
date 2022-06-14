from tkinter import Canvas
from tkinter import *
import cv2
from PIL import Image, ImageTk
import mysql.connector
def generate_report():
    canvas = Canvas(root, width='280', height='260', bg='sky blue').place(x=450, y=40)

    cap = cv2.Videocapture(0)
    if cap.isOpened():
        ret, frame = cap.read()
    else:
        ret = False

    face_classifier = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
   
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(gray, 1.3, 5)

    #scaling factor =1.3
    #minimum neighbour =5


    if faces is ():
        print("No face Detected")
        return None
    else:
        for (x,y,w,h) in faces:
            cropped_face = frame[y:y+h, x:x+w]
        cv2.imwrite("Captured_image.jpg", cropped_face)

        load = Image.open("Captured_image.jpg")
        photo = ImageTk.PhotoImage(load)

        #labels can be text or image

        img = Label(canvas, image=photo, width=200, height=200)
        img.image = photo
        
        img.place(x=0, y=40)

        cap.release()

    clf = cv2.face.LBPHFaceRecognizer_create()
    clf.read("classifier.xml")

    for (x,y,w,h) in faces:
        id, pred = clf.predict(gray[y:y+h,x:x+w])
        confidence = int(100*(1-pred/300))

        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd='',
            database= "face"
        )

        mycursor = mydb.cursor()

        mycursor.execute("Select Name, Age, Address, Offence, Officer, Date from criminalDetails where id=" + str(id))

        s = mycursor.fetchall()

        Label(canvas, text="Name :").place(x, y)
        Label(canvas, text=s[0][1]).place(x,y)

        Label(canvas, text="Age :").place(x,y)
        Label(canvas, text=s[0][2]).place(x,y)

        Label(canvas, text="Address :").place(x,y)
        Label(canvas, text=s[0][3]).place(x,y)

        Label(canvas, text=s[0][1]).place(x,y)

        Label(canvas, text="has been arrested for the offence").place(x,y)
        Label(canvas, text=s[0][4]).place(x,y)

        Label(canvas, text='by officer').place(x,y)
        Label(canvas, text=s[0][5]).place(x,y)

        Label(canvas, text="on the day").place(x,y)
        Label(canvas, text=s[0][6]).place(x,y)



        
