from lxml import html
import requests
from multiprocessing.dummy import Pool as ThreadPool
from config_local import config


START_DOMAIN = config["START_DOMAIN"]
LINKS_FILE =  config["LINKS_FILE"]


def scrape_page(path):
    page = requests.get(START_DOMAIN + path)
    tree = html.fromstring(page.content)
    infobox = tree.xpath("//table[@class='infobox']")
    if infobox[0] is not None:
        trs = infobox[0].xpath("tr")
        for tr in trs:
            tds = tr.xpath("td")
            for td in tds:
                print "TD: ", td.text_content()


# Get links from a file
with open(LINKS_FILE) as f:
    paths = f.readlines()

# Remove whitespace characters like `\n` at the end of each line
paths = [x.strip() for x in paths] 

pool = ThreadPool(8)
pool.map(scrape_page, paths)

# Close the pool and wait for the work to finish 
pool.close() 
pool.join() 