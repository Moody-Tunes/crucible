from locust import HttpUser, task, between


class BrowseActions(HttpUser):
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
        self.client.get('/tunes/browse/?emotion=HPY')
