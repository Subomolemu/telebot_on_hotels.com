import telebot
import datetime



@bot.message_handler(commands=['calendar'])
def get_calendar(message):
    now = datetime.datetime.now() #Текущая дата
    chat_id = message.chat.id
    date = (now.year,now.month)
    current_shown_dates[chat_id] = date #Сохраним текущую дату в словарь
    markup = create_calendar(now.year,now.month)
    bot.send_message(message.chat.id, "Пожалйста, выберите дату", reply_markup=markup)