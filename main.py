from wykop import WykopAPIv2
import os
import time
from typing import List


class WykopMessage:
    def __init__(self, external_id, date, text):
        self.external_id = external_id
        self.date = date
        self.text = text


def by_date(message: WykopMessage):
    return message.date


def extract_message(entry):
    external_id = entry['entry'].id
    date = entry['entry'].date
    text = entry['entry'].body
    return WykopMessage(external_id, date, text)


def remove_html(wykop_message: WykopMessage) -> WykopMessage:
    wykop_message.text = wykop_message.text.replace("<br />", "")
    return wykop_message


def is_message(entry) -> bool:
    return entry['type'] == 'entry'


def get_last_n_messages_from_tag(api, tag, n=10) -> List[WykopMessage]:
    response = api.get_tag(tag)
    only_messages = list(filter(is_message, response['data']))
    wykop_messages = list(map(extract_message, only_messages))
    wykop_messages.sort(key=by_date)
    return list(map(remove_html, wykop_messages))[:n]


def print_wykopMessage(message: WykopMessage):
    print("-----------")
    print()
    print(message.date)
    print()
    print(message.text)
    print()


def main_loop(api):
    all_message_ids = set()
    while True:
        new_messages = get_last_n_messages_from_tag(api, "apitest")
        messages_to_display = [m for m in new_messages if m.external_id not in all_message_ids]
        for m in messages_to_display:
            print_wykopMessage(m)
            all_message_ids.add(m.external_id)
        time.sleep(5)


def main():
    key = os.environ.get('WYKOP_TAKTYK_KEY')
    secret = os.environ.get('WYKOP_TAKTYK_SECRET')
    api = WykopAPIv2(key, secret)
    main_loop(api)


if __name__ == '__main__':
    main()
