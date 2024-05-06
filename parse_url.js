const url = require('url');

const urlString = 'https://gitlab.com/kicad/addons/repository/-/jobs/artifacts/main/raw/artifacts/resources.zip?job=update';

const urlString2 = 'https://gitlab.com/kicad/addons/repository/-/raw/main/packages.json?job=update';


// Parse the URL
const parsedUrl = new URL(urlString);

console.log(parsedUrl.toJSON())
console.log(JSON.stringify(parsedUrl, null, 2))
console.log('Protocol:', parsedUrl.protocol);
console.log('Hostname:', parsedUrl.hostname);
console.log('Port:', parsedUrl.port);
console.log('Path:', parsedUrl.pathname);
console.log('Query:', parsedUrl.searchParams.toString());
console.log('Fragment:', parsedUrl.hash);
