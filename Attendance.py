import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import *
from tkinter import filedialog
from tkcalendar import Calendar
from tkcalendar import DateEntry
import time
from time import strftime
import numpy as np
import face_recognition
import cv2
import csv
import os
from datetime import datetime
from PIL import Image, ImageTk, ImageEnhance


# Global variable to store student name
sname = ""


# Dictionary to store face encodings mapped to names
known_face_encodings = {}
sname = ""  # You can modify sname as needed based on your structure


# Function to save student details
def save(schno, sname, classbox, section, cal, entry):
    File = open("Student Details.csv", "a", newline="\n")
    wr = csv.writer(File)
    List = [schno, sname, classbox, section, cal]
    wr.writerow(List)
    File.close()

# Function to save attendance
def save2(sname, date, time):
    file = open("Daily Attendance.csv", "a", newline="\n")
    wr = csv.writer(file)
    List2 = [sname, date, time]
    wr.writerow(List2)
    file.close()

# Function to show a success message and save details
def details(schno, sname, classbox, section, cal, entry):
    messagebox.showinfo("", "Your details have been saved.")
    save(schno, sname, classbox, section, cal, entry)
    entry.destroy()



    
# Function to check face and save image
def checkface(sname, entry):
    cap = cv2.VideoCapture(0)
    face_cap = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    while True:
        ret, img = cap.read()
        col = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cap.detectMultiScale(col, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30), flags=cv2.CASCADE_SCALE_IMAGE)
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.imshow('frame', img)
        if not ret:
            break
        k = cv2.waitKey(1)
        if k % 256 == 13:  # Press Enter key
            file = sname + '.jpg'
            cv2.imwrite(file, img)
            break
    cap.release()
    cv2.destroyAllWindows()



#to compare and display the specified name
def recognize_faces(mark):
    cap = cv2.VideoCapture(0)
    known_face_encodings = []
    known_face_names = []

    # Specify the folder where known face images are stored
  
    folder_path = r"C:\Users\hp\OneDrive\Desktop\Face Recognition"
    
    # Load known faces from the folder
    for filename in os.listdir(folder_path):
        if filename.endswith(".jpg") :
            img_path = os.path.join(folder_path, filename)
            image = face_recognition.load_image_file(img_path)
            encoding = face_recognition.face_encodings(image)

            if encoding:  # Check if encoding was successful
                known_face_encodings.append(encoding[0])

                # Extract the name from the filename (remove the file extension)
                name = os.path.splitext(filename)[0]
                known_face_names.append(name)

    marked_attendance = False  # Flag to track if attendance is marked
    
    while True:
        ret, frame = cap.read()
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB

        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            # Check if the face matches any known face
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            if name == "Unknown":
                messagebox.showinfo("", "No person detected")

            
            # Use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
                
                # Ensure that there is a valid match
            if matches[best_match_index]:
                name = known_face_names[best_match_index]

                # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                # Display the name above the face
            cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)

            # Display the resulting image
            cv2.imshow('Video', frame)
            cv2.waitKey(30)

            # Mark attendance for the identified person
            if name != "Unknown":
                date = strftime("%D")
                time_str = strftime("%T")
                save2(name, date, time_str)  # Save attendance
                with open("Student Details.csv", "r") as file:
                    reader = csv.reader(file)
                    student_info = None
                    for row in reader:
                        if row[1] == name:  # Assuming 'name' is in the second column
                              student_info = row
                              break
    
                if student_info:
        # Format the student details for display
                     details = f"Name: {student_info[1]}\nScholar No: {student_info[0]}\nClass: {student_info[2]}\nSection: {student_info[3]}\nDOB: {student_info[4]}"
                     messagebox.showinfo("Attendance Marked", f"{name} has been marked present!\n\nDetails:\n{details}")
                else:
                    messagebox.showinfo("Attendance Marked", f"{name} has been marked present!\n\nNo further details found.")
                '''messagebox.showinfo("Attendance", f"{name} has been marked present!")
                marked_attendance = True  # Update the flag
                display_details()'''
        '''# Display the resulting image
                cv2.imshow('Video', frame)'''
        break
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    mark.destroy()
    cap.release()
    cv2.destroyAllWindows()




# Function to register student details
def register():
    entry = Tk()
    entry.geometry("1000x1000")
    entry.configure(bg="Dark slate grey")
    entry.title("Register your details")

    Label(entry, text="Enter your details below-", font=("Times new roman", 25)).place(x=350, y=40)
    Label(entry, text='Scholar no.', fg='black', font=("Tahoma", 20)).place(x=250, y=100)
    schno = Entry(entry, width=20, font=("Tahoma",20))
    schno.place(x=400, y=100)

    Label(entry, text='Name', fg='black', font=('tahoma', 20)).place(x=250, y=150)
    sname = Entry(entry, width=20, font=('Tahoma',20))
    sname.place(x=400, y=150)

    ttk.Label(entry, text='Class', font=('tahoma', 20)).place(x=250, y=200)
    classbox = ttk.Combobox(entry, values=['VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII'], font=("courier new", 20))
    classbox.place(x=400, y=200)
    classbox.current(6)

    ttk.Label(entry, text="Section", font=("tahoma", 20)).place(x=250, y=250)
    section = ttk.Combobox(entry, values=["A", "B", "C", "D", "E", "F", "G"], font=("tahoma", 20))
    section.place(x=400, y=250)
    section.current(0)

    Label(entry, text="DOB", fg="black", font=("tahoma", 20)).place(x=250, y=300)
    cal = DateEntry(entry, width=20, year=2007, month=10, day=24, background="darkblue", foreground="white", borderwidth=6)
    cal.place(x=400, y=300)

    Label(entry, text='Photo', fg='black', font=("Tahoma", 20)).place(x=250, y=350)
    Button(entry, text="Register Photo", command=lambda: checkface(sname.get(), entry), height=1, width=25, font=("calibri", 15)).place(x=400, y=350)

    Button(entry, text="Enter", command=lambda: details(schno.get(), sname.get(), classbox.get(), section.get(), cal.get(), entry), height=1, width=20, font=("calibri", 15)).place(x=400, y=500)




# Function to take attendance
def attendence():
    mark = Tk()
    mark.geometry("1000x1000")
    mark.configure(bg="indigo")
    mark.title("Attendance")

     #date of entry
    dt=Label(mark,text=(strftime("%D%n")),font=("tahoma",20),bg="floralwhite",width=10,height=2)
    date=strftime("%D%n")
    dt.place(x=500,y=100)
    Label(mark,text="Date of entry", fg="black", font=("tahoma",20)).place(x=300, y=100)
    #time of entry
    tm=Label(mark,text=(strftime("%T%n")),font=("tahoma",20),bg="floralwhite",width=10,height=2)
    tm.place(x=500,y=200)
    time=strftime("%T%n")
    Label(mark,text="Time of entry", fg="black", font=("tahoma",20)).place(x=300, y=200)

    Button(mark, text="Start Attendance", command=lambda: recognize_faces(mark), height=2, width=25, font=("Tahoma", 15)).place(x=350, y=350)
   



#main window
home=Tk()
home.geometry("1000x1000")
home.title("Home page")
home.configure(bg="Maroon")


# Add a background image (using PIL and ImageTk)
bg_image = Image.open("background.jpg")  # Ensure you have a background image in your project folder
bg_image = bg_image.resize((1000, 1000), Image.Resampling.LANCZOS)  # Replace ANTIALIAS with LANCZOS


# Adjust factor to make the image lighter
enhancer = ImageEnhance.Brightness(bg_image)
bg_image = enhancer.enhance(0.5)  # Adjust factor to make the image lighter

bg_photo = ImageTk.PhotoImage(bg_image)
bg_label = Label(home, image=bg_photo)  # Create label to hold background image
bg_label.place(relwidth=1, relheight=1)  # Make the background cover the whole window


l1=Label(home,text="WELCOME TO FACE RECOGNITION ATTENDENCE SYSTEM", fg="black",bg="white",font=("Times new Roman", 25)).place(x=50,y=20)
l2=Label(home,text="Give a smile and mark your attendence virtually!!", fg="black",bg="white",font=("Times New Roman", 25)).place(x=170, y=200)
sname=""

Button(home,text="Take Attendance",command=(attendence),height=1, width=40, font=("calibri",15)).place(x=330,y=350)
Button(home,text="Register Student details",command=(register),height=1, width=40, font=("calibri",15)).place(x=330,y=400)

