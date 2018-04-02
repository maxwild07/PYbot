

# -*- coding: utf-8 -*-

import requests
import telebot
from telebot import types
from time import sleep

TOKEN = '552505551:AAHEYUk1x8uXX9HWTMG-KY9PBevdj1OJeZA'

MONEY = 0 # exchange rates

CONV_DIR = 0 # convertation direction

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=["start"])
def first_start(message):
	bot.send_message(message.chat.id, "Доброго времени суток, {}, я могу помочь Вам с решением ежедневных задач".format(message.from_user.first_name))
	start(message)

def start(message): 
	keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
	keyboard.add(*[types.KeyboardButton(name) for name in ['Погода', 'Курс Валют', 'Новости']])
	bot.send_message(message.chat.id, 'Выберите нужную функцию',reply_markup=keyboard)


@bot.message_handler(regexp="Погода")
def weather(message): 
	response = requests.get("https://api.apixu.com/v1/forecast.json?key=4f177201ebb542d5a54184431180104&q=Kiev&lang=ru&days=2")
	data = response.json()
	description = data['current']['condition']['text']
	temp = data['current']['temp_c']
	temp_min = data['forecast']['forecastday'][0]['day']['mintemp_c']
	temp_max = data['forecast']['forecastday'][0]['day']['maxtemp_c']
	temp_feel = data['current']['feelslike_c']
	weatherID = data['current']['condition']['code']
	precipitation = data['forecast']['forecastday'][0]['day']['totalprecip_mm']
	emoji = getEmoji(weatherID)
	keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
	keyboard.add(*[types.KeyboardButton(name) for name in ['На завтра','Меню']])
	bot.send_message(message.chat.id, "Сегодня у нас " + description + emoji + 
									"\nТемпература составит " +str(int(temp_min))+"..."+str(int(temp_max))+"℃."+
									"\nОсадки: " + str(int(precipitation)) + " мм." +
									"\nСейчас "+str(int(temp)) + "℃, но ощущается как " + str(int(temp_feel))+"℃",reply_markup=keyboard)

@bot.message_handler(regexp="На завтра")
def tom_weather(message):
	response = requests.get("https://api.apixu.com/v1/forecast.json?key=4f177201ebb542d5a54184431180104&q=Kiev&lang=ru&days=2")
	data = response.json()
	description = data['forecast']['forecastday'][1]['day']['condition']['text']
	temp_min = data['forecast']['forecastday'][1]['day']['mintemp_c']
	temp_max = data['forecast']['forecastday'][1]['day']['maxtemp_c'] 
	weatherID = data['current']['condition']['code']
	precipitation = data['forecast']['forecastday'][1]['day']['totalprecip_mm']
	emoji = getEmoji(weatherID) 	
	bot.send_message(message.chat.id, "Завтра у нас " + description + emoji + 
									"\nТемпература составит " +str(int(temp_min))+"..."+str(int(temp_max))+"℃."+
									"\nОсадки: " + str(int(precipitation)) + " мм.")
	start(message)
########## exchange rates
	
@bot.message_handler(regexp="Курс Валют")
def currency(message): 
	keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
	keyboard.add(*[types.KeyboardButton(name) for name in ['＄', '€', '₽','Конвертировать','Меню']])
	bot.send_message(message.chat.id, 'Выберите действие',reply_markup=keyboard)

@bot.message_handler(regexp="Конвертировать")
def convert(message):
	keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
	keyboard.add(*[types.KeyboardButton(name) for name in ['Доллар в гривну', 'Евро в гривну', 'Рубль в гривну',
													  'Гривну в доллар', 'Гривну в евро', 'Гривну в рубль','Меню']])
	bot.send_message(message.chat.id, 'Выберите валюту',reply_markup=keyboard)


@bot.message_handler(regexp="Доллар в гривну")
def dol_g(message):
	data = get_money_info()
	global MONEY, CONV_DIR
	CONV_DIR = 0 
	MONEY = data[0]['buy']
	show_money_request(message)
	
	
@bot.message_handler(regexp="Евро в гривну")
def eur_g(message): 
	data = get_money_info()
	global MONEY, CONV_DIR
	CONV_DIR = 0 
	MONEY = data[1]['buy']
	show_money_request(message)


@bot.message_handler(regexp="Рубль в гривну")
def rub_g(message): 
	data = get_money_info()
	global MONEY, CONV_DIR 
	CONV_DIR = 0
	MONEY = data[2]['buy']
	show_money_request(message)

@bot.message_handler(regexp="Гривну в доллар")
def g_dol(message): 
	data = get_money_info()
	global MONEY, CONV_DIR
	CONV_DIR = 1
	MONEY = data[0]['sale']
	show_money_request(message)

@bot.message_handler(regexp="Гривну в евро")
def g_eur(message): 
	data = get_money_info()
	global MONEY, CONV_DIR 
	CONV_DIR = 1
	MONEY = data[1]['sale']
	show_money_request(message)

@bot.message_handler(regexp="Гривну в рубль")
def g_rub(message):  
	data = get_money_info()
	global MONEY, CONV_DIR
	CONV_DIR = 1  
	MONEY = data[2]['sale']
	show_money_request(message)


@bot.message_handler(regexp="＄")
def dollar(message): 
	data = get_money_info()
	buy = data[0]['buy']
	sale = data[0]['sale']
	bot.send_message(message.chat.id, "1＄ можно купить за " + str(sale[:5]) + "₴" 
								  + "\n1＄ можно продать за " + str(buy[:5]) + "₴")
	
@bot.message_handler(regexp="€")
def euro(message): 
	response = requests.get(" https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5")
	data = response.json()
	buy = data[1]['buy']
	sale = data[1]['sale']
	bot.send_message(message.chat.id, "1€ можно купить за " + str(sale[:5]) + "₴" 
								  + "\n1€ можно продать за " + str(buy[:5]) + "₴")	

@bot.message_handler(regexp="₽")
def rubl(message): 
	response = requests.get(" https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5")
	data = response.json()
	buy = data[2]['buy']
	sale = data[2]['sale']
	bot.send_message(message.chat.id, "1₽ можно купить за " + str(sale[:5]) + "₴" 
								  + "\n1₽ можно продать за " + str(buy[:5]) + "₴")									  	
	
########## NEWS

@bot.message_handler(regexp="Мировые новости")
def top(message): 
	response = requests.get("https://newsapi.org/v2/everything?q=о&language=ru&apiKey=08d40645632745818755098fdfbec6a8&sortBy=popularity&pagesize=5")
	data = response.json()
	for i in data['articles']:
		article = i['url']
		bot.send_message(message.chat.id, article)

@bot.message_handler(regexp="Новости")
def news(message): 
	keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
	keyboard.add(*[types.KeyboardButton(name) for name in ['Топ 5 🇺🇦', 'Технологии', 'Мировые новости','Меню']])
	bot.send_message(message.chat.id, 'Выберите тип новостей',reply_markup=keyboard)


@bot.message_handler(regexp="Топ")
def top(message): 
	response = requests.get("https://newsapi.org/v2/top-headlines?country=ua&apiKey=08d40645632745818755098fdfbec6a8&pagesize=5")
	data = response.json()
	for i in data['articles']:
		article = i['url']
		bot.send_message(message.chat.id, article)

@bot.message_handler(regexp="Технологии")
def top(message): 
	response = requests.get("https://newsapi.org/v2/top-headlines?country=ru&apiKey=08d40645632745818755098fdfbec6a8&pagesize=5&category=technology")
	data = response.json()
	for i in data['articles']:
		article = i['url']
		bot.send_message(message.chat.id, article)

@bot.message_handler(regexp="Меню")
def menu(message): 
	start(message)

@bot.message_handler(content_types=['text'])
def get_num(message):
	global MONEY, CONV_DIR
	if not message.text.isdigit():
		return
	if MONEY == 0:
		return
	if CONV_DIR == 0:		
		result = int(message.text) * float(MONEY)
	else: 
		result = int(message.text) / float(MONEY)	
	bot.send_message(message.chat.id, 'Вы получите '+ str(result)[:5])
	MONEY = 0
	start(message)	

def get_money_info():
	response = requests.get(" https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5")
	return response.json()

def show_money_request(message):
	keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
	keyboard.add('Меню')
	bot.send_message(message.chat.id, 'Введите сумму перевода',reply_markup=keyboard)

def getEmoji(weatherID):
	if weatherID:
		if  weatherID == 1273 or weatherID==1276 or weatherID==1087 or weatherID==1279 or weatherID==1282:
			return "⛈⚡"
		elif weatherID==1072 or weatherID==1150 or weatherID==1153 or weatherID==1168 or weatherID==1171:
			return "☔"
		elif (weatherID == 1063 or weatherID==1180 or weatherID==1183 or weatherID==1186 or weatherID==1189 or weatherID==1192 
			or weatherID==1195 or weatherID==1240 or weatherID==1243 or weatherID==1246):
			return "🌧"
		elif (weatherID==1066 or weatherID== 1114 or weatherID==1210 or weatherID==1213 or weatherID==1216
			or weatherID==1219 or weatherID==1222 or weatherID==1225 or weatherID==1255 or weatherID==1258 or weatherID==1117):
			return "❄☃"
		elif weatherID==1069 or weatherID==1204 or weatherID==1207 or weatherID==1249 or weatherID==1252:
			return "🌨"
		if weatherID == 1000:
			return "☀"
		elif weatherID == 1003:
			return "🌤"
		elif weatherID==1006 or weatherID==1009:
			return "☁"
		elif weatherID == 1030 or weatherID==1135 or weatherID==1147:
			return "🌫"	
		elif weatherID == 1198 or weatherID==1201:
			return "🌧❄"	
		else:
			return "🌆"   
	else:
		return "🌆"   		

# http://api.openweathermap.org/data/2.5/forecast?id=711660&APPID=ab7f60ac527062152b8ed51167e9ef12&lang=ru&units=metric

# https://api.apixu.com/v1/current.json?key=4f177201ebb542d5a54184431180104&q=Kiev&lang=ru
# https://api.apixu.com/v1/forecast.json?key=4f177201ebb542d5a54184431180104&q=Kiev&lang=ru&days=2
# https://newsapi.org/v2/top-headlines?country=ru&apiKey=08d40645632745818755098fdfbec6a8&pagesize=5&category=technology
# https://newsapi.org/v2/everything?q=о&language=ru&apiKey=08d40645632745818755098fdfbec6a8&sortBy=popularity
	
if __name__ == '__main__':
	 bot.polling(none_stop=True)