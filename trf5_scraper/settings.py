BOT_NAME = "trf5_scraper"
SPIDER_MODULES = ["trf5_scraper.spiders"]
NEWSPIDER_MODULE = "trf5_scraper.spiders"

ROBOTSTXT_OBEY = True
CONCURRENT_REQUESTS = 8
DOWNLOAD_DELAY = 0.5
COOKIES_ENABLED = False
DEFAULT_REQUEST_HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "pt-BR,pt;q=0.9,en;q=0.8",
}

ITEM_PIPELINES = {
    "trf5_scraper.pipelines.JsonLinesPipeline": 300,
}

# encoding
FEED_EXPORT_ENCODING = "utf-8"
