import os
import ptbot
from pytimeparse import parse
from dotenv import load_dotenv


def render_progressbar(total, iteration, prefix='', suffix='', length=30, fill='█', zfill='░'):
    iteration = min(total, iteration)
    percent = "{0:.1f}"
    percent = percent.format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    pbar = fill * filled_length + zfill * (length - filled_length)
    return '{0} |{1}| {2}% {3}'.format(prefix, pbar, percent, suffix)


def notify_progress(secs_left, message_id, tg_chat_id, total_time, bot):
    messege = (
        f"Осталось секунд: {secs_left}\n{render_progressbar(total_time, total_time - secs_left)}"
        )
    bot.update_message(tg_chat_id, message_id, messege)


def end_messege(tg_chat_id, bot):
    end_messege = "Время вышло"
    bot.send_message(tg_chat_id, end_messege)
    message = 'На сколько поставить таймер?'
    bot.send_message(tg_chat_id, message)


def timer(tg_chat_id, time, bot):
    messege_id = bot.send_message(tg_chat_id, "Запускаю таймер")
    bot.create_countdown(
        parse(time),
        notify_progress,
        message_id=messege_id,
        tg_chat_id=tg_chat_id,
        total_time=parse(time),
        bot=bot,
    )
    bot.create_timer(
        parse(time),
        end_messege,
        tg_chat_id=tg_chat_id,
        bot=bot,
    )


def main():
    load_dotenv('token.env')
    token = os.environ['BOT_API_TOKEN']
    tg_chat_id = os.environ['TG_CHAT_ID']
    bot = ptbot.Bot(token)
    bot.send_message(tg_chat_id, 'Бот запущен!\nНа сколько поставить таймер?')
    bot.reply_on_message(timer, bot=bot)
    bot.run_bot()


if __name__ == '__main__':
    main()
