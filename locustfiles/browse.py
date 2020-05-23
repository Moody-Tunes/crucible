import random

from bs4 import BeautifulSoup
from common.auth import UserAuth
from common.config import Config
from locust import HttpUser, between, task


class BrowseActions(UserAuth, HttpUser):
    emotions = Config.EMOTIONS
    wait_time = between(5, 9)

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
                'vote': random.randint(1, 100) % 2 == 0  # Randomize value for vote (coin flip for True or False)
            },
            headers={
                'X-CSRFToken': csrf_token,
                'Referer': 'https://moodytunes.vm/moodytunes/browse/',
            }
        )
