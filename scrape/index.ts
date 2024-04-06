import playwright from "playwright"
import { Database } from './storing/db.ts'
import { Readability } from "@mozilla/readability"
import { JSDOM } from "jsdom"
const browser = await playwright.chromium.launch({headless: false})
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
    await page.goto(url)
    for (const li of await page.getByRole('link').all()) { // 
        if (await li.textContent() == "Find Out More") {
            const href = await li.getAttribute('href')
            if (href) {
                // check if href has been visited before
                if (db.exists(href)) {
                    // console.log(href + " already visited")
                    continue;
                }
                try {
                    await page.goto(href)
                } catch (error) {
                    console.log(error);
                    continue;
                }
                let doc = new JSDOM(await page.content())
                let reader = new Readability(doc.window.document)
                let text = reader.parse()!.textContent
                console.log(text[0])
                db.push(href, text || "")
                await page.goto(url);
                // console.log(href + " done")
                // scrape(await li.getAttribute('href') || "")
            }
        }
    }
}
for (const url of Object.values(urls)) {
    await scrape(url).finally(() => { db.close() })
}

await browser.close();
