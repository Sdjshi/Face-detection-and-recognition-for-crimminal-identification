from tkinter import *
import bcrypt
from guianddetection import funccall
import mysql.connector




#defining login function
def login():
    #getting form data
    uname = username.get()
    pwd = password.get()

    mydb = mysql.connector.connect(
        host='localhost',
        user="root",
        passwd='',
        database="face"
    )
    #val = eval(username.get())  #string to tuple
    #print(val)

    mycursor = mydb.cursor()
    mycursor.execute("select Passwords from officerdetails where UserID=%s" , (uname, ))
    s= mycursor.fetchone()
    s=''+''.join(s) #tuple to string


    if bcrypt.checkpw(pwd.encode('utf-8'), s.encode('utf-8')):
        message.set("Login Successfull")

        funccall()

    else:
        message.set("Wrong password ")




    #else:
        #message.set("Incorrect Password")



    #applying empty validation




def Loginform():
    global login_screen
    login_screen = Tk()
    # Setting title of screen
    login_screen.title("Login Form")
    # setting height and width of screen
    login_screen.geometry("300x250")
    # declaring variable
    global message
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

    #Button(login_screen, text="Sign Up", width=10, height=1, bg="orange", command=registration_form).place(x=105, y=170)

    Button(login_screen, text="Exit", width=10, height=1, bg="red", fg='white', command=quit).place(x=105, y=170)

    login_screen.mainloop()



    # calling function Loginform
Loginform()





