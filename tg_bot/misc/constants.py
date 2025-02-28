import os

from dotenv import load_dotenv

load_dotenv()

CHANNEl_ID = '@test_channel_for_shop_tg_bot'  # '-1002357580808'
CHANNEL_URL = 'https://t.me/test_channel_for_shop_tg_bot'
# kb_list = [{'label': 'Легкий путь в Python', 'url': 'https://t.me/PythonPathMaster'}]
NOT_SUB_MESSAGE = "Для доступа к функционалу бота подпишитесь на канал!"
PAGINATION_ITEMS: int = 3

API_TOKEN_CHECK_URL = os.getenv('API_TOKEN_CHECK_URL')
GET_SERVICES_URL = os.getenv('GET_SERVICES_URL')
IMEI_CHECK_URL = os.getenv('IMEI_CHECK_URL')

HELP_TEXT = ("Бот для проверки IMEI устройств.\n"
             "Авторизируйтесь по одному из API-токенов "
             "(API Sandbox или API Live).\n"
             "Бот проверит, подойдет ли ваш API-токен для использования "
             "на бесплатном сервисе по проверке IMEI устройств\n"
             "Если для токена не будет найден бесплатный сервис, "
             "то Бот предложит вам ввести другой токен.\n "
             "Для запуска или перезапуска бота нажмите /start"
             )


class CheckHeadersConst(object):
    """Константа для работы с API-сервисом."""

    @staticmethod
    def headers(text: str) -> dict:
        return {
            'Authorization': f'Bearer {text}',
            'Accept-Language': 'en',
            'Content-Type': 'application/json',
        }
