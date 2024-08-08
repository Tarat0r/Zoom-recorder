import os
import subprocess
import time
import csv
import sys
import shlex


def read_table():

	data = []
	if not os.path.isfile("Times.csv"):
		sys.exit("The File 'Times.csv' does not exist!")
	with open('Times.csv', newline='') as csvfile:
		reader = csv.DictReader(csvfile)
		for row in reader:

			url = row['URL']
			hour_from, min_from = row['From'].split(":")[:2]
			hour_to, min_to = row['To'].split(":")[:2]
			dic = {'From': {'hour': int(hour_from), 'min': int(min_from)}, 'To': {
			                            'hour': int(hour_to), 'min': int(min_to)}, 'URL': url}
			print(dic)
			data.append(dic)

	return data


def check_time(times, reference):

	loctime = time.localtime()
	now_min = loctime.tm_min
	now_hour = loctime.tm_hour

	print("Time now: " + str(now_hour) + ":" + str(now_min))

	if now_hour > times[reference]['hour']:
		return True
	elif now_hour == times[reference]['hour'] and now_min >= times[reference]['min']:
		return True
	else:
		return False


def open_meeting(zoom_url):
	word = shlex.split("obs --startrecording --minimize-to-tray")
	obs = subprocess.Popen(word)

	word2 = shlex.split("firefox --new-tab --url " + zoom_url)
	# open firefox
	firefox = subprocess.Popen(word2)


	return obs


if __name__ == "__main__":

	print("Reading file")
	data = read_table()

	num_meetings = len(data)
	next_meeting = 0

	#while(next_meeting < num_meetings):
	while(1):
		print("Reading file")
		data = read_table()
		num_meetings = len(data)


		if next_meeting != num_meetings+1:
			print("Proof the start of the meeting " + str(next_meeting))
			start = check_time(data[next_meeting], 'From')

		if start:
			print("starting meeting " + str(next_meeting))
			obs = open_meeting(data[next_meeting]['URL'])

			print("Proof the end of the meeting " + str(next_meeting))
			while(not check_time(data[next_meeting], 'To')):
				time.sleep(60)

			subprocess.Popen.terminate(obs)
			time.sleep(5)

			os.system("kill $(ps ax | grep firefox | grep snap | awk '{print $1}')")
			os.system("kill $(ps ax | grep zoom-client | grep snap | awk '{print $1}')")
			start = False
			next_meeting += 1

		time.sleep(60)
#Reading file
#{'From': {'hour': 15, 'min': 26}, 'To': {'hour': 15, 'min': 28}, 'URL': 'abv.bg'}
#{'From': {'hour': 15, 'min': 10}, 'To': {'hour': 15, 'min': 12}, 'URL': 'https://mobilebulgaria.com/'}
