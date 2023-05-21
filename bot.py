#import 
import discord 
import requests 
from discord.ext import commands 
import random 
import translators as ts 
  
#config 
_ = ts.preaccelerate_and_speedtest() 
SPECIAL_CASES = {'ee': 'et'} 
LANGUAGES = {'af': 'afrikaans', 'sq': 'albanian', 'am': 'amharic', 'ar': 'arabic', 'hy': 'armenian', 'az': 'azerbaijani', 'eu': 'basque', 'be': 'belarusian', 'bn': 'bengali', 'bs': 'bosnian', 'bg': 'bulgarian', 'ca': 'catalan', 'ceb': 'cebuano', 'ny': 'chichewa', 'zh-cn': 'chinese (simplified)', 'zh-tw': 'chinese (traditional)', 'co': 'corsican', 'hr': 'croatian', 'cs': 'czech', 'da': 'danish', 'nl': 'dutch', 'en': 'english', 'eo': 'esperanto', 'et': 'estonian', 'tl': 'filipino', 'fi': 'finnish', 'fr': 'french', 'fy': 'frisian', 'gl': 'galician', 'ka': 'georgian', 'de': 'german', 'el': 'greek', 'gu': 'gujarati', 'ht': 'haitian creole', 'ha': 'hausa', 'haw': 'hawaiian', 'iw': 'hebrew', 'hi': 'hindi', 'hmn': 'hmong', 'hu': 'hungarian', 'is': 'icelandic', 'ig': 'igbo', 'id': 'indonesian', 'ga': 'irish', 'it': 'italian', 'ja': 'japanese', 'jw': 'javanese', 'kn': 'kannada', 'kk': 'kazakh', 'km': 'khmer', 'ko': 'korean', 'ku': 'kurdish (kurmanji)', 'ky': 'kyrgyz', 'lo': 'lao', 'la': 'latin', 'lv': 'latvian', 'lt': 'lithuanian', 'lb': 'luxembourgish', 'mk': 'macedonian', 'mg': 'malagasy', 'ms': 'malay', 'ml': 'malayalam', 'mt': 'maltese', 'mi': 'maori', 'mr': 'marathi', 'mn': 'mongolian', 'my': 'myanmar (burmese)', 'ne': 'nepali', 'no': 'norwegian', 'ps': 'pashto', 'fa': 'persian', 'pl': 'polish', 'pt': 'portuguese', 'pa': 'punjabi', 'ro': 'romanian', 'ru': 'russian', 'sm': 'samoan', 'gd': 'scots gaelic', 'sr': 'serbian', 'st': 'sesotho', 'sn': 'shona', 'sd': 'sindhi', 'si': 'sinhala', 'sk': 'slovak', 'sl': 'slovenian', 'so': 'somali', 'es': 'spanish', 'su': 'sundanese', 'sw': 'swahili', 'sv': 'swedish', 'tg': 'tajik', 'ta': 'tamil', 'te': 'telugu', 'th': 'thai', 'tr': 'turkish', 'uk': 'ukrainian', 'ur': 'urdu', 'uz': 'uzbek', 'vi': 'vietnamese', 'cy': 'welsh', 'xh': 'xhosa', 'yi': 'yiddish', 'yo': 'yoruba', 'zu': 'zulu', 'fil': 'Filipino', 'he': 'Hebrew'}
lang = input('Language: ')
  
#AI api 
API_URL = 'https://7015.deeppavlov.ai/model' 
  
#spam config 
symbols = 'QWERTYUIOP[]\ASDFGHJKL;ZXCVBNM,./qwertyuiopasdfghjklzxcvbnm 1234567890-=' 
spamsymbolcount = 1 
spamsymbol = random.choice(symbols) 
countofmessages = 0 
  
intents = discord.Intents.default() 
intents.message_content = True 
client = commands.Bot(command_prefix='/', intents=intents) 
  
def request_sentiment(message): 
    data = {'x': [message]} 
    res = requests.post(API_URL, json=data).json() 
    santiment = res[0][0] 
    return santiment 
  
#moderate 
@client.event 
async def on_message(message): 
  santiment = request_sentiment(ts.translate_text(message.content, to_language='ru') ) #send request and get answer 
  if santiment == 'positive': 
    if message.author.bot == False: 
      print(ts.translate_text('Позитивное сообщение', to_language=lang)  + santiment, '(', message.content, ')', message) 
  elif santiment == 'neutral': 
    if message.author.bot == False: 
      print(ts.translate_text('Нормальное сообщение', to_language=lang)  + santiment, '(', message.content, ')', message) 
  elif santiment == 'negative':  
    print(ts.translate_text('Негативное сообщение', to_language=lang)  + santiment, '(', message.content, ')', message) 
    await message.channel.purge(limit=1) 
    if message.author.nick != None: 
      if message.author.bot == False: 
        await message.channel.send(f'Сообщение пользователя {message.author.nick} ({message.author.name.strip()}#{message.author.discriminator}) удалено') 
    else: 
      await message.channel.send(f'Сообщение пользователя {message.author.name}#{message.author.discriminator} удалено') 
      
#includes commands for the bot. commands won't work without this line 
await client.process_commands(message) 
  
#commands 
@client.command(aliases= ['purge','delete']) 
@commands.has_role('Moderator') 
 @commands.has_permissions(manage_messages=True) 
async def clear(ctx, amount :int = -1, channel :str = 'none'): 
  if amount == -1: 
      await ctx.channel.purge(limit = 1000000) 
  else: 
    await ctx.channel.purge(limit = amount + 1) 
  
 #run 
 client.run('Your token bot')