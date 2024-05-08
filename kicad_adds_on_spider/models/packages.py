from pydantic import BaseModel

{
    "packages": [
        {
            "$schema": "https://go.kicad.org/pcm/schemas/v1",
            "author": {
                "contact": {
                    "web": "https://github.com/pointhi/kicad-color-schemes/"
                },
                "name": "Thomas Pointhuber"
            },
            "description": "Based on Solarized colorscheme from Ethan Schoonover",
            "description_full": "Based on Solarized colorscheme from Ethan Schoonover.\nSee https://ethanschoonover.com/solarized/ for more details.",
            "identifier": "com.github.pointhi.kicad-color-schemes.solarized-light",
            "license": "CC0-1.0",
            "maintainer": {
                "contact": {
                    "web": "https://github.com/pointhi/kicad-color-schemes/"
                },
                "name": "Thomas Pointhuber"
            },
            "name": "Solarized Light Theme",
            "resources": {
                "Github": "https://github.com/pointhi/kicad-color-schemes"
            },
            "type": "colortheme",
            "versions": [
                {
                    "download_sha256": "0be21e4d43066a1870a88eba7b627a4dac1c2fec20506dd50c78755200b412a3",
                    "download_size": 4390,
                    "download_url": "https://github.com/pointhi/kicad-color-schemes/releases/download/2021-12-05/com.github.pointhi.kicad-color-schemes.solarized-light_v1.2_pcm.zip",
                    "install_size": 5679,
                    "kicad_version": "5.99",
                    "status": "stable",
                    "version": "1.2"
                }
            ]
        },
        {
            "$schema": "https://go.kicad.org/pcm/schemas/v1",
            "author": {
                "contact": {
                    "web": "https://github.com/pointhi/kicad-color-schemes/"
                },
                "name": "Thomas Pointhuber"
            },
            "description": "Designed for printing",
            "description_full": "Designed for printing",
            "identifier": "com.github.pointhi.kicad-color-schemes.black-white",
            "license": "CC0-1.0",
            "maintainer": {
                "contact": {
                    "web": "https://github.com/pointhi/kicad-color-schemes/"
                },
                "name": "Thomas Pointhuber"
            },
            "name": "Black-White Theme",
            "resources": {
                "Github": "https://github.com/pointhi/kicad-color-schemes"
            },
            "type": "colortheme",
            "versions": [
                {
                    "download_sha256": "a6efe8dcbaf9d5e579dd9f565ed8c02ad30a896761b2c2fcc1911c7df8bce754",
                    "download_size": 3972,
                    "download_url": "https://github.com/pointhi/kicad-color-schemes/releases/download/2021-12-05/com.github.pointhi.kicad-color-schemes.black-white_v1.2_pcm.zip",
                    "install_size": 5161,
                    "kicad_version": "5.99",
                    "status": "stable",
                    "version": "1.2"
                }
            ]
        }
    ]
}

class Version(BaseModel):
    download_sha256: str
    download_size: int
    download_url: str
    install_size: int
    kicad_version: str
    status: str
    version: str

class Package(BaseModel):
    versions: list[Version]
    identifier: str
    name: str

class Packages(BaseModel):
    packages : list[Package]


