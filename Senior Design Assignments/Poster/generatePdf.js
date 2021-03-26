const puppeteer = require('puppeteer');

(async () => {
    const browser = await puppeteer.launch();
    const page = await browser.newPage();
    await page.goto(`file:///${__dirname}/Poster.html`, { waitUntil: 'networkidle2' });
    await page.pdf({
        path: 'Poster.pdf',
        width: '48in',
        height: '36in',
        printBackground: true,
        pageRanges: '1'
    });

    await browser.close();
})();
