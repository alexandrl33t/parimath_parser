import requests
from browsermobproxy import Server
from selenium import webdriver
import json
from urllib.parse import urlparse
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from config import headers, exec_path, serv_path


class PariParser:
    def __init__(self, url: str, har: str, driver_path: str, ser_path: str, user: str, password: str):
        print('Запускаем сервер')
        self.url = url
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('headless')
        self.options.add_argument("--ignore-certificate-errors")
        self.server = Server(ser_path, options={'port': 8090})
        self.server.start()
        self.proxy = self.server.create_proxy(params={"trustAllServers": "true"})
        self.options.add_argument("--proxy-server={0}".format(self.proxy.proxy))
        self.driver = webdriver.Chrome(options=self.options)
        self.proxy.new_har(har, options={'captureHeaders': True, 'captureContent': True})
        self.user = user
        self.password = password
        self.data = {}
        self.headers = {item['name']: item['value'] for item in headers}
        self.matches = []

    def start(self):
        self.login()
        self.get_match_list()

    def login(self):
        """
        Вход через селениум и сбор общей информации для дальнейших запросов
        :return:
        """
        print('Входим на сайт...')
        self.driver.get(self.url)
        number_input = WebDriverWait(self.driver, 10).until(
            ec.presence_of_element_located((By.CSS_SELECTOR, 'input[type="text"]'))
        )
        number_input.send_keys(self.user)
        pwd_input = WebDriverWait(self.driver, 10).until(
            ec.presence_of_element_located((By.CSS_SELECTOR, 'input[type="password"]'))
        )
        pwd_input.send_keys(self.password)
        pwd_input.send_keys(Keys.ENTER)

        for record in self.proxy.har['log']['entries']:
            url = record['request']['url']
            if 'createProcess' in url:
                self.data = json.loads(record["request"]["postData"]['text'])
                self.data.update(json.loads(record["response"]["content"]['text']))
                self.headers = {item['name']: item['value'] for item in record['request']['headers']}

    def get_match_list(self):
        """
        Получение списка матчей и общей инфы по ним
        """
        print('Получаем список матчей...')
        data = {
            "clientId": self.data['session']['client'],
            "fsid": self.data['session']['fsid'],
            "sysId": 1,
            "lang": "ru"
        }
        # Получаем матчи
        res = requests.post(
            'https://clientsapi01.pb06e2-resources.com/betsHistory/getLastCoupons',
            json=data,
            headers=self.headers
        )
        self.matches = json.loads(res.text)
        self.append_match_info()

    def append_match_info(self):
        # расширяем инфу по каждом матчу и записываем в лог файл
        print('Расширяем инфу по каждом матчу...')
        with open('driver/log.txt', mode='w') as log_file:
            for match in self.matches.get("coupons", []):
                data = {
                    "fsid": self.data['session']['fsid'],
                    "clientId": self.data['session']['client'],
                    "sysId": 1,
                    "regId": match['extra']['regCode'],
                    "betTypeName": "sport",
                    "lang": "ru"
                }
                res = requests.post(
                    'https://clientsapi01.pb06e2-resources.com/coupon/info',
                    json=data,
                    headers=self.headers
                )
                match.update(json.loads(res.text))
                log_file.write(json.dumps(match, indent=4) + "\n\n")

    def stop(self):
        self.driver.quit()
        self.server.stop()
        print('Успешно! Вывод можно посмотреть в driver/log.txt')


url = 'https://www.pari.ru/account/history/bets'
user = '9852404490'
pswd = 'Timour03042001'
parser = PariParser(
    url=url,
    har=f'{urlparse(url).hostname}/',
    driver_path=exec_path,
    ser_path=serv_path,
    user=user,
    password=pswd,
)

parser.start()
parser.stop()
