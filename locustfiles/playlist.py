import random

from locust import between, task
from locust.contrib.fasthttp import FastHttpUser

from common.auth import UserAuth
from common.config import Config
from libs.moodytunes_client import MoodyTunesClient


class PlaylistActions(UserAuth, FastHttpUser):
    emotions = Config.EMOTIONS
    emotion = None
    wait_time = between(5, 9)

    def on_start(self):
        super().on_start()
        self.create_playlist()

    def create_playlist(self):
        self.emotion = random.choice(self.emotions)

        # Get songs for the browse playlist for emotion to vote on
        resp = MoodyTunesClient.get_browse_playlist(self.client, self.emotion)
        resp_data = resp.json()

        csrf_token = MoodyTunesClient.get_csrf_token(self.client, '/moodytunes/browse/')

        for song in resp_data['results']:
            MoodyTunesClient.create_vote(self.client, song, self.emotion, True, self.host, csrf_token=csrf_token)

    @task
    def get_emotion_playlist(self):
        MoodyTunesClient.get_emotion_playlist(self.client, self.emotion)

    @task
    def delete_song_from_emotion_playlist(self):
        resp = MoodyTunesClient.get_emotion_playlist(self.client, self.emotion)
        resp_data = resp.json()

        # If there are songs in the playlist, delete a song from it
        if resp_data['results']:
            votes = resp_data['results']
            song = random.choice(votes)['song']
            MoodyTunesClient.delete_vote(self.client, song, self.emotion, self.host)

        # Otherwise, create a new playlist for the emotion
        else:
            self.create_playlist()
