import random
import string


class UserAuth(object):

    def on_start(self):
        self.client.verify = False  # Needed to avoid SSL errors with self-signed cert
        username, password = self.create_user()
        self.login(username, password)

    def create_user(self):
        response = self.client.get('/accounts/create/')
        csrf_token = response.cookies['csrftoken']

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
        response = self.client.get('/accounts/login/')
        csrf_token = response.cookies['csrftoken']

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
