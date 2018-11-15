colors = {
	"white": (255, 255, 255),
	"black": (0, 0, 0),
	"red": (255, 0, 0),
	"green": (0, 255, 0),
	"blue": (0, 0, 255)
}

def get_color(color_name, default_color = (255, 255, 0)):
	if color_name.lower() in colors.keys():
		return colors[color_name.lower()]
	return default_color