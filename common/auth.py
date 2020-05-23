import random
import string

from common.config import Config


class UserAuth(object):

    def on_start(self):
        username, password = self.create_user()
        self.login(username, password)

    def create_user(self):
        self.client.get('/accounts/create/')

        for cookie in self.client.cookiejar:
            if cookie.name == Config.CSRF_COOKIE_NAME:
                csrf_token = cookie.value

        username = ''.join(random.choice(string.ascii_lowercase) for _ in range(8))
        password = ''.join(random.choice(string.ascii_lowercase) for _ in range(16))

        self.client.post(
            '/accounts/create/',
            {
                'username': username,
                'password': password,
                'confirm_password': password,
                'csrfmiddlewaretoken': csrf_token
            },
            headers={
                Config.CSRF_HEADER_NAME: csrf_token,
                'Referer': 'https://moodytunes.vm/accounts/create/'
            }
        )

        return username, password

    def login(self, username, password):
        self.client.get('/accounts/login/')

        for cookie in self.client.cookiejar:
            if cookie.name == Config.CSRF_COOKIE_NAME:
                csrf_token = cookie.value

        self.client.post(
            '/accounts/login/',
            {
                'username': username,
                'password': password,
                'csrfmiddlewaretoken': csrf_token
            },
            headers={
                Config.CSRF_HEADER_NAME: csrf_token,
                'Referer': 'https://moodytunes.vm/accounts/login/'
            }
        )
