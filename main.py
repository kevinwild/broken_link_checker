import time
import requests
import logger
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import config
import time

protocols = ['https://']
logger = logger.Logger()
seeds = []
domain = ''

def run():
    # .. Get domains from file system /src
    domain_list = _get_url_list()
    global seeds
    global domain
    requires_www = False  # .. turned on when request fails with no www.. tries again adding www
    for domain in domain_list:
        seeds = [domain]
        for protocol in protocols:
            if requires_www:
                req_url = f"{protocol}www.{domain}"
                domain = f"www.{domain}"
            else:
                req_url = f"{protocol}{domain}"

            print(f"processing: {req_url}")
            try:
                rsp = requests.get(req_url, headers=config.HEADERS)
                request_time = rsp.elapsed.total_seconds()
                rsp_headers = get_header_data(rsp.headers)
                msg = get_msg(rsp)
                log_data = {'domain': domain,
                 'full_url': req_url,
                 'request_time': request_time,
                 'status': rsp.status_code,
                 'msg': msg
                 }
                log_data.update(rsp_headers)
                logger.log(log_data)
            except Exception as e:
                print(f'>>> Error with base request: {req_url} - {e}')
                logger.error({'domain': req_url, 'status': 'failed'})
                requires_www = True
                continue
            if not rsp.ok:
                logger.error({'domain': domain, 'status': rsp.status_code})
                continue
            # .. request is good keep going
            print('>> crawling domain:', req_url)
            seeds = get_links(domain, rsp.text)
            print(f">> {len(seeds)} seeds found")
            crawl(req_url, seeds)
            requires_www = False

def crawl(req_url, seeds):
    total_seeds = len(seeds)
    seed_count = 0
    for seed in seeds:
        # .. limit break
        if config.DOMAIN_SEED_LIMIT > 0:
            if config.DOMAIN_SEED_LIMIT <= seed_count:
                print(f">> Seed Limit Reached ({config.DOMAIN_SEED_LIMIT})")
                return
        seed_count += 1
        print(f">> processing seed ({seed_count} of {total_seeds})")
        tmp_url = f"{req_url}{seed}"
        rsp = requests.get(tmp_url, headers=config.HEADERS, timeout=config.REQUEST_TIMEOUT)
        msg = get_msg(rsp)
        rsp_headers = get_header_data(rsp.headers)
        log_data = {
            'domain': domain,
            'full_url': tmp_url,
            'status': rsp.status_code,
            'request_time': rsp.elapsed.total_seconds(),
            'msg': msg
        }
        log_data.update(rsp_headers)
        logger.log(log_data)
        print('----------')
        time.sleep(config.REQUEST_THROTTLE)
        print('----------')


# .. get links from given page
def get_links(domain, page, links=None):
    if links is None:
        links = []
    soup = BeautifulSoup(page, 'html.parser')
    for a in soup.find_all('a', href=True):
        url_obj = urlparse(a['href'])
        if check_domain(url_obj.netloc, domain):
            if url_obj.path != '' and url_obj.path not in links:
                links.append(url_obj.path)
    return links

def get_msg(rsp):
    if not rsp.ok:
        return rsp.text
    return None

# .. return list of urls from given file
def _get_url_list():
    rtn = []
    with open(config.SRC_FILE, 'r') as f:
        for line in f.readlines():
            rtn.append(line.strip())
    return rtn

def check_domain(url, domain):
    domains = [f"www.{domain}", domain]
    if url in domains:
        return True
    return False

def get_header_data(headers):
    rtn = {}
    rtn['from_cache'] = headers['x-webmgr-cache']
    rtn['brand'] = headers['x-webmgr-brand']
    rtn['theme'] = headers['x-webmgr-theme']
    return rtn




if __name__ == '__main__':
    run()
