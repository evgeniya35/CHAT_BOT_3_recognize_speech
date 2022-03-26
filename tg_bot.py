import logging
import os

from telegram import Update
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from environs import Env

from check_intent import detect_intent_texts
from tg_log_handler import TelegramLogsHandler

env = Env()
env.read_env()

logger = logging.getLogger(__file__)


def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    # update.message.reply_markdown_v2(fr'Hi {user.mention_markdown_v2()}\!', reply_markup=ForceReply(selective=True),)
    update.message.reply_text('Здравствуйте! Чем можем помочь?')


def handle_message(update: Update, context: CallbackContext) -> None:
    intent = detect_intent_texts(
        context.bot_data['project_id'],
        update.message.chat_id,
        update.message.text,
        'ru-RU'
    )
    update.message.reply_text(intent.query_result.fulfillment_text)


def main():
    tg_token = env.str('TG_TOKEN')
    tg_token_admin = env.str('TG_TOKEN_ADMIN')
    project_id = env.str('DF_PROJECT_ID')
    tg_chat_id = env.str('TG_CHAT_ID')
    
    tg_adm_bot = telegram.Bot(token=tg_token_admin)

    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
        )
    logger.addHandler(TelegramLogsHandler(tg_adm_bot, tg_chat_id))
    logger.info('TG bot running...')

    updater = Updater(tg_token)
    dispatcher = updater.dispatcher
    dispatcher.bot_data = {'project_id': project_id}
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(
        Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
