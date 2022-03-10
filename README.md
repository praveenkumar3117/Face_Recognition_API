# Face_Recognition_API

1)-->What does this program does
It provides an API through which prvides some face recognition features like search faces with an input image. It will give you
the best matchings from the database. Also it provides the option to add images to the database. Also to get info about a person.
User simply need to post an corresponding http request to fetch the required information

2)-->A description of how this program works (i.e. its logic)
SEARCH-FACES: The database is already containing a huge number of images with some encodings. When a user inputs a test image to search
the best matchings, it simply encode the test image then it calculate the face_distance of this image with each image in the database and
return the best matching images on the basis of face_distance.

Add_Face: When a user choose to add a single image to the database the program simply convert the input image into the encoding and then simply add this
image into the databases with suitable attributes.

Add_Faces_IN_BULK: When user wants to add multiple images at once it will provide a zip file containing  the images, the program will simply get the zip file
by zip handling methods and then extract it in a folder then create the encodings of all the images inside the folder and then add images to the database

Get_FACE_INFO: If the user simply inputs an id (database index), the program simply returns the information about the id to the user.
It is also connecting the database whenever it is required and close the connection after the request is processed


3)-->How to compile and run 
Simply extract the zip file and go into the code directory. Now install the required libraries if you found them missing while running, I am here providing
all the libraries, so there is lesser chance that you will need to install libraries but it may be possible sometimes. Now if you found any virtual environment
enabled simply deactivate it and if you find any pytest environment simply deacitvate it. Now open a terminal and run command : python3 main.py 
Now you can see the it will start running on some port number. Now to check the pytests simply open a new terminal and then run command : pytest
Make sure that the port number provided in the test_.py file is same as of the on which our main.py is runnning.
Now you can analyse the results. Always use the terminal only to run the code with given commands

Comments are also given in the code to understand code in a better way
Dont forget to deactivate any type of environment otherwise it may show some modules missing
