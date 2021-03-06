import os
import signal
import sys
import time
from argparse import ArgumentParser

from typing import List, NoReturn, Tuple
from wykop import MultiKeyWykopAPI, WykopAPI

from config import ProgramConfiguration, ImageConverterConfig
from image import ImageConverter

KEYS_FILE_NAME = '../keys'


class WykopMessage:
    def __init__(self, external_id, date, text, image_url):
        self.external_id = external_id
        self.date = date
        self.text = text
        self.image_url = image_url

    def has_image(self):
        return len(self.image_url) != 0


def by_date(message: WykopMessage):
    return message.date


def extract_message(entry) -> WykopMessage:
    external_id = entry.id
    date = entry.date
    text = entry.body
    if 'embed' in entry:
        image_url = entry['embed'].url
    else:
        image_url = ''
    return WykopMessage(external_id, date, text, image_url)


def get_last_n_messages_from_tag(api, tag: str, messages_to_take: int) -> List[WykopMessage]:
    try:
        response = api.tag_entries(tag)
    except Exception:
        print("Błąd podczas pobierania wiadomości z api wykopu")
        return []
    wykop_messages = list(map(extract_message, response))
    wykop_messages.sort(key=by_date, reverse=True)
    return wykop_messages[:messages_to_take]


def print_wykopMessage(message: WykopMessage, image_converter: ImageConverter,
                       config: ProgramConfiguration) -> NoReturn:
    text = f"""
{message.date}

{message.text}
"""
    print(text)
    if config.display_image and message.has_image():
        try:
            print(image_converter.convert_to_ascii(message.image_url))
        except:
            print("<Image error>")
    elif message.has_image():
        print("<Image>")


def main_loop(api: WykopAPI, config: ProgramConfiguration, image_converter: ImageConverter) -> NoReturn:
    all_message_ids = set()
    while True:
        new_messages = get_last_n_messages_from_tag(api, config.tag, config.messages_to_take)
        messages_to_display = [m for m in new_messages if m.external_id not in all_message_ids]
        messages_to_display.reverse()
        if len(messages_to_display) != 0 and config.show_new_message_separator:
            print("========================= nowe =========================")
        for m in messages_to_display:
            print_wykopMessage(m, image_converter, config)
            all_message_ids.add(m.external_id)
        try:
            time.sleep(config.check_interval)
        except KeyboardInterrupt:
            pass


def create_argument_parser() -> ArgumentParser:
    parser = ArgumentParser()
    parser.add_argument("tag", help="Watched tag")
    parser.add_argument("-i", default=10, type=int, metavar="INTERVAL",
                        help="How often try to download new messages from wykop api [in seconds]")
    parser.add_argument("-n", default=10, type=int, metavar="MESSAGES_NUMBER",
                        help="How many recent messages are downloaded each time")
    parser.add_argument("--no-images", default=True, dest='display_image', action='store_false',
                        help="Do not convert images into ascii images")
    parser.add_argument("--no-msg-separator", default=True, dest='show_separator', action='store_false',
                        help="Do not show new messages separator")
    return parser


def load_program_args(parser: ArgumentParser) -> ProgramConfiguration:
    args = parser.parse_args()
    return ProgramConfiguration(args.i, args.tag, args.n, args.display_image, args.show_separator)


def read_keys_from_file() -> List[List[str]]:
    with open(KEYS_FILE_NAME) as f:
        return [line.split() for line in f.readlines()]


def read_keys_from_envs() -> Tuple[str, str, str]:
    key = os.environ.get('WYKOP_TAKTYK_KEY')
    secret = os.environ.get('WYKOP_TAKTYK_SECRET')
    account_key = os.environ.get('WYKOP_TAKTYK_ACCOUNTKEY')
    return key, secret, account_key


def create_wykop_api():
    if os.path.isfile(KEYS_FILE_NAME):
        keys = read_keys_from_file()
        api = MultiKeyWykopAPI(keys, output='clear')
    else:
        key, secret, account_key = read_keys_from_envs()
        api = WykopAPI(key, secret, account_key=account_key,output='clear')
    api.authenticate()
    return api


def main() -> NoReturn:
    api = create_wykop_api()
    program_configuration = load_program_args(create_argument_parser())
    image_converter = ImageConverter(ImageConverterConfig())
    main_loop(api, program_configuration, image_converter)


def signal_handler(sig, frame):
    sys.exit(0)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    main()
