# camTGalert
[![GitHub issues](https://img.shields.io/github/issues/okno/camtgalert.svg)](https://github.com/okno/camtgalert/issues) [![GitHub stars](https://img.shields.io/github/stars/okno/camtgalert.svg)](https://github.com/okno/camtgalert/stargazers) [![Twitter](https://img.shields.io/twitter/url/https/github.com/okno/camtgalert.svg?style=social)](https://twitter.com/intent/tweet?text=Wow:&url=https%3A%2F%2Fgithub.com%2Fokno%2Fcamtgalert)
![GitHub license](https://img.shields.io/github/license/okno/camtgalert.svg)

## Descrizione
**camTGalert** is a Linux cli, GUI &amp; Daemon/Service application that captures images and videos from your webcam, detects motion and sends notifications via Telegram written by Pawel 'okno' Zorzan Urban.
All Photo and Videos will be stored on Telegram! (Infinite Space!) :-)

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
Tested on Debian 12, Ubuntu 22.04
### Dependencies
These are the main dependencies:
- git 
- python-telegram-bot
- opencv-python
- opencv-python-headless
- v4l-utils

### Download & Install 
Install git:
```
$ sudo apt install git -y
```
Clone Repository:
```
$ sudo git clone https://github.com/okno/camtgalert /opt/camtgalert
```
To install the depedencies run:
```
$ sudo apt install v4l-utils -y
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



```bash
sudo pip3 install -r /opt/camtgalert/requirements.txt
```
### Core 

Core Configurations

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

### Configuration Parameters 
Variabile | Description | Type
------------- | ------------- | -------------
time_recording | Set Recording Time in Seconds (Sec.) | Float
output_folder | Images and Videos Folder | String
max_storage | Max Storage Size in Gigabyte (Gb) | Int
log_file | LOG File full path | String
bot_token | Telegram Token | String 
group_id | Group ID to write on | Int 

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
website | https://pawelzorzan.com 
linkedin | https://www.linkedin.com/in/pawelzorzan

Do you want to have a conversation in private? Hit me up on my [twitter](https://twitter.com/pawelzorzan)
