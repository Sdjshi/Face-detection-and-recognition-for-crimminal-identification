import bcrypt
from email import message
from logging import root
from tkinter import *
from tkinter import font
import time

import mysql.connector


def register():
    pass1 = password1.get()
    pass2 = password2.get()

    if pass1 == pass2:
        mydb = mysql.connector.connect(
            host='localhost',
            user="root",
            passwd='',
            database="face"
        )
        encoded_pass = pass1.encode("utf-8")

        hashed = bcrypt.hashpw(encoded_pass, bcrypt.gensalt(10))


        mycursor = mydb.cursor()
        sql = "insert into officerdetails (OfficerName, OfficerID, UserID, Passwords) values(%s, %s, %s, %s)"
        val = (name.get(), officerid.get(), username.get(), hashed)

        mycursor.execute(sql, val)
        mydb.commit()
        message.set("Registration Successfull")





    else:
        if pass1 != pass2:
            message.set("Different Passwords")






def registration_form():
    root = Tk()

    root.geometry("300x350")

    root.title("Registration form")

    global message;
    global username
    global password1
    global password2
    global name
    global officerid

    username = StringVar()
    name = StringVar()
    officerid = StringVar()
    password1 = StringVar()
    password2 = StringVar()
    message = StringVar()

    Label(root, width="300", text="Register your details below", bg="red", fg="white").pack()

    Label(root, text="Name *").place(x=20, y=40)

    Entry(root, textvariable=name).place(x=140, y=42)

    Label(root, text="OfficerID *").place(x=20, y=80)
    # Username textbox
    Entry(root, textvariable=officerid).place(x=140, y=82)
    # Username Label
    Label(root, text="Username * ").place(x=20, y=120)
    # Username textbox
    Entry(root, textvariable=username).place(x=140, y=122)
    # Password Label
    Label(root, text="Password* ").place(x=20, y=160)
    # Password textbox
    Entry(root, textvariable=password1, show="*").place(x=140, y=162)

    Label(root, text="Confirm Password* ").place(x=20, y=200)
    # Password textbox
    Entry(root, textvariable=password2, show="*").place(x=140, y=202)
    # Label for displaying login status[success/failed]
    Label(root, text="", textvariable=message).place(x=95, y=220)
    # Login button
    Button(root, text="Register", width=10, height=1, bg="orange", command=register).place(x=105, y=250)

    Button(root, text="Exit", width=10, height=1, bg="red", fg='white', command=quit).place(x=105, y=290)



    root.mainloop()


registration_form()