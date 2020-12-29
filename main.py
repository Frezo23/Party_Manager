import tkinter as tk 
from tkinter import *
from PIL import Image, ImageTk
import numpy as np
import pyzbar.pyzbar as pyzbar
import cv2

Capture_code = True
width, height = 300,300

scanned = []


root = Tk()

root.geometry('500x500')
root.title('Party Manage')

Cam_view = tk.Label(root)
Cam_view.place(x=0,y=0)

cap = cv2.VideoCapture(0)

while True:
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
                print('Ten kod został już użyty')
            else:
                print(obj.data)
                scanned.append(obj.data)

    root.update()

root.mainloop()