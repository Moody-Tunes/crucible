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
    def delete_vote(client, song, emotion, csrf_token):
        """
        Delete a vote from an emotion playlist.

        :param client: (FastHttpSession) Client used by the Locust instance
        :param song: (dict) Song object to reference for request
        :param emotion: (str) Emotion codename to use in making the request
        :param csrf_token:(str) CSRF token to send in request

        :return: (locust.contrib.fasthttp.FastResponse)
        """

        return client.delete(
            '/tunes/vote/',
            json={
                'song_code': song['code'],
                'emotion': emotion,
            },
            headers={
                Config.CSRF_HEADER_NAME: csrf_token,
                'Referer': 'https://moodytunes.vm/moodytunes/playlists/',
            }
        )

    @staticmethod
    def create_vote(client, song, emotion, csrf_token, vote):
        """
        Register a vote for a song and emotion

        :param client: (FastHttpSession) Client used by the Locust instance
        :param song: (dict) Song object to reference for request
        :param emotion: (str) Emotion codename to use in making the request
        :param csrf_token: (str) CSRF token to send in request
        :param vote: (bool) Value for whether or not vote is "upvoted"

        :return: (locust.contrib.fasthttp.FastResponse)
        """
        return client.post(
            '/tunes/vote/',
            json={
                'song_code': song['code'],
                'emotion': emotion,
                'vote': vote
            },
            headers={
                Config.CSRF_HEADER_NAME: csrf_token,
                'Referer': 'https://moodytunes.vm/moodytunes/browse/',
            }
        )
