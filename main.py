import tkinter as tk 
from tkinter import *
from PIL import Image, ImageTk
import numpy as np
import pyzbar.pyzbar as pyzbar
from datetime import datetime
import qrcode
import time
import sys
import cv2
import os

Capture_code = True
Camera_read = True
width, height = 300,300

dane = ''
dane_scaned = ''
data_ = ''
zapis_qr = ''
a = 0

file_save = []
scanned = []
files_for_list = []
copy_files_list = []

try:
    file = open('logs.txt','r')
    dane = file.read()
    file.close()
    print(dane)
except:
    pass

#### FUNKCJE ####

def check_if_string_in_file(file_name, string_to_search):
    try:
        with open(file_name, 'r') as read_obj:
            for line in read_obj:
                if string_to_search in line:
                    return True
        return False
    except:
        pass

def odczytanie_plik():
    global files_for_list, a, copy_files_list
    a = 0
    try:
        log_file = open('logs.txt', 'r')
        files_for_list = log_file.readlines()

        # copy_files_list = files_for_list

        try:
            dane_list_box.delete(1,dane_list_box.size())
        except:
            pass

        for i in range(len(files_for_list)):
            dane_list_box.insert(END,files_for_list[a])
            a += 1
    except:
        pass

def save_logs():
    global scanned, dane, dane_scaned, file_save

    print(dane_scaned)
    print(scanned)

    data_ = datetime.now()
    data_ = data_.strftime('%Y-%d-%m|%H:%M:%S')
    dane =  dane + '[' + str(data_) + ']' + ' ' + str(dane_scaned) + '\n'
    print(dane)

    file = open('logs.txt', 'w')
    file.write(str(dane))
    file.close()

    odczytanie_plik()

def read_QR():
    global Camera_read, scanned, dane_scaned
    ### odczyt kodów QR z kamery

    while Camera_read == True:
        try:
            frame = cap.read()[1]
            img = cv2.flip(frame,1)
            img = cv2.resize(img,(width,height))
            img1 = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
            # img1 = cv2.Canny(img1, 100, 100)
            img = ImageTk.PhotoImage(Image.fromarray(img1))
            Cam_view['image'] = img

            if Capture_code == True:
                decode_obj = pyzbar.decode(frame)

                for obj in decode_obj:
                    if obj.data in scanned or check_if_string_in_file('logs.txt', str(obj.data)):
                        code_info.configure(text='kod został już użyty')
                    else:
                        code_info.configure(text=obj.data)
                        scanned.append(obj.data)
                        dane_scaned = str(scanned[len(scanned) - 1])
                        save_logs()
                        time.sleep(2)
            root.update()
        except RuntimeError:
            Camera_read = False


def odczyt():
    global Camera_read
    Camera_read = True
    ### odczyt kodów QR z kamery

    read_QR()

def wylacz_cam():
    global Camera_read
    Camera_read = False

def generuj():
    global zapis_qr

    zapis_qr = 'KLIENT: ' + klient_ent.get() + ' PROMOTOR: ' + promotor_ent.get()
    nazwa = klient_ent.get() + '.png'

    qr = qrcode.make(zapis_qr)
    qr.save(str(nazwa))

### tworzenie okna

root = Tk()

root.geometry('800x500')
root.title('QR Manager')

Teskst_QR = tk.Entry(root,bg='black')
Teskst_QR.place(x=0,y=0)

Cam_view = tk.Label(root)
Cam_view.place(x=0,y=0)

code_info = tk.Label(root)
code_info.place(x=0,y=303)

dane_list_box = tk.Listbox(root,width=80,height=15)
dane_list_box.place(x=305,y=60)

#### widgets for generating qr code

klient_ent = tk.Entry(root,width=50)
klient_ent.place(x=100,y=370)

klient_lbl = tk.Label(root,text='Dane klienta')
klient_lbl.place(x=0,y=370)

promotor_ent = tk.Entry(root,width=50)
promotor_ent.place(x=100,y=400)

promotor_lbl = tk.Label(root,text='Dane promotora')
promotor_lbl.place(x=0,y=400)

Odczytbtn = tk.Button(root,text='Włącz skaner',command=odczyt)
Odczytbtn.place(x=305,y=0)

Wylaczbtn = tk.Button(root,text='Wyłącz skaner',command=wylacz_cam)
Wylaczbtn.place(x=405,y=0)

Generujbtn = tk.Button(root,text='Generuj',command=generuj)
Generujbtn.place(x=0,y=430)

cap = cv2.VideoCapture(0)

odczytanie_plik()

### odczyt kodów QR z kamery

while Camera_read == True:
    read_QR()

root.mainloop()