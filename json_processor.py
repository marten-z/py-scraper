import json
from config_local import config


ENTITIES_FILE = config["ENTITIES_FILE"] 


with open(ENTITIES_FILE) as data_file:    
    entities = json.load(data_file)

for entity in entities:
    print entity['path']
    print json.dumps(entity)
    print '----------------------'

