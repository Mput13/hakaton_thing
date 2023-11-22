import configparser


def get_token():
    parser = configparser.ConfigParser()
    # Парсинг файла конфигурации
    parser.read("./bot.ini")
    return parser.get('TG_BOT', 'token')