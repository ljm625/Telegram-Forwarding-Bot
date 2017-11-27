import requests


class TelegramAPI(object):
    """
    This class is used to interact with telegram bot API and take actions.
    """

    def __init__(self,bot_token):
        self.token=bot_token
        pass

    def url_builder(self,api):
        return "https://api.telegram.org/bot{}/{}".format(self.token, api)

    def get(self,url,data=None):
        if type(data)==dict:
            resp=requests.get(self.url_builder(url),params=data)
        else:
            resp=requests.get(self.url_builder(url))
        if resp.status_code>=300:
            resp.raise_for_status()
        else:
            return resp.json()

    def post(self,url,data):

        if type(data)==dict:
            resp=requests.post(self.url_builder(url),data=data)

        else:
            raise BaseException("The data input is invalid")
        if resp.status_code>=300:
            resp.raise_for_status()
        else:
            return resp.json()


