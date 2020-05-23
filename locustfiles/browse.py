import random

from locust import between, task
from locust.contrib.fasthttp import FastHttpUser

from common.auth import UserAuth
from common.config import Config
from libs.moodytunes_client import MoodyTunesClient


class BrowseActions(UserAuth, FastHttpUser):
    emotions = Config.EMOTIONS
    wait_time = between(5, 9)

    @task(1)
    def get_browse_playlist(self):
        emotion = random.choice(self.emotions)

        self.client.get(
            '/tunes/browse/?emotion={}'.format(emotion),
            name='/tunes/browse/?emotion=[emotion]',
        )

    @task(2)
    def vote_on_song(self):
        emotion = random.choice(self.emotions)

        csrf_token = MoodyTunesClient.get_csrf_token(self.client, '/moodytunes/browse/')

        # Get a song from the browse playlist for emotion to vote on
        resp = self.client.get(
            '/tunes/browse/?emotion={}'.format(emotion),
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
                Config.CSRF_HEADER_NAME: csrf_token,
                'Referer': 'https://moodytunes.vm/moodytunes/browse/',
            }
        )
