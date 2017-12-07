#!/usr/bin/env python3
import json
import threading

import time
import yaml
import requests

from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError

from TelegramHelper import TelegramHelper
from TelethonChecker import TelethonChecker


def yaml_reader(config):
    with open(config) as f:
        return yaml.load(f)


config=yaml_reader("config.yaml")


def main():
    telethon=TelethonChecker.get_instance()
    tg=TelegramHelper.get_instance()
    telethon.set_update_handler(update_handler)
    bot_update=threading.Thread(target=get_bot_updates())
    bot_update.start()
    while 1:
        pass

def update_handler(update):
    # Update the config to get specific message.
    print(type(update).__name__)
    try:
        if type(update).__name__=="UpdateNewChannelMessage":
            msg=update.message
            # CHECK PEER ID
            if msg.to_id.channel_id==config['group_id'] and msg.from_id==config['user_id']:
                # Here is what we are looking for
                for keywords in config["keywords"]:
                    if keywords in msg.message:
                        print("We Got the CAR! {}".format(msg.message))
                        for user in TelethonChecker.get_instance().user_list:
                            TelegramHelper.get_instance().send_message(user,msg.message)
            # print(msg)
            print(update.message)
    except:
        pass

def bot_url_builder(api):
    return "https://api.telegram.org/bot{}/{}".format(config['bot_token'],api)

def get_bot_updates():
    while True:
        updates=TelegramHelper.get_instance().get_updates()
        if updates:
            for update in updates['result']:
                print(update)
                if update['message']['text']=="/subscribe":
                    # Subscribe the user to the list
                    if update['message']['from']['id'] not in TelethonChecker.get_instance().user_list:
                        print("Subscribe new user!")
                        TelegramHelper.get_instance().send_message(update['message']['from']['id'],"Hello, Thanks for subscribe to this Trading advice Channel. Pls be aware that all the message are just a forwarding of BitMEX Jack and no guarantee at all.")
                        TelethonChecker.get_instance().add_userlist(update['message']['from']['id'])
                    else:
                        print("Existing")
                        TelegramHelper.get_instance().send_message(update['message']['from']['id'],"You are already in the list.")
        time.sleep(5)

if __name__ == '__main__':
    main()
