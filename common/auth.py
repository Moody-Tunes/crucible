from libs.moodytunes_client import MoodyTunesClient


class UserAuth(object):

    def on_start(self):
        username, password = self.create_user()
        self.login(username, password)

    def create_user(self):
        return MoodyTunesClient.create_user(self.client)

    def login(self, username, password):
        return MoodyTunesClient.login(self.client, username, password)
