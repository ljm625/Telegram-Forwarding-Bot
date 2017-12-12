import yaml

from TelegramAPI import TelegramAPI


class TelegramHelper(object):
    """
    This class is used to implement some basic feature for telegram bot.
    """


    def __init__(self,bot_token,offset=0):
        self.api=TelegramAPI(bot_token)
        self.offset=offset # This offset is used to bypass updates.
        self.fetching_update=False # Act like a thread lock to make it thread safe, we don't want to receive multiple duplicate updates
        self.attempt=0
        pass

    @classmethod
    def get_instance(cls,offset=0):
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

            cls.instance=cls(bot_token=config['bot_token'],offset=offset)
            return cls.instance

    def get_updates(self):
        """
        Get Updates from the telegram server, lock implemented so at one time only one update api can be called.
        :return: the update info
        """
        if self.attempt>= 5:
            # Force reset the update status if timeout.
            self.fetching_update=False
            self.attempt=0
        if self.fetching_update:
            self.attempt+=1
            return None
        self.fetching_update=True # Update LOCK
        ### Stuff to do here
        try:
            result = self.api.get('getUpdates', data={"offset": self.offset})
            for update in result['result']:
                # print(update)
                # if update['message']['text']=="/subscribe":
                #     # Subscribe the user to the list
                #     print("Here!")
                #     if update['message']['from']['id'] not in user_list:
                #         print("Subscribe!")
                #         send_message(update['message']['from']['id'],"Hello, Thanks for subscribe to this Trading advice Channel. Pls be aware that all the message are just a forwarding of BitMEX Jack and no guarantee at all.")
                #         user_list.append(update['message']['from']['id'])
                #         update_userlist()
                #     else:
                #         print("Existing")
                #         send_message(update['message']['from']['id'],"You are already in the list.")
                # print(update['update_id'])
                self.offset=update['update_id']+1
                print("Offset {}".format(self.offset))
            self.fetching_update=False
            return result
        except Exception as e:
            print("Exception found")
            self.fetching_update=False
            return None

    def send_message(self,user_id,message):
        """
        Send a message to the user
        :param user_id: The user to receive the message
        :param message: Message content
        :return: success or not
        """
        def builder():
            return {
                "chat_id":user_id,
                "text":message
            }
        try:
            resp=self.api.post("sendMessage",builder())
            return True
        except Exception as e:
            print("API returns error : {}".format(e))
            return False

