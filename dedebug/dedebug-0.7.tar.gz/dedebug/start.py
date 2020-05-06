import json
import requests

# helpers
from .config import Config


class REQUEST(object):
    def __init__(self, project_name):

        self.url = '{}/{}/{}'.format(Config['BOT_HOST'], Config['BOT_HOST_MSGROUTE'], project_name)
        print('REQUESTED:', self.url)

        # CONFIG
        self.headers = {
            'Content-type': 'application/json',
            # 'Accept': 'text/plain',
            # 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        }
        self.timeout = 30

        # proxy_string = ''
        # self.proxy = {'http': proxy_string, 'https': proxy_string}
        self.proxy = None

    def get(self):
        req = requests.get(self.url, headers=self.headers, proxies=self.proxy, stream=False, timeout=self.timeout,
                           verify=False)
        content = req.content.decode('utf-8')

        if not req.status_code == 200:
            raise Exception('Error in response')

        return json.loads(content)

    def post(self, data):

        json_data = {
            'data': data,
        }

        req = requests.post(self.url, json=json_data, headers=self.headers, proxies=self.proxy, stream=False,
                            timeout=self.timeout,
                            verify=False)
        content = req.content.decode('utf-8')

        if not req.status_code == 200:
            raise Exception('Error in response')

        return content


class sendDebug(object):
    def __init__(self, project_name):
        self.project_name = project_name

    def message(self, data):
        res = REQUEST(project_name=self.project_name).post(data=data)
        return res


if __name__ == '__main__':
    res = sendDebug(project_name='kupi').message('Hello')
    res = sendDebug(project_name='kupi').message([1, 2, 3])

    print(res)
