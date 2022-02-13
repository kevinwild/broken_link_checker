SRC_FILE = 'src/url_list_example.txt'
REQUEST_THROTTLE = .50
DOMAIN_SEED_LIMIT = 150
REQUEST_TIMEOUT = 10
CRAWL = True
HEADERS = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '3600',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
    }
RSP_HEADERS = [
    'x-webmgr-cache',
    'x-webmgr-brand',
    'x-webmgr-theme'
]