from tkinter import *
import mysql.connector
import bcrypt
import cv2
import numpy as np
from PIL import Image,ImageTk
import os

import time



def funccall():
    root = Tk()

    root.geometry("500x500")
    root.resizable(0, 0)

    root.title("Criminal Identification System")



    mydb = mysql.connector.connect(
        host='localhost',
        user='root',
        passwd='',
        database='face'
    )

    mycursor = mydb.cursor()
    mycursor.execute("Select * from criminaldetails")
    myresult = mycursor.fetchall()

    id = 1000
    for x in myresult:
        id += 1

    Label(root, width=445, text="Criminal Identification System", bg='red', font="comicsansm 15 bold").pack()

    Label(root, text="Id").place(x=20, y=40)
    Label(root, text="Name").place(x=20, y=80)
    Label(root, text="Age").place(x=20, y=120)
    Label(root, text="Address").place(x=20, y=160)
    Label(root, text="Offence").place(x=20, y=200)
    Label(root, text="DateofArrest").place(x=20, y=280)
    Label(root, text="OfficerName").place(x=20, y=240)


    Label(root, text=f"{id}").place(x=180, y=40)

    namevalue=Entry(root)
    namevalue.place(x=180, y=80)

    agevalue=Entry(root)
    agevalue.place(x=180, y=120)

    addressvalue=Entry(root)
    addressvalue.place(x=180, y=160)

    offencevalue=Entry(root)
    offencevalue.place(x=180, y=200)

    dateofarrestvalue=Entry(root)
    dateofarrestvalue.place(x=180, y=280)

    officerNamevalue=Entry(root)
    officerNamevalue.place(x=180, y=240)

    Button(root, text="Train Datasets", width=25, height=1, bg="orange",command=train).place(x=25, y=340)


    def generate_report():

        def draw_boundary(img, classifier, scaleFactor, minNeighbors, color, text, clf):
            gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            features = classifier.detectMultiScale(gray_img, scaleFactor, minNeighbors)

            for (x, y, w, h) in features:
                cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)

                id, pred = clf.predict(gray_img[y:y + h, x:x + w])
                confidence = int(100 * (1 - pred / 300))

                mydb = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    passwd="",
                    database="face"
                )
                mycursor = mydb.cursor()
                mycursor.execute("select Criminalname from criminaldetails where id=" + str(id))
                s = mycursor.fetchone()
                s = "+".join(s)

                if confidence > 75:

                    cv2.putText(img, s, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 1, cv2.LINE_AA)
                    cv2.putText(img, f"{id}", (x, y - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 3, cv2.LINE_AA)

                    time.sleep(2)

                    def rpt():
                        win = Tk()
                        win.geometry("390x390")
                        win.title("Criminal Details")
                        win.resizable(0, 0)

                        Label(win, text="Report Generation", width=300, bg='red', fg='white').pack()

                        mydb = mysql.connector.connect(
                            host="localhost",
                            user="root",
                            passwd="",
                            database="face"
                        )
                        mycursor = mydb.cursor()
                        mycursor.execute(
                            "select CriminalName,Age,Address,Offence,Officer,DateOfArrest from criminaldetails where id=" + str(
                                id))
                        s = mycursor.fetchall()
                        # canvas=Canvas(width=200,height=200).place(x=195,y=0)
                        # imagi=PhotoImage(file="data/user." + str(id) + "." +f"{50}" + ".jpg")
                        # canvas.create_image(image=imagi)

                        Label(win, text="Name :").place(x=0, y=120)
                        Label(win, text=s[0][0]).place(x=100, y=120)

                        Label(win, text="Age :").place(x=0, y=160)
                        Label(win, text=s[0][1]).place(x=100, y=160)

                        Label(win, text="Address :").place(x=0, y=200)
                        Label(win, text=s[0][2]).place(x=100, y=200)

                        Label(win, text="Offence :").place(x=0, y=240)
                        Label(win, text=s[0][3]).place(x=100, y=240)

                        Label(win, text="Officer :").place(x=0, y=280)
                        Label(win, text=s[0][4]).place(x=100, y=280)

                        Label(win, text="Date of Arrest :").place(x=0, y=320)
                        Label(win, text=s[0][5]).place(x=100, y=320)

                        win.mainloop()

                    rpt()





                else:
                    cv2.putText(img, "UNKNOWN", (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 1, cv2.LINE_AA)

            return img

            # loading classifier

        faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

        clf = cv2.face.LBPHFaceRecognizer_create()
        clf.read("clasifier.xml")

        video_capture = cv2.VideoCapture(1)

        while True:
            ret, img = video_capture.read()
            img = draw_boundary(img, faceCascade, 1.3, 6, (255, 255, 255), "Face", clf)
            cv2.imshow("face Detection", img)

            if cv2.waitKey(1) == 13:
                break
        video_capture.release()
        cv2.destroyAllWindows()

    def generate_dataset():
        mydb = mysql.connector.connect(
            host='localhost',
            user="root",
            passwd='',
            database="face"
        )

        mycursor = mydb.cursor()
        mycursor.execute("Select * from criminaldetails")
        myresult = mycursor.fetchall()

        id = 1000

        for x in myresult:
            id += 1

        sql = "insert into criminaldetails (Id, CriminalName, Age, Address, Offence, Officer, DateOfArrest) values(%s,%s,%s,%s, %s, %s, %s)"
        val = (str(id), namevalue.get(), agevalue.get(), addressvalue.get(), offencevalue.get(), officerNamevalue.get(),dateofarrestvalue.get(),)

        mycursor.execute(sql, val)
        mydb.commit()

        face_classifier = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

        def face_cropped(img):
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_classifier.detectMultiScale(gray, 1.3, 5)
            # scaling factor=1.3
            # minimum neighbor=5

            if faces is ():
                return None
            for (x, y, w, h) in faces:
                cropped_face = img[y:y + h, x:x + w]
            return cropped_face

        cap = cv2.VideoCapture(1)
        id = str(id)
        img_id = 0

        while True:
            ret, frame = cap.read()
            if face_cropped(frame) is not None:
                img_id += 1
                face = cv2.resize(face_cropped(frame), (200, 200))
                face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
                file_name_path = "data/user." + str(id) + "." + str(img_id) + ".jpg"
                cv2.imwrite(file_name_path, face)
                cv2.putText(face, str(img_id), (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
                # (50,50) is the origin point from where text is to be written
                # font scale=1
                # thickness=2

                cv2.imshow("Cropped face", face)
                if cv2.waitKey(1) == 13 or int(img_id) == 400:
                    break
        cap.release()
        cv2.destroyAllWindows()
        print("Report Generated")

    # generate_dataset()

    Button(root, text="Generate Datasets", width=25, height=1, bg="orange", command=generate_dataset).place(x=255,
                                                                                                            y=340)

    Button(root, text="Live Detection", width=25, height=1, bg="orange" ,command = live_det).place(x=25, y=380)
    Button(root, text="Generate Report", width=25, height=1, bg="orange",command=generate_report).place(x=255, y=380)

    Button(root, text="Exit", bg="red", width=10, height=1, command=quit).place(x=200, y=450)
    # canvas = Canvas(root, width='280', height='260', bg='sky blue').place(x=450, y=40)
    root.mainloop()
def live_det():

    def draw_boundary(img, classifier, scaleFactor, minNeighbors, color, text, clf):
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        features = classifier.detectMultiScale(gray_img, scaleFactor, minNeighbors)

        for (x, y, w, h) in features:
            cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)

            id, pred = clf.predict(gray_img[y:y + h, x:x + w])
            confidence = int(100 * (1 - pred / 300))
            print(confidence)

            mydb = mysql.connector.connect(
                host= "localhost",
                user="root",
                passwd="",
                database="face"
            )
            mycursor = mydb.cursor()
            mycursor.execute("select Criminalname from criminaldetails where id="+str(id))
            s=mycursor.fetchone()
            s="+".join(s)

            if confidence > 75:

                cv2.putText(img, s, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,255), 2, cv2.LINE_AA)
                #cv2.putText(img, f"{id}", (x, y - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 3, cv2.LINE_AA)

            else:
                cv2.putText(img, "UNKNOWN", (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 1, cv2.LINE_AA)

        return img

    # loading classifier
    faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

    clf = cv2.face.LBPHFaceRecognizer_create()
    clf.read("clasifier.xml")

    video_capture = cv2.VideoCapture(1)

    while True:
        ret, img = video_capture.read()
        img = draw_boundary(img, faceCascade, 1.3, 6, (255, 255, 255), "Face", clf)
        cv2.imshow("face Detection", img)

        if cv2.waitKey(1) == 13:
            break
    video_capture.release()
    cv2.destroyAllWindows()



def train():
    def train_classifier(data_dir):
        path = [os.path.join(data_dir, f) for f in os.listdir(data_dir)]
        faces = []
        ids = []
        for image in path:
            img = Image.open(image).convert('L')
            imageNp = np.array(img, 'uint8')
            id = int(os.path.split(image)[1].split(".")[1])

            faces.append(imageNp)
            ids.append(id)
        ids = np.array(ids)

        # train the clssifier and save
        clf = cv2.face.LBPHFaceRecognizer_create()
        clf.train(faces, ids)
        clf.write("clasifier.xml")

    train_classifier("data")