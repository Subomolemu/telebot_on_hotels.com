from loader import bot
import handlers
from telebot.custom_filters import StateFilter
from utils.set_bot_commands import set_default_commands
from urllib3.exceptions import ReadTimeoutError

if __name__ == '__main__':
    try:
        bot.add_custom_filter(StateFilter(bot))
        set_default_commands(bot)
        bot.infinity_polling()
    except ReadTimeoutError as err:
        print(type(err), err)

