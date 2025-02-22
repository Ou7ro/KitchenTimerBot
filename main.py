import os
import ptbot
from pytimeparse import parse
from dotenv import load_dotenv


load_dotenv('token.env')
TOKEN = os.environ['BOT_API_TOKEN']
TG_CHAT_ID = os.environ['TG_CHAT_ID']
BOT = ptbot.Bot(TOKEN)


def render_progressbar(total, iteration, prefix='', suffix='', length=30, fill='█', zfill='░'):
    iteration = min(total, iteration)
    percent = "{0:.1f}"
    percent = percent.format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    pbar = fill * filled_length + zfill * (length - filled_length)
    return '{0} |{1}| {2}% {3}'.format(prefix, pbar, percent, suffix)


def notify_progress(secs_left, message_id, total_time):
    messege = (
        f"Осталось секунд: {secs_left}\n{render_progressbar(total_time, total_time - secs_left)}"
        )
    BOT.update_message(TG_CHAT_ID, message_id, messege)


def end_messege(author_id):
    end_messege = "Время вышло"
    BOT.send_message(author_id, end_messege)
    message = 'На сколько поставить таймер?'
    BOT.send_message(author_id, message)


def start_messege(author_id):
    start_messege = "Бот запущен!\nНа сколько поставить таймер?"
    BOT.send_message(author_id, start_messege)


def timer(chat_id, time):
    messege_id = BOT.send_message(chat_id, "Запускаю таймер")
    BOT.create_countdown(parse(time), notify_progress, message_id=messege_id, total_time=parse(time))
    BOT.create_timer(parse(time), end_messege, author_id=TG_CHAT_ID)


def main():
    start_messege(TG_CHAT_ID)
    BOT.reply_on_message(timer)
    BOT.run_bot()


if __name__ == '__main__':
    main()
