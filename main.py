from config.apiKey import ACCESS_TOKEN, ID_CHAT
from telebot import TeleBot, types
from tkinter import Tk, Label
from io import BytesIO
import webbrowser
import pyautogui
import psutil
import os
import threading

bot = TeleBot(ACCESS_TOKEN, parse_mode=None)

waiting_for_url = {}
waiting_for_text = {}
waiting_for_program_name = {}
waiting_for_confirmation = {}


def start_running():
    start_message = "Your computer is running. Please use /start or /help for assistance."
    bot.send_message(ID_CHAT, start_message)


start_running()


@bot.message_handler(commands=["help", "start"])
def send_message(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    buttons = [
        types.KeyboardButton("Screenshot 🖥️"),
        types.KeyboardButton("Tasklist 📑"),
        types.KeyboardButton("Stop App ❌"),
        types.KeyboardButton("Notification 🔔"),
        types.KeyboardButton("Open Url 🔗"),
        types.KeyboardButton("Restart 🔄"),
        types.KeyboardButton("Shutdown 🅾️")
    ]
    markup.add(*buttons)
    bot.send_message(message.chat.id, "Choose an option:", reply_markup=markup)


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if message.text in ["Screenshot 🖥️", "/screenshot"]:
        take_screenshot(message)
    elif message.text in ["Tasklist 📑", "/tasklist"]:
        show_tasklist(message)
    elif message.text in ["Stop App ❌", "/stopapp"]:
        request_text_input(message, "end_application")
    elif message.text in ["Notification 🔔", "/notification"]:
        request_text_input(message, "show_text")
    elif message.text in ["Open Url 🔗", "/openurl"]:
        request_text_input(message, "open_url")
    elif message.text in ["Shutdown 🅾️", "/shutdown", "Restart 🔄", "/restart"]:
        confirmation_handler(message, message.text)
    elif waiting_for_confirmation.get(message.chat.id):
        confirm_shutdown_restart(message)
    else:
        handle_waiting_for_input(message)


def show_inbox_message_gui_thread(text):
    def run_gui():
        top = Tk()
        top.title("Notification")
        top.attributes('-topmost', True)
        top.geometry("+%d+%d" % (top.winfo_screenwidth() // 2 - 200, top.winfo_screenheight() // 2 - 100))
        label = Label(top, text=text, padx=40, pady=40)
        label.pack()

        top.mainloop()

    # Start the GUI in a separate thread
    gui_thread = threading.Thread(target=run_gui, daemon=True)
    gui_thread.start()


# Update the show_inbox function to call the threaded version
def show_inbox(message):
    chat_id = message.chat.id
    if waiting_for_text.get(chat_id):
        text_to_show = message.text
        show_inbox_message_gui_thread(text_to_show)
        bot.send_message(chat_id, "Message displayed in GUI.")
        waiting_for_text[chat_id] = False


def take_screenshot(message):
    screenshot = pyautogui.screenshot()
    image_stream = BytesIO()
    screenshot.save(image_stream, format='PNG')
    image_stream.seek(0)
    bot.send_photo(message.chat.id, image_stream, caption="Here's the screenshot")


def show_tasklist(message):
    running_apps = {proc.info['name'] for proc in psutil.process_iter(['pid', 'name'])}
    if running_apps:
        bot.send_message(message.chat.id, '\n'.join(running_apps))
    else:
        bot.send_message(message.chat.id, "No running applications.")


def request_text_input(message, input_type):
    chat_id = message.chat.id
    if input_type == "show_text":
        bot.send_message(chat_id, "Enter message to display:")
        waiting_for_text[chat_id] = True
    elif input_type == "open_url":
        bot.send_message(chat_id, "Enter URL to open:")
        waiting_for_url[chat_id] = True
    elif input_type == "end_application":
        bot.send_message(chat_id, "Enter the program name to terminate:")
        waiting_for_program_name[chat_id] = True


def confirmation_handler(message, operation):
    chat_id = message.chat.id
    waiting_for_confirmation[chat_id] = operation
    bot.send_message(chat_id, f"Are you sure you want to {operation}? Type 'yes' to confirm or 'no' to cancel.")


def confirm_shutdown_restart(message):
    chat_id = message.chat.id
    text = message.text.lower()
    operation = waiting_for_confirmation[chat_id]

    if text == "yes":
        if operation in ["Shutdown 🅾️" or "/shutdown"]:
            os.system("shutdown /s /t 1")
            bot.send_message(chat_id, "Shutdown initiated.")
        elif operation in ["Restart 🔄" or "/restart"]:
            os.system("shutdown /r /t 1")
            bot.send_message(chat_id, "Restart initiated.")
    elif text == "no":
        bot.send_message(chat_id, f"{operation} cancelled.")
    else:
        bot.send_message(chat_id, "Please type 'yes' to confirm or 'no' to cancel.")
    waiting_for_confirmation[chat_id] = None


def handle_waiting_for_input(message):
    chat_id = message.chat.id
    if waiting_for_text.get(chat_id):
        show_inbox(message)
    elif waiting_for_url.get(chat_id):
        open_url(message)
    elif waiting_for_program_name.get(chat_id):
        end_application(message)


def open_url(message):
    chat_id = message.chat.id
    try:
        url = message.text
        if not url.startswith("http"):
            url = "https://" + url
        webbrowser.open(url)
        bot.send_message(chat_id, f"Opened URL: {url}")
    except Exception as e:
        bot.send_message(chat_id, "Failed to open URL.")
    finally:
        waiting_for_url[chat_id] = False


def end_application(message):
    chat_id = message.chat.id
    program_name = message.text.lower()
    for proc in psutil.process_iter(['name']):
        if program_name in proc.info['name'].lower():
            proc.kill()
            bot.send_message(chat_id, f"Terminated: {proc.info['name']}")
            break
    else:
        bot.send_message(chat_id, "No matching application found.")
    waiting_for_program_name[chat_id] = False


if __name__ == "__main__":
    bot.infinity_polling()
