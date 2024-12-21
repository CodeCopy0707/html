import os
import telebot
from flask import Flask
import time

# Initialize Flask app
app = Flask(__name__)

# Initialize the TeleBot with your bot token
TOKEN = '7910882641:AAEpXFHQsmArsbRV1_vuXp6u6ys6o42mhdo'  # Replace with your actual bot token
bot = telebot.TeleBot(TOKEN)

# Folder to store the HTML files
html_folder = './html_files/'

# Function to handle /start command
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Welcome! Use /help to see available commands.")

# Function to handle /help command
@bot.message_handler(commands=['help'])
def help(message):
    commands = '''
    /start - Start the bot and get a welcome message.
    /help - Get a list of available commands.
    /listfiles - List all hosted files.
    /upload <file> - Upload a file to host as HTML.
    '''
    bot.reply_to(message, commands)

# Function to handle /listfiles command
@bot.message_handler(commands=['listfiles'])
def listfiles(message):
    files = os.listdir(html_folder)
    if files:
        bot.reply_to(message, "\n".join(files))
    else:
        bot.reply_to(message, "No files are currently hosted.")

# Function to handle /upload command
@bot.message_handler(commands=['upload'])
def upload(message):
    if message.document:
        file = message.document
        file_path = f"./uploads/{file.file_name}"

        # Download the file
        file.download(file_path)

        # Convert the file to HTML
        if file.file_name.endswith('.txt'):
            html_file = convert_to_html(file_path)
            hosted_url = f"http://localhost:5000/{os.path.basename(html_file)}"  # Replace with your server IP for remote hosting
            bot.reply_to(message, f"File uploaded and converted to HTML. You can access it at: {hosted_url}")
        else:
            bot.reply_to(message, "Only .txt files are supported for conversion to HTML.")
    else:
        bot.reply_to(message, "Please upload a file to host.")

# Function to convert file to HTML (Simple example for text files)
def convert_to_html(file_path):
    file_name = os.path.basename(file_path)
    html_file_path = os.path.join(html_folder, file_name.replace('.txt', '.html'))
    
    with open(file_path, 'r') as f:
        content = f.read()
    
    with open(html_file_path, 'w') as f:
        f.write(f"<html><body><pre>{content}</pre></body></html>")
    
    return html_file_path

# Start bot polling
bot.polling()
