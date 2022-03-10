#from flask import request
from cgi import test
import pytest
import requests

def test_add_face():
    files = {'image': open('rohit_sharma.jpeg', 'rb')}
    r = requests.post("http://127.0.0.1:5000/add_face/", files=files, data={'name':'Rohit_Sharma','date':'current_date','location':'Mumbai','version':'rohit_sharma'})
    assert r.text == 'OK'

def test_search_face():
    files = {'image': open('abel_paceo.jpeg', 'rb')}
    r = requests.post("http://127.0.0.1:5000/search_faces/", files=files, data={'k':'3', 'tolerance': '0.6'})
    assert r.text == 'search_faces'

def test_add_faces_in_bulk():
    files = {'image': open('gg.zip', 'rb')}
    r = requests.post("http://127.0.0.1:5000/add_faces_in_bulk/", files=files)
    assert r.text == 'OK'

def test_get_face_info():
    r = requests.post("http://127.0.0.1:5000/get_face_info/", data={'id':'1546'})
    assert r.text == 'get_face_info'

def test_add_face1():
    files = {'image': open('virat_kohli.jpeg', 'rb')}
    r = requests.post("http://127.0.0.1:5000/add_face/", files=files, data={'name':'Virat_Kohli','date':'current_date','location':'Banglore','version':'Virat_Kohli'})
    assert r.text == 'OK'

def test_search_face():
    files = {'image': open('Zinedine_Zidane.jpg', 'rb')}
    r = requests.post("http://127.0.0.1:5000/search_faces/", files=files, data={'k':'3', 'tolerance': '0.6'})
    assert r.text == 'search_faces'

def test_add_faces_in_bulk1():
    files = {'image': open('dd.zip', 'rb')}
    r = requests.post("http://127.0.0.1:5000/add_faces_in_bulk/", files=files)
    assert r.text == 'OK'

def test_get_face_info():
    r = requests.post("http://127.0.0.1:5000/get_face_info/", data={'id':'2000'})
    assert r.text == 'get_face_info'



    
