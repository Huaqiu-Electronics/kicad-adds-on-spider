
require('https').globalAgent.options.ca = require('ssl-root-cas').create();
const https = require('https');
const fs = require('fs');

const url = "https://github.com/pointhi/kicad-color-schemes/releases/download/2021-12-05/com.github.pointhi.kicad-color-schemes.black-white_v1.2_pcm.zip";
const filePath = "kicad_color_scheme.zip";

const file = fs.createWriteStream(filePath);

https.get(url, response => {
    response.pipe(file);

    file.on('finish', () => {
        file.close(() => {
            console.log("File downloaded successfully.");
        });
    });
}).on('error', err => {
    fs.unlink(filePath, () => {
        console.error("Failed to download the file:", err);
    });
});
