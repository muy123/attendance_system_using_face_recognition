
import face_recognition
import cv2
import numpy as np
import csv
import pandas as pd
import os

video_capture = cv2.VideoCapture(0)

h_image = face_recognition.load_image_file("harsh.jpg")
h_face_encoding = face_recognition.face_encodings(h_image)[0]

k_image = face_recognition.load_image_file("krishna.jpg")
k_face_encoding = face_recognition.face_encodings(k_image)[0]

a_image = face_recognition.load_image_file("anshul.jpg")
a_face_encoding = face_recognition.face_encodings(a_image)[0]

known_face_encodings = [
    h_face_encoding,
    k_face_encoding,
    a_face_encoding
    
]
known_face_names = [
    "IIT2017098",
    "IIT2017117",
	"IIT2017119"
]
hashValues = {}
for name in known_face_names:
    hashValues[name] = 0
hashValues['Unknown'] = 0

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

while True:
    ret, frame = video_capture.read()
    
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    
    rgb_small_frame = small_frame[:, :, ::-1]
    if process_this_frame:
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]

            face_names.append(name)

    process_this_frame = not process_this_frame


    for (top, right, bottom, left), name in zip(face_locations, face_names):
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        hashValues[name] += 1
        if hashValues[name] > 30:
            fileInput = open(r"/home/anshul/Desktop/sem6proj/Attendance.csv")
            data = csv.reader(fileInput)
            csvData = []
            for row in data:
                csvData.append(row)
            fileInput.close()
            fileOuput = open("Temp.csv", 'w', newline='')
            date = "20/05/20"
            writer = csv.writer(fileOuput, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            if csvData[0][-1] != date:
                csvData[0].append(date)
                for i in range(1, len(csvData)):
                    csvData[i].append('A')

            for i in range(1, len(csvData)):
                if csvData[i][0] == name:
                    csvData[i][-1] = 'P'
            for row in csvData:
                writer.writerow(row)
            fileOuput.close()
            os.remove('Attendance.csv')
            os.rename('Temp.csv', 'Attendance.csv')
        print(hashValues)

    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()






