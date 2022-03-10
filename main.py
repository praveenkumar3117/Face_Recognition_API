import PIL.Image as Image
import io
import face_recognition
from PIL import Image
from flask import Flask, request
import json
import os
import face_recognition
import psycopg2
import zipfile
import shutil
import pickle
from face_recognition.face_recognition_cli import image_files_in_folder
import json
import dbconnect



insert_script = 'insert into image_table values(%s,%s, %s)'          #to be used to insert row into the database
server_app = Flask(__name__)
def search(Dict,cursor,mi):                      #function to find the best matchings of the test image
    counter=0
    rows=[]
    for i in Dict:
        # print(i[0])
        if counter>=mi:                         #simply appending the best matchings into some list and if the size of list becomes k then break the process
            break
        cursor.execute('select * from image_table where image_id=%s', (i[0],))   #executing the query
        for row in cursor.fetchall():
            rows.append(row)
        counter+=1
    return rows              #returning the result row of best matchings

def DB_Load(cursor):                #function to load the databases entries encodings so that I can calculate the face distance with the test images
    encodings = []
    for row in cursor.fetchall():
        encoding = pickle.loads(row[1])
        encodings.append(encoding)
    return encodings

def make_map(face_distances):                       #mapping the face distance of an image in database to its index so that i can use it in further process to find the best matchings
    Dict={}
    for i, face_distance in enumerate(face_distances):
        if face_distance < float(request.form['tolerance']):  #keeping all the images below the tolerance, later i will take top k images
            Dict[i] = face_distance
    return Dict                         #returning the Dictionary

@server_app.route("/search_faces/",methods=['POST'])          #function to search the faces
def search_faces():
    conn=dbconnect.connect()                 #establishing the database connection
    cursor = conn.cursor()                  #making a cursor
    image = Image.open(io.BytesIO(request.files['image'].stream.read()))    #reading the image
    rgb_im = image.convert('RGB')
    rgb_im.save('temp1.jpeg')                 #it recieves the file into .png format, so i am converting it into .jpeg format
    image_to_test = face_recognition.load_image_file("temp1.jpeg")              #loading test image
    cursor.execute('select * from image_table')                       #loading all the rows into the cursor
    conn.commit()
    encodings=DB_Load(cursor)                        #finding the encodings of all the database entries    
    image_to_test_encoding = face_recognition.face_encodings(image_to_test)[0]    #making its encoding
    face_distances = face_recognition.face_distance(encodings, image_to_test_encoding) #finding the face distances of test images with the database entries 
    Dict = make_map(face_distances)                      #mapping the face distances with the index
    # print(float(request.form['tolerance']))
    Dict=sorted(Dict.items(), key =lambda kv:(kv[1], kv[0])) #sorting the dictionary by face distance so that we can find the best matchings
    # print(Dict)
    min_l = min(len(Dict),int(request.form['k']))    #it might be possible that the database contains less entries, so to handle that error
    rows=search(Dict,cursor,min_l)    #getting the best matchings
    conn.close            #closing the database connection
    print(str(rows))
    return 'search_faces'

def Add_bulk(count,cursor):
       
    for class_dir in os.listdir("bulk"):                          #adding the photos in bulk
        if not os.path.isdir(os.path.join("bulk", class_dir)):
            continue
        
        for img_path in image_files_in_folder(os.path.join("bulk", class_dir)):
            image = face_recognition.load_image_file(img_path)    #loading current image of the loop
            temp = face_recognition.face_encodings(image)     #finding its encoding
            if len(temp) != 0:
                data = img_path.split("/")                 #trimming the path to get the file name
                a = data[len(data)-1]
                data1 = a.split(".")
                
                p={"name": data1[0], "version": data1[0], "date": "", "location":""}   #setting the attribute to the current image
                insert_value = (count,pickle.dumps(temp[0]),json.dumps(p))     #insertion value
                cursor.execute(insert_script,insert_value)     #inserting into the database
                count+=1            #count is used to keep the index of the entries in the database and it is increased as an entries is added

def handle_zip():      
    zi = request.files['image'].stream.read()     #reading the zip file by bytes
    with open("bulk.zip", 'wb') as output:        #wrting back the bytes to form a .zip file into bulk.zip
        output.write(zi)
    os.mkdir("bulk")
    with zipfile.ZipFile("bulk.zip", 'r') as ref:  #extracting the bulk.zip
        ref.extractall("bulk")

@server_app.route("/add_face/",methods=['POST'])
def add_face():                                        #function to add a face in the database
    conn=dbconnect.connect()                          #making database connection
    cursor = conn.cursor()                    #making  a cursor
    im = Image.open(io.BytesIO(request.files['image'].stream.read()))    #reading input image
    p = {"name": request.form['name'], "version": request.form['version'],     #setting the attribute of the image
        "date": request.form['date'], "location": request.form['location']}
    rgb_im = im.convert('RGB')     #converting it into suitable format
    rgb_im.save('temp.jpeg')
    cursor.execute('select count(*) from image_table')     #couting the total rows in the database so that we can add a new entry at size+1
    row = cursor.fetchone()  
    count=int(row[0])+1 
    cursor.execute('''create table IF NOT EXISTS image_table(image_id SERIAL PRIMARY KEY,np_array_bytes BYTEA, metaadata varchar(1000) NULL);''')
    image = face_recognition.load_image_file("temp.jpeg")   #loading the input image
    image_encoding = face_recognition.face_encodings(image)[0]    #finding the encoding
       
    insert_value = (count, pickle.dumps(image_encoding), json.dumps(p))      
    cursor.execute(insert_script,insert_value)         #insertion 
    print(count)    #to cross check the addition in the database
    conn.commit()
    return 'OK'

@server_app.route("/add_faces_in_bulk/",methods=['POST'])
def add_faces_in_bulk():      #function to add faces in bulk
    conn=dbconnect.connect()    #making database connection
    cursor = conn.cursor()       #making cursor
    cursor.execute('select count(*) from image_table')     #couting rows in database so that we can start adding entries from the index size+1
    row = cursor.fetchone()
    handle_zip()       #zip handling
    count=int(row[0])+1    #index from which we start insering entries
    Add_bulk(count,cursor)        #call the function that will add the entries in database
    conn.commit()      #commit the changes in the database
    cursor.execute('select count(*) from image_table')     #couting rows in database so that we can start adding entries from the index size+1
    row = cursor.fetchone()
    print(int(row[0]))
    conn.close
    try:
        shutil.rmtree("bulk")     #delete the bulk folder so that it can be used again otherwise it will throw an error showing that bulk already exists
    except OSError as e:
        print("Error: %s - %s." % (e.filename, e.strerror))
    return 'OK'

@server_app.route("/get_face_info/",methods=['POST'])
def get_face_info():      #function to find the face info when we get the index of the person in the database
    conn=dbconnect.connect()      #making database connection
    cursor = conn.cursor()          #making cursor
    id = request.form['id']        #getting the id for which we need to provide the information
    cursor.execute('select * from image_table where image_id=%s', (id,))   #executing the query here
    row = cursor.fetchone()
    print(row)    #just to crosscheck the info supplied

    conn.close()
    return 'get_face_info'

if __name__ == "__main__":
    server_app.run(debug=True, port=5000)