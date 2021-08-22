import face_recognition
import cv2
import numpy as np
import os
import glob

faces_encodings = []
nombres = []
cur_direc = os.getcwd()
path = os.path.join(cur_direc, 'caras', "")
archivos = [f for f in glob.glob(path+'*.jpg')]
number_files = len(archivos)
names = archivos.copy()

for i in range(number_files):
    globals()['image_{}'.format(i)] = face_recognition.load_image_file(archivos[i])
    globals()['image_encoding_{}'.format(i)] = face_recognition.face_encodings(globals()['image_{}'.format(i)])[0]
    faces_encodings.append(globals()['image_encoding_{}'.format(i)])
# Create array of known names
    names[i] = names[i].replace(path, "")  
    nombres.append(names[i])

face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

video_capture = cv2.VideoCapture(0)
while True:
    ret, frame = video_capture.read()
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = small_frame[:, :, ::-1]
    if process_this_frame:
        face_locations = face_recognition.face_locations( rgb_small_frame)
        face_encodings = face_recognition.face_encodings( rgb_small_frame, face_locations)
        face_names = []
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces (faces_encodings, face_encoding)
            name = "Unknown"
            face_distances = face_recognition.face_distance( faces_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = nombres[best_match_index]
            face_names.append(name)
    process_this_frame = not process_this_frame
# Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4
# Draw a rectangle around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
# Input text label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
# Display the resulting image
    cv2.imshow('Video', frame)
# Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break