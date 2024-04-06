import playwright from "playwright"
const browser = await playwright.chromium.launch()
const context = await browser.newContext()
const page = await context.newPage()

const urls = {
    grants: "https://www.gobusiness.gov.sg/gov-assist/grants/",
    loan: "https://www.gobusiness.gov.sg/gov-assist/loans/",
    taxIncentive: "https://www.gobusiness.gov.sg/gov-assist/tax-incentives/",
    programmes: "https://www.gobusiness.gov.sg/gov-assist/toolkits-programmes/"
}
await page.goto(urls.grants)
await page.screenshot({ path: 'screenshot.png' });
