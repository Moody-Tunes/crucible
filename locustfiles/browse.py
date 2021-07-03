import random

from locust import between, task
from locust.contrib.fasthttp import FastHttpUser

from common.auth import UserAuth
from common.config import Config
from libs.moodytunes_client import MoodyTunesClient


class BrowseActions(UserAuth, FastHttpUser):
    emotions = Config.EMOTIONS
    wait_time = between(5, 9)

    @task
    def get_browse_playlist_and_vote_on_song(self):
        emotion = random.choice(self.emotions)
        resp = MoodyTunesClient.get_browse_playlist(self.client, emotion)

        resp_data = resp.json()

        if resp_data['results']:
            song = random.choice(resp_data['results'])

            vote = random.choice([True, False])  # Randomize value for vote

            MoodyTunesClient.create_vote(self.client, song, emotion, vote, self.host)

    @task
    def get_last_playlist(self):
        MoodyTunesClient.get_last_playlist(self.client)
