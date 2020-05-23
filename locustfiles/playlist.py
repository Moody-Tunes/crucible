import random

from bs4 import BeautifulSoup
from locust import task, HttpUser, between

from common.auth import UserAuth
from common.config import Config


class PlaylistActions(UserAuth, HttpUser):
    emotions = Config.EMOTIONS
    emotion = None
    wait_time = between(5, 9)

    def on_start(self):
        super(PlaylistActions, self).on_start()
        self.create_playlist()

    def create_playlist(self):
        self.emotion = random.choice(self.emotions)

        resp = self.client.get('/moodytunes/browse/')

        # Parse CSRF token from response. Because we set the `HttpOnly`
        # attribute on the CSRF-Token we need to pull the token value
        # from the HTML config div like we do in the application
        soup = BeautifulSoup(resp.content, 'html.parser')
        csrf_token = soup.find(id='config')['data-csrf-token']

        # Get a song from the browse playlist for emotion to vote on
        resp = self.client.get(
            '/tunes/browse/',
            params={'emotion': self.emotion},
            name='/tunes/browse/?emotion=[emotion]',
        )

        resp_data = resp.json()

        for song in resp_data:
            self.client.post(
                '/tunes/vote/',
                json={
                    'song_code': song['code'],
                    'emotion': self.emotion,
                    'vote': True  # Need to be True for song to be in playlist
                },
                headers={
                    'X-CSRFToken': csrf_token,
                    'Referer': 'https://moodytunes.vm/moodytunes/browse/',
                }
            )

    @task(1)
    def get_emotion_playlist(self):
        self.client.get(
            '/tunes/playlist/',
            params={'emotion': self.emotion},
            name='/tunes/playlist/?emotion=[emotion]',
        )
