import requests
from datetime import datetime
import time
import blinkt

url = 'https://rrtp.comed.com/api?type=5minutefeed'

def display_color(price):
	'''Display LED colors based on price'''
	colors = {
		'blue': [0, 97, 255],
		'green': [0, 255, 0],
		'lime green': [128, 255, 0],
		'yellow': [255, 255, 0],
		'orange': [255, 29, 0],
		'red': [255, 0, 0]
		}
	blinkt.set_brightness(0.1)
	blinkt.set_clear_on_exit()
	if price < -999:
		color = colors['blue']
	elif price < 2.5:
		color = colors['green']
	elif price < 3:
		color = colors['lime green']
	elif price < 4:
		color = colors['yellow']
	elif price < 5:
		color = colors['orange']
	else:
		color = colors['red']
	
	blinkt.set_all(color[0], color[1], color[2])
	blinkt.show()

def current_hour_estimate(prices_dict):
	'''Return the current hour estimate in cents'''
	latest_time = datetime.fromtimestamp(float(prices_dict[0]['millisUTC']) / 1000.0)
	latest_hour = latest_time.hour
	latest_minute = latest_time.minute
	latest_price = float(prices_dict[0]['price'])
	prices_in_hour = [latest_price] * 12  # initialize all 12 periods in the hour at the price of latest_price
	period = 1
	while True:
		next_period_in_hour = datetime.fromtimestamp(float(prices_dict[period]['millisUTC']) / 1000.0)
		if next_period_in_hour.hour == latest_hour and next_period_in_hour.minute != 0:
			prices_in_hour[period] = float(prices_dict[period]['price'])
			period += 1
		else:
			break
	
	return(sum(prices_in_hour) / 12.0)

# Main program loop

while True:
	timeBegin = time.time()
	try:
		r = requests.get(url, timeout=30)
	except:
		display_color(-1000)
		timeEnd = time.time()
		timeElapsed = timeEnd - timeBegin
		time.sleep(300 - timeElapsed)
		continue
	prices_dict = r.json()
	
	estimate = current_hour_estimate(prices_dict)
	display_color(estimate)
	timeEnd = time.time()
	timeElapsed = timeEnd - timeBegin
	
	time.sleep(300 - timeElapsed)
