import requests, json, telebot, time, sys, get_live_matches, get_live_score, info

token = info.token
bot = info.bot

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "Howdy, how are you doing?")
	global chat_id
	chat_id = message.chat.id
	msg = bot.reply_to(message, "Welcome to test project\nEnter the match number whose updates you want to receive")
	ongoing_matches = get_live_matches.live_matches()
	info.send_msg(ongoing_matches, chat_id)
	bot.register_next_step_handler(msg, get_live_score.fetch_score)

bot.polling()
