from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import aiohttp
import asyncio
import time

url = 'https://www.bestbuy.com/site/nvidia-geforce-rtx-3080-10gb-gddr6x-pci-express-4-0-graphics-card-titanium-and-black/6429440.p?skuId=6429440'
url2 = 'https://www.bestbuy.com/site/pny-geforce-gt1030-2gb-pci-e-3-0-graphics-card-black/5901353.p?skuId=5901353'
url3 = 'https://www.bestbuy.com/site/pny-geforce-gt-710-2gb-pci-express-2-0-graphics-card-black/5092306.p?skuId=5092306'
cart = 'https://www.bestbuy.com/cart'
purchase= 'btn btn-lg btn-block btn-primary'
headers = {"User-Agent": "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.1.13) Gecko/20080401 BonEcho/2.0.0.13"}

in_stock = 'btn btn-primary btn-lg btn-block btn-leading-ficon add-to-cart-button'
in_stock_check = '.btn .btn-primary .btn-lg .btn-block .btn-leading-ficon .add-to-cart-button'
out_of_stock = 'btn btn-disabled btn-lg btn-block add-to-cart-button'

#options = Options()
#options.add_argument('--disable-blink-features=AutomationControlled')

driver = webdriver.Chrome(executable_path="E:\web_bot\chromedriver.exe")
driver.get(url3) 
time.sleep(5)
element = driver.find_element_by_css_selector('button.btn.btn-primary.btn-lg.btn-block.add-to-cart-button')
time.sleep(5)
element.click()
driver.get(cart)
time.sleep(5)



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
    #perform_purchase()
    if available is not None:
        print("Its in stock")
        return False
    if not_available is not None:
        print("Out of stock")
        return True
    else:
        return True

async def perform_purchase():
    driver = webdriver.Chrome(executable_path="E:\web_bot\chromedriver.exe")
    driver.get(url3)
    time.sleep(5)
    element = driver.find_element_by_css_selector('button.btn.btn-primary.btn-lg.btn-block.add-to-cart-button')
    time.sleep(5)
    element.click()
    driver.get(cart)
    time.sleep(5)


async def check_in_stock(web_page):
    while await check_availability(web_page):
        await asyncio.sleep(10)

asyncio.run(check_in_stock(url))

