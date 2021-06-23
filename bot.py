from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import aiohttp
import asyncio

url = 'https://www.bestbuy.com/site/nvidia-geforce-rtx-3080-10gb-gddr6x-pci-express-4-0-graphics-card-titanium-and-black/6429440.p?skuId=6429440'
headers = {"User-Agent": "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.1.13) Gecko/20080401 BonEcho/2.0.0.13"}

in_stock = 'btn btn-primary btn-lg btn-block btn-leading-ficon add-to-cart-button'
out_of_stock = 'btn btn-disabled btn-lg btn-block add-to-cart-button'

driver = webdriver.Chrome(executable_path="E:\web_bot\chromedriver.exe")
driver.get(url)

loop = asyncio.get_event_loop()

async def request_page(site):
  async with aiohttp.ClientSession(trust_env=True) as session:
    async with session.get(site, headers=headers) as r:
      return await r.text()
    
async def check_availability(check_site):
    response = await request_page(check_site)
    soup = BeautifulSoup(response, 'html.parser')
    available = soup.find('button', in_stock)
    not_available = soup.find('button', out_of_stock)
    if available is not None:
        print("Its in stock")
        return False
    if not_available is not None:
        print("Out of stock")
        return True
    else:
        return True

    
async def check_in_stock(web_page):
    while await check_availability(web_page):
        await asyncio.sleep(10)

#loop.run_forever(call_func())

asyncio.run(check_in_stock(url))

