from wykop import WykopAPIv2
import os
import time


def extract_message(entry):
    return entry['entry'].body


def remove_html(message):
    return message.replace("<br />", "")


def get_last_n_messages_from_tag(api, tag, n=10):
    response = api.get_tag(tag)
    data_ = response['data'][:n]
    messages = map(extract_message, data_)
    return list(map(remove_html, messages))


def main_loop(api):
    all_messages = set()
    while True:
        new_messages = get_last_n_messages_from_tag(api, "apitest")
        messages_to_display = [m for m in new_messages if m not in all_messages]
        for m in messages_to_display:
            print("-----------")
            print(m)
            all_messages.add(m)
        time.sleep(10)


def main():
    key = os.environ.get('WYKOP_TAKTYK_KEY')
    secret = os.environ.get('WYKOP_TAKTYK_SECRET')
    api = WykopAPIv2(key, secret)
    main_loop(api)


if __name__ == '__main__':
    main()
