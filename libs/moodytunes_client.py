from bs4 import BeautifulSoup


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
