import logging
import os

from vk_api import VkApi
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id

from environs import Env

from check_intent import detect_intent_texts

env = Env()
env.read_env()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__file__)


def handle_vk_message(event, vk_bot, project_id):
    answer = detect_intent_texts(
        project_id=project_id,
        session_id=event.user_id,
        text=event.text,
        language_code='ru-RU'
    )
    if not answer.query_result.intent.is_fallback:
        vk_bot.messages.send(
            user_id=event.user_id,
            random_id=get_random_id(),
            message=answer.query_result.fulfillment_text
        )


def main():
    logging.basicConfig(level=logging.INFO)

    vk_token = env.str('VK_APP_TOKEN')
    project_id = env.str('DF_PROJECT_ID')
    logger.info('VK bot running...')

    vk_session = VkApi(token=vk_token)
    longpoll = VkLongPoll(vk_session)
    vk_bot = vk_session.get_api()
    

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            handle_vk_message(event, vk_bot, project_id)


if __name__ == '__main__':
    main()
