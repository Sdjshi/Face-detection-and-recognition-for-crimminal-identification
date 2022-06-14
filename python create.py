import mysql.connector
mydb = mysql.connector.connect(host="localhost",user="root",passwd="",database="face")
mycursor = mydb.cursor()
mycursor.execute("Create table criminaldetails (Id varchar(200), CriminalName varchar(200), Age varchar(200), Address varchar(200), Offence varchar(200), Officer varchar(200), DateOfArrest varchar(200))")