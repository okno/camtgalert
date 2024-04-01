import cv2
import time
import os
import shutil
import logging
import subprocess
import configparser
import threading
import tkinter as tk
import numpy as np
from datetime import datetime
from PIL import Image, ImageTk
from queue import Queue
import telegram_functions as tf
import sys

def print_header():
    if os.geteuid() != 0:
        print("Devi eseguire questo programma come utente root.")
        exit()
    header = """
\033[1;31mcamTGalert - Pawel 'okno' Zorzan Urban
             https://pawelzorzan.com"""
    print(header)

def print_instructions():
    instructions = """
\033[1;32mWEBCAM to Telegram Application GUI & Daemon\033[0m"""
    print(instructions)

def check_dependencies():
    dependencies = ['python-telegram-bot', 'opencv-python', 'opencv-python-headless']
    missing_dependencies = []
    for dependency in dependencies:
        try:
            subprocess.check_output(['pip3', 'show', dependency])
        except subprocess.CalledProcessError:
            missing_dependencies.append(dependency)

    if missing_dependencies:
        print("\033[1;31mAttenzione: Le seguenti dipendenze sono mancanti:\033[0m")
        for dependency in missing_dependencies:
            print(f" - {dependency}")
        print("\033[1;31mPer favore, esegui i seguenti comandi per ottenerle tramite pip3:\033[0m")
        print("   - pip3 install " + " ".join(missing_dependencies))
        exit()
    try:
        subprocess.check_output(['v4l2-ctl', '--version'])
    except subprocess.CalledProcessError:
        print("\033[1;31mAttenzione: Il comando v4l2-ctl non è installato sul sistema.\033[0m")
        print("\033[1;31mAssicurati di avere installato il pacchetto v4l-utils.\033[0m")
        exit()

# Funzione per ottenere le informazioni sulla telecamera
def get_camera_info():
    try:
        output = subprocess.check_output(['v4l2-ctl', '--list-devices']).decode('utf-8')
        first_line = output.split('\n')[0] 
        return first_line
    except subprocess.CalledProcessError as e:
        logging.error("Errore durante l'esecuzione di v4l2-ctl per ottenere le informazioni sulla telecamera.")
        return "Informazioni sulla telecamera non disponibili"

# Funzione per aggiornare i contatori nella GUI
def update_counters():
    lbl_images_count.config(text=f"Foto acquisite: {image_count}")
    lbl_videos_count.config(text=f"Video registrati: {video_count}")
    root.after(100, update_counters)  # Chiamata ricorsiva per aggiornare i contatori ogni 100 millisecondi

# Funzione per acquisire immagini e rilevare il movimento
def capture_images_and_detect_motion(cap, fgbg, time_recording, output_folder, MIN_CONTOUR_AREA,
                                     bot, first_send_successful, exit_event, image_thumbnails_queue):
    global image_count, video_count
    image_count = 0  
    video_count = 0  

    def cleanup_folder():
        folder_size = sum(os.path.getsize(os.path.join(output_folder, f)) for f in os.listdir(output_folder) if os.path.isfile(os.path.join(output_folder, f)))
        folder_size_gb = folder_size / (1024 ** 3)  # Converti in gigabyte
        max_storage_gb = float(config.get('General', 'max_storage'))

        if folder_size_gb > max_storage_gb:
            files = sorted(os.listdir(output_folder), key=lambda x: os.path.getmtime(os.path.join(output_folder, x)))
            files_to_keep = files[-10:]  # Mantieni solo gli ultimi 10 file
            for file in files:
                if file not in files_to_keep:
                    os.remove(os.path.join(output_folder, file))
            logging.info("Effettuata Pulizia Cartella Dati")

    try:
        while not exit_event.is_set():
            cleanup_folder()  # Controlla e pulisce la cartella prima di acquisire nuovi file
            ret, frame = cap.read()
            if not ret:
                break
            fgmask = fgbg.apply(frame)
            blur = cv2.GaussianBlur(fgmask, (5, 5), 0)
            ret, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
            contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            motion_detected = False
            for contour in contours:
                if cv2.contourArea(contour) > MIN_CONTOUR_AREA:
                    motion_detected = True
                    x, y, w, h = cv2.boundingRect(contour)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                    break
            if motion_detected:
                logging.info("Rilevato Movimento - %s", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                now = datetime.now()
                video_filename = f"{output_folder}/motion_{now.strftime('%Y%m%d%H%M%S')}.avi"
                out = cv2.VideoWriter(video_filename, cv2.VideoWriter_fourcc(*'XVID'), 20.0,
                                      (int(cap.get(3)), int(cap.get(4))))
                start_time = time.time()
                last_image_filenames = []
                while time.time() - start_time < time_recording and not exit_event.is_set():
                    ret, frame = cap.read()
                    if not ret:
                        break
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                    out.write(frame)
                    if len(last_image_filenames) < 2:
                        image_filename = f"{output_folder}/motion_{now.strftime('%Y%m%d%H%M%S')}_{len(last_image_filenames) + 1}.jpg"
                        cv2.imwrite(image_filename, frame)
                        last_image_filenames.append(image_filename)
                out.release()
                if os.path.exists(video_filename):
                    for image_filename in last_image_filenames:
                        tf.send_photo(bot, image_filename)
                        img = Image.open(image_filename)
                        img.thumbnail((150, 150))
                        image_thumbnails_queue.put(img)
                        time.sleep(0.5)
                    tf.send_video(bot, video_filename)
                    os.remove(video_filename)
                    camera_info = get_camera_info()
                    message = f"ATTENZIONE: Rilevato movimento \nPostazione: {os.uname().nodename}, Telecamera: {camera_info}, Data e Ora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                    bot.send_message(tf.telegram_group_id, text=message)
                    if first_send_successful:
                        print("\033[92mConnessione ed invio effettuate con successo\033[0m")
                        print(" >> Monitoraggio in Corso!")
                        first_send_successful = False
                    image_count += len(last_image_filenames)
                    video_count += 1
                else:
                    logging.error("Errore durante l'invio del video")
    except KeyboardInterrupt:
        cap.release()
        cv2.destroyAllWindows()
        tf.exit_and_clear_ram(bot)

# Funzione per chiudere l'applicazione
def close_app():
    exit_event.set()
    tf.exit_and_clear_ram(bot)
    root.quit()

# Funzione per aggiornare le anteprime delle immagini nella GUI
def update_image_thumbnails():
    if not image_thumbnails_queue.empty():
        img = image_thumbnails_queue.get()
        img_thumbnail = ImageTk.PhotoImage(img)
        lbl_image_thumbnail.config(image=img_thumbnail)
        lbl_image_thumbnail.image = img_thumbnail
    root.after(100, update_image_thumbnails)  # Richiama la funzione dopo 100 millisecondi

def open_link(event):
    import webbrowser
    webbrowser.open_new("https://pawelzorzan.com")

def open_config_window():
    config_window = tk.Toplevel(root)
    config_window.title("Modifica Configurazione")
    
    # Leggi il file di configurazione
    config = configparser.ConfigParser()
    config.read('bot.config')
    
    time_recording_var = tk.StringVar(value=config.get('General', 'time_recording'))
    output_folder_var = tk.StringVar(value=config.get('General', 'output_folder'))
    media_size = tk.StringVar(value=config.get('General', 'max_storage'))
    log_file = tk.StringVar(value=config.get('General', 'log_file'))
    bot_token_var = tk.StringVar(value=config.get('Telegram', 'bot_token'))
    group_id_var = tk.StringVar(value=config.get('Telegram', 'group_id'))
    
    # Etichette e widget per la modifica dei valori di configurazione
    tk.Label(config_window, text="Tempo di registrazione (secondi):").grid(row=0, column=0, sticky="w")
    tk.Entry(config_window, textvariable=time_recording_var).grid(row=0, column=1)
    
    tk.Label(config_window, text="Cartella di destinazione:").grid(row=1, column=0, sticky="w")
    tk.Entry(config_window, textvariable=output_folder_var).grid(row=1, column=1)
    
    tk.Label(config_window, text="Token del BOT:").grid(row=2, column=0, sticky="w")
    tk.Entry(config_window, textvariable=bot_token_var).grid(row=2, column=1)
    
    tk.Label(config_window, text="ID del gruppo:").grid(row=3, column=0, sticky="w")
    tk.Entry(config_window, textvariable=group_id_var).grid(row=3, column=1)
    
    tk.Label(config_window, text="Dimensione Storage (Gb):").grid(row=4, column=0, sticky="w")
    tk.Entry(config_window, textvariable=media_size).grid(row=4, column=1)

    tk.Label(config_window, text="Log file:").grid(row=5, column=0, sticky="w")
    tk.Entry(config_window, textvariable=log_file).grid(row=5, column=1)

    # Funzione per salvare le modifiche e creare un backup del file di configurazione
    def save_config():
        config.set('General', 'time_recording', time_recording_var.get())
        config.set('General', 'output_folder', output_folder_var.get())
        config.set('Telegram', 'bot_token', bot_token_var.get())
        config.set('Telegram', 'group_id', group_id_var.get())
        config.set('General', 'max_storage', media_size.get())
        config.set('General', 'log_file', log_file.get())

        with open('bot.config', 'w') as config_file:
            config.write(config_file)
        
        # Crea una copia di backup del file di configurazione
        backup_folder = 'backups'
        if not os.path.exists(backup_folder):
            os.makedirs(backup_folder)
        backup_filename = f"{backup_folder}/bot.config.backup_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        shutil.copyfile("bot.config", backup_filename)
        
        config_window.destroy()  # Chiudi la finestra di modifica configurazione
    
    # Pulsante per salvare le modifiche
    save_button = tk.Button(config_window, text="Save & Backup", command=save_config)
    save_button.grid(row=7, column=0, columnspan=2, pady=10)

# Leggi il file di configurazione
config = configparser.ConfigParser()
config.read('bot.config')
time_recording = float(config.get('General', 'time_recording'))
output_folder = config.get('General', 'output_folder')
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

print_header()
check_dependencies()
print_instructions()

log_file_var= config.get('General', 'log_file')

# DEBUG Area 
# print(f"DEBUG {log_file_var}")

if "--gui" in sys.argv[1:]:
    root = tk.Tk()
    root.title("camTGalert")

    exit_event = threading.Event()

    root.protocol("WM_DELETE_WINDOW", close_app)

    exit_button = tk.Button(root, text="Close Monitoring & BOT Connection", command=close_app)
    exit_button.grid(row=4, column=0, columnspan=2, pady=10)

    lbl_images_count = tk.Label(root, text="Foto acquisite: 0")
    lbl_images_count.grid(row=2, column=1, padx=5, pady=5)

    lbl_videos_count = tk.Label(root, text="Video registrati: 0")
    lbl_videos_count.grid(row=3, column=1, padx=5, pady=5)

    lbl_image_thumbnail = tk.Label(root)  # Aggiunto questo label per le anteprime delle immagini
    lbl_image_thumbnail.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

    # Coda per le anteprime delle immagini
    image_thumbnails_queue = Queue()

    cap = cv2.VideoCapture(0)
    fgbg = cv2.createBackgroundSubtractorMOG2(history=100, varThreshold=50, detectShadows=True)
    MIN_CONTOUR_AREA = 1000

    bot = tf.initialize_bot()
    first_send_successful = True

    threading.Thread(target=capture_images_and_detect_motion, args=(cap, fgbg, time_recording, output_folder,
                                                                     MIN_CONTOUR_AREA, bot, first_send_successful,
                                                                     exit_event, image_thumbnails_queue)).start()

    update_counters()  
    update_image_thumbnails()

    config_button = tk.Button(root, text="Modifica Configurazione", command=open_config_window)
    config_button.grid(row=0, column=0, columnspan=2, pady=10)

    
    developed_by_label = tk.Label(root, text="Sviluppato da Pawel 'okno' Zorzan Urban", font=("Helvetica", 8), fg="blue", cursor="hand2")
    developed_by_label.grid(row=6, column=0, columnspan=2)
    developed_by_label.bind("<Button-1>", open_link) 

    root.mainloop()
else:
    cap = cv2.VideoCapture(0)
    fgbg = cv2.createBackgroundSubtractorMOG2(history=100, varThreshold=50, detectShadows=True)
    MIN_CONTOUR_AREA = 1000

    bot = tf.initialize_bot()
    first_send_successful = True

    exit_event = threading.Event()

    # Coda per le anteprime delle immagini
    image_thumbnails_queue = Queue()

    try:
        capture_images_and_detect_motion(cap, fgbg, time_recording, output_folder, MIN_CONTOUR_AREA,
                                         bot, first_send_successful, exit_event, image_thumbnails_queue)
    except KeyboardInterrupt:
        cap.release()
        cv2.destroyAllWindows()
        tf.exit_and_clear_ram(bot)
