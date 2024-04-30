import telebot
from config import token, keys
from extensions import ExchangeException, Exchange

#создает экзепляр класса телебот

bot = telebot.TeleBot(token)

#обрабатывает основные команды

@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message):
    text = 'Привет! Я Бот-конвертер:  \n- Показать список доступных валют - /values \
    \n- Для конвертации введите команду в формате <название валюты> <название валюты в которую переводим> <количество валюты>\n \
- Подробная инструкция по конвертации - /help'
    bot.reply_to(message, text)

@bot.message_handler(commands=['help'])
def help(message: telebot.types.Message):
    text = ('Чтобы начать конвертацию, введите команду боту в следующем формате:'
            ' \n<название валюты, которую переводим> <название валюты, в какую хотим перевести> <количество переводимой валюты>\n \n'
            'Пример команды: евро рубль 50.5\n \nЧтобы увидеть список всех доступных валют, введите команду\n/values')
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key,))
    bot.reply_to(message, text)

#обрабатываем конвертацию через ввод текста

@bot.message_handler(content_types=['text'])
def get_price(message: telebot.types.Message):
    try:
        values = message.text.lower()
        values = values.split(' ')

        #проверяем верное ли количество значений будет передано в функцию

        if len(values) != 3 and len(values) != 2:
            raise ExchangeException('Введите команду или 3 параметра. Например: доллар евро 16.33')

        elif len(values) == 3:
            quote, base, amount = values
            total_base = Exchange.get_price(quote, base, amount)

        #добавил вариант, когда человек вводит две валюты для получения цены одной единицы
        elif len(values) == 2:
            quote, base = values
            amount = 1
            total_base = Exchange.get_price(quote, base, amount)

    #если не удалось получить тотал_бэйс в предыдущих блоках, то вызываем ошибки из собственного класса

    except ExchangeException as e:
        bot.reply_to(message, f'Ошибка ввода:\n{e}')

    #если ошибка не относится к моему классу, то вызывется общее испключение

    except Exception as e:
        bot.reply_to(message, f'Что-то пошло не так с {e}. Обратитесь в техническую поддержку')

    #этот блок выполняется, если не возникли ошибки на блоках эксепт, выводим результат

    else:
        text = f'{amount} {quote} = {total_base} {base}'
        bot.send_message(message.chat.id, text)


bot.polling()
