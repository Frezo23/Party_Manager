import tkinter as tk 
from tkinter import *
from PIL import Image, ImageTk
import numpy as np
import pyzbar.pyzbar as pyzbar
import datetime
import time
import cv2
import os

Capture_code = True
Camera_read = True
width, height = 300,300

dane = ''
dane_scaned = ''
data_ = ''

file_save = []

scanned = []


def save_logs():
    global scanned, dane, dane_scaned, file_save

    print(dane_scaned)
    print(scanned)

    data_ = datetime.datetime.now()

    dane =  dane + '[' + str(data_) + ']' + ' ' + str(dane_scaned) + '\n'
    print(dane)

    file = open('logs.txt', 'w')
    file.write(str(dane))

def read_QR():
    global Camera_read, scanned, dane_scaned
    ### odczyt kodów QR z kamery

    while Camera_read == True:
        frame = cap.read()[1]
        img = cv2.flip(frame,1)
        img = cv2.resize(img,(width,height))
        img1 = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        img = ImageTk.PhotoImage(Image.fromarray(img1))
        Cam_view['image'] = img

        if Capture_code == True:
            decode_obj = pyzbar.decode(frame)

            for obj in decode_obj:
                if obj.data in scanned:
                    code_info.configure(text='kod został już użyty')
                else:
                    code_info.configure(text=obj.data)
                    scanned.append(obj.data)
                    dane_scaned = str(scanned[len(scanned) - 1])
                    save_logs()
                    time.sleep(2)

        root.update()


def odczyt():
    global Camera_read
    Camera_read = True
    ### odczyt kodów QR z kamery
    read_QR()

def generuj():
    global Camera_read
    Camera_read = False


### tworzenie okna

root = Tk()

root.geometry('500x500')
root.title('QR Manager')

Cam_view = tk.Label(root)
Cam_view.place(x=0,y=0)

code_info = tk.Label(root)
code_info.place(x=0,y=301)

Odczytbtn = tk.Button(root,text='Odczyt kodu',command=odczyt)
Odczytbtn.place(x=301,y=0)

Generujbtn = tk.Button(root,text='Generowanie',command=generuj)
Generujbtn.place(x=401,y=0)

cap = cv2.VideoCapture(0)


### odczyt kodów QR z kamery

while Camera_read == True:
    read_QR()

root.mainloop()