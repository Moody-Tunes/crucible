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
    def get_browse_playlist(self):
        emotion = random.choice(self.emotions)
        MoodyTunesClient.get_browse_playlist(self.client, emotion)

    @task
    def vote_on_song(self):
        emotion = random.choice(self.emotions)

        # Get a song from the browse playlist for emotion to vote on
        resp = MoodyTunesClient.get_browse_playlist(self.client, emotion)
        resp_data = resp.json()
        song = random.choice(resp_data)

        vote = random.choice([True, False])  # Randomize value for vote

        MoodyTunesClient.create_vote(self.client, song, emotion, vote)
