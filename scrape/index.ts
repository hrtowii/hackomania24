import playwright from "playwright"
import { Database } from './storing/db.ts'
const browser = await playwright.chromium.launch()
const context = await browser.newContext()
const page = await context.newPage()
context.setDefaultTimeout(120000)
const urls = {
    grants: "https://www.gobusiness.gov.sg/gov-assist/grants/",
    loan: "https://www.gobusiness.gov.sg/gov-assist/loans/",
    taxIncentive: "https://www.gobusiness.gov.sg/gov-assist/tax-incentives/",
    programmes: "https://www.gobusiness.gov.sg/gov-assist/toolkits-programmes/"
}

const db = new Database(
    "./database.json"
)

const scrape = async (url: string) => {
    if (url == "") {
        // continue
    }
    await page.goto(url)
    for (const li of await page.getByRole('link').all()) { // 
        if (await li.textContent() == "Find Out More") {
            const href = await li.getAttribute('href')
            if (href) {
                await page.goto(href)
                let text = await page.locator('body').textContent()
                console.log(href, text)
                db.push(href, text || "")
                // scrape(await li.getAttribute('href') || "")
            }
        }
    }
}
for (const url of Object.values(urls)) {
    await scrape(url)
}
db.close();
// await scrape(urls.grants).finally(() => { db.close() })
// const links = await page.locator.('')

// console.log(links);

await browser.close();
