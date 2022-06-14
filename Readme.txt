
1.encryptedregistration.py(It registers new user and saves it to the database)
   create a database named "face" and create table officerdetails
(sql = "insert into officerdetails (OfficerName, OfficerID, UserID, Passwords) values(%s, %s, %s, %s)")
this is for officer details

2.create criminaldetails table
("insert into criminaldetails (Id, CriminalName, Age, Address, Offence, Officer, DateOfArrest) values(%s,%s,%s,%s, %s, %s, %s)")

Note: You can create and modify database as per your wish , just change it in the code.

3.loginmodule_guidance.py
	this is the main program , here you login with officer details

4.guianddetection.py
	this is the program run from"loginmodule_guidance.py"

NOTE:You can ignore other .py files those only have the concept codes for this program
	"Data" folder contains the image data 





************HOW TO USE**************

1. After registering new criminals use "loginmodule_guidance.py" to enter main program.
2. Here you can register new criminals by filling data and then clicking on "Generate Datasets"(It takes upto 400 images of the face , make sure webcam is up and running before clicking it)
   NOTE:This program is made with external webcam in mind so, use external webcam.
3. After step 2 click on Train Datasets to train the data
   NOTE:It creates a 'classifier.xml' file if not there could be some module errors.
4. After that you can use "Live Detection" and "Generate Report"

