import requests

class CrawlerUtils:

    def download_file(url, file_path):
        response = requests.get(url)
        
        if response.status_code == 200:
            with open(file_path, 'wb') as f:
                f.write(response.content)
            print("File downloaded successfully.")
        else:
            print("Failed to download the file.")
