import telebot, requests, json
token = <TOKEN>
bot = telebot.TeleBot(token)
def send_msg(msg, chat_id):
	url2 = 'https://api.telegram.org/bot'+token+'/sendMessage'
	data = {'chat_id': chat_id, 'text': msg}
	requests.post(url2, data).json()

#currently not using
def receive_msg():
	url1 = 'https://api.telegram.org/bot'+token+'/getUpdates'
	response = requests.get(url1)
	text = response.json()['result']
	if len(text) > 0:
		user_msg = text[-1]['message']['text']
		return user_msg
	return text
def thanks(message):
	bot.reply_to(message, "Thank You!:D")