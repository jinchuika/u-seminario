from .base import *

try:
	print("local")
	from .local import *
	live = False
except:
	live = True

if live:
	from .production import * 