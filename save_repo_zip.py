import requests

url = "https://github.com/pointhi/kicad-color-schemes/releases/download/2021-12-05/com.github.pointhi.kicad-color-schemes.black-white_v1.2_pcm.zip"
file_path = "kicad_color_scheme.zip"

response = requests.get(url)

if response.status_code == 200:
    with open(file_path, 'wb') as f:
        f.write(response.content)
    print("File downloaded successfully.")
else:
    print("Failed to download the file.")
