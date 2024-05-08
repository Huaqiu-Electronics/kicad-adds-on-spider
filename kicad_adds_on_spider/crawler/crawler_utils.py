import requests
import os
class CrawlerUtils:

    def save_content_to_file(content, file_path):
        with open(file_path, 'wb') as f:
            f.write(content)


    def download_content(url):
        response = requests.get(url)

        if response.status_code == 200:
            return response.content

        return None

    def download_content_and_save(url, file_path):
        content = CrawlerUtils.download_content(url)

        if content is not None:
            CrawlerUtils.save_content_to_file(content, file_path)
            return True

        return False

    def download_content_string(url):
        content = CrawlerUtils.download_content(url)
        if content is not None:
            return content.decode('utf-8')

        return None

    def create_directory_if_not_exists(path):
        if not os.path.exists(path):
            try:
                os.makedirs(path)
                print("Directory created successfully:", path)
            except OSError as e:
                print("Error:", e)
        else:
            print("Directory already exists:", path)