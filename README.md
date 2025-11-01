## 🖥️ Keylogger 5155

A **Python-based GUI Keylogger** built with `CustomTkinter`, `Pynput`, and `Pillow`, capable of capturing keyboard inputs, **screenshots**, **clipboard data**, and **system information** — all managed via a beautiful graphical interface.

## Overview

This project demonstrates how real-time keylogging, screenshot capturing, and automated reporting can be implemented securely using Python.
It provides:

* An interactive GUI to control all operations.
* Automatic logging of keyboard activity and clipboard data.
* Screenshot capture at some defined intervals.
* Optional email delivery of all collected logs.

## Features

### 1. **Keylogging**

* Captures every keystroke pressed on the keyboard.
* Logs include letters, numbers, function keys, and special keys (`Enter`, `Backspace`, etc.).
* Stored safely in:
  ```
  app/data/key_log.txt
  ```

### 2. **Clipboard Capture**

* Periodically reads clipboard data (text).
* Stores the last copied text content into:
  ```
  app/data/clipboard.txt
  ```

### 3️. **Screenshot Capturing**

* Takes full-screen screenshots at regular intervals using `Pillow (PIL)`.
* The image is timestamped and saved automatically.
* All screenshots are stored as PNGs in:
  ```
  app/data/screenshots/
  ```

### 4️. **System Information Logging**

* Gathers important device details such as:
  * OS name and version
  * Hostname
  * Processor type
  * IP address
* Saved in:
  ```
  app/data/systeminfo.txt
  ```

### 5. **Email Automation**

* Periodically sends collected logs and screenshots as ZIP file via email.
* Credentials and recipient are securely managed via `.env` file.

## 📁Folder Structure

```
📦 GKeylogger-5155
├── app/
│   ├── data/
│   │   ├── key_log.txt
│   │   ├── clipboard.txt
│   │   ├── systeminfo.txt
│   │   └── screenshots/
│   │       └── *.png
│   ├── .gitignore
│   ├── guikeylogger.py
│   ├── requirements.txt 
├── config.json
├── package.json
└── README.md
```

## Tech Stack

* **Python 3.9+**
* **CustomTkinter**
* **Pynput**
* **Pillow (PIL)**
* **Pyperclip**
* **smtplib (built-in)**
* **python-dotenv 1.0+**

## Installation & Setup

### 1. Clone Repository

```bash
git clone https://github.com/<your-username>/Keylogger5155.git
cd Keylogger5155/app
```

### 2. Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate     # Windows
source venv/bin/activate  # Linux/Mac
```

### 3. Install Requirements

```bash
pip install -r requirements.txt
```

### 4. Configure Environment

Create a `.env` file:

```bash
email=email@gmail.com
pass=password
```

### 6. Run the App

```bash
python guikeylogger.py
```

## Example Output

```
📁 data/
├── key_log.txt
│    [2025-11-01 08:30:12] Key pressed: A
│    [2025-11-01 08:30:13] Key pressed: B

├── clipboard.txt
│    Copied Text: "Hello World"

├── screenshots/
│    screenshot_2025-11-01_08-31-00.png

└── systeminfo.txt
│    OS: Windows 10
│    Hostname: user-PC
│    Processor: Intel Core i5
│    IP: 192.xxx.x.5
```

## Contributing

1. Fork the repo
2. Create a feature branch
   ```bash
   git checkout -b feature-name
   ```
3. Commit changes
   ```bash
   git commit -m "Added new feature"
   ```
4. Push and create a Pull Request

## Community

This project is part of Opcode, IIIT Bhagalpur. Maintainers will review PRs, suggest changes, and merge contributions. Use Issues to report bugs or suggest features.
