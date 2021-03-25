#using pyTelegramBotAPI
import requests, json, telebot, time
token = <TOKEN>
bot = telebot.TeleBot(token)

def live_matches():
	curr_matches_url = "https://cricapi.com/api/cricket?apikey=<KEY>" #here I'm using the KEY obtained from cricapi.com
	curr_matches = requests.get(curr_matches_url)
	match_data = curr_matches.json()['data']
	global unique_id_arr, score_arr
	unique_id_arr, score_arr = [], []
	match_details = ""
	for i in match_data:
		unique_id_arr.append(i["unique_id"])
	for i in range(len(match_data)):
		score_arr.append(match_data[i]["title"])
		score_arr[i] += "\n"
		match_details += str(i+1) + ". "
		match_details += score_arr[i]
	send_msg(match_details)

def send_msg(msg):
	url2 = 'https://api.telegram.org/bot'+token+'/sendMessage'
	data = {'chat_id': <CHAT_ID>, 'text': msg}
	requests.post(url2, data).json()
	
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "Howdy, how are you doing?")
	msg = bot.reply_to(message, "Welcome to test project\nEnter the match number whose updates you want to receive")
	live_matches()
	bot.register_next_step_handler(msg, fetch_score)

def fetch_score(message):
	chat_id = message.chat.id
	match_no = message.text
	if match_no < '1' or match_no > str(len(score_arr)):
		msg = bot.reply_to(message, "Error!\nSelect a no. from the above list only")
		return bot.register_next_step_handler(msg, fetch_score)
	elif 1 <= int(match_no) <= len(score_arr):
		unique_id = unique_id_arr[int(match_no)-1]
		global match_url
		match_url = "https://cricapi.com/api/cricketScore?unique_id="+unique_id+"&apikey=<KEY>
		loop(match_url)
	else:
		msg = bot.reply_to(message, "Error!\nSelect a no. from the above list only")
		return bot.register_next_step_handler(msg, fetch_score)
  
def loop(match_url):
	prev_info = ""
	while True:
		response = requests.get(match_url)
		info = response.json()['score']
		if str(info) != prev_info:
			prev_info = str(info)
			send_msg(info)
		else:
			pass
		#this handler needs to be fixed
		@bot.message_handler(commands=['stop', 'end'])
		def stop(message):
			bot.polling.abort = True #an arbitrary command which raises error to end the program

bot.enable_save_next_step_handlers(delay=2)
bot.load_next_step_handlers()
bot.polling()

#currently not using these functions
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
