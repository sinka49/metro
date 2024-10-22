BASE_URL = 'https://online.metro-cc.ru'
# CATEGORY = '/category/gotovye-bljuda-polufabrikaty' здесь можно указать любую категорию
CATEGORY = '/category/ovoshchi-i-frukty/frukty/f/brend/bez-brenda'
URL_PARAMS = '?in_stock=1'
PAGE = '&page='
SRC_FOR_WRITE = './src/'
FILE_FOR_WRITE = '-output.csv'
COOKIES = 'is18Confirmed=true; pickupStore=10; metroStoreId=10;'

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/130.0.0.0 Safari/537.36',
    'Upgrade-Insecure-Requests': '1',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,'
              '*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'Cache-Control': 'no-cache',
    'Priority': 'u=0, i',
    'Sec-Ch-Ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
    'Sec-Ch-Ua-Mobile': '?0',
    'Sec-Ch-Ua-Platform': 'macOS',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Cookie': COOKIES
}
