from kicad_adds_on_spider.crawler.crawler_utils import CrawlerUtils
from kicad_adds_on_spider.crawler.git_worker import GitWorker
from kicad_adds_on_spider.crawler.kicad_utils import KicadUtils
from kicad_adds_on_spider.models.packages import Package ,Packages, Version
from kicad_adds_on_spider.models.repository import Repository
import json
import time
import os


KICAD_OFFICIAL_REPOSITORY_URL = "https://repository.kicad.org/repository.json"

ASSET_HTTPS_DOWNLOAD_PREFIX = "https://gitee.com/kicad-mirror/kicad-addons/raw/master/"

DEFAULT_REFRESH_INTERVAL = 60 * 60 * 24 * 1

DEFAULT_RETRY_INTERVAL  = 60* 10

class Worker:
    def __init__(self  ,  home_dir :str , url_prefix : str = ASSET_HTTPS_DOWNLOAD_PREFIX, refresh_interval : int = DEFAULT_REFRESH_INTERVAL ):
        self._url_prefix = url_prefix
        self._home_dir = home_dir
        self._refresh_interval = refresh_interval
        self._repository = None
        self._packages = None
        self._git_worker = GitWorker(home_dir)
        self._git_worker.clone_git()


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
        self._repository.name = "KiCad official repository mirror"
        with open(self.repository_fp, "w") as f:
            f.write(self._repository.model_dump_json())
            f.close()

    def _update_libraries(self):

        total_lib_cnt = 0
        failed_lib_cnt = 0

        for pkg in self._packages.packages:
            for version in pkg.versions:
                total_lib_cnt += 1
                try:
                    CrawlerUtils.download_content_and_save(version.download_url, self.get_library_save_path(pkg, version))
                    version.download_url = self.get_library_download_url(pkg, version)

                except :
                    self._git_worker.add_mgs("Download adds-on for " + pkg.name + " version " + version.version + " failed")
                    failed_lib_cnt += 1

        self._git_worker.add_mgs("Total adds-on count: " + str(total_lib_cnt)+ " success count: " + str(total_lib_cnt - failed_lib_cnt) + " failed count: " + str(failed_lib_cnt))

    def _do_update(self):
        while True:
            try:
                self._git_worker.pull_git()
                self._repository = Repository(**json.loads(CrawlerUtils.download_content_string(KICAD_OFFICIAL_REPOSITORY_URL)))
                self._packages = Packages(**json.loads(CrawlerUtils.download_content_string(self._repository.packages.url)))
                self._update_libraries()
                self._update_resource()
                self._update_packages()
                self._update_repository()
                self._git_worker.commit()
                return 
            except Exception as e:
                self._git_worker.log_error(str(e))
                time.sleep(DEFAULT_RETRY_INTERVAL)

    def run(self):
        while True:
            try:
                self._do_update()
                time.sleep(self._refresh_interval)                
            except Exception as e:
                self._git_worker.log_error(str(e))            
