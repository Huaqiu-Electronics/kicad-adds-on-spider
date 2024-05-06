from kicad_adds_on_spider.models.packages import Package, Version


class KicadUtils:
    def format_zip_name( pkg : Package , version : Version):
        return f"{pkg.identifier}-{version.version}.zip"

    def format_zip_url( url_prefix : str ,  pkg : Package , version : Version):
        return f"{url_prefix}/{KicadUtils.format_zip_name(pkg, version)}"

    def get_sha256(file_path):
        import hashlib
        with open(file_path, "rb") as f:
            return hashlib.sha256(f.read()).hexdigest()

    def get_update_time_utc():
        import datetime
        return datetime.datetime.utcnow().isoformat()

    def get_update_timestamp():
        import datetime
        return datetime.datetime.utcnow().timestamp()