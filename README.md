# camTGalert
[![GitHub issues](https://img.shields.io/github/issues/okno/camtgalert.svg)](https://github.com/okno/camtgalert/issues) [![GitHub stars](https://img.shields.io/github/stars/okno/camtgalert.svg)](https://github.com/okno/camtgalert/stargazers) [![Twitter](https://img.shields.io/twitter/url/https/github.com/okno/camtgalert.svg?style=social)](https://twitter.com/intent/tweet?text=Wow:&url=https%3A%2F%2Fgithub.com%2Fokno%2Fcamtgalert)
![GitHub license](https://img.shields.io/github/license/okno/camtgalert.svg)

## Descrizione
**camTGalert** is a Linux cli, GUI &amp; Daemon/Service application that captures images and videos from your webcam, detects motion and sends notifications via Telegram written by Pawel 'okno' Zorzan Urban. 
 All Photos and Videos will be stored on Telegram! (Infinite Space!) :-)

## Main Functions 
- `Capture Photos`
- `Compare Photos`
- `Detect Motion`
- `Highlights Motion Area`
- `Video Record`
- `Daemon Mode`
- `Graphic User Interface`
- `Live Preview`
- `Easy configuration`
- `Configuration Backup`
- `Telegram BOT Connection`
- `Multi Thread`
- `Logging`
- `Auto Cleaning Files`

## Installation
Tested on :
- Debian 12.5 bookworm
- Debian 11.9 bullseye
- Ubuntu 22.04
 
Pyton Versions:
- Python 3.11.2
- Python 3.9.2
### Dependencies
These are the main dependencies:
- git 
- python-telegram-bot
- opencv-python
- opencv-python-headless
- v4l-utils
- tk
- pillow
- telebot

### Download & Install 
To install the depedencies run:
```
$ sudo apt install python3 python3-pip python3-tk git v4l-utils -y
```
Now check if your Camera, Webcam, UVC(USB Video Class) device is correctly connected and the driver has a device: 
```
$ v4l2-ctl --list-devices
```
If you see something like this, your camera should be on the /dev/video0 device. 
```
HP HD Webcam [Fixed]: HP HD Web (usb-0000:00:1a.0-1.3):
        /dev/video0
        /dev/video1
        /dev/media0
```
Clone Repository:
```
$ sudo git clone https://github.com/okno/camtgalert /opt/camtgalert
```
Install Python requirements: 
```bash
$ sudo pip3 install -r /opt/camtgalert/requirements.txt
```
### BOT Installation
- Get BOT from BOTfather in Telegram
- Get Group ID From Telegram
  
Copy the default config file to your new one: 
```
$ sudo cp /opt/camtgalert/bot.config.default /opt/camtgalert/bot.config
```
Edit the configuration and set yout Token and Group ID, to exit the editor press CTRL+X :
```
$ sudo pico /opt/camtgalert/bot.config
```
# Now you are ready to go!
To run the bot exec the follow command and take a look at your Telegram Group or Telegram Chat
```
$ sudo python3 /opt/camtgalert/camtgalert.py 
```
To close the application just press ```CTRL+c``` and wait few seconds to let the ram clean.
# Graphic User Interface 
<p align="center">
<img src="https://raw.githubusercontent.com/okno/camtgalert/master/screenshotGUI.jpeg" /></p>
<center>
 
If you want to use the Graphic User Interface 
```
$ sudo python3 /opt/camtgalert/camtgalert.py --gui
```
To quit the GUI, just press the "Close Monitoring & BOT Connection" button or press X from the titlebar or ```CTRL+c``` from the terminal and wait few seconds to let the ram clean.
If everything is perfect you should see something like this:
```
okno@xuna:/opt/camtgalert$ sudo python3 /opt/camtgalert/camtgalert.py --gui 

camTGalert - Pawel 'okno' Zorzan Urban
             https://pawelzorzan.com

WEBCAM to Telegram Application GUI & Daemon
Connessione ed invio effettuate con successo
 >> Monitoraggio in Corso!
 >> camTGalert terminato con successo!
okno@xuna:/opt/camtgalert$ 
```
### Paths, Logs, Files: 
File | Description
------------- | -------------
/opt/camtgalert/ | Default Working camTGalert Folder
/opt/camtgalert/bot.config | Default Configuration File 
/opt/camtgalert/camtgalert.py | Main Application File
/opt/camtgalert/telegram_functions.py | BOT Functions 
/opt/camtgalert/telegrambotcam.service | Systemd Service Registration file
/opt/camtgalert/video_img | Default Video and Image Folder
/opt/camtgalert/backups | Default Configuraton Backup Folder
/var/log/telegrambotcam.log | Default Logfile 
### Configuration Parameters 
Variabile | Description | Type
------------- | ------------- | -------------
time_recording | Set Recording Time in Seconds (Sec.) | Float
output_folder | Images and Videos Folder | String
max_storage | Max Storage Size in Gigabyte (Gb) | Int
log_file | LOG File full path | String
bot_token | Telegram Token | String 
group_id | Group ID to write on | Int 
### Troubleshooting
To see the logs open another terminal or use tmux and run: 
```
tail -f /var/log/telegrambotcam.log
```
## Issue #1
If you see this error: 
```
Traceback (most recent call last):
  File "/opt/camtgalert/camtgalert.py", line 12, in <module>
    from PIL import Image, ImageTk
ImportError: cannot import name 'ImageTk' from 'PIL' (/usr/lib/python3/dist-packages/PIL/__init__.py)
```
Run this command to solve the problem: 
```sudo pip3 install --upgrade pillow```
## TODO!
- Optimize Threads and Loops 
- Complete English Translate
- Complete Italian Translate

### Contribution
You can contribute in following ways:

   - Report bugs
   - Give suggestions to make it better
   - Fix issues & submit a pull request

### Credits 
 `Pawel Zorzan Urban` alias okno 
Contact | URL
------------- | -------------
Website | https://pawelzorzan.com 
LinkedIN | https://www.linkedin.com/in/pawelzorzan
Twitter | https://twitter.com/pawelzorzan
Do you want to have a conversation in private? Hit me up on my [twitter](https://twitter.com/pawelzorzan)
