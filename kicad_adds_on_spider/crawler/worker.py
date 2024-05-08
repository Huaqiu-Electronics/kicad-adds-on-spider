from kicad_adds_on_spider.crawler.crawler_utils import CrawlerUtils
from kicad_adds_on_spider.crawler.kicad_utils import KicadUtils
from kicad_adds_on_spider.models.packages import Package ,Packages, Version
from kicad_adds_on_spider.models.repository import Repository
import json
import time
import os

KICAD_OFFICIAL_REPOSITORY_URL = "https://repository.kicad.org/repository.json"

ASSET_HTTPS_DOWNLOAD_PREFIX = "https://gitee.com/kicad-mirror/kicad-addons/raw/master/"

DEFAULT_REFRESH_INTERVAL = 60 * 60 * 24 * 2


class Worker:
    def __init__(self  ,  home_dir :str , url_prefix : str = ASSET_HTTPS_DOWNLOAD_PREFIX, refresh_interval : int = DEFAULT_REFRESH_INTERVAL ):
        CrawlerUtils.create_directory_if_not_exists(home_dir)
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

    def get_library_save_path(self, pkg: Package, version: Version):
        return os.path.join(self._home_dir, KicadUtils.format_zip_name(pkg, version))

    def get_library_download_url(self, pkg: Package, version: Version):
        return KicadUtils.format_zip_url(self._url_prefix, pkg, version)

    def _update_resource(self):
        CrawlerUtils.download_content_and_save(self._repository.resources.url, self.resource_fp)
        self._repository.resources.url = self.resource_url
        self._repository.resources.sha256 = KicadUtils.get_sha256(self.resource_fp)

    def _update_packages(self):
        with open(self.packages_fp, "w") as f:
             f.write(self._packages.model_dump_json())
             f.close()
        self._repository.packages.url = self.packages_url
        self._repository.packages.sha256 = KicadUtils.get_sha256(self.packages_fp)

    def _update_repository(self):
        with open(self.repository_fp, "w") as f:
            f.write(self._repository.model_dump_json())
            f.close()

    def _update_libraries(self):
        for pkg in self._packages.packages:
            print("Begin update library for " + pkg.name)
            for version in pkg.versions:
                print("Begin update library for " + pkg.name + " version " + version.version )

                try:
                    CrawlerUtils.download_content_and_save(version.download_url, self.get_library_save_path(pkg, version))
                    version.download_url = self.get_library_download_url(pkg, version)

                except :
                    print("Download library for " + pkg.name + " version " + version.version + " failed")

    def run(self):
        while True:
            self._repository = Repository(**json.loads(CrawlerUtils.download_content_string(KICAD_OFFICIAL_REPOSITORY_URL)))
            self._packages = Packages(**json.loads(CrawlerUtils.download_content_string(self._repository.packages.url)))

            print("Begin update libraries")
            self._update_libraries()
            print("End update libraries")

            print("Begin update resources")
            self._update_resource()
            print("End update resources")

            print("Begin update packages")
            self._update_packages()
            print("End update packages")

            print("Begin update repository")
            self._update_repository()
            print("End update repository")

            time.sleep(self._refresh_interval)

