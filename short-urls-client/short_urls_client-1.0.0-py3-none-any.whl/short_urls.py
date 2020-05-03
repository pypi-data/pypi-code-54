import requests


class ShortUrls:
    def __init__(self, domain, api_key):
        self.domain = domain
        self.api_key = api_key

    def list(self):
        request = requests.get('https://{}/admin'.format(self.domain), headers=self.__headers())
        response = request.json()
        return response['urls']

    def create(self, url, token=None):
        data = {
            'url': url
        }
        if token is not None:
            data['custom_url'] = token

        request = requests.post('https://{}/admin'.format(self.domain), headers=self.__headers(), json=data)

        if request.status_code == 200:
            response = request.json()
            return response['short_url']

        if request.status_code == 409:
            raise ValueError('This URL has already been created')

        raise RuntimeError('An unexpected error occurred')

    def delete(self, url):
        token = url.split('/')[-1]
        request = requests.delete('https://{}/admin/{}'.format(self.domain, token), headers=self.__headers())

        return request.status_code == 200

    def __headers(self):
        return {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'x-api-key': self.api_key
        }
