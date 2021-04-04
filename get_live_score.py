import requests, json, get_live_matches, info
bot = info.bot
def fetch_score(message):
	global chat_id, flag
	chat_id = message.chat.id
	match_no = message.text
	flag = 1
	#checking if the number entered is present in the displayed list
	if not match_no.isdigit():
	    msg = bot.reply_to(message, 'Error1!\nSelect a no. from the above list only')
	    return bot.register_next_step_handler(msg, fetch_score)
	elif 1 <= int(match_no) <= len(get_live_matches.score_arr):
		pin_msg = bot.send_message(chat_id, "To stop receiving updates,\nclick ""/end or ""/stop anytime")
		#Pinning the above message
		bot.pin_chat_message(chat_id, pin_msg.id)
		unique_id = get_live_matches.unique_id_arr[int(match_no)-1]
		global match_url
		match_url = "https://cricapi.com/api/cricketScore?unique_id="+unique_id+"&apikey=<KEY>"#get the data about the desired match
		loop(match_url)
	else:
		msg = bot.reply_to(message, "Error2!\nSelect a no. from the above list only")
		return bot.register_next_step_handler(msg, fetch_score)

def loop(match_url):
	prev_info = ""
	#continuously fetch data
	while flag:
		response = requests.get(match_url)
		match_score = response.json()['score']

		#display only when the score updates
		if str(match_score) != prev_info:
			prev_info = str(match_score)
			bot.send_message(chat_id, match_score)
		else:
			pass

#Breaking the loop
@bot.message_handler(commands = ['stop', 'end'])
def stop(msg):
	global flag
	flag = 0
	bot.unpin_chat_message(chat_id)
	bot.send_message(chat_id, "Thank You for checking me out 😃\nTo start over enter ""/start or ""/help")
	bot.send_sticker(chat_id, "CAACAgIAAxkBAAIGz2BqGFp7S9iQQqU0txVJSzX9oKWGAALkAAOWn4wOxwgM9TN-1vceBA")
