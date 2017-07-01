from lxml import html
import requests
from multiprocessing.dummy import Pool as ThreadPool
from config_local import config


START_DOMAIN = config["START_DOMAIN"]
START_WEB_PAGE = config["START_WEB_PAGE"]
RELEVANT_URI = config["RELEVANT_URI"]


found_links = []
visited_links = []


# Get all the links on the page
def get_all_anchors(webpage):
    page = requests.get(START_DOMAIN + webpage)
    tree = html.fromstring(page.content)
    return tree.xpath('//a/@href')

# Check if the link is relevant
def is_relevant_link(link):
    return link.startswith(RELEVANT_URI) and link not in found_links

# Remove non-relevant links
def filter_relevant_links(anchors):
    return filter(lambda x: is_relevant_link(x), anchors)

# Gather relevant links from a relevant web page
def gather_relevant_links(link):
    if link not in visited_links:
        # print "Gathering relevant links for link:", link
        relevant_links = filter_relevant_links(get_all_anchors(link))
        visited_links.append(link)
        
        for relevant_link in relevant_links:
            if relevant_link not in found_links:
                found_links.append(relevant_link)
        
        return relevant_links
    # print "Link %s has already been visited, skipping..." % link
    return []

def gather_relevant_links_recursively(link):
    relevant_links = gather_relevant_links(link)        
    for relevant_link in relevant_links:
        gather_relevant_links(relevant_link)

def is_interesting_found_link(link):
    return ":" not in link

def filter_found_links(found_links):
    return filter(lambda x: is_interesting_found_link(x), found_links)
        

# Get all links from the start page
relevant_start_links = gather_relevant_links(START_WEB_PAGE)

print "Started gathering links from %d start links" % len(relevant_start_links)

pool = ThreadPool(8)
pool.map(gather_relevant_links_recursively, relevant_start_links)

# Close the pool and wait for the work to finish 
pool.close() 
pool.join() 

filtered_found_links = filter_found_links(found_links)

#print "Found %d links: %s" % (len(filtered_found_links), filtered_found_links)
print "Found %d links in total" % len(filtered_found_links)

# Write found links to a file
file = open('test.txt', 'w')
for link in filtered_found_links:
    print>>file, link
