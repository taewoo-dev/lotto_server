from crawlers.crawler import Crawler
from service.lottoService import LottoService




if __name__ == "__main__":
    # app = Crawler()
    # app.crawling_lottos()
    app = LottoService()
    app.run()
