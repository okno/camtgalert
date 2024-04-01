# telegram_functions.py

import telebot
import os
import logging
import configparser

config = configparser.ConfigParser()
config.read('bot.config')
bot_token = config.get('Telegram', 'bot_token')
telegram_group_id = config.getint('Telegram', 'group_id')
log_file_var = config.get('General', 'log_file')

# Configura il livello di logging desiderato
logging.basicConfig(filename=log_file_var, level=logging.DEBUG)

# Inizializza il bot di Telegram
def initialize_bot():
    bot = telebot.TeleBot(bot_token)
    logging.info("Bot inizializzato con successo.")
    return bot
def send_photo(bot, photo_path):
    with open(photo_path, 'rb') as photo:
        bot.send_photo(telegram_group_id, photo)
    logging.info("Foto inviata con successo.")
def send_video(bot, video_path):
    with open(video_path, 'rb') as video:
        bot.send_video(telegram_group_id, video)
    logging.info("Video inviato con successo.")
def send_message(bot, message):
    bot.send_message(telegram_group_id, text=message)
    logging.info("Messaggio inviato con successo.")

# Rimuovere dalla ram i dati del bot ed uscire
def exit_and_clear_ram(bot):
    logging.info("Uscita dal programma e pulizia della RAM...")
    del bot
    import subprocess
    subprocess.run(["sync"])
    subprocess.run(["sudo", "swapoff", "-a"])
    subprocess.run(["sudo", "sh", "-c", "echo 3 > /proc/sys/vm/drop_caches"])
    subprocess.run(["sudo", "swapon", "-a"])
    print(" >> camTGalert terminato con successo!")
    import sys
    sys.exit()
