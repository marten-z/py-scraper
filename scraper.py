from lxml import html
import requests
from multiprocessing.dummy import Pool as ThreadPool
from config_local import config


START_DOMAIN = config["START_DOMAIN"]
START_WEB_PAGE = config["START_WEB_PAGE"]
RELEVANT_URI = config["RELEVANT_URI"]


# Get all the links on the page
def get_all_anchors(webpage):
    page = requests.get(START_DOMAIN + webpage)
    tree = html.fromstring(page.content)
    return tree.xpath('//a/@href')

# Check if the link is relevant
def is_relevant_link(x):
    return x.startswith(RELEVANT_URI)

# Remove non-relevant links
def filter_relevant_links(anchors):
    return filter(lambda x: is_relevant_link(x), anchors)

# Gather relevant links from a relevant web page
def gather_relevant_links(link):
    return filter_relevant_links(get_all_anchors(link))


# Remove all links which do not belong to the current domain
relevant_start_links = gather_relevant_links(START_WEB_PAGE)

pool = ThreadPool(10)


relevant_links = pool.map(gather_relevant_links, relevant_start_links)

# keeping track of already visited links

print "Relevant links: ", relevant_links


# close the pool and wait for the work to finish 
pool.close() 
pool.join() 
