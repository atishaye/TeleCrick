import requests, json
#parsing data from cricapi.com
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
	return match_details