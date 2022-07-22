class TestLogin:

    def test_email_should_redirect_to_welcome_page(self, client, test_club):
        email = test_club['email']
        resp = client.post('/show-summary', data={'email': email})
        data = resp.data.decode()
        assert resp.status_code == 200
        assert '<title>Summary | GUDLFT Registration</title>' in data

    def test_email_should_return_a_flash_message(self, client):
        resp = client.post('/show-summary', data={'email': 'unregistered_email@test.fr'})
        data = resp.data.decode()
        assert resp.status_code == 302
        assert '<title>Redirecting...</title>' in data
