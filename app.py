import telebot
from config import keys, TOKEN
from extensions import ConversionException, APIException

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message: telebot.types.Message):
    text = 'Чтобы начать работу введите команду боту в следующем формате:\n<имя валюты цену которой вы хотите узнать> \
<имя валюты в которой надо узнать цену первой валюты> \
<количество первой валюты>\nУвидить список всех доступных валют: /values'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def handle_value(message: telebot.types.Message):
    text_1 = 'Доступные валюты:'
    for key in keys.keys():
        text_1 = '\n'.join((text_1, key, ))
    bot.reply_to(message, text_1)

@bot.message_handler(content_types=['text', ])
def get_price(message: telebot.types.Message):
    try:
        values = message.text.split(" ")

        if len(values) != 3:
            raise ConversionException('Слишком много параметров.')

        quote, base, amount = values
        total_base = APIException.get_price(quote, base, amount)

    except ConversionException as e:
        bot.reply_to(message, f'Ошибка со стороны пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} - {total_base}'
        bot.send_message(message.chat.id, text)


bot.polling()
