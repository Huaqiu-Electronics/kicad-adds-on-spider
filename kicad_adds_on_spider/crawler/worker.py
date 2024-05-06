from kicad_adds_on_spider.crawler.crawler_utils import CrawlerUtils
from kicad_adds_on_spider.models.packages import Package
from kicad_adds_on_spider.models.repository import Repository
import json
import time
import os

KICAD_OFFICIAL_REPOSITORY_URL = "https://repository.kicad.org/repository.json"

ASSET_HTTPS_DOWNLOAD_PREFIX = "https://gitee.com/kicad-mirror/kicad-addons/raw/master/"

DEFAULT_REFRESH_INTERVAL = 60 * 60 * 24 * 2


class Worker:
    def __init__(self  ,  home_dir :str , refresh_interval : int = DEFAULT_REFRESH_INTERVAL , url_prefix : str = ""):
        self._url_prefix = url_prefix
        self._home_dir = home_dir
        self._refresh_interval = refresh_interval
        self._repository = None
        self._packages = None

    @property
    def resource_fp(self):
        return os.path.join(self._home_dir, "resources.zip")

    @property
    def resource_url(self):
        return self._url_prefix + "resources.zip"


    @property
    def repository_fp(self):
        return os.path.join(self._home_dir, "repository.json")

    @property
    def repository_url(self):
        return self._url_prefix + "repository.json"

    @property
    def packages_fp(self):
        return os.path.join(self._home_dir, "packages.json")

    @property
    def packages_url(self):
        return self._url_prefix + "packages.json"

    def _update_resource(self):
        CrawlerUtils.download_content_and_save(self._repository.resources.url, self.resource_fp)
        self._repository.resources.url = self.resource_url
        self._repository.resources.sha256 = CrawlerUtils.get_sha256(self.resource_fp)

    def _update_packages(self):
        with open(self.packages_fp, "w") as f:
             f.write(self._packages.model_dump_json())
             f.close()
        self._repository.packages.url = self.packages_url
        self._repository.packages.sha256 = CrawlerUtils.get_sha256(self.packages_fp)

    def _update_libraries(self):
        pass

    def run(self):
        while True:
            self._repository = Repository(json.loads(CrawlerUtils.download_content_string(KICAD_OFFICIAL_REPOSITORY_URL)))
            self._packages = Package(json.loads(CrawlerUtils.download_content_string(self._repository.packages.url)))
            self._update_resource()
            self._update_packages()
            self._update_libraries()
            time.sleep(self._refresh_interval)






