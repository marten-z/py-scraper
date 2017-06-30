from lxml import html
import requests


START_WEB_PAGE = ''
RELEVANT_URI = ''


# Get all the links on the page
def get_all_anchors(webpage):
    page = requests.get(webpage)
    tree = html.fromstring(page.content)
    return tree.xpath('//a/@href')

# Check if the link is relevant
def is_relevant_link(x):
    return x.startswith(RELEVANT_URI)

# Remove non-relevant links
def filter_relevant_links(anchors):
    return filter(lambda x: is_relevant_link(x), anchors)


# Remove all links which do not belong to the current domain
relevantLinks = filter_relevant_links(get_all_anchors(START_WEB_PAGE))

# Visit each link and store all links found on that web page, 
# while keeping track of already visited links

