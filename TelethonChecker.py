import json

import yaml
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError


class TelethonChecker(object):
    """
    Use Telethon to check all the messages in the account and pick the correct message
    """

    def __init__(self,config):
        """
        Init the telethon client.
        """

        self.client = TelegramClient("session_name",
                                int(config["api_id"]),
                                config["api_hash"],
                                proxy=None,
                                update_workers=config["worker"])
        print('INFO: Connecting to Telegram Servers...', end='', flush=True)
        self.client.connect()
        print('Done!')
        self.read_userlist()
        if not self.client.is_user_authorized():
            print('INFO: Unauthorized user')
            self.client.send_code_request(config["phone"])
            code_ok = False
            while not code_ok:
                code = input('Enter the auth code: ')
                try:
                    code_ok = self.client.sign_in(config["phone"], code)
                except SessionPasswordNeededError:
                    return
        print('INFO: Client initialized succesfully!')

    @classmethod
    def get_instance(cls):
        """
        Class Object generator, used to make sure only one Telegram helper object is generated
        :param bot_token: The token of the bot
        :param offset: The offset of the update
        :return: The TelegramHelper object
        """
        try:
            if cls.instance:
                return cls.instance
            else:
                raise Exception("No instance")
        except Exception as e:
            def yaml_reader(config):
                with open(config) as f:
                    return yaml.load(f)
            config = yaml_reader("config.yaml")
            cls.instance=cls(config=config)
            return cls.instance


    def set_update_handler(self,func):
        self.client.add_update_handler(func)


    def read_userlist(self):
        try:
            with open("users.txt",'r+') as file:
                try:
                    self.user_list=json.loads(file.read())
                    print(self.user_list)
                except:
                    file.write(json.dumps([]))
        except:
            with open("users.txt", "w+") as file:
                file.write(json.dumps([]))

    def update_userlist(self):
        with open("users.txt","w+") as file:
            file.write(json.dumps(self.user_list))

    def add_userlist(self,user_id):
        self.user_list.append(user_id)
        self.update_userlist()