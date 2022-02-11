Purpose: crawl list of domains and look for error status 
---
- install requirements.txt `pip install -r requirements.txt`
---
Config Settings:
-
- REQUEST_THROTTLE = number of seconds to wait per request
- DOMAIN_SEED_LIMIT = number of seed links to capture from home page
- REQUEST_TIMEOUT = number of seconds to wait before moving on to the next request
- CRAWL = crawl links on a page, if set to false, will only crawl domain in the list provided
- HEADERS = headers to be attached to each request
### Run Program ###
- edit config to desired results
- run `python main.py`
- view results in output/logs.db
