data = {}

def get_info(key, missing=None):
	if key in data.keys():
		return data[key]
	else:
		return missing

def set_info(key, value):
	global data
	data[key] = value