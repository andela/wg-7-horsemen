import requests
import urllib
import base64


class FitBit:
    """Class to handle all fitbit operation"""

    # App settings from fitbit as regards the app
    CLIENT_ID = '22CFSD'
    CLIENT_SECRET = 'e59051dd78a808c292efdcc2dff50dbb'
    SCOPE = 'weight'
    REDIRECT_URI = 'http://localhost:8000/en/fitbit/fetch'

    # Authorization and authentication URIs
    AUTHORIZE_URI = 'https://www.fitbit.com/oauth2/authorize'
    TOKEN_REQUEST_URI = 'https://api.fitbit.com/oauth2/token'

    def ComposeAuthorizationuri(self):
        """Method helps to compose authorization uri with the intended params"""

        # parameters for authorization
        params = {
            'client_id': self.CLIENT_ID,
            'response_type': 'code',
            'scope': self.SCOPE,
            'redirect_uri': self.REDIRECT_URI
        }

        # encode the parameters
        urlparams = urllib.parse.urlencode(params)
        # construct and return authorization_uri
        return self.AUTHORIZE_URI + '?' + urlparams

    def RequestAccessToken(self, code):
        """Method to get exchange access_code with access token from fitbits"""

        # Authentication header
        client_id = self.CLIENT_ID.encode('utf-8')
        secret = self.CLIENT_SECRET.encode('utf-8')
        headers = {
            'Authorization': 'Basic MjJDRlNEOmU1OTA1MWRkNzhhODA4YzI5MmVmZGNjMmRmZjUwZGJi',
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        # parameters for requesting tokens
        params = {
            'code': code,
            'grant_type': 'authorization_code',
            'client_id': client_id,
            'redirect_uri': self.REDIRECT_URI
        }

        # request for token
        response = requests.post(
            self.TOKEN_REQUEST_URI,
            data=params,
            headers=headers)

        if response.status_code != 200:
            raise Exception("Action unsuccessful " + str(response.status_code))

        # get the tokens
        response = response.json()
        token = dict()
        token['access_token'] = response['access_token']
        token['refresh_token'] = response['refresh_token']

        return token

    def RefreshToken(self, token):
        """ Refresh expired access token """

        # authentication header
        client_id = self.CLIENT_ID.encode('utf-8')
        secret = self.CLIENT_SECRET.encode('utf-8')
        headers = {
            'Authorization': 'Basic MjJDRlNEOmU1OTA1MWRkNzhhODA4YzI5MmVmZGNjMmRmZjUwZGJi',
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        # parameters for refresh token request
        params = {
            'grant_type': 'refresh_token',
            'refresh_token': token['refresh_token']
        }

        # request for token
        response = requests.post(self.TOKEN_REQUEST_URL, data=params, headers=headers)

        if response.status_code != 200:
            raise Exception("Action unsuccessful")

        # replace tokens
        token['access_token'] = response.access_token
        token['refresh_token'] = response.refresh_token

        return token

    def GetWeight(self, token):
        """Method makes call to API"""

        headers = {
            'Authorization': 'Bearer ' + token['access_token']
        }

        url = 'https://api.fitbit.com/1/user/-/body/weight/date/today/30d.json'

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            return response.json()
        elif response.status_code == 401:
            token = self.RefreshToken(token)
            self.GetWeight(token)
        else:
            raise Exception("Action unsuccessful")
