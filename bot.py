# -*- coding: utf-8 -*-

import requests

from time import sleep

url = "https://api.telegram.org/bot" + "567208933:AAHo5Yp9YQDCOQ5jYh06T-uYZ9_EYApQ4tI/"

f = open('log.txt', 'a')


def get_updates_json(request):  
    params = {'timeout': 100, 'offset': None}
    response = requests.get(request + 'getUpdates', data=params)
    return response.json()


def last_update(data):  
    results = data['result']
    total_updates = len(results) - 1
    return results[total_updates]

def get_chat_id(update):  
    chat_id = update['message']['chat']['id']
    return chat_id

def get_text(update):  
    text = update['message']['text']
    print(text)
    return text

def get_name(update):  
    name = update['message']['from']['first_name']
    lastname = update['message']['from']['last_name']
    return name,lastname

def send_mess(chat, text):  
    params = {'chat_id': chat, 'text': text}
    response = requests.post(url + 'sendMessage', data=params)
    return response

def send_stick(chat, stick):  
    params = {'chat_id': chat, 'sticker': stick}
    response = requests.post(url + 'sendSticker', data=params)
    return response

#def geophone():
#
#    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
#    button_phone = types.KeyboardButton(text="Отправить номер телефона", request_contact=True)
#    button_geo = types.KeyboardButton(text="Отправить местоположение", request_location=True)
#    keyboard.add(button_phone, button_geo)
#    pass

    
def main():  
    update_id = last_update(get_updates_json(url))['update_id']
    while True:
    	update = last_update(get_updates_json(url))
        if update_id == update['update_id']:
           name = get_name(update)
           text = get_text(update)
           send_mess(get_chat_id(update), 'Добрый день выберите услугу:')
#           geophone()
           		#send_stick(get_chat_id(update), 'CAADAgADGQAD3xibF1YNx5YnXjycAg')
           #inputText = get_text(update)

           #inputText.encode('utf-8')
           #f.write (inputText)

           update_id += 1
        sleep(1)       

if __name__ == '__main__':  
    main()
