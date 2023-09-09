import telebot
import requests

API_TOKEN = open('key.txt').readline()

bot = telebot.TeleBot(API_TOKEN)


@bot.message_handler(commands=['DDD'])
def ddd(message):
    txt = message.text.split()

    if len(txt) < 2:
        bot.send_message(message.chat.id, 'formato invalido utilize /DDD <codigo>')
        return

    url = f"https://brasilapi.com.br/api/ddd/v1/{txt[1]}"
    xhtml = requests.get(url)

    if xhtml.status_code != 200:
        bot.send_message(message.chat.id, 'DDD não encontrado')
        return

    cdd = xhtml.json()

    cdd['cities'].sort()

    response = f'''
Estado: {cdd['state']}
Cidades:
'''
    for i in cdd['cities']:
        response += i+',\n'

    bot.send_message(message.chat.id, response)


@bot.message_handler(commands=['CEP'])
def cep(message):
    txt = message.text.split()

    if len(txt) < 2:
        bot.send_message(message.chat.id, 'formato invalido use /CEP <codigo>')

    url = f'https://brasilapi.com.br/api/cep/v1/{txt[1]}'

    xhttp = requests.get(url)

    if xhttp.status_code != 200:
        bot.send_message(message.chat.id, 'CEP não encontrado')

    address = xhttp.json()

    response = f"{address['city']} - {address['state']}\n"
    if 'street' in address:
        response += f"Rua: {address['street']}\n"
    if 'neighborhood' in address:
        response += f"Bairro: {address['neighborhood']}\n"

    bot.send_message(message.chat.id, response)


@bot.message_handler(func=lambda message: True)
def default_(message):
    text = '''
Serviços disponiveis:
/CEP
/DDD
'''
    bot.reply_to(message, text)


bot.infinity_polling()
