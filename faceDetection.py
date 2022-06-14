from tkinter import *

import bcrypt
import cv2
import mysql.connector


def login():
    uname = username.get()
    pwd = password.get()

    mydb = mysql.connector.connect(
        host='localhost',
        user='root',
        passwd='',
        database='face'
    )

    mycursor = mydb.cursor()
    mycursor.execute("select Passwords from officerdetails where UserID=%s", (uname,))
    s = mycursor.fetchone()
    s = ''+''.join(s)

    if bcrypt.checkpw(pwd.encode('utf-8'),s.encode('utf-8')):
        message.set("Login Successful")

        root = Tk()

        root.geometry("775x500")
        root.resizable(0,0)


        root.title("Criminal Identification System")

        # global idvalue
        # global namevalue
        # global agevalue
        # global offencevalue
        # global addressvalue
        # global officerNamevalue
        # global dateofarrestvalue

        idvalue = StringVar()
        namevalue = StringVar()
        offencevalue = StringVar()
        agevalue = StringVar()
        addressvalue = StringVar()
        dateofarrestvalue = StringVar()
        officerNamevalue = StringVar()
        # checkboxvalue=IntVar()

        mydb = mysql.connector.connect(
            host='localhost',
            user='root',
            passwd='0000',
            database='Records'
        )

        mycursor = mydb.cursor()
        mycursor.execute("Select * from criminaldetails")
        myresult = mycursor.fetchall()

        id=1000
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
        Entry(root, textvariable=namevalue).place(x=180, y=80)
        Entry(root, textvariable=agevalue).place(x=180, y=120)
        Entry(root, textvariable=addressvalue).place(x=180, y=160)
        Entry(root, textvariable=offencevalue).place(x=180, y=200)
        Entry(root, textvariable=dateofarrestvalue).place(x=180, y=280)
        Entry(root, textvariable=officerNamevalue).place(x=180, y=240)





        Button(root, text="Train Datasets", width=25, height=1, bg="orange").place(x=25,y=340)


        def generate_dataset():
            mydb= mysql.connector.connect(
                host='localhost',
                user="root",
                passwd='0000',
                database="Records"
            )

            mycursor= mydb.cursor()
            mycursor.execute("Select * from criminaldetails")
            myresult = mycursor.fetchall()

            id = 1000

            for x in myresult:
                id += 1

            sql= "insert into criminaldetails (Id, CriminalName, Age, Address, Offence, Officer, DateOfArrest) values(%s,%s,%s,%s, %s, %s, %s)"
            val= (str(id), namevalue.get(), agevalue.get(), addressvalue.get(), offencevalue.get(),officerNamevalue.get(), dateofarrestvalue.get(),)

            mycursor.execute(sql,val)
            mydb.commit()



            face_classifier = cv2.CascadeClassifier ("haarcascade_frontalface_default.xml")
            def face_cropped(img):
              gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
              faces = face_classifier.detectMultiScale(gray,1.3,5)
               #scaling factor=1.3
               #minimum neighbor=5

              if faces is ():
                 return None
              for(x,y,w,h) in faces:
                cropped_face=img[y:y+h,x:x+w]
              return cropped_face

            cap = cv2.VideoCapture(0)
            id=1
            img_id=0

            while True:
                ret,frame = cap.read()
                if face_cropped(frame) is not None:
                    img_id+=1
                    face = cv2.resize(face_cropped(frame),(200,200))
                    face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
                    file_name_path ="data/user."+str(id)+"."+str(img_id)+".jpg"
                    cv2.imwrite(file_name_path,face)
                    cv2.putText(face,str(img_id),(50,50),cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
                    #(50,50) is the origin point from where text is to be written
                    #font scale=1
                    #thickness=2

                    cv2.imshow("Cropped face",face)
                    if cv2.waitKey(1)==13 or int(img_id)==400:
                        break
            cap.release()
            cv2.destroyAllWindows()
            print("Collecting samples is completed.....")
        #generate_dataset()

        Button(root, text="Generate Datasets", width=25, height=1, bg="orange",command=generate_dataset).place(x=255,y=340)



        Button(root, text="Live Detection", width=25, height=1, bg="orange").place(x=25, y=380)
        Button(root, text="Generate Report", width=25, height=1, bg="orange").place(x=255, y=380)

               # Checkbutton(root, text="Do you want to save details?", textvariable=checkboxvalue).place(x=180,y=360)

        Button(root, text="Exit", bg="red", width=10, height=1, command=quit).place(x=200, y=450)


        canvas = Canvas(root, width='280', height='260', bg='sky blue').place(x=450, y=40)

        root.mainloop()


def Loginform():
    global login_screen
    login_screen = Tk()
    # Setting title of screen
    login_screen.title("Login Form")
    # setting height and width of screen
    login_screen.geometry("300x250")
    # declaring variable
    global message;
    global username
    global password
    username = StringVar()
    password = StringVar()
    message = StringVar()

    # Creating layout of login form
    Label(login_screen, width="300", text="Please enter details below", bg="red", fg="white").pack()
    # Username Label
    Label(login_screen, text="Username * ").place(x=20, y=40)
    # Username textbox
    Entry(login_screen, textvariable=username).place(x=90, y=42)
    # Password Label
    Label(login_screen, text="Password * ").place(x=20, y=80)
    # Password textbox
    Entry(login_screen, textvariable=password, show="*").place(x=90, y=82)
    # Label for displaying login status[success/failed]
    Label(login_screen, text="", textvariable=message).place(x=95, y=100)
    # Login button
    Button(login_screen, text="Login", width=10, height=1, bg="orange", command=login).place(x=105, y=130)

    Button(login_screen, text="Exit", width=10, height=1, bg="red", fg='white', command=quit).place(x=105, y=170)

    login_screen.mainloop()


# calling function Loginform
Loginform()



