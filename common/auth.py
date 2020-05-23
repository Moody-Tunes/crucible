import random
import string


class UserAuth(object):

    def on_start(self):
        self.client.verify = False  # Needed to avoid SSL errors with self-signed cert
        username, password = self.create_user()
        self.login(username, password)

    def create_user(self):
        self.client.get('/accounts/create/')

        for cookie in self.client.cookiejar:
            if cookie.name == 'csrftoken':
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
                'X-CSRFToken': csrf_token,
                'Referer': 'https://moodytunes.vm/accounts/create/'
            }
        )

        return username, password

    def login(self, username, password):
        self.client.get('/accounts/login/')

        for cookie in self.client.cookiejar:
            if cookie.name == 'csrftoken':
                csrf_token = cookie.value

        self.client.post(
            '/accounts/login/',
            {
                'username': username,
                'password': password,
                'csrfmiddlewaretoken': csrf_token
            },
            headers={
                'X-CSRFToken': csrf_token,
                'Referer': 'https://moodytunes.vm/accounts/login/'
            }
        )
