try:
	import requests
except:
	print("Module requests not imported.")

def display_score_on_led_display(score):
	headers = {
		# Already added when you pass json= but not when you pass data=
		# 'Content-Type': 'application/json',
	}

	json_data = {
		'ledDisplay': str(score),
	}

	response = requests.post('http://localhost:8020/api/control', headers=headers, json=json_data)

	# Note: json_data will not be serialized by requests
	# exactly as it was in the original request.
	#data = '{ "ledDisplay": "123456789" }'
	#response = requests.post('http://localhost:8020/api/control', headers=headers, data=data)