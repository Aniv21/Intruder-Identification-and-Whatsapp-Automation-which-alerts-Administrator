import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from shutil import *
import os
import cv2
import numpy as np
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from twilio.rest import Client

driver = webdriver.Chrome('C:\\Users\\dell\\Desktop\\ChromeDriver\\chromedriver')
driver.get("http://web.whatsapp.com")
driver.maximize_window()
driver.implicitly_wait(20)
name = "Samba"
msg = "Intruder Detected " \
      "Please Find Help :-!!"
count = 2

def printtext():
    global registration_number
    string = registration_number.get()
    return string


def printtext2():
    global name_of_student
    string2 = name_of_student.get()
    return string2


def detect():
    folder = printtext()
    user = printtext2()
    sampleNum = 0
    facecascade = cv2.CascadeClassifier(
        'opencv\\opencv\\sources\\opencv-master\\data\\haarcascades\\haarcascade_frontalface_default.xml')
    camera = cv2.VideoCapture(0)
    count = 0
    while (True):
        printtext()
        printtext2()
        ret, frame = camera.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = facecascade.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces:
            sampleNum = sampleNum + 1
            img = cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            f = cv2.resize(gray[y:y + h, x:x + h], (500, 500))
            cv2.imwrite("Images/" + user + "." + str(folder) + "." + str(sampleNum) + ".jpg", f)
            count += 1
            cv2.waitKey(200)
        cv2.imshow("camera : ", frame)
        cv2.waitKey(1)
        if sampleNum > 25:
            break
    camera.release()
    cv2.destroyAllWindows()


# Trainer

def trainer():
    recogniser = cv2.face.LBPHFaceRecognizer_create()
    path = 'Images//'

    def getimageIds(path):
        imagepaths = [os.path.join(path, f) for f in os.listdir(path)]
        faces = []
        Ids = []
        for imagepath in imagepaths:
            faceimg = Image.open(imagepath).convert('L')
            facenp = np.array(faceimg, 'uint8')
            Id = int(os.path.split(imagepath)[-1].split('.')[1])
            faces.append(facenp)
            print(Id)
            Ids.append(Id)
            cv2.imshow('Training the dataset', facenp)
            cv2.waitKey(10)
        return Ids, faces

    Ids, faces = getimageIds(path)
    recogniser.train(faces, np.array(Ids))
    recogniser.save('recogniser//recogniser_all.yml')
    cv2.destroyAllWindows()


path = 'Images'
imagepaths = [os.path.join(path, f) for f in os.listdir(path)]
path = 'Images'
for imagepath in imagepaths:
    ID = int(os.path.split(imagepath)[-1].split('.')[1])
imagepaths = [os.path.join(path, f) for f in os.listdir(path)]
path = 'Images'

file = open("testfile.txt", "a+")
file.write("NAME")
file.write(",")

file.write("REGD.NO")
file.write(",")
file.write("DATE,TIME")
file.write("\n")
folder = '0'


def recognise():
    path = 'Images'
    imagepaths = [os.path.join(path, f) for f in os.listdir(path)]
    path = 'Images'
    for imagepath in imagepaths:
        ID = int(os.path.split(imagepath)[-1].split('.')[1])
    facecascade = cv2.CascadeClassifier(
        'opencv\\opencv\\sources\\opencv-master\\data\\haarcascades\\haarcascade_frontalface_default.xml')
    rec = cv2.face.LBPHFaceRecognizer_create()  # Local Binary Pattern histogram
    print(rec)
    rec.read('recogniser\\recogniser_all.yml')
    camera = cv2.VideoCapture(0)
    sampleNum = 0
    folder = '0'
    font = cv2.FONT_HERSHEY_SCRIPT_COMPLEX
    while (True):
        ret, frame = camera.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = facecascade.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces:
            sampleNum = sampleNum + 1
            img = cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            folder, conf = rec.predict(gray[y:y + h, x:x + w])
            print(conf)
            if (conf > 60):
                cv2.putText(frame, "Not Recognized", (x, y + h), font, 2, 255)
                input('Enter anything after scanning QR code')
                user = driver.find_element_by_xpath('//span[@title = "{}"]'.format(name))
                user.click()
                msg_box = driver.find_element_by_class_name('_2S1VP')
                for i in range(count):
                    msg_box.send_keys(msg)
                    button = driver.find_element_by_class_name('_2lkdt')
                    button.click()
                account_sid="AC******************************"
                auth_token = "********************************"
                client = Client(account_sid,auth_token)
                message = client.messages.create(to="+919059960444 ",from_="(616)207-1195",body="Intruder Detected....Please call 100")
                print(message.sid)
            elif (conf < 60):
                cv2.putText(frame, str(folder), (x, y + h), font, 2, 255)
                f = cv2.resize(gray[y:y + h, x:x + h], (500, 500))
                cv2.waitKey(100)
        cv2.imshow("camera : ", frame)
        cv2.waitKey(1)
        if sampleNum > 15:
            break
    camera.release()
    cv2.destroyAllWindows()


# recogniser2
def recognise1():
    path = 'Images'
    imagepaths = [os.path.join(path, f) for f in os.listdir(path)]
    path = 'Images'
    for imagepath in imagepaths:
        ID = int(os.path.split(imagepath)[-1].split('.')[1])
    facecascade = cv2.CascadeClassifier(
        'opencv\\opencv\\sources\\opencv-master\\data\\haarcascades\\haarcascade_frontalface_default.xml')
    rec = cv2.face.LBPHFaceRecognizer_create()
    print(rec)
    rec.read('recogniser\\recogniser_all.yml')
    camera = cv2.VideoCapture(0)
    sampleNum = 0
    folder = '0'
    font = cv2.FONT_HERSHEY_DUPLEX
    if (rec):
        temperature = 12
    while (True):
        ret, frame = camera.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = facecascade.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces:
            sampleNum = sampleNum + 1
            img = cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            folder, conf = rec.predict(gray[y:y + h, x:x + w])
            cv2.putText(frame, str(folder), (x, y + h), font, 2, 255)
            f = cv2.resize(gray[y:y + h, x:x + h], (500, 500))
            if (str(folder) == details[0]):
                file.write((details[1]))
            file.write(",")
            file.write(str(folder))
            file.write(",")
            file.write(time.strftime("%d/%m/%y"))
            file.write(",")
            file.write(time.strftime("%I:%M:%S"))
            file.write("\n")
            cv2.waitKey(10)
        cv2.imshow("camera : ", frame)
        cv2.waitKey(1)
        if sampleNum > 0:
            break
    camera.release()
    cv2.destroyAllWindows()


def raise_frame(frame):
    frame.tkraise()


root = tk.Tk()
root.title("Intruder Identification using Machine Learning")

f1 = tk.Frame(root)
filename = 'face.jpg'
canvas = tk.Canvas(f1, width=740, height=370)
canvas.pack()
tk_img = ImageTk.PhotoImage(file=filename)
canvas.create_image(250, 200, image=tk_img)
next_button = ttk.Button(f1, text='Next', command=lambda: raise_frame(f2)).pack()
next_button_window = canvas.create_window(600, 340, anchor='nw')
quit_button = ttk.Button(f1, text="Quit", command=root.quit, width=8)
quit_button_window = canvas.create_window(440, 385, window=quit_button)

f2 = tk.Frame(root)
label1 = tk.Label(f2, text="Regd ID")
registration_number = tk.Entry(f2)
label1.pack(side='left')
registration_number.pack(side='left')
registration_number.focus_set()
label2 = tk.Label(f2, text="Name")
name_of_student = tk.Entry(f2)
label2.pack(side='left')
name_of_student.pack(side='left')
"""okay1 = ttk.Button(f2, text='Confirm Regd.No', command=printtext)
okay1_window = canvas.create_window(500, 380)
okay2 = ttk.Button(f2, text='Confirm Name', command=printtext2)
okay1.pack()
okay2.pack()"""
filename2 = 'img2.png'
canvas = tk.Canvas(f2, width=740, height=370)
canvas.pack()
tk_img2 = ImageTk.PhotoImage(file=filename2)
canvas.create_image(250, 200, image=tk_img2)
next_button2 = ttk.Button(f2, text='Next', command=lambda: raise_frame(f3)).pack()
next_button2_window = canvas.create_window(600, 340)
back_button = ttk.Button(f2, text="Back", command=lambda: raise_frame(f1), width=5)
back_button1_window = canvas.create_window(430, 384, window=back_button)

# Detection Button

detectionbut = ttk.Button(f2, text='Scan the face', command=detect, width=15)
detectionbut_window = canvas.create_window(505, 385, window=detectionbut)
# 3rd page

f3 = tk.Frame(root)
filename3 = 'img3.png'
canvas = tk.Canvas(f3, width=740, height=370)
canvas.pack()
tk_img3 = ImageTk.PhotoImage(file=filename3)
canvas.create_image(450, 300, image=tk_img3)
next_button3 = ttk.Button(f3, text='Next', command=lambda: raise_frame(f4)).pack()
next_button3_window = canvas.create_window(600, 340)
back_button2 = ttk.Button(f3, text="Back", command=lambda: raise_frame(f2), width=5)
back_button2_window = canvas.create_window(430, 384, window=back_button2)
Trainer = ttk.Button(f3, text='Trainer', command=trainer, width=10)
Trainer_window = canvas.create_window(487, 385, window=Trainer)

f4 = tk.Frame(root)

filename4 = 'last.jpg'
canvas = tk.Canvas(f4, width=750, height=400)
canvas.pack()
tk_img4 = ImageTk.PhotoImage(file=filename4)
canvas.create_image(300, 200, image=tk_img4)
back_button3 = ttk.Button(f4, text="Back", command=lambda: raise_frame(f3), width=5)
back_button3_window = canvas.create_window(450, 384, window=back_button3)
recogniser = ttk.Button(f4, text='Recogniser', command=recognise)
recogniser_window = canvas.create_window(517, 385, window=recogniser)

for frame in (f1, f2, f3, f4):
    frame.grid(row=0, column=0, sticky='news')

raise_frame(f1)
root.mainloop()
