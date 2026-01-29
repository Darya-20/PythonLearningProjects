#import requests
import json
import telegram_bot
#import telebot

import sys
print(sys.path)
try:
    import requests
    print(requests.__file__)
except ImportError as e:
    print(e)
