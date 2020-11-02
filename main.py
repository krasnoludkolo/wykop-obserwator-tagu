from wykop import WykopAPIv2

import os
import time
from typing import List, NoReturn
from argparse import ArgumentParser
import signal
import sys

from config import ProgramConfiguration, ImageConverterConfig
from image import ImageConverter


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
    raw = entry['entry']
    external_id = raw.id
    date = raw.date
    text = raw.body
    if 'embed' in raw:
        image_url = raw['embed'].url
    else:
        image_url = ''
    return WykopMessage(external_id, date, text, image_url)


def is_message(entry) -> bool:
    return entry['type'] == 'entry'


def get_last_n_messages_from_tag(api, tag: str, messages_to_take: int) -> List[WykopMessage]:
    try:
        response = api.get_tag(tag)
    except Exception:
        print("Błąd podczas pobierania wiadomości z api wykopu")
        return []
    only_messages = list(filter(is_message, response['data']))
    wykop_messages = list(map(extract_message, only_messages))
    wykop_messages.sort(key=by_date, reverse=True)
    return wykop_messages[:messages_to_take]


def print_wykopMessage(message: WykopMessage, image_converter: ImageConverter,
                       config: ProgramConfiguration) -> NoReturn:
    print("-----------")
    print()
    print(message.date)
    print()
    print(message.text)
    print()
    if config.display_image and message.has_image():
        try:
            print(image_converter.convert_to_ascii(message.image_url))
        except:
            print("<Image error>")
    elif message.has_image():
        print("<Image>")


def main_loop(api: WykopAPIv2, config: ProgramConfiguration, image_converter: ImageConverter) -> NoReturn:
    all_message_ids = set()
    while True:
        new_messages = get_last_n_messages_from_tag(api, config.tag, config.messages_to_take)
        messages_to_display = [m for m in new_messages if m.external_id not in all_message_ids]
        messages_to_display.reverse()
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
    return parser


def load_program_args(parser: ArgumentParser) -> ProgramConfiguration:
    args = parser.parse_args()
    return ProgramConfiguration(args.i, args.tag, args.n, args.display_image)


def main() -> NoReturn:
    key = os.environ.get('WYKOP_TAG_KEY')
    secret = os.environ.get('WYKOP_TAG_SECRET')
    api = WykopAPIv2(key, secret, output='clear')
    program_configuration = load_program_args(create_argument_parser())
    image_converter = ImageConverter(ImageConverterConfig())
    main_loop(api, program_configuration, image_converter)


def signal_handler(sig, frame):
    sys.exit(0)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    main()
