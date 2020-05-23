import random

from bs4 import BeautifulSoup
from locust import HttpUser, task, between


class BrowseActions(HttpUser):
    emotions = ['MEL', 'CLM', 'HPY', 'EXC']  # TODO: Move to config?

    wait_time = between(5, 9)

    def on_start(self):
        self.client.verify = False  # Needed to avoid SSL errors with self-signed cert
        self.login()

    def login(self):
        # login to the application
        response = self.client.get('/accounts/login/')
        csrf_token = response.cookies['csrftoken']

        # TODO: Move username and password to config?
        self.client.post(
            '/accounts/login/',
            {
                'username': 'test',
                'password': '12345',
                'csrfmiddlewaretoken': csrf_token
            },
            headers={
                'X-CSRFToken': csrf_token,
                'Referer': 'https://moodytunes.vm/accounts/login/'
            }
        )

    @task(1)
    def get_browse_playlist(self):
        self.client.get(
            '/tunes/browse/',
            params={'emotion': random.choice(self.emotions)},
            name='/tunes/browse/?emotion=[emotion]',
        )

    @task(2)
    def vote_on_song(self):
        emotion = random.choice(self.emotions)

        resp = self.client.get('/moodytunes/browse/')

        # Parse CSRF token from response. Because we set the `HttpOnly`
        # attribute on the CSRF-Token we need to pull the token value
        # from the HTML config div like we do in the application
        soup = BeautifulSoup(resp.content, 'html.parser')
        csrf_token = soup.find(id='config')['data-csrf-token']

        # Get a song from the browse playlist for emotion to vote on
        resp = self.client.get(
            '/tunes/browse/',
            params={'emotion': random.choice(self.emotions)},
            name='/tunes/browse/?emotion=[emotion]',
        )

        resp_data = resp.json()
        song = random.choice(resp_data)

        self.client.post(
            '/tunes/vote/',
            json={
                'song_code': song['code'],
                'emotion': emotion,
                'vote': True
            },
            headers={
                'X-CSRFToken': csrf_token,
                'Referer': 'https://moodytunes.vm/moodytunes/browse/',
            }
        )
