import logging
import os

from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from environs import Env

from check_intent import detect_intent_texts

env = Env()
env.read_env()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    # update.message.reply_markdown_v2(fr'Hi {user.mention_markdown_v2()}\!', reply_markup=ForceReply(selective=True),)
    update.message.reply_text('Здравствуйте')


def echo(update: Update, context: CallbackContext) -> None:
    print(update.message.chat_id)
    intent = detect_intent_texts(
        context.bot_data['project_id'],
        update.message.chat_id,
        update.message.text,
        'ru-RU'
    )
    update.message.reply_text(intent.query_result.fulfillment_text)


def main():
    tg_token = env.str('TG_TOKEN')
    project_id = env.str('DF_PROJECT_ID')

    updater = Updater(tg_token)
    dispatcher = updater.dispatcher
    dispatcher.bot_data = {'project_id': project_id}
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(
        Filters.text & ~Filters.command, echo))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
