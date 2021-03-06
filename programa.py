import sqlite3
import re
from sqlite3 import Error
import face_recognition
import cv2
import numpy as np
import os
import warnings
warnings.filterwarnings("ignore")

cur_direc = os.getcwd()
path = os.path.join(cur_direc, 'caras', "")

def screen_clear():
   # for mac and linux(here, os.name is 'posix')
   if os.name == 'posix':
      _ = os.system('clear')
   else:
      # for windows platfrom
      _ = os.system('cls')

def esUsuario(usuario):
    if re.match("^[a-zA-Z0-9_-]+$", usuario):
        return True
    else:
        return False

def conectar():

    try:

        con = sqlite3.connect('mydatabase.db')

        cursorObj = con.cursor()

        cursorObj.execute('CREATE TABLE IF NOT EXISTS usuarios(id integer PRIMARY KEY, nombre text, info text)')

        con.commit()

        return con

    except Error:

        print(Error)

def existeUsuario(con, nombre):

    cursorObj = con.cursor()

    cursorObj.execute('SELECT nombre FROM usuarios WHERE nombre = ?', [nombre])

    rows = cursorObj.fetchall()

    cursorObj.close()

    if(len (rows)>0):
        return True
    else:
        return False

def obtenerUsuario(con, nombre):

    cursorObj = con.cursor()

    cursorObj.execute('SELECT id, nombre, info FROM usuarios WHERE nombre = ?', [nombre])

    rows = cursorObj.fetchall()

    cursorObj.close()

    return rows[0]



def nuevoUsario(con, nombre, info):
    cursorObj = con.cursor()

    datos = (nombre, info)

    cursorObj.execute('INSERT INTO usuarios(nombre, info) VALUES(?, ?)', datos)

    cursorObj.close()

    con.commit()

def tomarFoto(nombre):
    face_locations = []
    process_this_frame = True
    video_capture = cv2.VideoCapture(0)
    while True:
        ret, frame = video_capture.read()
        cleanframe = frame.copy()
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = small_frame[:, :, ::-1]
        if process_this_frame:
            face_locations = face_recognition.face_locations( rgb_small_frame)
        process_this_frame = not process_this_frame
    # Display the results
        for (top, right, bottom, left) in face_locations:
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4
    # Draw a rectangle around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
    # Display the resulting image
        cv2.imshow('Video', frame)
    # Hit 'q' on the keyboard to quit!
        if (cv2.waitKey(1) & 0xFF == ord(' ')) and (len(face_locations)>0) and (len(face_locations)<2):
            cv2.destroyAllWindows()
            cv2.imwrite(os.path.join(path, nombre+".jpg"), cleanframe)
            break

def validarFoto(nombre):
    face_locations = []
    process_this_frame = True

    user_image = face_recognition.load_image_file(os.path.join(path, nombre+".jpg"))
    user_face_encoding = face_recognition.face_encodings(user_image)[0]

    video_capture = cv2.VideoCapture(0)
    while True:
        ret, frame = video_capture.read()
        cleanframe = frame.copy()
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = small_frame[:, :, ::-1]
        if process_this_frame:
            face_locations = face_recognition.face_locations( rgb_small_frame)
            if (len(face_locations)>0) and (len(face_locations)<2):
                face_encodings = face_recognition.face_encodings( rgb_small_frame, face_locations)
                matches = face_recognition.compare_faces ([user_face_encoding], face_encodings[0])
                if(matches[0]):
                    return True
        process_this_frame = not process_this_frame
    # Display the results
        for (top, right, bottom, left) in face_locations:
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4
    # Draw a rectangle around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
    # Display the resulting image
        cv2.imshow('Video', frame)
    # Hit 'q' on the keyboard to quit!
        if (cv2.waitKey(1) & 0xFF == ord('q')):
            cv2.destroyAllWindows()
            return False


opc = "E"

# print(validarFoto("ivan"))

db = conectar()

screen_clear()

while(opc!="Y" and opc!="N"):
    opc=input("Crear nueva cuenta? (Y: Si/N: No)\n")

if(opc=="Y"):
    user = input("Escribe un nombre de usuario (Solo letras, numeros, y guiones)\n")
    isNew = False
    while(not isNew):
        while(not esUsuario(user)):
            user = input("Usuario invalido, escribe uno nuevo (Solo letras, numeros, y guiones)\n")
        isNew = not existeUsuario(db, user)
        if(not isNew):
            user = input("Nombre de usuario ya en uso, escribe uno nuevo\n")
    info = input("Escribe tu informacion privada\n")
    nuevoUsario(db, user, info)
    screen_clear()
    print("Tomando rostro. Cuando su rostro este marcado con un cuadro, presione \"espacio\"")
    tomarFoto(user)

screen_clear()
print("Inicio de Sesion")
user = input("Digita tu nombre de usuario\n")
while(not esUsuario(user)):
    user = input("Usuario invalido(Solo letras, numeros, y guiones)\n")

if(existeUsuario(db, user)):
    screen_clear()
    print("Confirmando rostro. Presione \"q\" para cancelar")
    if validarFoto(user):
        datos = obtenerUsuario(db, user)
        screen_clear()
        print("ID: " + str(datos[0]) + "\nNombre: " + datos[1] + "\nInformacion privada: " + datos[2])
    else:
        print("Rostro sin confirmar. Saliendo.")
else:
    print("Este usuario no existe")

        
    





# sql_insert(con, entities)

