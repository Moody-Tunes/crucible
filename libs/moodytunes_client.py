import random
import string

from bs4 import BeautifulSoup

from common.config import Config


class MoodyTunesClient(object):
    """Helper class for interacting with MoodyTunes"""

    @staticmethod
    def get_csrf_token(client, endpoint):
        """
        Make a GET request to a page and parse the CSRF token from the response.
        This is used when making unsafe HTTP requests (POST, DELETE) as those
        requests need to pass a CSRF token to the application. Because we set
        the `HttpOnly` attribute on the CSRF-Token we need to pull the token value
        from the HTML config div like we do in the application.

        :param client: (FastHttpSession) Client used by the Locust instance
        :param endpoint: (str) Endpoint to call for the CSRF token

        :return: (str)
        """
        resp = client.get(endpoint)

        soup = BeautifulSoup(resp.content, 'html.parser')
        return soup.find(id='config')['data-csrf-token']

    @staticmethod
    def create_user(client):
        """
        Create a user with a random username and password for the application

        :param client: (FastHttpSession) Client used by the Locust instance

        :return: (tuple) Username, Password combination for created user
        """
        username = ''.join(random.choice(string.ascii_lowercase) for _ in range(8))
        password = ''.join(random.choice(string.ascii_lowercase) for _ in range(16))
        csrf_token = ''

        client.get('/accounts/create/')

        for cookie in client.cookiejar:
            if cookie.name == Config.CSRF_COOKIE_NAME:
                csrf_token = cookie.value

        client.post(
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

    @staticmethod
    def login(client, username, password):
        """
        Log in to application with provided user credentials

        :param client: (FastHttpSession) Client used by the Locust instance
        :param username: (str) Username for the authenticated user
        :param password: (str) Password for the authenticated user

        :return: (locust.contrib.fasthttp.FastResponse)
        """
        client.get('/accounts/login/')
        csrf_token = ''

        for cookie in client.cookiejar:
            if cookie.name == Config.CSRF_COOKIE_NAME:
                csrf_token = cookie.value

        return client.post(
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

    @staticmethod
    def get_browse_playlist(client, emotion):
        """
        Get a browse playlist for the given emotion

        :param client: (FastHttpSession) Client used by the Locust instance
        :param emotion: (str) Emotion codename to use in making the request

        :return: (locust.contrib.fasthttp.FastResponse)
        """
        return client.get(
            '/tunes/browse/?emotion={}'.format(emotion),
            name='/tunes/browse/?emotion=[emotion]',
        )

    @staticmethod
    def get_emotion_playlist(client, emotion):
        """
        Get a playlist for the songs the user has voted as making them feel
        the specified emotion.

        :param client: (FastHttpSession) Client used by the Locust instance
        :param emotion: (str) Emotion codename to use in making the request

        :return: (locust.contrib.fasthttp.FastResponse)
        """
        return client.get(
            '/tunes/playlist/?emotion={}'.format(emotion),
            name='/tunes/playlist/?emotion=[emotion]',
        )

    @staticmethod
    def delete_vote(client, song, emotion):
        """
        Delete a vote from an emotion playlist.

        :param client: (FastHttpSession) Client used by the Locust instance
        :param song: (dict) Song object to reference for request
        :param emotion: (str) Emotion codename to use in making the request

        :return: (locust.contrib.fasthttp.FastResponse)
        """
        referer = 'https://moodytunes.vm/moodytunes/playlists/'
        csrf_token = MoodyTunesClient.get_csrf_token(client, referer)

        return client.delete(
            '/tunes/vote/',
            json={
                'song_code': song['code'],
                'emotion': emotion,
            },
            headers={
                Config.CSRF_HEADER_NAME: csrf_token,
                'Referer': referer,
            }
        )

    @staticmethod
    def create_vote(client, song, emotion, vote):
        """
        Register a vote for a song and emotion

        :param client: (FastHttpSession) Client used by the Locust instance
        :param song: (dict) Song object to reference for request
        :param emotion: (str) Emotion codename to use in making the request
        :param vote: (bool) Value for whether or not vote is "upvoted"

        :return: (locust.contrib.fasthttp.FastResponse)
        """
        referer = 'https://moodytunes.vm/moodytunes/browse/'
        csrf_token = MoodyTunesClient.get_csrf_token(client, referer)

        return client.post(
            '/tunes/vote/',
            json={
                'song_code': song['code'],
                'emotion': emotion,
                'vote': vote
            },
            headers={
                Config.CSRF_HEADER_NAME: csrf_token,
                'Referer': referer,
            }
        )
