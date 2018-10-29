#!/usr/bin/env python
# -*- coding: utf-8 -*-

import telebot, time, logging, subprocess
from telebot import types
import requests

logger = telebot.logger
bot = telebot.TeleBot("") # your bot ID goes here

telebot.logger.setLevel(logging.DEBUG)

time_ignore = 5 * 60
allowed_numbers = [203526833] # replace with your user ID

base_url = 'http://192.168.0.4:82' # replace with your NodeMCU ip address
turn_on_endpoint = '/on'
turn_off_endpoint = '/off'
status_endpoint = '/status'

def make_request(url):
    """Makes web request to specified url. Returns response text"""
    try:
        req = requests.get(url)
    except requests.exceptions.RequestException as e:
        return 'error' + str(e)
    return req.text.replace('\n', '')

def return_default_kbd():
    """Creates and returns the default markup keyboard"""
    markup = types.ReplyKeyboardMarkup()
    buttonOn = types.KeyboardButton('/on')
    buttonOff = types.KeyboardButton('/off')
    buttonStatus = types.KeyboardButton('/status')
    buttonKeepOn = types.KeyboardButton('/keeponfor')
    markup.row(buttonOn, buttonOff)
    markup.row(buttonStatus)
    markup.row(buttonKeepOn)
    return markup

@bot.message_handler(commands=['start'])
def handle_start_help(m):
    if (int(time.time()) - time_ignore) > m.date:
        return
    bot.send_message(m.chat.id, 'Please choose an action. ' + str(m.chat.id), reply_markup = return_default_kbd())

@bot.message_handler(commands=['on'])
def turn_on(m):
    """Manually turns on the heater"""
    if (int(time.time()) - time_ignore) > m.date:
       return
    if(m.chat.id not in allowed_numbers):
       return
    bot.send_message(m.chat.id, 'Heat turned on ' + make_request(base_url + turn_on_endpoint))

@bot.message_handler(commands=['off'])
def turn_off(m):
    """Manually turns off the heater"""
    if (int(time.time()) - time_ignore) > m.date:
        return
    if(m.chat.id not in allowed_numbers):
        return
    bot.send_message(m.chat.id, 'Heat turned off ' + make_request(base_url + turn_off_endpoint))

@bot.message_handler(commands=['status'])
def status(m):
    """Gets the current heater status (On or off)"""
    if (int(time.time()) - time_ignore) > m.date:
        return
    if(m.chat.id not in allowed_numbers):
        return
    req = make_request(base_url + status_endpoint)
    status = 'off' if int(req) == 0 else 'on'
    bot.send_message(m.chat.id, 'Currently, heat is ' + status)


@bot.message_handler(commands=['keeponfor'])
def keep_on_for_handler(m):
    if (int(time.time()) - time_ignore) > m.date:
        return
    if(m.chat.id not in allowed_numbers):
        return

    markup = types.ReplyKeyboardMarkup(one_time_keyboard = True)
    button_1_hour = types.KeyboardButton('1 hour')
    button_2_hours = types.KeyboardButton('2 hours')
    button_3_hours = types.KeyboardButton('3 hours')
    button_6_hours = types.KeyboardButton('6 hours')
    button_12_hours = types.KeyboardButton('12 hours')
    button_24_hours = types.KeyboardButton('24 hours')
    button_cancel = types.KeyboardButton('Cancel')
    markup.row(button_1_hour, button_2_hours, button_3_hours)
    markup.row(button_6_hours, button_12_hours, button_24_hours)
    markup.row(button_cancel)

    msg = bot.send_message(m.chat.id, 'For how long?', reply_markup = markup)
    bot.register_next_step_handler(msg, keep_on_for)

def keep_on_for(m):
    """Turns heater on and keeps it on for the specified amount of time"""
    if (int(time.time()) - time_ignore) > m.date:
        return
    chat_text = m.text.replace('/keeponfor ', '').lower()
    if(m.chat.id not in allowed_numbers):
        return
    if chat_text == 'cancel':
        bot.send_message(m.chat.id, 'Cancelled', reply_markup = types.ReplyKeyboardRemove(selective = False))
        return

    end_command = 'at now + {} -f ./turnOffHeat.sh'.format(chat_text)
    process = subprocess.Popen(end_command, shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    _, atoutput = process.communicate()

    output = ''
    if process.returncode == 0:
        make_request(base_url + turn_on_endpoint) # turn on heating
        output += 'Successfully scheduled. Heat will be turned off at ' + atoutput[-21:-5]
    else:
        output += 'An error has occurred'
    
    bot.send_message(m.chat.id, output, reply_markup = types.ReplyKeyboardRemove(selective = False))

@bot.message_handler(commands=['clearall'])
def clear_all(m):
    """Deletes all AT jobs from the system"""
    if (int(time.time()) - time_ignore) > m.date:
        return
    if(m.chat.id not in allowed_numbers):
        return
    command = 'for i in `atq | awk \'{print $1}\'`;do atrm $i;done'
    process = subprocess.Popen(command, shell = True, stdout = subprocess.PIPE)
    process.communicate()
    bot.send_message(m.chat.id, 'Successfully deleted all heat jobs')

bot.polling(none_stop = True)
