from pathlib import Path


#путь к прокси серверу
serv_path = str(Path.cwd() / 'driver' / 'browsermob-proxy-2.1.4' / 'bin' / 'browsermob-proxy')

#путь к хром драйверу
exec_path = str(Path.cwd() / 'driver' / 'chromedriver.exe')

#заголовки на всякий случай
headers = [
            {
              "name": "Accept",
              "value": "*/*"
            },
            {
              "name": "Accept-Encoding",
              "value": "gzip, deflate, br"
            },
            {
              "name": "Accept-Language",
              "value": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7"
            },
            {
              "name": "Connection",
              "value": "keep-alive"
            },
            {
              "name": "Content-Length",
              "value": "121"
            },
            {
              "name": "Content-Type",
              "value": "text/plain;charset=UTF-8"
            },
            {
              "name": "Host",
              "value": "clientsapi03.pb06e2-resources.com"
            },
            {
              "name": "Origin",
              "value": "https://www.pari.ru"
            },
            {
              "name": "Referer",
              "value": "https://www.pari.ru/"
            },
            {
              "name": "Sec-Fetch-Dest",
              "value": "empty"
            },
            {
              "name": "Sec-Fetch-Mode",
              "value": "cors"
            },
            {
              "name": "Sec-Fetch-Site",
              "value": "cross-site"
            },
            {
              "name": "User-Agent",
              "value": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Mobile Safari/537.36"
            },
            {
              "name": "sec-ch-ua",
              "value": "\"Not/A)Brand\";v=\"99\", \"Google Chrome\";v=\"115\", \"Chromium\";v=\"115\""
            },
            {
              "name": "sec-ch-ua-mobile",
              "value": "?1"
            },
            {
              "name": "sec-ch-ua-platform",
              "value": "\"Android\""
            }
          ]
