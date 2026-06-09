"""Configuración del scraper de Price Manager."""

BOT_NAME = "price_manager_scraper"

ROBOTSTXT_OBEY = False

CONCURRENT_REQUESTS = 4
DOWNLOAD_DELAY = 1.0

AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 1.0
AUTOTHROTTLE_MAX_DELAY = 5.0

DEFAULT_REQUEST_HEADERS = {
  "User-Agent": (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/120.0 Safari/537.36"
  ),
  "Accept-Language": "es-AR,es;q=0.9,en;q=0.8",
}

ITEM_PIPELINES = {
  "price_manager.scraper.pipelines.StarComputacionValidationPipeline": 100,
  "price_manager.scraper.pipelines.StarComputacionDuplicatesPipeline": 200,
  "price_manager.scraper.pipelines.StarComputacionJsonLinesPipeline": 300,
}