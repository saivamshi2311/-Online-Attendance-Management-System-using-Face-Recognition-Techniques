import tkinter as tk
from tkinter import *
import cv2
import csv
import os
import numpy as np
from PIL import Image,ImageTk #pillow
import pandas as pd
import datetime
import time

#####Window is our Main frame of system
mainwindow=tk.Tk()
mainwindow.title("Online Attendence Evaluation System")
#window = tk.Tk()
#window.title("FAMS-Face Recognition Based Attendance Management System")

mainwindow.geometry('550x450')
mainwindow.configure(background='red')

            
def admin_panel():
    win = tk.Tk()
    #win.iconbitmap('AMS.ico')
    win.title("LogIn")
    win.geometry('880x420')
    win.configure(background='snow')
    def log_in():
        username = un_entr.get()
        password = pw_entr.get()

        if username == 'vamshi' :
            if password == '12345':
                window=tk.Tk()
                window.title("enrollment of student")
                window.geometry('880x420')
                window.configure(background='snow')
                lbl = tk.Label(window, text="Enter Enrollment", width=20, height=2, fg="black", bg="deep pink", font=('times', 15, ' bold '))
                lbl.place(x=200, y=200)
                def testVal(inStr,acttyp):
                    if acttyp == '1': #insert
                        if not inStr.isdigit():
                            return False
                        return True
                def clear():
                    txt.delete(first=0, last=22)
                def clear1():
                    txt2.delete(first=0, last=22)
                def del_sc1():
                    sc1.destroy()
                def err_screen():
                    global sc1
                    sc1 = tk.Tk()
                    sc1.geometry('300x100')
                    sc1.iconbitmap('AMS.ico')
                    sc1.title('Warning!!')
                    sc1.configure(background='snow')
                    Label(sc1,text='Enrollment & Name required!!!',fg='red',bg='white',font=('times', 16, ' bold ')).pack()
                    Button(sc1,text='OK',command=del_sc1,fg="black"  ,bg="lawn green"  ,width=9  ,height=1, activebackground = "Red" ,font=('times', 15, ' bold ')).place(x=90,y= 50)


                def err_screen():
                    global sc1
                    sc1 = tk.Tk()
                    sc1.geometry('300x100')
                    sc1.iconbitmap('AMS.ico')
                    sc1.title('Warning!!')
                    sc1.configure(background='snow')
                    Label(sc1,text='Enrollment & Name required!!!',fg='red',bg='white',font=('times', 16, ' bold ')).pack()
                    Button(sc1,text='OK',command=del_sc1,fg="black"  ,bg="lawn green"  ,width=9  ,height=1, activebackground = "Red" ,font=('times', 15, ' bold ')).place(x=90,y= 50)

                ##Error screen2
                def del_sc2():
                    sc2.destroy()
                def err_screen1():
                    global sc2
                    sc2 = tk.Tk()
                    sc2.geometry('300x100')
                    sc2.iconbitmap('AMS.ico')
                    sc2.title('Warning!!')
                    sc2.configure(background='snow')
                    Label(sc2,text='Please enter your subject name!!!',fg='red',bg='white',font=('times', 16, ' bold ')).pack()
                    Button(sc2,text='OK',command=del_sc2,fg="black"  ,bg="lawn green"  ,width=9  ,height=1, activebackground = "Red" ,font=('times', 15, ' bold ')).place(x=90,y= 50)
                def trainimg():
                    print(dir(cv2.face))
                    recognizer = cv2.face.LBPHFaceRecognizer_create()
                    global detector
                    detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
                    try:
                        global faces,Id
                        faces, Id = getImagesAndLabels("TrainingImage")
                    except Exception as e:
                        l='please make "TrainingImage" folder & put Images'
                        Notification.configure(text=l, bg="SpringGreen3", width=50, font=('times', 18, 'bold'))
                        Notification.place(x=350, y=400)

                        recognizer.train(faces, np.array(Id))
                    try:
                        recognizer.save("TrainingImageLabel\Trainner.yml")
                    except Exception as e:
                        q='Please make "TrainingImageLabel" folder'
                        Notification.configure(text=q, bg="SpringGreen3", width=50, font=('times', 18, 'bold'))
                        Notification.place(x=350, y=400)

                    res = "Model Trained"  # +",".join(str(f) for f in Id)
                    Notification.configure(text=res, bg="SpringGreen3", width=50, font=('times', 18, 'bold'))
                    Notification.place(x=250, y=400)
                
                ###For take images for datasets
                def take_img():
                    l1 = txt.get()
                    l2 = txt2.get()
                    if l1 == '':
                        err_screen()
                    elif l2 == '':
                        err_screen()
                    else:
                        try:
                            cam = cv2.VideoCapture(0)
                            detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
                            Enrollment = txt.get()
                            Name = txt2.get()
                            sampleNum = 0
                            while (True):
                                ret, img = cam.read()
                                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                                faces = detector.detectMultiScale(gray, 1.3, 5)
                                for (x, y, w, h) in faces:
                                    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                                    # incrementing sample number
                                    sampleNum = sampleNum + 1
                                    # saving the captured face in the dataset folder
                                    cv2.imwrite("TrainingImage/ " + Name + "." + Enrollment + '.' + str(sampleNum) + ".jpg",
                                        gray[y:y + h, x:x + w])
                                    cv2.imshow('Frame', img)
                                     # wait for 100 miliseconds
                                if cv2.waitKey(1) & 0xFF == ord('q'):
                                    break
                                # break if the sample number is morethan 100
                                elif sampleNum > 70:
                                    break
                            cam.release()
                            cv2.destroyAllWindows()
                            ts = time.time()
                            Date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                            Time = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                            row = [Enrollment, Name, Date, Time]
                            with open('StudentDetails\StudentDetails.csv', 'a+') as csvFile:
                                writer = csv.writer(csvFile, delimiter=',')
                                writer.writerow(row)
                                csvFile.close()
                            res = "Images Saved for Enrollment : " + Enrollment + " Name : " + Name
                            Notification.configure(text=res, bg="SpringGreen3", width=50, font=('times', 18, 'bold'))
                            Notification.place(x=250, y=400)
                        except FileExistsError as F:
                            f = 'Student Data already exists'
                            Notification.configure(text=f, bg="Red", width=21)
                            Notification.place(x=450, y=400)
                def ex():
                    exit()
                def del_sc1():
                    sc1.destroy()
                ###for choose subject and fill attendance
                def subjectchoose():
                    def Fillattendances():
                        sub=tx.get()
                        now = time.time()  ###For calculate seconds of video
                        future = now + 20
                        if time.time() < future:
                            if sub == '':
                                err_screen1()
                            else:
                                recognizer = cv2.face.LBPHFaceRecognizer_create()  # cv2.createLBPHFaceRecognizer()
                                try:
                                    recognizer.read("TrainingImageLabel\Trainner.yml")
                                except:
                                    e = 'Model not found,Please train model'
                                    Notifica.configure(text=e, bg="red", fg="black", width=33, font=('times', 15, 'bold'))
                                    Notifica.place(x=20, y=250)

                                harcascadePath = "haarcascade_frontalface_default.xml"
                                faceCascade = cv2.CascadeClassifier(harcascadePath)
                                df = pd.read_csv("StudentDetails\StudentDetails.csv")
                                cam = cv2.VideoCapture(0)
                                font = cv2.FONT_HERSHEY_SIMPLEX
                                col_names = ['Enrollment', 'Name', 'Date', 'Time']
                                global attendance
                                attendance = pd.DataFrame(columns=col_names)
                                while True:
                                    ret, im = cam.read()
                                    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
                                    faces = faceCascade.detectMultiScale(gray, 1.2, 5)
                                    for (x, y, w, h) in faces:
                                        global Id

                                        Id, conf = recognizer.predict(gray[y:y + h, x:x + w])
                                        if (conf <70):
                                            print(conf)
                                            global Subject
                                            global aa
                                            global date
                                            global timeStamp
                                            Subject = tx.get()
                                            ts = time.time()
                                            date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                                            timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                                            aa = df.loc[df['Enrollment'] == Id]['Name'].values
                                            global tt
                                            tt = str(Id) + "-" + aa
                                            En = '15624031' + str(Id)
                                            attendance.loc[len(attendance)] = [Id, aa, date, timeStamp]
                                            cv2.rectangle(im, (x, y), (x + w, y + h), (0, 260, 0), 7)
                                            cv2.putText(im, str(tt), (x + h, y), font, 1, (255, 255, 0,), 4)

                                        else:
                                            Id = 'Unknown'
                                            tt = str(Id)
                                            cv2.rectangle(im, (x, y), (x + w, y + h), (0, 25, 255), 7)
                                            cv2.putText(im, str(tt), (x + h, y), font, 1, (0, 25, 255), 4)
                                    if time.time() > future:
                                        break

                                    attendance = attendance.drop_duplicates(['Enrollment'], keep='first')
                                    cv2.imshow('Filling attedance..', im)
                                    key = cv2.waitKey(30) & 0xff
                                    if key == 27:
                                        break

                                ts = time.time()
                                date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                                timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                                Hour, Minute, Second = timeStamp.split(":")
                                fileName = Subject + "_" + date + "_" + Hour + "-" + Minute + "-" + Second + ".csv"
                                attendance = attendance.drop_duplicates(['Enrollment'], keep='first')
                                print(attendance)
                                attendance.to_csv(fileName, index=False)
                                #csvfile=r"C:\Users\ADMIN\Downloads\Attendace_management_system-master\Attendace_management_system-master\StudentDetails\StudentDetails.csv"
                                #attendance.to_csv(csvfile)"""
                                ##Create table for Attendance
                                date_for_DB = datetime.datetime.fromtimestamp(ts).strftime('%Y_%m_%d')
                                DB_Table_name = str( Subject + "_" + date_for_DB + "_Time_" + Hour + "_" + Minute + "_" + Second)
                                import pymysql.connections

                                ###Connect to the database
                                try:
                                    global cursor
                                    connection = pymysql.connect(host='localhost', user='root', password='', db='Face_reco_fill')
                                    cursor = connection.cursor()
                                except Exception as e:
                                    print(e)

                                sql = "CREATE TABLE " + DB_Table_name + """
                                (ID INT NOT NULL AUTO_INCREMENT,
                                ENROLLMENT varchar(100) NOT NULL,
                                 NAME VARCHAR(50) NOT NULL,
                                 DATE VARCHAR(20) NOT NULL,
                                 TIME VARCHAR(20) NOT NULL,
                                 PRIMARY KEY (ID)
                                 );
                                """
                                ####Now enter attendance in Database
                                insert_data =  "INSERT INTO " + DB_Table_name + " (ID,ENROLLMENT,NAME,DATE,TIME) VALUES (0, %s, %s, %s,%s)"
                                VALUES = (str(Id), str(aa), str(date), str(timeStamp))
                                try:
                                    cursor.execute(sql)  ##for create a table
                                    cursor.execute(insert_data, VALUES)##For insert data into table
                                except Exception as ex:
                                    print(ex)  #

                                M = 'Attendance filled Successfully'
                                Notifica.configure(text=M, bg="Green", fg="white", width=33, font=('times', 15, 'bold'))
                                Notifica.place(x=20, y=250)

                                cam.release()
                                cv2.destroyAllWindows()

                                import csv
                                import tkinter
                                root = tkinter.Tk()
                                root.title("Attendance of " + Subject)
                                root.configure(background='snow')
                                cs = 'C:\Users\saiva\OneDrive\Desktop\mini\Online-Attendence-Evaluation-System/' + fileName
                                with open(cs, newline="") as file:
                                    reader = csv.reader(file)
                                    r = 0

                                    for col in reader:
                                        c = 0
                                        for row in col:
                                            # i've added some styling
                                            label = tkinter.Label(root, width=8, height=1, fg="black", font=('times', 15, ' bold '),
                                                  bg="lawn green", text=row, relief=tkinter.RIDGE)
                                            label.grid(row=r, column=c)
                                            c += 1
                                        r += 1
                                root.mainloop()
                                print(attendance)

                    ###windo is frame for subject chooser
                    windo = tk.Tk()
                    windo.iconbitmap('AMS.ico')
                    windo.title("Enter subject name...")
                    windo.geometry('580x320')
                    windo.configure(background='snow')
                    Notifica = tk.Label(windo, text="Attendance filled Successfully", bg="Green", fg="white", width=33,
                            height=2, font=('times', 15, 'bold'))

                    def Attf():
                        import subprocess
                        subprocess.Popen(r'explorer /select,"C:/Users/saiva/OneDrive/Desktop/mini/Online-Attendence-Evaluation-System/Attendance/-------Check atttendance-------"')
    
                    attf = tk.Button(windo,  text="Check Sheets",command=Attf,fg="black"  ,bg="lawn green"  ,width=12  ,height=1 ,activebackground = "Red" ,font=('times', 14, ' bold '))
                    attf.place(x=430, y=255)

                    sub = tk.Label(windo, text="Enter Subject", width=15, height=2, fg="white", bg="blue2", font=('times', 15, ' bold '))
                    sub.place(x=30, y=100)

                    tx = tk.Entry(windo, width=20, bg="yellow", fg="red", font=('times', 23, ' bold '))
                    tx.place(x=250, y=105)

                    fill_a = tk.Button(windo, text="Fill Attendance", fg="white",command=Fillattendances, bg="deep pink", width=20, height=2,
                       activebackground="Red", font=('times', 15, ' bold '))
                    fill_a.place(x=250, y=160)
                    windo.mainloop()
                def admin_login():
                        wins = tk.Tk()
                        #win.iconbitmap('AMS.ico')
                        wins.title("LogIn")
                        wins.geometry('880x420')
                        wins.configure(background='snow')
                        def log_in():
                            username = un_entr.get()
                            password = pw_entr.get()
                            print(username,password)

                            if username == 'vamshi' :
                                if password == '12345':
                                    csvfile=r"C:\Users\saiva\OneDrive\Desktop\mini\Online-Attendence-Evaluation-System\StudentDetails\StudentDetails.csv"
                                    dfe=pd.read_csv(csvfile)
                                    print(dfe)
                                    
                        un = tk.Label(wins, text="Enter username", width=15, height=2, fg="white", bg="blue2",
                        font=('times', 15, ' bold '))
                        un.place(x=30, y=50)

                        pw = tk.Label(wins, text="Enter password", width=15, height=2, fg="white", bg="blue2",
                        font=('times', 15, ' bold '))
                        pw.place(x=30, y=150)
                        def c00():
                            un_entr.delete(first=0, last=22)

                        un_entr = tk.Entry(wins, width=20, bg="yellow", fg="red", font=('times', 23, ' bold '))
                        un_entr.place(x=290, y=55)

                        def c11():
                            pw_entr.delete(first=0, last=22)

                        pw_entr = tk.Entry(wins, width=20,show="*", bg="yellow", fg="red", font=('times', 23, ' bold '))
                        pw_entr.place(x=290, y=155)

                        c0 = tk.Button(wins, text="Clear", command=c00, fg="black", bg="deep pink", width=10, height=1,
                            activebackground="Red", font=('times', 15, ' bold '))
                        c0.place(x=690, y=55)

                        c1 = tk.Button(wins, text="Clear", command=c11, fg="black", bg="deep pink", width=10, height=1,
                            activebackground="Red", font=('times', 15, ' bold '))
                        c1.place(x=690, y=155)

                        Login = tk.Button(wins, text="LogIn", fg="black", bg="lime green", width=20,
                            height=2,
                            activebackground="Red",command=log_in, font=('times', 15, ' bold '))
                        Login.place(x=290, y=250)
                        wins.mainloop()
                        

                txt = tk.Entry(window, validate="key", width=20, bg="yellow", fg="red", font=('times', 25, ' bold '))
                txt['validatecommand'] = (txt.register(testVal),'%P','%d')
                txt.place(x=550, y=210)

                lbl2 = tk.Label(window, text="Enter Name", width=20, fg="black", bg="deep pink", height=2, font=('times', 15, ' bold '))
                lbl2.place(x=200, y=300)

                txt2 = tk.Entry(window, width=20, bg="yellow", fg="red", font=('times', 25, ' bold '))
                txt2.place(x=550, y=310)

                clearButton = tk.Button(window, text="Clear",command=clear,fg="black"  ,bg="pink"  ,width=10  ,height=1 ,activebackground = "Red" ,font=('times', 15, ' bold '))
                clearButton.place(x=950, y=210)

                clearButton1 = tk.Button(window, text="Clear",command=clear1,fg="black"  ,bg="pink"  ,width=10 ,height=1, activebackground = "Red" ,font=('times', 15, ' bold '))
                clearButton1.place(x=950, y=310)

                AP = tk.Button(window, text="Check Register students",command=admin_login,fg="black"  ,bg="yellow"  ,width=19 ,height=1, activebackground = "Red" ,font=('times', 15, ' bold '))
                AP.place(x=990, y=410)

                takeImg = tk.Button(window, text="Take Images",command=take_img,fg="white"  ,bg="blue2"  ,width=20  ,height=3, activebackground = "Red" ,font=('times', 15, ' bold '))
                takeImg.place(x=90, y=500)

                trainImg = tk.Button(window, text="Train Images",fg="black",command=trainimg ,bg="lawn green"  ,width=20  ,height=3, activebackground = "Red" ,font=('times', 15, ' bold '))
                trainImg.place(x=390, y=500)

                FA = tk.Button(window, text="Automatic Attendace",fg="white",command=subjectchoose  ,bg="blue"  ,width=20  ,height=3, activebackground = "Red" ,font=('times', 15, ' bold '))
                FA.place(x=690, y=500)

                Notification = tk.Label(window, text="All things good", bg="Green", fg="white", width=15,
                      height=3, font=('times', 17, 'bold'))


                quitWindow = tk.Button(window, text="close", command=ex  ,fg="black"  ,bg="lawn green"  ,width=20  ,height=3, activebackground = "Red" ,font=('times', 15, ' bold '))
                quitWindow.place(x=990, y=500)
                window.mainloop()
                
        
    un = tk.Label(win, text="Enter username", width=15, height=2, fg="white", bg="blue2",
                   font=('times', 15, ' bold '))
    un.place(x=30, y=50)

    pw = tk.Label(win, text="Enter password", width=15, height=2, fg="white", bg="blue2",
                  font=('times', 15, ' bold '))
    pw.place(x=30, y=150)
    def c00():
        un_entr.delete(first=0, last=22)

    un_entr = tk.Entry(win, width=20, bg="yellow", fg="red", font=('times', 23, ' bold '))
    un_entr.place(x=290, y=55)

    def c11():
        pw_entr.delete(first=0, last=22)

    pw_entr = tk.Entry(win, width=20,show="*", bg="yellow", fg="red", font=('times', 23, ' bold '))
    pw_entr.place(x=290, y=155)

    c0 = tk.Button(win, text="Clear", command=c00, fg="black", bg="deep pink", width=10, height=1,
                            activebackground="Red", font=('times', 15, ' bold '))
    c0.place(x=690, y=55)

    c1 = tk.Button(win, text="Clear", command=c11, fg="black", bg="deep pink", width=10, height=1,
                   activebackground="Red", font=('times', 15, ' bold '))
    c1.place(x=690, y=155)

    Login = tk.Button(win, text="LogIn", fg="black", bg="lime green", width=20,
                       height=2,
                       activebackground="Red",command=log_in, font=('times', 15, ' bold '))
    Login.place(x=290, y=250)
    win.mainloop()
trainImg = tk.Button(mainwindow, text="login",fg="black",command=admin_panel ,bg="lawn green"  ,width=20  ,height=3, activebackground = "Red" ,font=('times', 15, ' bold '))
trainImg.place(x=100, y=100)
